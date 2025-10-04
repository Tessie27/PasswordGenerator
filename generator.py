import sys
import string
import secrets
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QLabel, QLineEdit, QPushButton, QCheckBox, 
                             QSpinBox, QComboBox, QTextEdit, QMessageBox, QSlider, 
                             QProgressBar, QApplication, QGridLayout)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont

from word_manager import WordManager
from styles import ThemeManager

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.word_manager = WordManager()
            self.settings = QSettings("PasswordGenerator", "App")
            self.setup_interface()
            self.load_preferences()
        except Exception as e:
            self.show_critical_error(str(e))
    
    def show_critical_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Startup Error")
        msg.setText("Couldn't start Password Generator")
        msg.setInformativeText(message)
        msg.exec_()
        sys.exit(1)
    
    def setup_interface(self):
        self.setWindowTitle('Password Generator')
        self.setGeometry(100, 100, 500, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel('Theme:'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Light', 'Dark'])
        self.theme_combo.currentTextChanged.connect(self.switch_theme)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        options_group = QGroupBox('Password Options')
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(6)
        
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel('Length:'))
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setRange(8, 127)
        self.length_slider.setValue(16)
        self.length_slider.valueChanged.connect(self.update_length_display)
        length_layout.addWidget(self.length_slider)
        
        self.length_label = QLabel('16')
        self.length_label.setFixedWidth(25)
        self.length_label.setAlignment(Qt.AlignCenter)
        length_layout.addWidget(self.length_label)
        options_layout.addLayout(length_layout)
        
        chars_layout = QGridLayout()
        self.uppercase_cb = QCheckBox('A-Z')
        self.uppercase_cb.setChecked(True)
        chars_layout.addWidget(self.uppercase_cb, 0, 0)
        
        self.lowercase_cb = QCheckBox('a-z')
        self.lowercase_cb.setChecked(True)
        chars_layout.addWidget(self.lowercase_cb, 0, 1)
        
        self.numbers_cb = QCheckBox('0-9')
        self.numbers_cb.setChecked(True)
        chars_layout.addWidget(self.numbers_cb, 1, 0)
        
        self.special_cb = QCheckBox('Special')
        self.special_cb.setChecked(True)
        chars_layout.addWidget(self.special_cb, 1, 1)
        options_layout.addLayout(chars_layout)
        
        word_layout = QHBoxLayout()
        self.words_cb = QCheckBox('Mix Words')
        self.words_cb.toggled.connect(self.toggle_word_options)
        word_layout.addWidget(self.words_cb)
        
        word_layout.addWidget(QLabel('Words:'))
        self.word_count_spin = QSpinBox()
        self.word_count_spin.setRange(2, 6)
        self.word_count_spin.setValue(3)
        self.word_count_spin.setEnabled(False)
        self.word_count_spin.setFixedWidth(50)
        word_layout.addWidget(self.word_count_spin)
        
        word_layout.addStretch()
        options_layout.addLayout(word_layout)
        
        layout.addWidget(options_group)
        
        button_layout = QHBoxLayout()
        self.generate_standard_btn = QPushButton('Generate Standard')
        self.generate_standard_btn.clicked.connect(self.generate_standard_password)
        button_layout.addWidget(self.generate_standard_btn)
        
        self.generate_words_btn = QPushButton('Generate Words')
        self.generate_words_btn.clicked.connect(self.generate_word_password)
        self.generate_words_btn.setEnabled(False)
        button_layout.addWidget(self.generate_words_btn)
        
        layout.addLayout(button_layout)
        
        password_group = QGroupBox('Generated Password')
        password_layout = QVBoxLayout(password_group)
        
        self.password_display = QTextEdit()
        self.password_display.setMaximumHeight(80)
        self.password_display.setFont(QFont('Courier', 10))
        password_layout.addWidget(self.password_display)
        
        actions_layout = QHBoxLayout()
        self.copy_btn = QPushButton('Copy')
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        actions_layout.addWidget(self.copy_btn)
        
        self.modify_btn = QPushButton('Modify')
        self.modify_btn.clicked.connect(self.modify_password)
        actions_layout.addWidget(self.modify_btn)
        
        self.regenerate_btn = QPushButton('Regenerate')
        self.regenerate_btn.clicked.connect(self.regenerate_password)
        actions_layout.addWidget(self.regenerate_btn)
        
        password_layout.addLayout(actions_layout)
        
        layout.addWidget(password_group)
        
        custom_group = QGroupBox('Custom Password')
        custom_layout = QHBoxLayout(custom_group)
        
        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText('Type your own password here...')
        custom_layout.addWidget(self.custom_input)
        
        self.use_custom_btn = QPushButton('Use')
        self.use_custom_btn.clicked.connect(self.use_custom_password)
        self.use_custom_btn.setFixedWidth(60)
        custom_layout.addWidget(self.use_custom_btn)
        
        layout.addWidget(custom_group)
        
        self.statusBar().showMessage(f'Loaded {self.word_manager.get_word_count()} words')

    def toggle_word_options(self, checked):
        self.word_count_spin.setEnabled(checked)
        self.generate_words_btn.setEnabled(checked)

    def update_length_display(self, value):
        self.length_label.setText(str(value))

    def build_character_pool(self):
        char_pool = ""
        if self.lowercase_cb.isChecked():
            char_pool += string.ascii_lowercase
        if self.uppercase_cb.isChecked():
            char_pool += string.ascii_uppercase
        if self.numbers_cb.isChecked():
            char_pool += string.digits
        if self.special_cb.isChecked():
            char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return char_pool

    def generate_diverse_password(self, char_pool, length):
        password_chars = []
        
        if self.lowercase_cb.isChecked():
            password_chars.append(secrets.choice(string.ascii_lowercase))
        if self.uppercase_cb.isChecked():
            password_chars.append(secrets.choice(string.ascii_uppercase))
        if self.numbers_cb.isChecked():
            password_chars.append(secrets.choice(string.digits))
        if self.special_cb.isChecked():
            password_chars.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(char_pool))
        
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)

    def generate_standard_password(self):
        try:
            length = self.length_slider.value()
            
            if length < 8:
                QMessageBox.warning(self, "Too Short", "Password should be at least 8 characters!")
                return
            
            char_pool = self.build_character_pool()
            if not char_pool:
                QMessageBox.warning(self, "No Options", "Please pick at least one character type!")
                return
            
            password = self.generate_diverse_password(char_pool, length)
            self.password_display.setPlainText(password)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong: {e}")

    def generate_word_password(self):
        if not self.words_cb.isChecked():
            return
        
        try:
            num_words = self.word_count_spin.value()
            
            selected_words = self.word_manager.get_random_words(num_words)
            
            processed_words = []
            for word in selected_words:
                processed_word = ''.join(
                    secrets.choice([char.upper(), char.lower()]) if char.isalpha() else char
                    for char in word
                )
                processed_words.append(processed_word)
            
            password_parts = []
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            numbers = "0123456789"
            
            for i, word in enumerate(processed_words):
                password_parts.append(word)
                
                if i < len(processed_words) - 1:
                    separator_choice = secrets.choice([1, 2, 3, 4])
                    
                    if separator_choice == 1:
                        password_parts.append(secrets.choice(special_chars))
                    elif separator_choice == 2:
                        password_parts.append(secrets.choice(numbers))
                    elif separator_choice == 3:
                        password_parts.append(secrets.choice(special_chars))
                        password_parts.append(secrets.choice(numbers))
                    else:
                        num_chars = secrets.choice([1, 2, 3])
                        for _ in range(num_chars):
                            char_type = secrets.choice([1, 2])
                            if char_type == 1:
                                password_parts.append(secrets.choice(special_chars))
                            else:
                                password_parts.append(secrets.choice(numbers))
            
            password = ''.join(password_parts)
            
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in special_chars for c in password)
            
            if not has_upper:
                insert_pos = secrets.randbelow(len(password))
                password = password[:insert_pos] + secrets.choice(string.ascii_uppercase) + password[insert_pos:]
            
            if not has_lower:
                insert_pos = secrets.randbelow(len(password))
                password = password[:insert_pos] + secrets.choice(string.ascii_lowercase) + password[insert_pos:]
            
            if not has_digit:
                insert_pos = secrets.randbelow(len(password))
                password = password[:insert_pos] + secrets.choice(string.digits) + password[insert_pos:]
            
            if not has_special:
                insert_pos = secrets.randbelow(len(password))
                password = password[:insert_pos] + secrets.choice(special_chars) + password[insert_pos:]
            
            while len(password) < 8:
                char_pool = string.ascii_letters + string.digits + special_chars
                insert_pos = secrets.randbelow(len(password))
                password = password[:insert_pos] + secrets.choice(char_pool) + password[insert_pos:]
            
            self.password_display.setPlainText(password)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Couldn't create word password: {e}")

    def use_custom_password(self):
        password = self.custom_input.text().strip()
        if not password:
            QMessageBox.warning(self, "Empty", "Please type a password first!")
            return
            
        if len(password) < 8:
            QMessageBox.warning(self, "Too Short", "Password needs to be at least 8 characters!")
            return
            
        if len(password) > 127:
            QMessageBox.warning(self, "Too Long", "Password can't be longer than 127 characters!")
            return
            
        self.password_display.setPlainText(password)
        self.custom_input.clear()

    def copy_to_clipboard(self):
        password = self.password_display.toPlainText()
        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            self.statusBar().showMessage("Copied to clipboard!", 3000)
        else:
            QMessageBox.warning(self, "Nothing to Copy", "Generate a password first!")

    def modify_password(self):
        current_password = self.password_display.toPlainText()
        if not current_password:
            QMessageBox.warning(self, "Nothing to Edit", "No password to modify!")
            return
            
        self.custom_input.setText(current_password)
        self.password_display.setPlainText("")

    def regenerate_password(self):
        if self.words_cb.isChecked():
            self.generate_word_password()
        else:
            self.generate_standard_password()

    def switch_theme(self, theme_name):
        app = QApplication.instance()
        if theme_name == "Dark":
            ThemeManager.apply_dark_theme(app)
        else:
            ThemeManager.apply_light_theme(app)
        
        self.settings.setValue('theme', theme_name)

    def load_preferences(self):
        theme = self.settings.value('theme', 'Light')
        self.theme_combo.setCurrentText(theme)
        self.switch_theme(theme)
        
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
        
        window_state = self.settings.value('windowState')
        if window_state:
            self.restoreState(window_state)

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        event.accept()
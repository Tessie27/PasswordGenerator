import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLabel, QLineEdit, QPushButton, QCheckBox,
                             QSpinBox, QComboBox, QTextEdit, QMessageBox, QSlider,
                             QProgressBar, QApplication, QGridLayout)
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QFont

from generator_logic import (
    generate_diverse_password,
    score_password_strength,
    validate_custom_password,
    SPECIAL_CHARS
)
from word_manager import WordManager
from styles import ThemeManager

# Clipboard auto-clear delay in milliseconds (30 seconds)
CLIPBOARD_CLEAR_DELAY = 30_000


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self._clipboard_timer = QTimer(self)
        self._clipboard_timer.setSingleShot(True)
        self._clipboard_timer.timeout.connect(self._clear_clipboard)
        self._last_mode = "standard" 
        try:
            self.word_manager = WordManager()
            self.settings = QSettings("PasswordGenerator", "App")
            self.setup_interface()
            self.load_preferences()
        except Exception as e:
            self._show_critical_error(str(e))


    def _show_critical_error(self, message: str):
        """Show a critical error dialog and exit."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Startup Error")
        msg.setText("Couldn't start Password Generator")
        msg.setInformativeText(message)
        msg.exec_()
        sys.exit(1)

    def _show_warning(self, title: str, message: str):
        """Show a reusable warning dialog."""
        QMessageBox.warning(self, title, message)

    def setup_interface(self):
        self.setWindowTitle('Password Generator')
        self.setGeometry(100, 100, 520, 620)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        # Theme selector
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel('Theme:'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Light', 'Dark'])
        self.theme_combo.currentTextChanged.connect(self.switch_theme)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # Password options
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

        # Generate buttons
        button_layout = QHBoxLayout()
        self.generate_standard_btn = QPushButton('Generate Standard')
        self.generate_standard_btn.clicked.connect(self.generate_standard_password)
        button_layout.addWidget(self.generate_standard_btn)

        self.generate_words_btn = QPushButton('Generate Words')
        self.generate_words_btn.clicked.connect(self.generate_word_password)
        self.generate_words_btn.setEnabled(False)
        button_layout.addWidget(self.generate_words_btn)
        layout.addLayout(button_layout)

        # Generated password display
        password_group = QGroupBox('Generated Password')
        password_layout = QVBoxLayout(password_group)

        self.password_display = QTextEdit()
        self.password_display.setMaximumHeight(80)
        self.password_display.setFont(QFont('Courier', 10))
        self.password_display.textChanged.connect(self._on_password_changed)
        password_layout.addWidget(self.password_display)

        # ── Strength meter ──
        strength_layout = QHBoxLayout()
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setFixedHeight(12)
        self.strength_bar.setTextVisible(False)
        strength_layout.addWidget(self.strength_bar)

        self.strength_label = QLabel("—")
        self.strength_label.setFixedWidth(80)
        self.strength_label.setAlignment(Qt.AlignCenter)
        strength_layout.addWidget(self.strength_label)
        password_layout.addLayout(strength_layout)

        # ── Entropy display ──
        self.entropy_label = QLabel("Entropy: —")
        self.entropy_label.setAlignment(Qt.AlignCenter)
        password_layout.addWidget(self.entropy_label)

        # ── Suggestion label ──
        self.suggestion_label = QLabel("")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet("color: orange; font-size: 10px;")
        password_layout.addWidget(self.suggestion_label)

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

        # Custom password
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

    def _on_password_changed(self):
        """Update strength meter whenever the password display changes."""
        password = self.password_display.toPlainText()
        result = score_password_strength(password)

        self.strength_bar.setValue(result["score"])
        self.strength_label.setText(result["label"])
        self.entropy_label.setText(f"Entropy: {result['entropy']} bits")

        # Color the bar based on label
        colors = {
            "Weak":        "#e74c3c",
            "Fair":        "#e67e22",
            "Strong":      "#2ecc71",
            "Very Strong": "#27ae60",
        }
        color = colors.get(result["label"], "#aaa")
        self.strength_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: 4px; }}"
        )

        # Show first suggestion if any
        if result["is_common"]:
            self.suggestion_label.setText("⚠️ This is a very common password!")
        elif result["suggestions"]:
            self.suggestion_label.setText(f"💡 {result['suggestions'][0]}")
        else:
            self.suggestion_label.setText("✅ Great password!")


    def copy_to_clipboard(self):
        password = self.password_display.toPlainText()
        if not password:
            self._show_warning("Nothing to Copy", "Generate a password first!")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(password)

        # Start auto-clear countdown
        self._clipboard_timer.start(CLIPBOARD_CLEAR_DELAY)
        self.statusBar().showMessage("Copied! Clipboard will clear in 30 seconds.", 5000)

    def _clear_clipboard(self):
        """Auto-clear clipboard after delay."""
        clipboard = QApplication.clipboard()
        if clipboard.text() and clipboard.text() == self.password_display.toPlainText():
            clipboard.clear()
            self.statusBar().showMessage("Clipboard cleared for security.", 3000)


    def generate_standard_password(self):
        try:
            password = generate_diverse_password(
                length=self.length_slider.value(),
                lowercase=self.lowercase_cb.isChecked(),
                uppercase=self.uppercase_cb.isChecked(),
                numbers=self.numbers_cb.isChecked(),
                special=self.special_cb.isChecked()
            )
            self.password_display.setPlainText(password)
            self._last_mode = "standard"
        except ValueError as e:
            self._show_warning("Invalid Options", str(e))
        except Exception as e:
            self._show_warning("Error", f"Something went wrong: {e}")

    def generate_word_password(self):
        if not self.words_cb.isChecked():
            return
        try:
            import secrets as _secrets
            import string as _string

            num_words = self.word_count_spin.value()
            selected_words = self.word_manager.get_random_words(num_words)

            processed_words = []
            for word in selected_words:
                processed_word = ''.join(
                    _secrets.choice([char.upper(), char.lower()]) if char.isalpha() else char
                    for char in word
                )
                processed_words.append(processed_word)

            password_parts = []
            numbers = "0123456789"

            for i, word in enumerate(processed_words):
                password_parts.append(word)
                if i < len(processed_words) - 1:
                    separator_choice = _secrets.choice([1, 2, 3, 4])
                    if separator_choice == 1:
                        password_parts.append(_secrets.choice(SPECIAL_CHARS))
                    elif separator_choice == 2:
                        password_parts.append(_secrets.choice(numbers))
                    elif separator_choice == 3:
                        password_parts.append(_secrets.choice(SPECIAL_CHARS))
                        password_parts.append(_secrets.choice(numbers))
                    else:
                        for _ in range(_secrets.choice([1, 2, 3])):
                            if _secrets.choice([1, 2]) == 1:
                                password_parts.append(_secrets.choice(SPECIAL_CHARS))
                            else:
                                password_parts.append(_secrets.choice(numbers))

            password = ''.join(password_parts)

            # Ensure all character types present
            for check, pool, inserter in [
                (any(c.isupper() for c in password), _string.ascii_uppercase, None),
                (any(c.islower() for c in password), _string.ascii_lowercase, None),
                (any(c.isdigit() for c in password), _string.digits, None),
                (any(c in SPECIAL_CHARS for c in password), SPECIAL_CHARS, None),
            ]:
                if not check:
                    pos = _secrets.randbelow(len(password))
                    char = _secrets.choice(pool)
                    password = password[:pos] + char + password[pos:]

            self.password_display.setPlainText(password)
            self._last_mode = "words"

        except Exception as e:
            self._show_warning("Error", f"Couldn't create word password: {e}")

   
    def use_custom_password(self):
        password = self.custom_input.text().strip()
        is_valid, reason = validate_custom_password(password)

        if not is_valid:
            messages = {
                "empty": "Please type a password first!",
                "too_short": "Password needs to be at least 8 characters!",
                "too_long": "Password can't be longer than 127 characters!"
            }
            self._show_warning("Invalid Password", messages.get(reason, "Invalid password."))
            return

        self.password_display.setPlainText(password)
        self.custom_input.clear()

    def modify_password(self):
        current_password = self.password_display.toPlainText()
        if not current_password:
            self._show_warning("Nothing to Edit", "No password to modify!")
            return
        self.custom_input.setText(current_password)
        self.password_display.setPlainText("")

    def regenerate_password(self):
        if self._last_mode == "words" and self.words_cb.isChecked():
            self.generate_word_password()
        else:
            self.generate_standard_password()

    def toggle_word_options(self, checked: bool):
        self.word_count_spin.setEnabled(checked)
        self.generate_words_btn.setEnabled(checked)

    def update_length_display(self, value: int):
        self.length_label.setText(str(value))


    def switch_theme(self, theme_name: str):
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
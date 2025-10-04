from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class ThemeManager:
    @staticmethod
    def apply_dark_theme(app):
        app.setStyle('Fusion')
        
        dark_palette = QPalette()
        
        # Base colors
        dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        
        # Disabled colors
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(150, 150, 150))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(150, 150, 150))
        
        app.setPalette(dark_palette)

        app.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            
            QWidget {
                font-size: 11px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 8px;
                margin-top: 0.5ex;
                padding-top: 8px;
                background-color: #3a3a3a;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #fff;
                font-size: 11px;
            }
            
            /* Modern Gradient Buttons */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6A11CB, stop:1 #2575FC);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 11px;
                min-height: 36px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7B1CFF, stop:1 #3685FF);
                box-shadow: 0 4px 15px rgba(106, 17, 203, 0.4);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5A0CB0, stop:1 #1C65E0);
                box-shadow: 0 2px 8px rgba(106, 17, 203, 0.3);
            }
            
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #555, stop:1 #666);
                color: #888;
                box-shadow: none;
            }
            
            QLineEdit, QTextEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                min-height: 24px;
            }
            
            QSpinBox, QComboBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                min-height: 24px;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
            
            QCheckBox {
                color: white;
                spacing: 6px;
                font-size: 11px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 2px solid #666;
                background-color: #2b2b2b;
            }
            
            QCheckBox::indicator:checked {
                border: 2px solid #4a90e2;
                background-color: #4a90e2;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 6px;
                background: #404040;
                margin: 2px 0;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 2px solid #3a80d2;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #5aa0f2;
            }
            
            QLabel {
                font-size: 11px;
                color: white;
            }
            
            QStatusBar {
                background-color: #3a3a3a;
                color: white;
                font-size: 10px;
                padding: 4px;
            }
        """)

    @staticmethod
    def apply_light_theme(app):
        app.setStyle('Fusion')
        
        light_palette = QPalette()
        
        # Base colors
        light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(QPalette.Base, Qt.white)
        light_palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.ToolTipBase, Qt.white)
        light_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_palette.setColor(QPalette.Text, Qt.black)
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, Qt.black)
        light_palette.setColor(QPalette.BrightText, Qt.red)
        light_palette.setColor(QPalette.Link, QColor(0, 100, 200))
        light_palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        light_palette.setColor(QPalette.HighlightedText, Qt.white)
        
        app.setPalette(light_palette)
        
        app.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            QWidget {
                font-size: 11px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 0.5ex;
                padding-top: 8px;
                background-color: #ffffff;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                color: #333;
                font-size: 11px;
            }
            
            /* Modern Gradient Buttons */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 11px;
                min-height: 36px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #768efa, stop:1 #865bb2);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #566eda, stop:1 #663b92);
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            }
            
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ccc, stop:1 #ddd);
                color: #888;
                box-shadow: none;
            }
            
            QLineEdit, QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                min-height: 24px;
            }
            
            QSpinBox, QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                min-height: 24px;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
            
            QCheckBox {
                color: black;
                spacing: 6px;
                font-size: 11px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 2px solid #999;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                border: 2px solid #667eea;
                background-color: #667eea;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #ccc;
                height: 6px;
                background: #e9ecef;
                margin: 2px 0;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background: #667eea;
                border: 2px solid #566eda;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #768efa;
            }
            
            QLabel {
                font-size: 11px;
                color: black;
            }
            
            QStatusBar {
                background-color: #e9ecef;
                color: black;
                font-size: 10px;
                padding: 4px;
            }
        """)
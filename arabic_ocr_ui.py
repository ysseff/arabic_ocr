import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QTextBrowser, QWidget,
    QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QSize

import pytesseract
from PIL import Image, ImageOps
from gtts import gTTS
from playsound import playsound

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


class BackgroundWindow(QWidget):
    def __init__(self, image_path):
        super().__init__()

        # Load background image
        self.pixmap = QPixmap(image_path)
        self.setFixedSize(self.pixmap.width(), self.pixmap.height())
        self.setWindowTitle("Arabic OCR")

        # Background label
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())

        button_width = 180
        aspect_ratio = 448 / 238
        button_height = int(button_width / aspect_ratio)

        # Scan Button
        self.scan_button = QPushButton(self)
        self.scan_button.setGeometry(27, 231, button_width, button_height)
        self.scan_button.setIcon(QIcon('scan_button.png'))
        self.scan_button.setIconSize(QSize(button_width, button_height))
        self.scan_button.setStyleSheet("background: transparent; border: none;")
        self.scan_button.clicked.connect(self.scan_clicked)

        # Copy Button
        self.copy_button = QPushButton(self)
        self.copy_button.setGeometry(340, 420, 180, 95)
        self.copy_button.setIcon(QIcon('copy_button.png'))
        self.copy_button.setIconSize(QSize(180, 95))
        self.copy_button.setStyleSheet("background: transparent; border: none;")
        self.copy_button.clicked.connect(self.copy_clicked)

        # Speak Button
        self.speak_button = QPushButton(self)
        self.speak_button.setGeometry(585, 420, 180, 95)
        self.speak_button.setIcon(QIcon('speak_button.png'))
        self.speak_button.setIconSize(QSize(180, 95))
        self.speak_button.setStyleSheet("background: transparent; border: none;")
        self.speak_button.clicked.connect(self.speak_clicked)

        # Arabic Text Browser
        self.text_edit = QTextBrowser(self)
        self.text_edit.setGeometry(278, 95, 555, 325)
        self.text_edit.setStyleSheet("""
            QTextBrowser {
                background: transparent;
                color: #6ABD9E;
                border: none;
                padding: 10px;
                letter-spacing: 0px;
            }
        """)
        cairo_font = QFont("Cairo", 24)
        self.text_edit.setFont(cairo_font)
        self.text_edit.setLayoutDirection(Qt.RightToLeft)
        self.text_edit.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Placeholder Text
        example_text = "مرحباً بك في تطبيق Arabic OCR!"
        self.text_edit.setText(example_text)

    def scan_clicked(self):
        options = QFileDialog.Options()
        file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.gif)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a file to scan", "", file_filter, options=options)

        if file_name:
            print(f"Selected file: {file_name}")

            try:
                img = Image.open(file_name)
                img = img.convert('L')
                img = ImageOps.autocontrast(img)

                ocr_result = pytesseract.image_to_string(
                    img,
                    lang='ara',
                    config='--tessdata-dir /opt/homebrew/share/tessdata'
                )

                print("OCR Result:", repr(ocr_result))

                if ocr_result.strip() == "":
                    QMessageBox.warning(self, "OCR Result", "No Arabic text detected.")
                else:
                    self.text_edit.setText(ocr_result)
                    QMessageBox.information(self, "OCR Result", "Text extracted successfully!")

            except Exception as e:
                print("Error during OCR:", e)
                QMessageBox.critical(self, "OCR Error", str(e))

    def copy_clicked(self):
        text_to_copy = self.text_edit.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)
        print(f"Copied text to clipboard: {text_to_copy}")
        QMessageBox.information(self, "Copied", "Text copied to clipboard!")

    def speak_clicked(self):
        text_to_speak = self.text_edit.toPlainText().strip()
        if not text_to_speak:
            QMessageBox.warning(self, "Speak", "No text to speak.")
            return

        try:
            # Convert text to speech (Arabic)
            tts = gTTS(text=text_to_speak, lang='ar')
            temp_audio = "temp_speech.mp3"
            tts.save(temp_audio)

            # Play the mp3
            playsound(temp_audio)

            # Clean up temp file
            os.remove(temp_audio)

        except Exception as e:
            print("Error during speech synthesis:", e)
            QMessageBox.critical(self, "Speech Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackgroundWindow("ocr_background.png")
    window.show()
    sys.exit(app.exec_())
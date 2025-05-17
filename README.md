# 📝 Arabic OCR App

A **desktop application** built with **PyQt5** that performs **Arabic Optical Character Recognition (OCR)** from images using **Tesseract OCR**, with features for text extraction, clipboard copying, and speech synthesis.


## 🚀 Features

- Extract **Arabic text** from images (OCR).
- **Copy** recognized text to clipboard.
- **Read aloud** extracted text using Text-to-Speech.
- Clean and user-friendly graphical interface.
- Contrast enhancement for better OCR accuracy.


## 📦 Requirements

```bash
pip install PyQt5 pillow pytesseract gTTS playsound
```

Also, ensure **Tesseract OCR** is installed and accessible:

```bash
brew install tesseract
```

Arabic language data required:

```bash
brew install tesseract-lang
```

Or manually place ara.traineddata inside Tesseract's tessdata directory.

## 🛠️ How to Run

```bash
python arabic_ocr_app.py
```

## 📂 File Dependencies

* ocr_background.png — Background image for the GUI.
* scan_button.png — Icon for the scan button.
* copy_button.png — Icon for the copy button.
* speak_button.png — Icon for the speak button.

Make sure these images are in the same directory as your Python script.

## 🖼️ Application Screenshot

<img width="986" alt="arabic_ocr_with_tts" src="https://github.com/user-attachments/assets/f5b734a5-6422-4157-87b4-06ae758ffde0" />

## 🧠 Workflow

1. Click **Scan** to select an image and extract Arabic text.
2. Review the recognized text in the text box.
3. Click **Copy** to copy the text to clipboard.
4. Click **Speak** to read the text aloud in Arabic.

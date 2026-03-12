# 📄 PDF Splitter and Guide Number Recognizer

**PDF Splitter and Guide Number Recognizer** is a Python desktop application designed to process large PDF documents that contain multiple shipping guides or similar documents.

The application automatically identifies **guide numbers located in the upper-right section of each page** and also searches for **barcode-like numeric patterns located in the lower part of the document**.

Once a guide number is detected, the program **splits the original PDF into individual files**, naming each file using the detected guide number.

If a page cannot be identified, it is automatically stored inside an **Unidentified** folder for manual review.

This tool is particularly useful for **logistics workflows, shipping operations, and document management processes** where large batches of PDF guides must be separated automatically.

---

# ✨ Features

- Automatic **PDF page splitting**
- **Guide number detection** from printed text
- **Pattern recognition** inside barcode strings
- **OCR fallback detection** using Tesseract
- Automatic **file naming based on detected guide numbers**
- **Unidentified page separation**
- **Graphical user interface**
- **Real-time progress bar**
- Automatic **output folder opening after processing**

---

# ⚙️ How the Program Works

The application processes the document in several stages.

### 1. PDF Selection

The user selects a PDF file using the graphical interface.

### 2. Native Text Extraction

The program first attempts to extract text directly from the PDF using `pdfplumber`.  
If the guide number is embedded as text, this method is the fastest and most accurate.

### 3. Pattern Recognition

The system searches for patterns such as:
N° 12345678


It also searches for **barcode-like numeric sequences** embedded within longer strings.

### 4. OCR Detection (Fallback)

If the guide number cannot be found through text extraction, the program:

- Converts the page into an image
- Crops the **upper-right section of the document**
- Preprocesses the image
- Runs **Tesseract OCR**

This allows the system to detect numbers even in **scanned PDFs**.

### 5. Automatic PDF Splitting

Each page is saved as an individual PDF file.

If the guide number is detected:
82959712.pdf

If the guide number is not detected:
Page_5_Review.pdf


These unidentified files are automatically placed inside the **Unidentified** folder.

---

# 📚 Libraries Used

The program relies on several Python libraries that handle different parts of the processing pipeline.

## os

Used for operating system interactions including directory creation, file path handling, file existence checking, and automatically opening the output folder.

## re (Regular Expressions)

Used to detect guide numbers through **pattern matching**.

Example patterns:
N° 12345678
000000000123456780000000000


Regular expressions allow the program to detect numbers even when formatting changes slightly.

## threading

Used to run the processing logic in a **separate thread**, preventing the graphical interface from freezing while large PDFs are being processed.

## tkinter

Provides the **graphical user interface (GUI)** of the application.

The interface includes:

- File selection
- Start processing button
- Progress bar
- Status messages
- Completion alerts

## pdf2image

Converts PDF pages into images when OCR analysis is required.

Main function used:
convert_from_path()


## pytesseract

Python wrapper for the **Tesseract OCR engine** used to extract text from images when the PDF does not contain embedded text.

## OpenCV (cv2)

Used for **image preprocessing** before OCR including cropping the region of interest, grayscale conversion, and thresholding.

## numpy

Used for **image array manipulation** during OpenCV processing.

## pikepdf

Handles **PDF manipulation and splitting**, including opening the original PDF, extracting pages, creating new documents, and saving them individually.

## pdfplumber

Used for **native text extraction** from PDFs before OCR is attempted.

---

# 📂 Output Structure

After processing, the program generates the following structure:
Separate_Files/
│
├── 82959712.pdf
├── 82959713.pdf
├── 82959714.pdf
│
└── Unidentified/
├── Page_5_Review.pdf
├── Page_12_Review.pdf


Identified guides are saved using the **guide number as the filename**, while unidentified pages are placed in the **Unidentified** folder.

---

# 📦 Requirements

Python 3.9+

External tools required:

- **Tesseract OCR**
- **Poppler**

Install Python dependencies with:
pip install pdf2image pytesseract opencv-python numpy pikepdf pdfplumber

---

# 👨‍💻 Author

Created by **Domingo Galaz Ramirez**

© All rights reserved

![PDF](https://github.com/user-attachments/assets/9084ba8b-a18b-43ce-b2f0-acb657139787)


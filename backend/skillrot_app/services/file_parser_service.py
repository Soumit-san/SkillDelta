import io
import re
import pdfplumber
import pytesseract
import pandas as pd
import docx

from PIL import Image
from typing import Dict
from pdf2image import convert_from_bytes


# ============================================================
# 🔹 OCR CONFIG (Windows Safe)
# ============================================================

# ✅ Works on both Windows and Render (Linux)
import os

if os.name == "nt":  # Windows
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:  # Linux (Render)
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# ============================================================
# 🔹 TEXT CLEANER (NEW)
# ============================================================

def clean_extracted_text(text: str) -> str:
    """
    Cleans OCR noise & broken words.
    """

    # ✅ Fix common OCR mistakes
    text = text.replace("lncorrect", "Incorrect")
    text = text.replace("lcorrect", "Incorrect")
    text = text.replace("Concurre ncy", "Concurrency")

    # ✅ Remove strange symbols but keep useful ones
    text = re.sub(r"[^\w\s%&:\-]", " ", text)

    # ✅ Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# 🔹 MAIN ENTRY
# ============================================================

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:

    filename = filename.lower()

    try:

        if filename.endswith(".txt"):
            text = file_bytes.decode(errors="ignore")

        elif filename.endswith(".pdf"):
            text = extract_from_pdf(file_bytes)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            text = extract_from_image(file_bytes)

        elif filename.endswith(".docx"):
            text = extract_from_docx(file_bytes)

        elif filename.endswith(".csv"):
            text = extract_from_csv(file_bytes)

        elif filename.endswith((".xlsx", ".xls")):
            text = extract_from_excel(file_bytes)

        else:
            text = file_bytes.decode(errors="ignore")

        # 🔥 CLEAN TEXT BEFORE RETURNING
        return clean_extracted_text(text)

    except Exception as e:
        print("File parsing error:", e)
        return ""


# ============================================================
# 🔹 PDF PARSER
# ============================================================

def extract_from_pdf(file_bytes: bytes) -> str:
    text = ""

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # 🔥 OCR fallback if no text layer
        if not text.strip():
            images = convert_from_bytes(file_bytes)
            for img in images:
                text += pytesseract.image_to_string(img)

    except Exception as e:
        print("PDF parsing error:", e)

    return text


# ============================================================
# 🔹 IMAGE OCR
# ============================================================

def extract_from_image(file_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)
    except Exception as e:
        print("Image OCR error:", e)
        return ""


# ============================================================
# 🔹 DOCX
# ============================================================

def extract_from_docx(file_bytes: bytes) -> str:
    try:
        document = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e:
        print("DOCX parsing error:", e)
        return ""


# ============================================================
# 🔹 CSV
# ============================================================

def extract_from_csv(file_bytes: bytes) -> str:
    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
        return df.to_string()
    except Exception as e:
        print("CSV parsing error:", e)
        return ""


# ============================================================
# 🔹 EXCEL
# ============================================================

def extract_from_excel(file_bytes: bytes) -> str:
    try:
        df = pd.read_excel(io.BytesIO(file_bytes))
        return df.to_string()
    except Exception as e:
        print("Excel parsing error:", e)
        return ""

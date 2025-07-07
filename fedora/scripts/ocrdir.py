#!/usr/bin/env python3


import os
import fitz  # PyMuPDF
import pytesseract
from tqdm import tqdm
from pathlib import Path
from PIL import Image
import io

INPUT_DIR = "."
OUTPUT_DIR = "ocr_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def is_pdf_searchable(pdf_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        if page.get_text().strip():  # Found real text
            return True
    return False


def ocr_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    new_pdf = fitz.open()  # New PDF with OCR text

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")

        # OCR with Tesseract
        image = Image.open(io.BytesIO(img_data))
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension="pdf")

        # Append OCR'd page to new PDF
        ocr_page = fitz.open("pdf", pdf_bytes)
        new_pdf.insert_pdf(ocr_page)

    new_pdf.save(output_path)


def main():
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        input_path = os.path.join(INPUT_DIR, pdf_file)
        output_path = os.path.join(OUTPUT_DIR, pdf_file)

        if is_pdf_searchable(input_path):
            print(f"[SKIP] Already searchable: {pdf_file}")
            continue

        try:
            ocr_pdf(input_path, output_path)
            print(f"[OCR DONE] {pdf_file}")
        except Exception as e:
            print(f"[ERROR] Failed to OCR {pdf_file}: {e}")


if __name__ == "__main__":
    main()

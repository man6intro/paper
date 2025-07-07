#!/usr/bin/env python

import os
import sys
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader, PdfWriter


def extract_pages_with_string(search_str, output_dir="extracted_page"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        print(f"Scanning {pdf_file}...")
        try:
            reader = PdfReader(pdf_file)
        except Exception as e:
            print(f"Cannot open {pdf_file}: {e}")
            continue

        for page_number in range(len(reader.pages)):
            # Extract text using pdfminer
            try:
                text = extract_text(pdf_file, page_numbers=[page_number])
            except Exception as e:
                print(f"Cannot extract text from page {page_number+1}: {e}")
                continue

            if text and search_str.lower() in text.lower():
                writer = PdfWriter()
                writer.add_page(reader.pages[page_number])

                base_name = os.path.splitext(pdf_file)[0]
                output_filename = f"{base_name}_page_{page_number + 1}.pdf"
                output_path = os.path.join(output_dir, output_filename)

                with open(output_path, "wb") as f:
                    writer.write(f)

                print(f"Found and saved: {output_filename}")


if len(sys.argv) < 2:
    print("Usage: python extract_pdf_page.py <search_string>")
    sys.exit(1)

search_string = sys.argv[1]
extract_pages_with_string(search_string)

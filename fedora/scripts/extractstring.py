#!/usr/bin/env python3


import os
import sys
import re
import fitz  # PyMuPDF
from multiprocessing import Pool, cpu_count

OUTPUT_DIR = "extracted_page"


def load_search_strings(arg):
    if os.path.isfile(arg) and arg.lower().endswith(".txt"):
        with open(arg, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    else:
        return [arg.strip()]


def build_search_pattern(search_strings):
    # Allows partial, case-insensitive matches like "hoo" in "hooligan"
    escaped = [re.escape(s) for s in search_strings]
    return re.compile("|".join(escaped), re.IGNORECASE)


def process_pdf(args):
    pdf_file, pattern = args

    try:
        doc = fitz.open(pdf_file)
    except Exception as e:
        print(f"❌ Cannot open {pdf_file}: {e}")
        return

    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    modified = False

    for page_number in range(len(doc)):
        try:
            text = doc[page_number].get_text()
        except Exception as e:
            print(f"❌ Error reading page {page_number + 1} of {pdf_file}: {e}")
            continue

        if pattern.search(text):
            output_filename = f"{base_name}_page_{page_number + 1}.pdf"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            if os.path.exists(output_path):
                print(f"⏭️ Already exists: {output_filename}")
                continue

            try:
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_number, to_page=page_number)
                new_doc.save(output_path)
                new_doc.close()
                print(f"✅ Saved: {output_filename}")
                modified = True
            except Exception as e:
                print(f"❌ Failed to write page {page_number + 1}: {e}")

    doc.close()
    if not modified:
        print(f"❌ No match found in {pdf_file}")


def main(arg):
    search_strings = load_search_strings(arg)
    if not search_strings:
        print("❌ No search strings found.")
        sys.exit(1)

    pattern = build_search_pattern(search_strings)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    pdf_files = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No PDF files found in current directory.")
        return

    tasks = [(pdf_file, pattern) for pdf_file in pdf_files]

    with Pool(cpu_count()) as pool:
        pool.map(process_pdf, tasks)


if len(sys.argv) < 2:
    print("Usage:")
    print("  python extract_pdf_page.py 'search string'")
    print("  python extract_pdf_page.py search_terms.txt")
    sys.exit(1)

main(sys.argv[1])

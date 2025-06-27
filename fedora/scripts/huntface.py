#!/usr/bin/env python3

import cv2
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import numpy as np
import os


OUTPUT_DIR = "output_faces"
TARGET_WIDTH_CM = 5
TARGET_HEIGHT_CM = 7
DPI = 300
TARGET_SIZE_PX = (int(TARGET_WIDTH_CM / 2.54 * DPI), int(TARGET_HEIGHT_CM / 2.54 * DPI))
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

os.makedirs(OUTPUT_DIR, exist_ok=True)

face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)


def detect_and_crop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    results = []
    for x, y, w, h in faces:
        center_x = x + w // 2
        box_h = int(h * 2.5)
        box_w = int(box_h * 0.75)

        x1 = max(center_x - box_w // 2, 0)
        y1 = max(y - int(h * 0.8), 0)  # nice frame,0.6 will cut the head a bit
        x2 = min(center_x + box_w // 2, image.shape[1])
        y2 = min(y1 + box_h, image.shape[0])

        crop = image[y1:y2, x1:x2]
        results.append(crop)
    return results


def center_and_pad_to_passport(crop):
    img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    img = ImageOps.fit(
        img, TARGET_SIZE_PX, method=Image.Resampling.LANCZOS, centering=(0.5, 0.4)
    )
    return img


def save_cropped_image(pil_image, base_name, index):
    filename = os.path.join(OUTPUT_DIR, f"{base_name}_{index}.jpg")
    pil_image.save(filename, format="JPEG", dpi=(DPI, DPI))


def process_image_file(filepath, base_name):
    image = cv2.imread(filepath)
    if image is None:
        print(f"Could not read image: {filepath}")
        return
    crops = detect_and_crop(image)
    for i, crop in enumerate(crops):
        result = center_and_pad_to_passport(crop)
        save_cropped_image(result, base_name, i)


def process_pdf_file(filepath, base_name):
    doc = fitz.open(filepath)
    for page_number in range(len(doc)):
        pix = doc[page_number].get_pixmap(dpi=DPI)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        crops = detect_and_crop(image)
        for i, crop in enumerate(crops):
            result = center_and_pad_to_passport(crop)
            save_cropped_image(result, f"{base_name}_p{page_number}", i)


def process_files(start_dir):
    for dirpath, _, filenames in os.walk(start_dir):
        for filename in filenames:
            if OUTPUT_DIR in dirpath:
                continue  # Skip output directory
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, start_dir)
            base_name = os.path.splitext(rel_path.replace(os.sep, "_"))[0]
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                process_image_file(filepath, base_name)
            elif filename.lower().endswith(".pdf"):
                process_pdf_file(filepath, base_name)


print("Scanning current directory and subdirectories for PDFs and images...")
process_files(os.getcwd())
print(f"Done! Cropped and formatted passport-style photos saved in '{OUTPUT_DIR}'.")

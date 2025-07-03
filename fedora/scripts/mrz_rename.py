#!/usr/bin/env python3

import re
import warnings
from pathlib import Path
from passporteye.mrz.image import MRZPipeline

# --- Suppress future warnings from skimage ---
warnings.filterwarnings("ignore", category=FutureWarning)

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def sanitize(text):
    return re.sub(r"[^A-Z0-9]", "_", text.upper())


class SafeMRZPipeline(MRZPipeline):
    @property
    def result(self):
        try:
            res = super().result
            if res and "method" not in res.aux:
                res.aux["method"] = "unknown"
            return res
        except KeyError as e:
            print(f"[!] KeyError in PassportEye: {e}")
            return None


def rename_file_with_mrz(file_path: Path):
    result = SafeMRZPipeline(str(file_path)).result
    if result is None:
        print(f"[!] MRZ not found or failed in: {file_path.name}")
        return

    fields = result.to_dict()
    doc_number = sanitize(fields.get("number", "UNKNOWN"))
    surname = sanitize(fields.get("surname", "UNKNOWN"))

    new_name = f"{doc_number}_{surname}{file_path.suffix.lower()}"
    new_path = file_path.with_name(new_name)

    counter = 1
    while new_path.exists():
        new_name = f"{doc_number}_{surname}_{counter}{file_path.suffix.lower()}"
        new_path = file_path.with_name(new_name)
        counter += 1

    file_path.rename(new_path)
    print(f"[✓] Renamed: {file_path.name} -> {new_name}")


def main():
    current_dir = Path.cwd()
    for file in current_dir.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXT:
            rename_file_with_mrz(file)


main()

#!/usr/bin/env python3
"""
flatten_copy_with_autoname.py

Flattens all files from nested directories into a single target directory.
Automatically renames duplicate files with zero-padded numbers.
"""

import os
import shutil
from pathlib import Path


def get_padded_name(base, ext, counter):
    """Return a filename with padded counter"""
    padding = max(3, len(str(counter)))
    return f"{base}_{counter:0{padding}d}{ext}"


def generate_unique_name(dump_dir, original_name):
    """Avoid name collisions in the dump directory"""
    base = original_name.stem
    ext = original_name.suffix
    candidate = dump_dir / original_name.name
    counter = 1

    while candidate.exists():
        new_name = get_padded_name(base, ext, counter)
        candidate = dump_dir / new_name
        counter += 1

    return candidate


def copy_all_files_flat(src_dir, dump_dir):
    """copy all files to dump_dir"""
    src_dir = Path(src_dir).resolve()
    dump_dir = Path(dump_dir).resolve()

    if not src_dir.exists():
        print(f"Source directory does not exist: {src_dir}")
        return

    dump_dir.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(src_dir):
        for file_name in files:
            source_path = Path(root) / file_name
            target_path = generate_unique_name(dump_dir, Path(file_name))

            try:
                shutil.copy2(source_path, target_path)
                print(f"Copied: {source_path} -> {target_path.name}")
            except Exception as e:
                print(f"Error copying {source_path}: {e}")


if __name__ == "__main__":
    src = input("Enter source folder path: ").strip()
    dst = input("Enter dump folder path: ").strip()
    copy_all_files_flat(src, dst)

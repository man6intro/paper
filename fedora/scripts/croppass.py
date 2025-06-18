import os
from PIL import Image
from rembg import new_session, remove
import numpy as np

# Load segmentation session once
session = new_session("u2net_human_seg")


def get_subject_bbox(img):
    """Run rembg to get the subject mask and compute its bounding box."""
    result = remove(img, session=session, only_mask=True)
    mask_np = np.array(result.convert("L"))
    binary = mask_np > 10  # threshold to identify subject

    coords = np.argwhere(binary)
    if coords.size == 0:
        return None  # No subject found
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    return (x0, y0, x1, y1)


def process_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB")

            bbox = get_subject_bbox(img)
            if bbox:
                cropped = img.crop(bbox)
                cropped.save(output_path, format="JPEG")
                print(f"Cropped: {input_path} → {output_path}")
            else:
                print(f"No subject found in {input_path}, skipped.")
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")


def process_images_recursive(input_dir, output_dir):
    supported_extensions = (".png", ".jpg", ".jpeg")
    os.makedirs(output_dir, exist_ok=True)

    input_dir_abs = os.path.abspath(input_dir)
    output_dir_abs = os.path.abspath(output_dir)

    for dirpath, dirnames, filenames in os.walk(input_dir):
        dirpath_abs = os.path.abspath(dirpath)

        # Skip the output directory and its children
        if dirpath_abs.startswith(output_dir_abs):
            continue

        for filename in filenames:
            if filename.lower().endswith(supported_extensions):
                input_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(dirpath, input_dir)
                save_dir = os.path.join(output_dir, rel_path)
                os.makedirs(save_dir, exist_ok=True)

                output_filename = os.path.splitext(filename)[0] + ".jpg"
                output_path = os.path.join(save_dir, output_filename)

                process_image(input_path, output_path)


if __name__ == "__main__":
    input_directory = "."  # current working directory
    output_directory = "cropped_subject_original_bg"
    process_images_recursive(input_directory, output_directory)

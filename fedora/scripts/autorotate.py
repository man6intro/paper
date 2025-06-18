import os
from PIL import Image
import numpy as np
from rembg import remove, new_session

# Load once
session = new_session()

# Get subject mask using rembg
def get_mask(img):
    mask = remove(img, session=session, only_mask=True)
    return np.array(mask.convert("L")) > 10  # binary mask

# Score based on subject pixels in the bottom half
def bottom_score(mask):
    h, _ = mask.shape
    return mask[h // 2 :, :].sum()

# Try 0°, 90°, 180°, 270° and pick best
def auto_rotate(img, filename):
    print(f"🔍 Analyzing: {filename}")
    best_score = -1
    best_img = img
    best_angle = 0

    for angle in [0, 90, 180, 270]:
        rotated = img.rotate(angle, expand=True)
        try:
            mask = get_mask(rotated)
            score = bottom_score(mask)
            print(f" → {angle}° → score: {score}")
            if score > best_score:
                best_score = score
                best_img = rotated
                best_angle = angle
        except Exception as e:
            print(f" ✗ Error on {filename} at {angle}°: {e}")
            continue

    print(f" ✅ Best angle: {best_angle}°\n")
    return best_img

# Walk through current directory
def process_directory(input_dir="."):
    supported_exts = (".jpg", ".jpeg", ".png")
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith(supported_exts):
                fpath = os.path.join(root, fname)
                try:
                    with Image.open(fpath) as img:
                        result = auto_rotate(img, fname)
                        result.save(fpath)  # Overwrite original
                except Exception as e:
                    print(f" ✗ Error opening {fname}: {e}")

# Run
if __name__ == "__main__":
    process_directory(".")

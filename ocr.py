import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np
import os

# Uncomment and set path if on Windows:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path: str) -> np.ndarray:
    """Enhance image quality before OCR."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    # Sharpen
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    # Threshold (Otsu)
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text_from_image(image_path: str) -> dict:
    """
    Extract text from a pill/medicine image using OCR.
    Returns dict with raw text, cleaned tokens, and confidence info.
    """
    try:
        processed = preprocess_image(image_path)
        # Use PIL image for pytesseract
        pil_img = Image.fromarray(processed)

        # Multiple OCR configs for best result
        configs = [
            "--psm 6",   # Uniform block of text
            "--psm 11",  # Sparse text
            "--psm 3",   # Fully automatic
        ]

        best_text = ""
        best_conf = 0

        for cfg in configs:
            data = pytesseract.image_to_data(pil_img, config=cfg, output_type=pytesseract.Output.DICT)
            confidences = [int(c) for c in data["conf"] if int(c) > 0]
            avg_conf = sum(confidences) / len(confidences) if confidences else 0
            text = pytesseract.image_to_string(pil_img, config=cfg)
            if avg_conf > best_conf:
                best_conf = avg_conf
                best_text = text

        tokens = clean_tokens(best_text)

        return {
            "success": True,
            "raw_text": best_text,
            "tokens": tokens,
            "confidence": round(best_conf, 2),
        }

    except Exception as e:
        return {
            "success": False,
            "raw_text": "",
            "tokens": [],
            "confidence": 0,
            "error": str(e),
        }

def clean_tokens(text: str) -> list:
    """Clean and tokenize extracted text into meaningful drug name candidates."""
    import re
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)
    words = text.split()
    # Filter short noise words and common non-drug tokens
    noise = {"mg", "ml", "tab", "cap", "the", "and", "for", "use", "only", "each", "with"}
    tokens = [w.strip() for w in words if len(w) > 2 and w.lower() not in noise]
    return list(dict.fromkeys(tokens))  # deduplicate preserving order

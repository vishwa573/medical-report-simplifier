# extract.py
"""
Module: extract
Purpose: Extract raw text from medical reports (image or direct text).
"""

import pytesseract # type: ignore
import cv2 # type: ignore
import re
from paddleocr import PaddleOCR # type: ignore

import logging


logging.disable(logging.INFO) 

def _parse_ocr_results(results):
    """Helper to parse the complex dictionary from PaddleOCR."""
    if not results or not results[0]:
        return [], 0.0
    image_results = results[0]
    texts = image_results.get('rec_texts', [])
    scores = image_results.get('rec_scores', [])
    if not texts or not scores:
        return [], 0.0
    avg_confidence = sum(scores) / len(scores) if scores else 0.0
    return texts, round(avg_confidence, 4)

def _preprocess_for_handwriting(image_path):
    """Applies OpenCV filters to improve handwriting recognition."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    binary_img = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    # Un comment the next lines if you want to see the preprocessed image
    # cv2.imshow("Preprocessed Image", binary_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
   
    return cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

def extract_text_from_report(ocr_engine, image_path, confidence_threshold=0.90):
    """
    Runs an adaptive OCR process and returns a tuple of the final text string
    and the corresponding average confidence score.
    """
    try:
        # Run on the original image ---
        print("--- Running OCR Pass 1 (Original Image) ---")
        results_pass1 = ocr_engine.predict(image_path)
        texts_pass1, avg_confidence_pass1 = _parse_ocr_results(results_pass1)
        
        print(f"Confidence on original: {avg_confidence_pass1:.2f}")

        if avg_confidence_pass1 >= confidence_threshold:
            # Return both text and confidence ---
            return "\n".join(texts_pass1), avg_confidence_pass1

        # If confidence is low, preprocess and try again ---
        print(f"\nLow confidence. Applying handwriting preprocessing...")
        preprocessed_image = _preprocess_for_handwriting(image_path)
        
        print("--- Running OCR Pass 2 (Preprocessed Image) ---")
        results_pass2 = ocr_engine.predict(preprocessed_image)
        
        # Capture the confidence from the second pass ---
        texts_pass2, avg_confidence_pass2 = _parse_ocr_results(results_pass2)
        
        print(f"Confidence on preprocessed: {avg_confidence_pass2:.2f}")
        
        # Return both text and new confidence ---
        return "\n".join(texts_pass2), avg_confidence_pass2

    except FileNotFoundError:
        print(f"ERROR: The file was not found at path: {image_path}")
        # Return a consistent tuple for errors ---
        return None, 0.0
    except Exception as e:
        print(f"An unexpected error occurred during OCR: {e}")
        # Return a consistent tuple for errors ---
        return None, 0.0



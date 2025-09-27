# Pipeline.py
"""
Pipeline driver for the Medical Report Simplifier.
Takes raw text input or images and processes it into structured JSON.
"""

import json
from core.extract import  extract_text_from_report
from core.parser import  normalize_tests,_extract_test_lines_from_text
from core.summarizer import generate_summary
# from paddleocr import PaddleOCR 


def clean_status_word(status: str) -> str:
    """Normalizes common status typos to standard labels: high, low, normal."""
    status_map = {
        "hgh": "high",
        "hi": "high",
        "loh": "low",
        "noraml": "normal",
    }
    return status_map.get(status.lower(), status.lower())


def process_medical_report(raw_text: str = None, image_path: str = None, ocr_engine=None):
    """
    The single entry point for the entire processing pipeline.
    It handles either a raw_text string or an image_path, fixes the tuple bug,
    and provides accurate confidence scores for Step 1.
    """
    final_raw_text = ""
    # Set a default confidence score for the raw text case 
    step1_confidence = 1.0 

    # --- Step 0: Determine Input and Get Raw Text ---
    if image_path:
        if not ocr_engine:
            return {"status": "error", "reason": "OCR engine not provided for image processing."}
        
        final_raw_text, ocr_confidence = extract_text_from_report(ocr_engine, image_path)
        step1_confidence = ocr_confidence # Update confidence with the real OCR score
        
        # This check now correctly operates on the string part of the tuple
        if final_raw_text is None:
             return {"status": "error", "reason": "Image file not found or could not be processed."}
        if not final_raw_text.strip():
            return {"status": "unprocessed", "reason": "OCR failed: No text could be extracted from the image."}
            
    elif raw_text:
        final_raw_text = raw_text
        # The step1_confidence will remain its default of 1.0
    else:
        return {"status": "error", "reason": "No input provided (either text or image is required)."}

    try:
        # Step 1: Extract test lines from the raw text
        print("=== Step 1: OCR/Text Extraction  ===")
        extraction_result = _extract_test_lines_from_text(final_raw_text)
        # print("Extracted Lines:", extraction_result)
        step1_output = {
            "tests_raw": [line.strip() for line in final_raw_text.split("\n") if line.strip()],
            "correction_confidence": step1_confidence
        }
        print(json.dumps(step1_output, indent=2))
        
        if not extraction_result:
            return {"status": "unprocessed", "reason": "No hallucinated tests not present in input"} #Used this reason becasue this was mentioned in the problem statment ,but the wording is confusing

        # Step 2: Normalize the extracted test lines
        print("\n=== Step 2: Normalization ===")
        normalization_result = normalize_tests(extraction_result)
        normalized_tests = normalization_result.get("tests", [])
        print(json.dumps(normalization_result, indent=2))

        if not normalized_tests:
            return {"status": "unprocessed", "reason": "No hallucinated tests not present in input."}
        
        # Step 3: Generate the summary
        print("\n=== Step 3: Patient-Friendly Summary ===")
        summary_result = generate_summary(normalized_tests)
        print(json.dumps(summary_result, indent=2))
        
        # Step 4: Return the final, successful output
        print("\n=== Step 4: Final Output ===")
        final_output = {
            "tests": normalized_tests,
            "summary": summary_result["summary"],
            "status": "ok"
        }
        print(json.dumps(final_output, indent=2))
        return final_output

    except Exception as e:
        return {"status": "error", "reason": str(e)}



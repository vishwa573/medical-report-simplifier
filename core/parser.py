# parser.py
"""
Module: parser
Purpose: Correct OCR typos in test names and normalize them into structured JSON.
"""

import re
from thefuzz import process, fuzz 
from core.knowledge_base import VALID_TEST_NAMES, MEDICAL_TESTS

def _extract_test_lines_from_text(raw_text: str) -> list[str]:
    headers_to_remove = ['cbc:', 'bc:']
    processed_text = raw_text.lower()
    for header in headers_to_remove:
        processed_text = processed_text.replace(header, '')

    # Insert space between letters and numbers
    processed_text = re.sub(r'([a-zA-Z])(?=\d)', r'\1 ', processed_text)

    # Split into lines
    lines = re.split(r'[\n;]+', processed_text)

    # Forgiving regex pattern
    pattern = re.compile(
        r"([a-zA-Z\s\(\)]+?)"     # Name
        r"\s*:?\s*"                # Optional colon/space
        r"([\d,.]+)"               # Value
        r"\s*"                     # Optional space
        r"([a-zA-Z\s/µdL]+)?"      # Optional unit
        r"(?:\s*\(([\w\s]+)\)?)?", # Optional status
        re.IGNORECASE
    )

    extracted_lines = []
    for line in lines:
        matches = pattern.finditer(line)
        extracted_lines.extend([m.group(0).strip() for m in matches])

    return extracted_lines


# --- Example Usage ---
# test_string_1 = "CBC: Hemoglobin: 10.2 g/dL (Low), WBC 11,200 /uL (High)"
# test_string_2 = "BUN 8mg/dL(Low)\nPlatelets: 15000o /uL (Low)"

# print(_extract_test_lines_from_text(test_string_1))
# print(_extract_test_lines_from_text(test_string_2))

def find_best_test_name_match(raw_name: str, valid_names: list[str], score_cutoff: int = 75):
    """
    Finds the best matching test name from a predefined list using fuzzy string matching.

    Args:
        raw_name (str): The test name extracted from OCR, which may have errors.
        valid_names (list[str]): The list of correct test names from the knowledge base.
        score_cutoff (int): The minimum confidence score (0-100) to consider a match valid.

    Returns:
        str or None: The best matching valid test name, or None if no match meets the cutoff.
    """
    # process.extractOne finds the best match and its score
    best_match, score = process.extractOne(raw_name, valid_names)
    
    if score >= score_cutoff:
        return best_match
    else:
        print(f"Warning: No confident match found for '{raw_name}'. Best guess was '{best_match}' with score {score}. Skipping.")
        return None
    
def _sanitize_unit(unit_str: str) -> str:
    """A helper function to clean up unit strings for comparison."""
    # 1. Convert to lowercase
    sanitized = unit_str.lower()
    # 2. Remove all whitespace
    sanitized = re.sub(r'\s+', '', sanitized)
    # 3. Correct common OCR mistakes (add more as you find them)
    if 'ul' in sanitized:
        sanitized = sanitized.replace('ul', 'µl').replace('μl', 'µl') 
    
    return sanitized


def _determine_status(status_raw, value, test_info):
    """
    Determines the final status of a test.
    It normalizes a written status, or derives it from the value if the status is missing.
    Returns the status string ('high', 'low', 'normal') or None if the test should be skipped.
    """
    if status_raw:
        # Case 1: A status IS written in the text -> Normalize it.
        status_phrase = status_raw.lower()
        status_map = {
            "high": "high", "hgh": "high", "h": "high","ligh": "high",
            "low": "low", "l": "low", "loh": "low",
            "normal": "normal", "n": "normal", "noraml": "normal"
        }
        status = status_map.get(status_phrase)
        if status is None:  # If not an abbreviation, check for keywords
            if 'high' in status_phrase:
                status = 'high'
            elif 'low' in status_phrase:
                status = 'low'
            else:
                print(f"Warning: Unknown status phrase '{status_phrase}'. Skipping.")
                return None # Signal to skip this test
        return status
    else:
        # Case 2: A status IS NOT written -> Derive it from the value.
        ref_range = test_info['ref_range']
        if value < ref_range['low']:
            return 'low'
        elif value > ref_range['high']:
            return 'high'
        else:
            return 'normal'

def normalize_tests(corrected_lines: list[str]):
    """
    Converts corrected test lines into structured JSON (Refactored for clarity).
    """
    normalized_results = []
    pattern = re.compile(
        # Group 1: Name (letters, spaces, digits, dots, parentheses)
        r"([a-zA-Z\s\d\.\(\)]+?)"
        # Matches a colon (with optional spaces) OR one or more spaces
        r"(?:\s*:\s*|\s+)"
        # Group 2: Value (digits, commas, dots, and o/O for zero)
        r"([\d,.oO]+)\s*"
        # Group 3: Optional Unit (with spaces and µ allowed)
        r"([a-zA-Z\s/µdL]+)?"
        # Group 4: Optional Status (in parentheses, with optional space before)
        r"(?:\s*\(([\w\s]+)\))?",
        
        re.IGNORECASE
        )

    for line in corrected_lines:
        match = pattern.search(line)
        if not match:
            continue
            
        # --- 1. Extract Data ---
        raw_name = match.group(1).strip()
        value_str = match.group(2).replace(',', '').replace('o', '0').replace('O', '0')
        unit_raw = match.group(3).strip() if match.group(3) else None
        status_raw = match.group(4)
        
        # --- 2. Validate Name ---
        best_match_name = find_best_test_name_match(raw_name, VALID_TEST_NAMES)
        if not best_match_name:
            continue
        test_info = MEDICAL_TESTS.get(best_match_name)
        
        # --- 3. Validate Unit ---
        if unit_raw:
            if _sanitize_unit(unit_raw) != _sanitize_unit(test_info["unit"]):
                print(f"Warning: Unit mismatch for '{best_match_name}'. Expected '{test_info['unit']}', got '{unit_raw}'. Skipping.")
                continue
        
        try:
            value = float(value_str)
        except ValueError:
            continue
            
        # --- 4. Determine Status using the helper function ---
        status = _determine_status(status_raw, value, test_info)
        if status is None:
            continue

        # --- 5. Append Result ---
        normalized_results.append({
            "name": best_match_name,
            "value": value,
            "unit": test_info["unit"],
            "status": status,
            "ref_range": test_info["ref_range"]
        })

    # --- 6. Calculate Confidence and Return ---
    normalization_confidence = round(
        (len(normalized_results) / len(corrected_lines)) if corrected_lines else 0.0, 2
    )
    return {
        "tests": normalized_results,
        "normalization_confidence": normalization_confidence
    }


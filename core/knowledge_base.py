# knowledge_base.py
"""
Module: knowledge_base
Purpose: Centralized repository of medical test information, reference ranges, and explanations.
"""

MEDICAL_TESTS = {
    # --- Complete Blood Count (CBC) Panel ---
    "hemoglobin": {
        "unit": "g/dL",
        "ref_range": {"low": 12.0, "high": 15.0},
        "explanation_low": "is lower than the normal range, which may relate to anemia or nutritional issues.",
        "explanation_high": "is higher than the normal range, which can occur due to dehydration or other conditions.",
    },
    "wbc": {
        "unit": "/uL",
        "ref_range": {"low": 4000, "high": 11000},
        "explanation_low": "count is lower than the normal range, which can reduce the body's ability to fight infection.",
        "explanation_high": "count is higher than the normal range, which may be linked to infection or inflammation.",
    },
    "platelets": {
        "unit": "/uL",
        "ref_range": {"low": 150000, "high": 450000},
        "explanation_low": "count is lower than the normal range, which may increase bleeding risk.",
        "explanation_high": "count is higher than the normal range, which may increase the risk of clotting.",
    },
    "rbc": {
        "unit": "million/uL",
        "ref_range": {"low": 4.2, "high": 5.4},
        "explanation_low": "count is lower than the normal range, which may indicate anemia or blood loss.",
        "explanation_high": "count is higher than the normal range, which may relate to dehydration or other conditions.",
    },
    
    # --- Metabolic Panel ---
    "glucose": {
        "unit": "mg/dL",
        "ref_range": {"low": 70, "high": 100},
        "explanation_low": "level is lower than the normal range, which may indicate hypoglycemia.",
        "explanation_high": "level is higher than the normal range, which may indicate a risk of diabetes."
    },
    "creatinine": {
        "unit": "mg/dL",
        "ref_range": {"low": 0.6, "high": 1.3},
        "explanation_low": "level is lower than the normal range, which is usually not a cause for concern.",
        "explanation_high": "level is higher than the normal range, which may indicate issues with kidney function.",
    },
    "bun": {
        "unit": "mg/dL",
        "ref_range": {"low": 7, "high": 20},
        "explanation_low": "level is lower than the normal range, which is usually not a cause for concern.",
        "explanation_high": "level (Blood Urea Nitrogen) is higher than the normal range, which may relate to kidney function or dehydration.",
    },
    "sodium": {
        "unit": "mEq/L",
        "ref_range": {"low": 135, "high": 145},
        "explanation_low": "level is lower than the normal range, which can be caused by various conditions including fluid loss.",
        "explanation_high": "level is higher than the normal range, often related to dehydration.",
    },
    "potassium": {
        "unit": "mEq/L",
        "ref_range": {"low": 3.5, "high": 5.0},
        "explanation_low": "level is lower than the normal range, which can affect muscle and heart function.",
        "explanation_high": "level is higher than the normal range, which can also impact heart function.",
    },

    # --- Lipid Panel ---
    "cholesterol": {
        "unit": "mg/dL",
        "ref_range": {"low": 125, "high": 200},
        "explanation_low": "level is lower than the normal range, which is rarely a concern.",
        "explanation_high": "level is higher than the normal range, which may increase the risk of heart disease.",
    },
    "triglycerides": {
        "unit": "mg/dL",
        "ref_range": {"low": 0, "high": 150},
        "explanation_low": "level is within the normal range.", # Low is not typically a concern
        "explanation_high": "level is higher than the normal range, which is a risk factor for heart disease.",
    },

    # --- Aliases for common names ---
    "blood sugar (fasting)": {
        "unit": "mg/dL",
        "ref_range": {"low": 70, "high": 100},
        "explanation_low": "level is lower than the normal range for a fasting test, which can cause dizziness or weakness.",
        "explanation_high": "level is higher than the normal range for a fasting test, which may indicate a risk of diabetes.",
    },
    "blood sugar (postprandial)": {
        "unit": "mg/dL",
        "ref_range": {"low": 70, "high": 140},
        "explanation_low": "level is lower than the normal range after a meal, which can cause fatigue.",
        "explanation_high": "level is higher than the normal range after a meal, which may indicate impaired glucose tolerance.",
    },
}

# List of all valid names for fuzzy matching
VALID_TEST_NAMES = list(MEDICAL_TESTS.keys())
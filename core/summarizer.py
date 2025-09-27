# summarizer.py
"""
Module: summarizer
Purpose: Generate patient-friendly summaries from normalized test data.
"""
from core.knowledge_base import MEDICAL_TESTS

def generate_summary(normalized_tests: list[dict]):
    """
    Generates a polished, patient-friendly summary from normalized test data,
    incorporating final suggestions for robustness and readability.
    """
    summary_points = []
    explanations = []
    # You can adjust this limit
    summary_limit = 3 

    for test in normalized_tests:
        name = test.get("name", "Unknown Test")
        status = test.get("status", "normal").lower()
        test_key = name.lower()

        if status != "normal":
            # Capitalize test names for better readability
            summary_points.append(f"{status} {name}")

            explanation_key = f"explanation_{status}"
            explanation_phrase = MEDICAL_TESTS.get(test_key, {}).get(explanation_key, "")
            
            # Check for empty explanation before appending
            if explanation_phrase:
                explanations.append(f"{name} {explanation_phrase}")
            else:
                explanations.append(f"{name}: No specific explanation is available for this result.")
        else:
            explanations.append(f"{name}: This result is within the normal range.")

    # Build the final summary sentence
    if not summary_points:
        summary = "All test results appear to be within the normal range."
    else:
        #  Limit the length of the summary for readability
        if len(summary_points) > summary_limit:
            first_few = ", ".join(summary_points[:summary_limit])
            remaining_count = len(summary_points) - summary_limit
            summary = f"Your report shows {first_few}, and {remaining_count} more abnormal results."
        elif len(summary_points) == 1:
            summary = f"Your report shows {summary_points[0]}."
        elif len(summary_points) == 2:
            summary = f"Your report shows {summary_points[0]} and {summary_points[1]}."
        else: # Handles 3 items (or whatever the summary_limit is)
            summary = "Your report shows " + ", ".join(summary_points[:-1]) + f", and {summary_points[-1]}."

    return {
        "summary": summary,
        # Softer fallback phrasing
        "explanations": explanations or ["No additional details are available for these results."]
    }
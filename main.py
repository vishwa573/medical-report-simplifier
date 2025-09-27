# main.py

from fastapi import FastAPI, File, UploadFile, HTTPException # type: ignore
import uvicorn # type: ignore
import shutil
import os
from paddleocr import PaddleOCR # type: ignore
from pydantic import BaseModel
import uuid

# --- Import the single, main processing function from your pipeline ---
from core.pipeline import process_medical_report

# --- 1. Initialize Heavy Models ONCE ---
print("Initializing PaddleOCR engine (this may take a moment)...")
ocr_engine = PaddleOCR(use_textline_orientation=True, lang='en')
print("Engine initialized.")


# --- 2. Create the FastAPI Application ---
app = FastAPI(
    title="Medical Report Simplifier API",
    description="An API that takes a medical report (image or text) and returns a patient-friendly summary.",
    version="1.0.0"
)

# --- Define the request model for the text endpoint ---
class ReportText(BaseModel):
    text: str


# --- 3. Define the API Endpoints ---

@app.post("/process-report/image/")
async def process_image_report(file: UploadFile = File(...)):
    """
    Handles image uploads by saving the file and passing its path to the main processing pipeline.
    """
    temp_file_path = f"temp_{uuid.uuid4().hex}_{file.filename}"

    try:
        # Save the uploaded file to a temporary path
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call the single pipeline function, providing the image_path and ocr_engine
        final_report = process_medical_report(image_path=temp_file_path, ocr_engine=ocr_engine)
        
        # Check if the pipeline returned an error and raise a proper HTTP Exception
        if final_report.get("status") in ["error", "unprocessed"]:
            status_code = 400 if final_report.get("status") == "unprocessed" else 500
            raise HTTPException(status_code=status_code, detail=final_report.get("reason", "Processing failed"))

        
        return final_report

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/process-report/text/")
async def process_text_report(report: ReportText):
    """
    Handles raw text submissions by passing the text to the main processing pipeline.
    """
    # Call the single pipeline function, providing the raw_text
    final_report = process_medical_report(raw_text=report.text)
    
    # Check if the pipeline returned an error
    if final_report.get("status") in ["error", "unprocessed"]:
        status_code = 400 if final_report.get("status") == "unprocessed" else 500
        raise HTTPException(status_code=status_code, detail=final_report.get("reason"))
    
    return final_report


@app.get("/")
def read_root():
    return {"message": "Welcome! See API docs at /docs"}


# --- Run the server ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
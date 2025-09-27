-----

````markdown
# AI-Powered Medical Report Simplifier

![Status](https://img.shields.io/badge/status-complete-success)

A robust backend service built with FastAPI that takes scanned or typed medical reports and transforms them into structured, patient-friendly JSON summaries. This project uses a sophisticated OCR pipeline to handle real-world images, including handwritten and angled documents, and employs a rule-based system to ensure the final output is accurate and trustworthy.

---

## 🎥 Demo Video

A short screen recording demonstrating the API handling both typed and handwritten reports via image and text endpoints.

**[Watch the Demo Video](https://drive.google.com/drive/folders/1GIS4x2-1XhdndGpleBycNVuGihPluJDh?usp=drive_link)**

---

## ✨ Key Features

* **Dual API Endpoints**: Separate, dedicated endpoints for handling both **image uploads** (`/process-report/image/`) and **raw text** submissions (`/process-report/text/`).
* **Advanced OCR Pipeline**: Utilizes an adaptive two-pass system with **PaddleOCR** and **OpenCV** to achieve high accuracy on challenging inputs, including:
    * Handwritten notes.
    * Images taken at an angle or in poor lighting.
    * Documents with complex layouts.
* **Intelligent Text Normalization**: A powerful parsing engine built with **Regex** and **Fuzzy String Matching** (`thefuzz`) that cleans and structures messy OCR output. It automatically corrects common typos in test names and handles various data formats.
* **Data-Driven Status Inference**: If a written status like `(High)` or `(Low)` is missing, the service intelligently derives the status by comparing the numerical value to the reference ranges stored in its internal knowledge base.
* **Safety-First Guardrails**: The system is built with critical guardrails to ensure reliability. It safely rejects tests with unrecognizable units or ambiguous data, prioritizing trustworthy output over completeness.
* **Patient-Friendly Summaries**: Generates a simple, natural language summary of abnormal results and provides clear explanations for each test, making complex medical data easy to understand.

---

## 🏗️ Architecture and Design Choices

The service is built as a multi-stage pipeline designed for robustness and accuracy.

1.  **Input Layer (FastAPI)**: The API, built with FastAPI, provides two distinct endpoints for image and text input, ensuring clear and validated entry points.
2.  **OCR & Preprocessing Layer**:
    * An important decision in this project was the choice of OCR engine. The initial prototype was developed using the **Tesseract OCR engine**. However, during testing against challenging real-world inputs, its limitations in accuracy became apparent.
    * To meet the project's requirements, the OCR module was re-engineered using **PaddleOCR**. Its modern models, combined with a custom **OpenCV** preprocessing pipeline (for binarization and perspective correction), delivered significantly higher accuracy on both printed and handwritten text.
3.  **Normalization Layer**: This stage takes the raw text from the OCR. A robust `re.finditer` pattern extracts all potential test strings, handling single-line, multi-line, and comma-separated formats.
4.  **Enrichment & Validation Layer**: Each extracted line is validated against the internal **Knowledge Base**. Test names are corrected using fuzzy matching, units are sanitized and validated, and the status is determined (either from the text or derived from the value). This rule-based approach was chosen to guarantee safety and adhere to the project's **"no hallucination"** requirement.
5.  **Summarization Layer**: The final, validated list of tests is passed to a summarizer that generates a patient-friendly summary and explanations based on the pre-defined templates in the knowledge base.

---

## 🛠️ Technology Stack

* **Backend Framework**: FastAPI
* **OCR Engine**: PaddleOCR
* **Computer Vision**: OpenCV
* **Text Processing**: TheFuzz (Fuzzy String Matching), Regex
* **Server**: Uvicorn
* **Language**: Python 3.11

---

## 🚀 Setup and Installation

To run this project locally, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/vishwa573/medical-report-simplifier.git](https://github.com/vishwa573/medical-report-simplifier.git)
    cd medical-report-simplifier
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the API server:**
    ```bash
    python main.py
    ```
    The server will start on `http://127.0.0.1:8000`.

---

## ⚙️ API Usage Examples

The API provides two main endpoints for processing medical reports.

### 1. Process a Report from an Image

* **Endpoint:** `POST /process-report/image/`
* **Description:** Upload an image file (`.png`, `.jpg`, etc.) of a medical report.
* **`curl` Example:**

    ```bash
    curl -X POST "[http://127.0.0.1:8000/process-report/image/](http://127.0.0.1:8000/process-report/image/)" ^
    -H "accept: application/json" ^
    -F "file=@/path/to/your/sample_image.png" | python -m json.tool
    ```

### 2. Process a Report from Raw Text

* **Endpoint:** `POST /process-report/text/`
* **Description:** Send a raw text string inside a JSON object.
* **`curl` Example:**

    ```bash
    curl -X POST "[http://127.0.0.1:8000/process-report/text/](http://127.0.0.1:8000/process-report/text/)" ^
    -H "Content-Type: application/json" ^
    -d "{\"text\": \"Hemoglobin: 10.2 g/dL (Low), WBC: 11,200 /uL (High)\"}" | python -m json.tool
    ```
````

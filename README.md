# 🩺 AI-Powered Medical Report Simplifier

![Status](https://img.shields.io/badge/status-complete-success)

A robust backend service built with **FastAPI** that extracts medical test results from scanned or typed reports and transforms them into structured, **patient-friendly JSON summaries**.

The system is built with a **two-pass OCR pipeline (PaddleOCR + OpenCV)** to handle real-world image challenges like handwriting, angled scans, and poor lighting. It also includes a **rule-based normalization and validation layer** to ensure trustworthy, safe outputs.

---

## 🎥 Demo Video

A short screen recording demonstrating the API handling **clean typed**, **angled typed**, **handwritten**, and **direct text inputs**.

**👉 [Watch the Demo Video](https://drive.google.com/drive/folders/1GIS4x2-1XhdndGpleBycNVuGihPluJDh?usp=drive_link)**

---

## ✨ Key Features

✅ **Dual API Endpoints**: Separate endpoints for **image uploads** (`/process-report/image/`) and **raw text** (`/process-report/text/`).

✅ **Adaptive OCR Pipeline**: Uses **PaddleOCR** with a second-pass **OpenCV preprocessing** step for handwriting and low-quality scans.

✅ **Text Normalization Engine**: Regex + Fuzzy Matching (`thefuzz`) to clean noisy OCR output, correct typos, and standardize test names.

✅ **Knowledge-Driven Validation**:

* Corrects units and validates ranges.
* Derives `(High)` or `(Low)` status automatically if missing.
* Rejects untrustworthy/ambiguous results (safety-first).
  ✅ **Patient-Friendly Summaries**: Generates plain-language explanations for abnormal results.
  ✅ **Guardrails**: Ensures correctness and avoids hallucination by relying on strict validation and medical knowledge base.

---

## 🏗️ Architecture
An important decision in this project was the choice of OCR engine. The initial prototype was developed using the Tesseract engine. While powerful for clean text, it became clear during testing that achieving high accuracy on varied handwriting and angled photos would require an extensive and complex preprocessing pipeline.

To create a more robust service, the OCR module was re-engineered using PaddleOCR. Its modern architecture, combined with a targeted OpenCV preprocessing pipeline, delivered significantly higher out-of-the-box accuracy on these challenging real-world documents. 

The system is designed as a **multi-stage pipeline**:

1. **Input Layer (FastAPI)**

   * Handles two clear entry points: text and image.

2. **OCR & Preprocessing Layer**

   * Primary OCR with **PaddleOCR**.
   * If confidence < threshold → second-pass OCR with **OpenCV preprocessing** (grayscale, adaptive thresholding).

3. **Normalization Layer**

   * Regex extracts structured test lines.
   * Fuzzy matching corrects test names (e.g., `hemglobin → hemoglobin`).
   * Handles variations like commas, line breaks, and inconsistent units.

4. **Enrichment & Validation Layer**

   * Maps results against a medical knowledge base.
   * Infers status (high/low/normal) if missing.
   * Applies **guardrails**: rejects invalid results (e.g., missing units, nonsense values).

5. **Summarization Layer**

   * Generates a **natural language summary** and explanations.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI
* **OCR Engine**: PaddleOCR
* **CV Preprocessing**: OpenCV
* **Text Processing**: Regex, TheFuzz (fuzzy matching)
* **Server**: Uvicorn
* **Language**: Python 3.11

---

## 🚀 Setup & Installation

1. **Clone the repo**

```bash
git clone https://github.com/vishwa573/medical-report-simplifier.git
cd medical-report-simplifier
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate   # macOS/Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the server**

```bash
python main.py
```

Server will start at: `http://127.0.0.1:8000`

---

## ⚙️ API Endpoints

### 1. Process Report from Image

* **Endpoint**: `POST /process-report/image/`
* **Description**: Upload an image (`.png`, `.jpg`) of a report.
* **Curl Example**:

```bash
curl -X POST "http://127.0.0.1:8000/process-report/image/" 
-F "file=@{FILE_PATH_TO_YOUR_IMAGE}" | python -m json.tool
```

```bash
curl -X POST "http://127.0.0.1:8000/process-report/image/" 
-F "file=@{FILE_PATH_TO_YOUR_IMAGE}" | python -m json.tool
```
```bash
curl -X POST "http://127.0.0.1:8000/process-report/image/" 
-F "file=@{FILE_PATH_TO_YOUR_IMAGE}" | python -m json.tool
```

---

### 2. Process Report from Raw Text

* **Endpoint**: `POST /process-report/text/`
* **Description**: Send raw report text in JSON.
* **Curl Example**:

```bash
curl -X POST "http://127.0.0.1:8000/process-report/text/" 
-H "Content-Type: application/json" 
-d "{\"text\": \"Hemoglobin 10.2 g/dL (Low), WBC 11,200 /uL (High)\"}" | python -m json.tool
```
---

### 📦 **Optional: Run with Docker**

You can run the project inside a Docker container for a consistent environment. Make sure you have Docker Desktop installed on your machine before proceeding.

1.Clone the GitHub repository
```bash
git clone https://github.com/vishwa573/medical-report-simplifier.git
cd medical-report-simplifier
```

2.Build the Docker image
This command reads the Dockerfile in the current directory and builds the image.

```bash
docker build -t medical-report-simplifier .
```

3.Run the container
This launches the FastAPI server inside Docker and maps it to port 8000 on your machine.
```bash
docker run -p 8000:8000 medical-report-simplifier
```

4.Access the API
Open your browser and visit the FastAPI docs or or make API calls to the endpoints:
http://127.0.0.1:8000/docs

Note: Docker Desktop must be installed and running for the above commands to work.

---

## 🧪 Test Cases Covered

The project has been tested against the following input types:

1. **Clean typed report (PNG)** ✅
2. **Typed but angled/scanned report** ✅
3. **Handwritten report** ✅ (via OpenCV preprocessing + PaddleOCR)
4. **Direct text input (JSON)** ✅

Each case produces structured JSON and patient-friendly summaries.
Sample test cases are available in the images directory.

---

## 🔒 Guardrails & Error Handling

* Rejects empty or unprocessable input.
* Returns clear error messages (e.g., *"OCR failed: No text extracted"*).
* Ignores unrecognized or malformed test lines.
* Falls back to preprocessing for low OCR confidence.

---

## 📌 Submission Checklist

* [x] Working FastAPI backend with `/process-report/text/` and `/process-report/image/`.
* [x] Handles **typed, angled, handwritten, and raw text** inputs.
* [x] OCR confidence handling with preprocessing fallback.
* [x] Guardrails against invalid/untrustworthy data.
* [x] Patient-friendly summarization.
* [x] Demo video + curl examples included.

---

## 👤 Author

**Vishwa Sundar S**
📌 Smart Manufacturing @ IIITDM Kancheepuram
📧 [svishwasundar6@gmail.com](mailto:svishwasundar6@gmail.com)
🔗 [GitHub](https://github.com/vishwa573)



---

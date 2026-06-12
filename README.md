# AI Receipt Bill Splitter

An AI-powered web application that automatically extracts receipt information and calculates bill splitting among participants.

Built with **Python**, **Streamlit**, and **Google Gemini 2.5 Flash**.

---

# Project Overview

AI Receipt Bill Splitter is a web-based application designed to simplify the process of splitting bills among multiple people.

The system uses Artificial Intelligence to automatically extract receipt information from uploaded receipt images and calculate how much each participant should pay based on item ownership.

The project was developed as part of an AI Prototype Assignment covering:

1. Receipt Extraction Model Research
2. Prototype Development
3. Evaluation and Analysis

---

# Features

## Receipt Extraction

The application automatically extracts:

* Store name
* Item name
* Quantity
* Unit price
* Total item price
* Subtotal
* Tax
* Service charge
* Total bill

---

## Participant Management

Users can:

* Add participants directly from the UI
* Manage multiple participants
* Assign purchased items to specific participants

---

## Bill Splitting

The system automatically:

* Calculates each participant's subtotal
* Distributes tax and additional charges proportionally
* Calculates the final payment amount per participant

---

## Validation

The application validates:

```text
Total Split Amount = Total Receipt Amount
```

to ensure accurate bill calculations.

---

## Download Results

Users can export:

* CSV Report
* JSON Report

---

## History Management

Users can:

* View bill split history
* Clear history
* Reset application state

---

# Pre-Prototype Research

Before developing the final prototype, several OCR-free document understanding models were evaluated using two receipt images:

### Dataset

* Retail Receipt (Pradana Swalayan)
* Restaurant Receipt (Mie Gacoan)

The objective was to compare:

* Extraction accuracy
* Inference speed
* Output quality
* Suitability for receipt understanding

---

## Model 1 — Donut

Model:

```text
naver-clova-ix/donut-base-finetuned-cord-v2
```

### Results

Advantages:

* Fully local model
* OCR-free architecture
* Able to extract most receipt items

Limitations:

* Incorrect extraction of subtotal and total bill
* Multiple parsing errors on restaurant receipts
* Slower inference

Average Inference Time:

```text
20 – 22 seconds
```

---

## Model 2 — Florence-2

Model:

```text
microsoft/Florence-2-base
```

### Results

Advantages:

* Powerful multimodal architecture

Limitations:

* Failed to generate usable receipt information
* Output was not structured
* Unsuitable without additional fine-tuning

Average Inference Time:

```text
25 – 38 seconds
```

---

## Model 3 — Pix2Struct

Model:

```text
google/pix2struct-base
```

### Results

Advantages:

* OCR-free architecture

Limitations:

* Failed to extract meaningful receipt information
* Extremely slow on CPU

Average Inference Time:

```text
Approximately 16 minutes per image
```

---

## Model 4 — Gemini 2.5 Flash

Model:

```text
gemini-2.5-flash
```

### Results

Advantages:

* Highest extraction accuracy
* Structured JSON output
* Fast inference
* Accurate subtotal, tax, and total bill extraction

Average Inference Time:

```text
6 – 8 seconds
```

---

## Model Comparison

| Model            | Accuracy | Speed     | Decision |
| ---------------- | -------- | --------- | -------- |
| Donut            | Medium   | Medium    | Baseline |
| Florence-2       | Low      | Medium    | Rejected |
| Pix2Struct       | Low      | Very Slow | Rejected |
| Gemini 2.5 Flash | High     | Fast      | Selected |

---

# Final Model Selection

Based on qualitative evaluation and inference speed testing, **Gemini 2.5 Flash** was selected as the primary receipt extraction model.

Reasons:

* Highest extraction accuracy
* Fastest response time
* Structured JSON output
* Better understanding of receipt layouts
* More reliable across different receipt types

Donut is retained as an experimental fallback model.

---

# System Architecture

```text
User
 │
 ▼
Upload Receipt
 │
 ▼
Gemini Receipt Extraction
 │
 ▼
Structured JSON Receipt
 │
 ▼
Participant Assignment
 │
 ▼
Bill Split Calculation
 │
 ▼
Validation
 │
 ▼
Download Result
```

---

# Project Structure

```text
Assignment_Day_51/
│
├── app.py
│
├── models/
│   ├── gemini_model.py
│   └── donut_model.py
│
├── services/
│   └── bill_splitter.py
│
├── pre_prototype/
│   ├── donut_pre.py
│   ├── florence_pre.py
│   └── pix2struct_pre.py
│
├── receipts/
│   ├── nota_minimarket.jpg
│   └── nota_restoran.jpg
│
├── results/
│   ├── donut/
│   ├── florence/
│   ├── gemini/
│   └── pix2struct/
│
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd Assignment_Day_51
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Get your API key from:

https://aistudio.google.com/

---

# Running the Application

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# Testing Results

The application was tested using:

* Retail receipts
* Restaurant receipts

Evaluation criteria:

* Item extraction accuracy
* Total bill accuracy
* Inference speed
* Split bill correctness

---

# Product Evaluation

## Strengths

* Accurate receipt extraction
* Automatic bill splitting
* Clean and user-friendly interface
* Downloadable reports
* Validation mechanism
* History tracking

---

## Limitations

### AI Model

* Gemini requires internet access
* API rate limits may occur
* Low-quality receipt images may reduce accuracy

### Web Application

* Shared-item splitting is not supported
* No user authentication
* History is session-based

---

# Future Improvements

Potential future enhancements:

* Shared item splitting
* Database integration (SQLite/PostgreSQL)
* User authentication
* Receipt preprocessing
* Fine-tuned receipt extraction model
* Cloud deployment
* Multi-language receipt support

---

# Technologies Used

* Python
* Streamlit
* Google Gemini 2.5 Flash
* Donut
* PyTorch
* Transformers
* Pandas
* Pillow
* dotenv

---

# Author

**Hilmi Aji**
AI Receipt Bill Splitter Project

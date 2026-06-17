# AI Receipt Bill Splitter

An AI-powered receipt processing and bill splitting application built with Streamlit, Gemini AI, and Donut OCR.

The application automatically extracts receipt information from images, supports multiple receipt uploads, and provides advanced bill splitting features including single payer, equal split, and custom percentage allocation.

---

# Project Overview

Managing shared expenses from receipts can be time-consuming, especially when multiple people order different items and additional charges such as tax and service fees must be distributed fairly.

AI Receipt Bill Splitter solves this problem by combining Artificial Intelligence, OCR, and automated bill splitting logic into a single application.

Users can upload one or multiple receipts, automatically extract transaction details using Gemini AI, assign items to participants, and calculate each participant's payment responsibility accurately.

---

## Application Screenshots

### Upload Receipt
![Upload Receipt](results_figure/Upload%20Receipt.jpeg)

### Multi Receipt
![Multi Receipt](results_figure/Multi%20Receipt.jpeg)

### Assign Items
![Assign Items](results_figure/Equal,%20Custom,%20Single%20Items.jpeg)

### Bill Split Result
![Bill Split Result](results_figure/Bill%20Split%20Result.jpeg)

# Features

## AI Receipt Extraction

* Extract receipt information from images
* Store name detection
* Itemized product extraction
* Quantity detection
* Unit price extraction
* Total price extraction
* Tax extraction
* Service charge extraction
* Total bill calculation

## OCR Models

### Gemini 2.5 Flash (Primary Model)

* Fast extraction
* Structured JSON output
* High accuracy receipt understanding
* Intelligent receipt parsing

### Donut OCR (Fallback Model)

* Local OCR processing
* Automatic fallback when Gemini API is unavailable
* Improved application reliability

---

# System Architecture

```text
┌─────────────────────────────┐
│         Streamlit UI        │
│   Upload & User Interface   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   Receipt Extraction Layer  │
│     Gemini 2.5 Flash AI     │
└──────────────┬──────────────┘
               │
               │ Fallback
               ▼
┌─────────────────────────────┐
│         Donut OCR           │
│ Local Vision OCR Processing │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Receipt Processing      │
│       Receipt Merger        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Bill Split Engine      │
│                             │
│  • Single Split             │
│  • Equal Split              │
│  • Custom Percentage Split  │
│  • Tax Distribution         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Result Generation      │
│ Reports, Charts & Exports   │
└─────────────────────────────┘
```

---

# Core Components

## Streamlit Frontend

Responsible for:

* Receipt upload
* Multiple receipt management
* Participant management
* Item assignment
* Result visualization
* Report download

---

## Gemini Receipt Extractor

Primary AI model used for receipt understanding.

Responsibilities:

* Receipt understanding
* Product extraction
* Quantity extraction
* Price extraction
* Structured JSON generation

Model:

```text
Gemini 2.5 Flash
```

---

## Donut OCR Fallback

Fallback OCR engine when Gemini API is unavailable.

Responsibilities:

* Local receipt OCR
* Backup extraction pipeline
* Reliability enhancement

Model:

```text
naver-clova-ix/donut-base-finetuned-cord-v2
```

---

## Receipt Merger Service

Responsible for:

* Combining multiple receipts
* Aggregating totals
* Preserving receipt information
* Creating unified transactions

File:

```text
services/receipt_merger.py
```

---

## Bill Splitter Service

Responsible for:

### Single Split

Assign item cost to a single participant.

### Equal Split

Divide item cost equally among selected participants.

### Custom Percentage Split

Allocate item cost using user-defined percentages.

### Tax & Service Distribution

Automatically distribute additional charges proportionally based on participant contribution.

File:

```text
services/bill_splitter.py
```

---

# Multi Receipt Support

Users can upload and merge multiple receipts into a single transaction.

Supported formats:

* JPG
* JPEG
* PNG

Example:

```text
Receipt A
+
Receipt B
+
Receipt C

↓

Combined Receipt
```

---

# Advanced Bill Splitting

## Single Payer

Assign an item to a single participant.

Example:

```text
Burger → Hilmi
```

---

## Equal Split

Split an item equally among selected participants.

Example:

```text
Pizza (Rp 90,000)

Hilmi
Keni
Rina

↓

Rp 30,000 each
```

---

## Custom Percentage Split

Split an item using custom percentages.

Example:

```text
Pizza (Rp 90,000)

Hilmi → 50%
Keni → 30%
Rina → 20%

↓

Hilmi → Rp 45,000
Keni → Rp 27,000
Rina → Rp 18,000
```

---

# Automatic Tax and Service Distribution

Tax and service charges are automatically distributed proportionally based on each participant's subtotal contribution.

This ensures fair allocation of additional costs and prevents manual calculation errors.

---

# Validation System

The application validates:

* Custom percentage totals equal 100%
* Equal split contains at least one participant
* Split total matches receipt total
* Rounding differences are automatically corrected

---

# Application Workflow

```text
User Upload Receipt(s)
          │
          ▼
 Gemini Receipt Extraction
          │
          ▼
 Gemini Available?
      ┌───┴───┐
      │       │
     Yes      No
      │       │
      ▼       ▼
 Gemini     Donut OCR
 Result     Fallback
      │       │
      └───┬───┘
          ▼
 Receipt Processing
          │
          ▼
 Multiple Receipts?
      ┌───┴───┐
      │       │
     Yes      No
      │       │
      ▼       ▼
 Receipt    Continue
 Merger
      │
      ▼
 Add Participants
      │
      ▼
 Assign Items
      │
      ▼
 Choose Split Mode
      │
      ├─ Single Split
      ├─ Equal Split
      └─ Custom Percentage
      │
      ▼
 Calculate Bill Split
      │
      ▼
 Generate Reports
      │
      ▼
 Download Results
```

---

# Project Structure

```text
AI-Receipt-Bill-Splitter
│
├── app.py
│
├── models
│   ├── gemini_model.py
│   └── donut_model.py
│
├── services
│   ├── bill_splitter.py
│   └── receipt_merger.py
│
├── pre_prototype
│   ├── donut_pre.py
│   ├── florence_pre.py
│   └── pix2struct_pre.py
│
├── receipts
├── results
├── results_figure
│
├── test_gemini.py
├── test_split.py
├── requirements.txt
└── README.md
```

---

# Pre-Prototype Experiments

Before building the final application, multiple OCR and vision-language models were evaluated.

## Pix2Struct

* Tested receipt understanding capability
* Slow inference on CPU
* Poor structured extraction performance

## Florence

* Tested as an alternative vision-language model
* Experimental stage
* Less reliable for receipt extraction

## Donut

* Strong OCR performance
* Better structured extraction
* Selected as fallback OCR model

## Gemini 2.5 Flash

* Best extraction quality
* Fast inference
* Selected as primary extraction model

---

# Installation

## Clone Repository

```bash
git clone https://github.com/hilmiaji28/AI-Receipt-Bill-Splitter.git

cd AI-Receipt-Bill-Splitter
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Run Application

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# Technology Stack

| Category             | Technology                |
| -------------------- | ------------------------- |
| Frontend             | Streamlit                 |
| AI Model             | Gemini 2.5 Flash          |
| OCR Fallback         | Donut OCR                 |
| Deep Learning        | PyTorch                   |
| Transformers         | Hugging Face Transformers |
| Data Processing      | Pandas                    |
| Visualization        | Plotly                    |
| Image Processing     | Pillow                    |
| Programming Language | Python                    |

---

# Future Improvements

* Multi-user collaboration
* Shared payment links
* QRIS integration
* WhatsApp export
* Expense analytics dashboard
* Cloud deployment

---

# Author

**Hilmi Aji**
Sales & Distribution Professional | AI & Machine Learning Engineer

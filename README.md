# AI Receipt Bill Splitter

An AI-powered receipt processing and bill splitting application built with Streamlit, Gemini AI, and Donut OCR.

The application automatically extracts receipt information, supports multiple receipt uploads, and provides advanced bill splitting features including single payer, equal split, and custom percentage allocation.

---

## Features

### AI Receipt Extraction

* Extract receipt information from images
* Store name detection
* Itemized product extraction
* Quantity detection
* Unit price extraction
* Total price extraction
* Tax and service charge extraction
* Total bill calculation

### OCR Models

#### Gemini 2.5 Flash (Primary Model)

* Fast extraction
* Structured JSON output
* High accuracy receipt understanding

#### Donut OCR (Fallback Model)

* Local OCR processing
* Automatic fallback when Gemini API is unavailable
* Ensures application reliability

---

## Multi Receipt Support

Users can upload and merge multiple receipts into a single transaction.

Supported formats:

* JPG
* JPEG
* PNG

Example:

Receipt A + Receipt B + Receipt C

↓

Combined Receipt

---

## Advanced Bill Splitting

### Single Payer

Assign an item to a single participant.

Example:

Burger → Hilmi

### Equal Split

Split an item equally among selected participants.

Example:

Pizza (Rp 90,000)

Hilmi
Keni
Rina

↓

Rp 30,000 each

### Custom Percentage Split

Split an item using custom percentages.

Example:

Pizza (Rp 90,000)

Hilmi → 50%
Keni → 30%
Rina → 20%

↓

Hilmi → Rp 45,000
Keni → Rp 27,000
Rina → Rp 18,000

---

## Automatic Tax and Service Distribution

Tax and service charges are automatically distributed proportionally based on each participant's subtotal contribution.

This ensures fair allocation of additional costs.

---

## Validation System

The application validates:

* Custom percentage totals equal 100%
* Equal split contains at least one participant
* Split total matches receipt total
* Rounding differences are automatically corrected

---

## Application Workflow

1. Upload receipt image(s)
2. Extract receipt information using Gemini AI
3. Fallback to Donut OCR if Gemini is unavailable
4. Merge multiple receipts (optional)
5. Add participants
6. Assign items to participants
7. Choose split mode:

   * Single
   * Equal
   * Custom Percentage
8. Calculate bill split
9. Review results
10. Download reports

---

## Project Structure

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
│
├── results
│   ├── donut
│   ├── florence
│   ├── gemini
│   └── pix2struct
│
├── results_figure
│
├── test_gemini.py
├── test_split.py
├── requirements.txt
└── README.md
```

---

## Pre-Prototype Experiments

Before building the final application, multiple OCR and vision-language models were evaluated.

### Pix2Struct

* Tested receipt understanding capability
* Slow inference on CPU
* Poor structured extraction performance

### Florence

* Tested as an alternative vision-language model
* Experimental stage
* Less reliable for receipt extraction

### Donut

* Strong OCR performance
* Better structured extraction
* Selected as fallback OCR model

### Gemini 2.5 Flash

* Best extraction quality
* Fast inference
* Selected as primary extraction model

---

## Installation

### Clone Repository

```bash
git clone https://github.com/hilmiaji28/AI-Receipt-Bill-Splitter.git

cd AI-Receipt-Bill-Splitter
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

## Technologies Used

* Python
* Streamlit
* Google Gemini API
* Donut OCR
* Transformers
* PyTorch
* Pandas
* Pillow

---

## Future Improvements

* Multi-user collaboration
* Shared payment links
* QRIS integration
* WhatsApp export
* Expense analytics dashboard
* Cloud deployment

---

## Author

Hilmi Aji

Agricultural Engineering – Bandung Institute of Technology (ITB)

Sales & Distribution Professional | Data Science & Machine Learning Enthusiast

from pprint import pprint

from models.gemini_model import (
    GeminiReceiptExtractor
)

from services.bill_splitter import (
    BillSplitter
)

extractor = (
    GeminiReceiptExtractor()
)

receipt = (
    extractor.extract_receipt(
        "receipts/nota_restoran.jpg"
    )
)

assignments = {
    "MIE GACOAN LV 1": "Hilmi",
    "MIE GACOAN LV 2": "Rina",
    "MIE GACOAN LV 3": "Keni",
    "UDANG KEJU": "Hilmi",
    "UDANG RAMBUTAN": "Rina",
    "ES GOBAK SODOR": "Keni",
    "TEA": "Hilmi"
}

splitter = BillSplitter()

result = splitter.calculate(
    receipt,
    assignments
)

print("\nRESULT")
print("=" * 50)

pprint(result)

print("\nTOTAL")
print("=" * 50)

print(
    sum(result.values())
)

print(
    receipt["total_bill"]
)
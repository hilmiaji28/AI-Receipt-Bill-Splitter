from pprint import pprint

from models.gemini_model import (
    GeminiReceiptExtractor
)

extractor = GeminiReceiptExtractor()

receipt = extractor.extract_receipt(
    "receipts/nota_restoran.jpg"
)

print("\nSTORE")
print("=" * 50)

print(
    receipt["store_name"]
)

print("\nITEMS")
print("=" * 50)

for item in receipt["items"]:

    print(
        item["name"],
        item["quantity"],
        item["total_price"]
    )

print("\nSUMMARY")
print("=" * 50)

print(
    "Subtotal:",
    receipt["subtotal"]
)

print(
    "Tax:",
    receipt["tax"]
)

print(
    "Service:",
    receipt["service_charge"]
)

print(
    "Total:",
    receipt["total_bill"]
)

print("\nFULL JSON")
print("=" * 50)

pprint(receipt)
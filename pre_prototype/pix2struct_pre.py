import os
import time
from pathlib import Path

import torch
from PIL import Image

from transformers import (
    Pix2StructProcessor,
    Pix2StructForConditionalGeneration
)

MODEL_ID = "google/pix2struct-base"

print("Loading Pix2Struct model...")

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = Pix2StructProcessor.from_pretrained(
    MODEL_ID
)

model = Pix2StructForConditionalGeneration.from_pretrained(
    MODEL_ID
).to(device)

print(f"Using device: {device}")

receipt_folder = "receipts"
output_folder = "results/pix2struct"

os.makedirs(output_folder, exist_ok=True)

PROMPT = """
Extract receipt information.

Return:
- store name
- item name
- quantity
- unit price
- total item price
- subtotal
- tax
- service charge
- total bill

Output structured text.
"""

for file_name in os.listdir(receipt_folder):

    if not file_name.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):
        continue

    image_path = os.path.join(
        receipt_folder,
        file_name
    )

    print(f"\nProcessing: {file_name}")

    image = Image.open(
        image_path
    ).convert("RGB")

    inputs = processor(
        images=image,
        text=PROMPT,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    start_time = time.time()

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=512
    )

    inference_time = time.time() - start_time

    result = processor.decode(
        generated_ids[0],
        skip_special_tokens=True
    )

    print("=" * 70)
    print(result)
    print("=" * 70)
    print(f"Inference Time: {inference_time:.2f} sec")

    txt_file = Path(file_name).stem + ".txt"

    with open(
        os.path.join(output_folder, txt_file),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(f"FILE: {file_name}\n")
        f.write(f"TIME: {inference_time:.2f}\n\n")
        f.write(result)

print("\nDone.")
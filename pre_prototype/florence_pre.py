import os
import time
from pathlib import Path

import torch
from PIL import Image

from transformers import (
    AutoProcessor,
    AutoModelForCausalLM
) 

MODEL_ID = "microsoft/Florence-2-base"

print("Loading Florence-2 model...")

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
).to(device)

print(f"Using device: {device}")

receipt_folder = "receipts"
output_folder = "results/florence"

os.makedirs(output_folder, exist_ok=True)

PROMPT = """
Extract all receipt information.

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
        text=PROMPT,
        images=image,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
    }

    start_time = time.time()

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=512,
        do_sample=False
    )

    inference_time = time.time() - start_time

    result = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

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
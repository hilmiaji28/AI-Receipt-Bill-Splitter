import os
import time
from pathlib import Path

import torch
from PIL import Image
from transformers import DonutProcessor
from transformers import VisionEncoderDecoderModel

MODEL_NAME = "naver-clova-ix/donut-base-finetuned-cord-v2"

print("Loading Donut model...")

processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

print(f"Using device: {device}")

receipt_folder = "receipts"
output_folder = "results/donut"

os.makedirs(output_folder, exist_ok=True)

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

    task_prompt = "<s_cord-v2>"

    decoder_input_ids = processor.tokenizer(
        task_prompt,
        add_special_tokens=False,
        return_tensors="pt"
    ).input_ids.to(device)

    pixel_values = processor(
        image,
        return_tensors="pt"
    ).pixel_values.to(device)

    start_time = time.time()

    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=1024,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1
    )

    inference_time = time.time() - start_time

    result = processor.batch_decode(
        outputs,
        skip_special_tokens=False
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
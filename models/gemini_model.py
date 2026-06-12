import json
import os

from dotenv import load_dotenv
from google import genai
from PIL import Image
from models.donut_model import (
    DonutReceiptExtractor
) 


class GeminiReceiptExtractor:

    def __init__(self):

        self.donut = DonutReceiptExtractor()

        load_dotenv()

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = "gemini-2.5-flash"

        self.prompt = """
You are a receipt extraction AI.

Extract all receipt information.

Return ONLY valid JSON.

Schema:

{
  "store_name": "",
  "items": [
    {
      "name": "",
      "quantity": 0,
      "unit_price": 0,
      "total_price": 0
    }
  ],
  "subtotal": 0,
  "tax": 0,
  "service_charge": 0,
  "total_bill": 0
}

Rules:
- Use numbers only.
- Do not add explanations.
- Return JSON only.
"""

    def extract_receipt(
        self,
        image_source
    ) -> dict:

        image = Image.open(
            image_source
        )

        try:

            response = (
                self.client.models.generate_content(
                    model=self.model_name,
                    contents=[
                        self.prompt,
                        image
                    ]
                )
            )

            result_text = (
                response.text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            receipt_data = json.loads(
                result_text
            )

            receipt_data[
                "model_used"
            ] = "Gemini 2.5 Flash"

            return receipt_data

        except Exception as e:

            print(
                f"Gemini failed: {e}"
            )

            print(
                "Switching to Donut..."
            )

            donut_result = (
                self.donut.extract_receipt(
                    image_source
                )
            )

            donut_result[
                "model_used"
            ] = "Donut (Fallback)"

            return donut_result
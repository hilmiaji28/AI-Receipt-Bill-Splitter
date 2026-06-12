import re
import torch

from PIL import Image
from transformers import (
    DonutProcessor,
    VisionEncoderDecoderModel
)


class DonutReceiptExtractor:

    def __init__(self):

        self.model_name = (
            "naver-clova-ix/"
            "donut-base-finetuned-cord-v2"
        )

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.processor = (
            DonutProcessor.from_pretrained(
                self.model_name
            )
        )

        self.model = (
            VisionEncoderDecoderModel
            .from_pretrained(
                self.model_name
            )
        )

        self.model.to(
            self.device
        )

    def extract_receipt(
        self,
        image_source
    ):

        image = Image.open(
            image_source
        ).convert("RGB")

        task_prompt = "<s_cord-v2>"

        decoder_input_ids = (
            self.processor.tokenizer(
                task_prompt,
                add_special_tokens=False,
                return_tensors="pt"
            )
            .input_ids
            .to(self.device)
        )

        pixel_values = (
            self.processor(
                image,
                return_tensors="pt"
            )
            .pixel_values
            .to(self.device)
        )

        outputs = self.model.generate(
            pixel_values,
            decoder_input_ids=
            decoder_input_ids,
            max_length=1024,
            pad_token_id=
            self.processor.tokenizer.pad_token_id,
            eos_token_id=
            self.processor.tokenizer.eos_token_id
        )

        result = (
            self.processor.batch_decode(
                outputs,
                skip_special_tokens=False
            )[0]
        )

        return self.parse_output(
            result
        )

    def parse_output(
        self,
        text
    ):

        store_name = "Unknown"

        match = re.search(
            r"<s_nm>(.*?)</s_nm>",
            text
        )

        if match:
            store_name = match.group(1)

        items = []

        item_matches = re.findall(
            r"<s_nm>(.*?)</s_nm>.*?"
            r"<s_unitprice>(.*?)</s_unitprice>.*?"
            r"<s_cnt>(.*?)</s_cnt>.*?"
            r"<s_price>(.*?)</s_price>",
            text,
            re.DOTALL
        )

        for item in item_matches:

            try:

                items.append(
                    {
                        "name": item[0],

                        "quantity":
                        self.safe_int(
                            item[2]
                        ),

                        "unit_price":
                        self.safe_int(
                            item[1]
                        ),

                        "total_price":
                        self.safe_int(
                            item[3]
                        )
                    }
                )

            except:
                continue

        subtotal = self.find_number(
            text,
            "subtotal_price"
        )

        tax = self.find_number(
            text,
            "tax_price"
        )

        total = self.find_number(
            text,
            "total_price"
        )

        return {

            "store_name":
            store_name,

            "items":
            items,

            "subtotal":
            subtotal,

            "tax":
            tax,

            "service_charge":
            0,

            "total_bill":
            total,

            "model_used":
            "Donut (Fallback)"
        }

    def safe_int(
        self,
        value
    ):

        try:

            return int(
                re.sub(
                    r"[^\d]",
                    "",
                    value
                )
            )

        except:

            return 0

    def find_number(
        self,
        text,
        tag
    ):

        pattern = (
            rf"<s_{tag}>"
            rf"(.*?)"
            rf"</s_{tag}>"
        )

        match = re.search(
            pattern,
            text
        )

        if match:

            return self.safe_int(
                match.group(1)
            )

        return 0
class ReceiptMerger:

    @staticmethod
    def merge(receipts):

        merged_items = []

        subtotal = 0
        tax = 0
        service_charge = 0
        total_bill = 0

        for receipt in receipts:

            store_name = receipt.get(
                "store_name",
                "Unknown Store"
            )

            for item in receipt.get(
                "items",
                []
            ):

                item_copy = item.copy()

                item_copy[
                    "store_name"
                ] = store_name

                merged_items.append(
                    item_copy
                )

            subtotal += receipt.get(
                "subtotal",
                0
            )

            tax += receipt.get(
                "tax",
                0
            )

            service_charge += receipt.get(
                "service_charge",
                0
            )

            total_bill += receipt.get(
                "total_bill",
                0
            )

        return {
            "store_name":
            "Combined Receipt",

            "items":
            merged_items,

            "subtotal":
            subtotal,

            "tax":
            tax,

            "service_charge":
            service_charge,

            "total_bill":
            total_bill
        }
class BillSplitter:

    def calculate(
        self,
        receipt: dict,
        assignments: dict
    ):

        subtotal = receipt["subtotal"]

        total_bill = receipt["total_bill"]

        extra_cost = (
            total_bill - subtotal
        )

        person_subtotal = {}

        # ==========================
        # ITEM SUBTOTAL
        # ==========================

        for idx, item in enumerate(receipt["items"]):

            assignment_key = (
                f"{item['name']}_{idx}"
            )

            payer = assignments[
                assignment_key
            ]

            item_total = item[
                "total_price"
            ]

            if payer not in person_subtotal:

                person_subtotal[payer] = 0

            person_subtotal[payer] += item_total

        # ==========================
        # DISTRIBUTE TAX/SERVICE
        # ==========================

        final_result = {}

        allocated_extra = 0

        people = list(
            person_subtotal.keys()
        )

        for i, person in enumerate(people):

            subtotal_person = (
                person_subtotal[person]
            )

            ratio = (
                subtotal_person / subtotal
            )

            extra_share = round(
                ratio * extra_cost
            )

            if i == len(people) - 1:

                extra_share = (
                    extra_cost
                    - allocated_extra
                )

            else:

                allocated_extra += (
                    extra_share
                )

            final_result[person] = (
                subtotal_person
                + extra_share
            )

        return final_result

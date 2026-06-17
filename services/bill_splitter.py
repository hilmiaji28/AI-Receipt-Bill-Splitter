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

        for idx, item in enumerate(
            receipt["items"]
        ):

            assignment_key = (
                f"{item['name']}_{idx}"
            )

            assignment = assignments[
                assignment_key
            ]

            item_total = item[
                "total_price"
            ]

            mode = assignment[
                "mode"
            ]

            # ======================
            # SINGLE
            # ======================

            if mode == "single":

                payer = assignment[
                    "payer"
                ]

                if payer not in person_subtotal:

                    person_subtotal[
                        payer
                    ] = 0

                person_subtotal[
                    payer
                ] += item_total

            # ======================
            # EQUAL SPLIT
            # ======================

            elif mode == "equal":

                participants = assignment[
                    "participants"
                ]

                if len(
                    participants
                ) == 0:

                    continue

                share = (
                    item_total
                    / len(participants)
                )

                for person in participants:

                    if person not in person_subtotal:

                        person_subtotal[
                            person
                        ] = 0

                    person_subtotal[
                        person
                    ] += share

            # ======================
            # CUSTOM %
            # ======================

            elif mode == "custom":

                percentages = assignment[
                    "participants"
                ]

                for (
                    person,
                    pct
                ) in percentages.items():

                    if person not in person_subtotal:

                        person_subtotal[
                            person
                        ] = 0

                    amount = (
                        item_total
                        * pct
                        / 100
                    )

                    person_subtotal[
                        person
                    ] += amount

        # ==========================
        # DISTRIBUTE TAX / SERVICE
        # ==========================

        final_result = {}

        allocated_extra = 0

        people = list(
            person_subtotal.keys()
        )

        for i, person in enumerate(
            people
        ):

            subtotal_person = (
                person_subtotal[
                    person
                ]
            )

            ratio = (
                subtotal_person
                / subtotal
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

            amount = round(
                subtotal_person
                + extra_share
            )

            final_result[
                person
            ] = amount

        # ==========================
        # ROUNDING CORRECTION
        # ==========================

        difference = (
            total_bill
            - sum(
                final_result.values()
            )
        )

        if difference != 0:

            last_person = list(
                final_result.keys()
            )[-1]

            final_result[
                last_person
            ] += difference

        return final_result
import pandas as pd
import plotly.express as px
import streamlit as st

from models.gemini_model import GeminiReceiptExtractor
from services.bill_splitter import BillSplitter
from datetime import datetime
from services.receipt_merger import (
    ReceiptMerger
)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Receipt Bill Splitter",
    page_icon="🧾",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.receipt-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
}

.header-box {
    padding: 20px;
    border-radius: 20px;
    background: linear-gradient(
        90deg,
        #2563eb,
        #1d4ed8
    );
    color: white;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SERVICES
# ==================================================

extractor = GeminiReceiptExtractor()
splitter = BillSplitter()

if "history" not in st.session_state:
    st.session_state["history"] = []

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🧾 AI Bill Splitter")

    st.success("Gemini 2.5 Flash")

    st.markdown("---")

    st.markdown("""
### Workflow

1️⃣ Upload Receipt

2️⃣ Extract Receipt

3️⃣ Add Participants

4️⃣ Assign Items

5️⃣ Calculate Split

6️⃣ View Result
""")

    st.markdown("---")

    if len(st.session_state["history"]) > 0:

        st.subheader("📜 History")

        history_df = pd.DataFrame(
            st.session_state["history"]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "🧹 Clear History",
            use_container_width=True
        ):
            st.session_state["history"] = []
            st.rerun()

    st.markdown("---")

    if st.button(
        "🗑️ Reset Application",
        use_container_width=True
    ):

        history = st.session_state.get(
            "history",
            []
        )

        st.session_state.clear()

        st.session_state["history"] = history

        st.rerun()

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class='header-box'>
<h1>AI Receipt Bill Splitter</h1>
<p>
Upload a receipt, automatically extract items with Gemini AI,
assign each item to participants,
and calculate the final bill split.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# UPLOAD
# ==================================================

st.subheader("📤 Upload Receipt")

uploaded_files = st.file_uploader(
    "Upload Receipt(s)",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    accept_multiple_files=True
)

if uploaded_files:

    if "merger" not in st.session_state:
        st.session_state["merger"] = ReceiptMerger()

    merger = st.session_state["merger"]

    uploaded_file = None

    # ==========================================
    # SINGLE RECEIPT
    # ==========================================

    if len(uploaded_files) == 1:

        uploaded_file = uploaded_files[0]

        st.success(
            "✅ One receipt uploaded"
        )

        col1, col2 = st.columns([1, 2])

        with col1:

            st.image(
                uploaded_file,
                caption="Receipt Preview",
                use_container_width=True
            )

        with col2:

            st.info(
                "Click Extract Receipt to analyze the uploaded receipt."
            )

            if st.button(
                "🚀 Extract Receipt",
                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing receipt..."
                ):

                    receipt = (
                        extractor.extract_receipt(
                            uploaded_file
                        )
                    )

                    st.session_state["receipt"] = receipt

                    st.session_state.pop(
                        "result",
                        None
                    )

                    st.session_state.pop(
                        "assignments",
                        None
                    )

                    st.toast(
                        "Receipt extracted successfully ✅"
                    )

                    st.rerun()

    # ==========================================
    # MULTIPLE RECEIPTS
    # ==========================================

    else:

        st.subheader(
            "🧾 Uploaded Receipts"
        )

        cols = st.columns(
            len(uploaded_files)
        )

        for idx, file in enumerate(
            uploaded_files
        ):

            with cols[idx]:

                st.image(
                    file,
                    caption=file.name,
                    use_container_width=True
                )

        if st.button(
            "🚀 Merge & Extract Receipts",
            use_container_width=True
        ):

            with st.spinner(
                "⏳ Processing receipts..."
            ):

                try:

                    all_receipts = []

                    for file in uploaded_files:

                        receipt_data = (
                            extractor.extract_receipt(
                                file
                            )
                        )

                        all_receipts.append(
                            receipt_data
                        )

                    merged_result = (
                        merger.merge(
                            all_receipts
                        )
                    )

                    st.session_state[
                        "receipt"
                    ] = merged_result

                    st.session_state.pop(
                        "result",
                        None
                    )

                    st.session_state.pop(
                        "assignments",
                        None
                    )

                    st.success(
                        f"✅ Merged {len(uploaded_files)} receipts into one!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Error merging receipts: {e}"
                    )

# ==================================================
# SHOW RECEIPT
# ==================================================

if "receipt" in st.session_state:

    receipt = st.session_state[
        "receipt"
    ]

    st.markdown("---")

    st.subheader(
        f"🏪 {receipt['store_name']}"
    )

    if receipt.get(
        "model_used"
    ):

        st.info(
            f"🤖 Model Used: "
            f"{receipt['model_used']}"
        )

    # ==============================================
    # SUMMARY METRICS
    # ==============================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Subtotal",
            f"Rp {receipt['subtotal']:,}"
        )

    with col2:

        st.metric(
            "Tax",
            f"Rp {receipt['tax']:,}"
        )

    with col3:

        st.metric(
            "Service",
            f"Rp {receipt['service_charge']:,}"
        )
    
    with col4:
        st.metric(
            "Total Bill",
            f"Rp {receipt['total_bill']:,}"
        )

    st.markdown("---")

    # ==============================================
    # ITEMS TABLE
    # ==============================================

    st.subheader(
        "🛒 Receipt Items"
    )

    df = pd.DataFrame(
        receipt["items"]
    )

    rename_map = {
        "store_name": "Store",
        "name": "Item Name",
        "quantity": "Quantity",
        "unit_price": "Unit Price",
        "total_price": "Total Price"
    }

    df = df.rename(
        columns=rename_map
    )

    display_columns = [
        col
        for col in [
            "Store",
            "Item Name",
            "Quantity",
            "Unit Price",
            "Total Price"
        ]
        if col in df.columns
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")

    # ==============================================
    # PARTICIPANTS
    # ==============================================

    st.subheader("👥 Participants")

    num_participants = st.number_input(
        "Number of Participants",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    participants = []

    cols = st.columns(2)

    for i in range(num_participants):

        with cols[i % 2]:

            name = st.text_input(
                f"Participant {i+1}",
                key=f"participant_{i}"
            )

            if name.strip():

                participants.append(
                    name.strip()
                )

    if len(participants) == num_participants:

        st.markdown("---")

        # ==========================================
        # ASSIGN ITEMS
        # ==========================================

        with st.expander(
            "📝 Assign Items to Participants",
            expanded=True
        ):

            assignments = {}

            for idx, item in enumerate(receipt["items"]):

                item_key = f"{item['name']}_{idx}"

                st.markdown(
                    f"**{item['name']}** "
                    f"(Rp {item['total_price']:,})"
                )

                mode = st.radio(
                    "Split Mode",
                    [
                        "Single",
                        "Equal",
                        "Custom"
                    ],
                    horizontal=True,
                    key=f"mode_{item_key}"
                )

                # ==========================
                # SINGLE
                # ==========================

                if mode == "Single":

                    payer = st.selectbox(
                        "Payer",
                        participants,
                        key=f"payer_{item_key}"
                    )

                    assignments[item_key] = {
                        "mode": "single",
                        "payer": payer
                    }

                # ==========================
                # EQUAL SPLIT
                # ==========================

                elif mode == "Equal":

                    selected = st.multiselect(
                        "Participants",
                        participants,
                        default=participants[:2],
                        key=f"equal_{item_key}"
                    )

                    assignments[item_key] = {
                        "mode": "equal",
                        "participants": selected
                    }

                # ==========================
                # CUSTOM %
                # ==========================

                else:

                    selected = st.multiselect(
                        "Participants",
                        participants,
                        default=participants[:1],
                        key=f"custom_{item_key}"
                    )

                    percentages = {}

                    total_pct = 0

                    for person in selected:

                        pct = st.number_input(
                            f"{person} %",
                            min_value=0,
                            max_value=100,
                            value=0,
                            step=5,
                            key=f"pct_{item_key}_{person}"
                        )

                        percentages[person] = pct

                        total_pct += pct

                    st.caption(
                        f"Total Percentage: {total_pct}%"
                    )

                    assignments[item_key] = {
                        "mode": "custom",
                        "participants": percentages
                    }

        st.markdown("---")

        # ==========================================
        # CALCULATE BUTTON
        # ==========================================

        if st.button(
            "💰 Calculate Bill Split",
            use_container_width=True
        ):
            for value in assignments.values():

                if value["mode"] == "equal":

                    if len(
                        value["participants"]
                    ) == 0:

                        st.error(
                            "Equal split requires at least one participant."
                        )

                        st.stop()

                if value["mode"] == "custom":

                    if len(
                        value["participants"]
                    ) == 0:

                        st.error(
                            "Custom split requires at least one participant."
                        )

                        st.stop()

                    total_pct = sum(
                        value["participants"].values()
                    )

                    if total_pct != 100:

                        st.error(
                            "Custom percentage must equal 100%"
                        )

                        st.stop()

            result = (
                splitter.calculate(
                    receipt,
                    assignments
                )
            )

            st.session_state["assignments"] = assignments
            st.session_state["result"] = result

            st.session_state["history"].append(
                {
                    "Date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "Store": receipt["store_name"],
                    "Total": f"Rp {receipt['total_bill']:,}",
                    "Participants": len(result)
                }
            )

            st.rerun()

# ==================================================
# RESULT
# ==================================================

if "result" in st.session_state:

    st.markdown("---")

    st.subheader(
        "📊 Bill Split Result"
    )

    result = st.session_state[
        "result"
    ]

    receipt = st.session_state[
        "receipt"
    ]

    assignments = st.session_state.get(
        "assignments",
        {}
    )   

    # ==============================================
    # RESULT TABLE
    # ==============================================

    result_df = pd.DataFrame(
        {
            "Participant": result.keys(),
            "Amount": result.values()
        }
    )

    split_csv = (
        result_df.to_csv(
            index=False
        )
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Split Result",
        data=split_csv,
        file_name="bill_split_result.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # ==============================================
    # FULL TRANSACTION CSV
    # ==============================================

    detail_rows = []

    for idx, item in enumerate(
        receipt["items"]
    ):

        assignment = assignments.get(
            f"{item['name']}_{idx}",
            {}
        )

        mode = assignment.get(
            "mode",
            "-"
        )

        paid_by = "-"

        split_detail = "-"

        if mode == "single":

            paid_by = assignment.get(
                "payer",
                "-"
            )

        elif mode == "equal":

            participants = assignment.get(
                "participants",
                []
            )

            split_detail = ", ".join(
                participants
            )

        elif mode == "custom":

            percentages = assignment.get(
                "participants",
                {}
            )

            parts = []

            for person, pct in percentages.items():

                parts.append(
                    f"{person} ({pct}%)"
                )

            split_detail = ", ".join(
                parts
            )

        detail_rows.append(
            {
                "Item": item["name"],
                "Quantity": item["quantity"],
                "Unit Price": item["unit_price"],
                "Total Price": item["total_price"],
                "Split Mode": mode,
                "Paid By": paid_by,
                "Split Detail": split_detail
            }
        )
                
    detail_df = pd.DataFrame(
        detail_rows
    )

    summary_rows = []

    for person, amount in result.items():

        summary_rows.append(
            {
                "Participant": person,
                "Amount": amount
            }
        )

    summary_df = pd.DataFrame(
        summary_rows
    )

    export_file = []

    export_file.append(
        f"Store,{receipt['store_name']}"
    )

    export_file.append(
        f"Subtotal,{receipt['subtotal']}"
    )

    export_file.append(
        f"Tax,{receipt['tax']}"
    )

    export_file.append(
        f"Service,{receipt['service_charge']}"
    )

    export_file.append(
        f"Total Bill,{receipt['total_bill']}"
    )

    export_file.append("")

    export_file.append(
        "ITEM DETAILS"
    )

    export_file.append(
        detail_df.to_csv(index=False)
    )

    export_file.append("")

    export_file.append(
        "BILL SPLIT RESULT"
    )

    export_file.append(
        summary_df.to_csv(index=False)
    )

    detail_csv = "\n".join(
        export_file
    ).encode("utf-8")

    st.download_button(
        label="📄 Download Full Transaction",
        data=detail_csv,
        file_name="full_transaction_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    # ==============================================
    # CHARTS
    # ==============================================

    col1, col2 = st.columns([1, 1])

    with col1:

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        fig = px.pie(
            result_df,
            names="Participant",
            values="Amount",
            title="Bill Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    # ==============================================
    # VALIDATION
    # ==============================================

    total_split = sum(
        result.values()
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Receipt Total",
            f"Rp {receipt['total_bill']:,}"
        )

    with c2:

        st.metric(
            "Split Total",
            f"Rp {total_split:,}"
        )

    if abs(
        total_split
        -
        receipt["total_bill"]
    ) <= 1:

        st.success(
            "✅ Validation Passed: Split total matches receipt total."
        )

    else:

        st.error(
            "❌ Validation Failed."
        )

    st.markdown("---")

    # ==============================================
    # PERSON CARDS
    # ==============================================

    st.subheader(
        "💵 Amount Per Person"
    )

    cols = st.columns(
        min(len(result), 4)
    )

    for idx, (person, amount) in enumerate(
        result.items()
    ):

        with cols[idx % len(cols)]:

            st.metric(
                label=person,
                value=f"Rp {amount:,}"
            )

    st.markdown("---")
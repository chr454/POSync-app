
import streamlit as st
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Moniepoint Transactions",
    layout="wide"
)

# Load CSS if available
try:
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except FileNotFoundError:
    pass

st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("🏦 Moniepoint Transactions")
st.markdown("""
Record and manage Moniepoint withdrawals, POS transfers, and sales.

You can edit individual cells, add new rows, and delete transactions
directly from the tables.
""")

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

st.session_state.setdefault("moniepoint_withdrawals", [])
st.session_state.setdefault("moniepoint_transfers", [])
st.session_state.setdefault("moniepoint_sales", [])


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_records(records, numeric_columns, text_columns):
    """
    Normalize records after editing.

    Blank numeric cells become 0.0.
    Blank text cells become empty strings.
    Missing dates are automatically populated.
    """

    cleaned = []

    for record in records:
        row = dict(record)

        # Ensure every record has a date
        if not row.get("Date"):
            row["Date"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        # Ensure numeric values are valid numbers
        for column in numeric_columns:
            value = pd.to_numeric(
                row.get(column, 0),
                errors="coerce"
            )

            row[column] = (
                0.0 if pd.isna(value) else float(value)
            )

        # Ensure text values are strings
        for column in text_columns:
            value = row.get(column, "")
            row[column] = "" if pd.isna(value) else str(value)

        cleaned.append(row)

    return cleaned


def display_transaction_table(
    state_key,
    editor_key,
    numeric_columns,
    text_columns
):
    """
    Display an editable transaction table.

    Streamlit's data editor provides built-in row addition
    and deletion through num_rows='dynamic'.
    """

    records = st.session_state[state_key]

    if not records:
        st.info("No transactions recorded yet.")
        return

    # Clean existing records before displaying them
    records = clean_records(
        records,
        numeric_columns,
        text_columns
    )

    st.session_state[state_key] = records

    df = pd.DataFrame(records)

    # Ensure expected columns exist
    for column in numeric_columns + text_columns:
        if column not in df.columns:
            df[column] = 0.0 if column in numeric_columns else ""

    if "Date" not in df.columns:
        df["Date"] = ""

    # Keep a consistent column order
    columns = ["Date"] + text_columns + numeric_columns
    df = df[columns]

    # Configure numeric columns
    column_config = {
        "Date": st.column_config.TextColumn(
            "Date",
            disabled=True
        )
    }

    for column in numeric_columns:
        column_config[column] = st.column_config.NumberColumn(
            column,
            min_value=0.0,
            step=100.0,
            format="₦%.2f"
        )

    for column in text_columns:
        column_config[column] = st.column_config.TextColumn(
            column
        )

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        key=editor_key
    )

    # Save and normalize edited records
    updated_records = edited_df.to_dict("records")

    st.session_state[state_key] = clean_records(
        updated_records,
        numeric_columns,
        text_columns
    )


# =========================================================
# MONIEPOINT WITHDRAWAL FORM
# =========================================================

st.markdown('<div class="form-section">', unsafe_allow_html=True)

st.subheader("💸 Moniepoint Withdrawals")

with st.form("moniepoint_withdrawal_form", clear_on_submit=True):

    mw_amount_withdrawn = st.number_input(
        "Amount Withdrawn",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="mw_amount_withdrawn"
    )

    mw_amount_paid_out = st.number_input(
        "Amount Paid Out",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="mw_amount_paid_out"
    )

    mw_charge = st.number_input(
        "Charge",
        min_value=0.0,
        step=10.0,
        format="%.2f",
        key="mw_charge"
    )

    mw_submit = st.form_submit_button(
        "💾 Save Moniepoint Withdrawal"
    )

    if mw_submit:

        st.session_state.moniepoint_withdrawals.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Amount Withdrawn": mw_amount_withdrawn,
            "Amount Paid Out": mw_amount_paid_out,
            "Charge": mw_charge
        })

        st.success("Moniepoint withdrawal recorded.")

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# MONIEPOINT POS TRANSFER FORM
# =========================================================

st.markdown('<div class="form-section">', unsafe_allow_html=True)

st.subheader("🔄 Moniepoint POS Transfers")

with st.form("moniepoint_transfer_form", clear_on_submit=True):

    mt_money_received = st.number_input(
        "Money Received",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="mt_money_received"
    )

    mt_money_paid_out = st.number_input(
        "Money Paid Out",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="mt_money_paid_out"
    )

    mt_charge = st.number_input(
        "Charge",
        min_value=0.0,
        step=10.0,
        format="%.2f",
        key="mt_charge"
    )

    mt_submit = st.form_submit_button(
        "💾 Save Moniepoint Transfer"
    )

    if mt_submit:

        st.session_state.moniepoint_transfers.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Money Received": mt_money_received,
            "Money Paid Out": mt_money_paid_out,
            "Charge": mt_charge
        })

        st.success("Moniepoint transfer recorded.")

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# MONIEPOINT SALES FORM
# =========================================================

st.markdown('<div class="form-section">', unsafe_allow_html=True)

st.subheader("🛒 Moniepoint Sales")

with st.form("moniepoint_sales_form", clear_on_submit=True):

    ms_transaction_type = st.text_input(
        "Transaction Type",
        placeholder="e.g. Airtime, Data, Electricity, Cable TV",
        key="ms_transaction_type"
    )

    ms_details = st.text_input(
        "Details",
        placeholder="Enter additional details",
        key="ms_details"
    )

    ms_amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="ms_amount"
    )

    ms_charge = st.number_input(
        "Charge",
        min_value=0.0,
        step=10.0,
        format="%.2f",
        key="ms_charge"
    )

    ms_submit = st.form_submit_button(
        "💾 Save Moniepoint Sale"
    )

    if ms_submit:

        st.session_state.moniepoint_sales.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Transaction Type": ms_transaction_type,
            "Details": ms_details,
            "Amount": ms_amount,
            "Charge": ms_charge
        })

        st.success("Moniepoint sale recorded.")

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# TRANSACTION TABLES
# =========================================================

st.markdown("---")
st.subheader("📋 Moniepoint Transaction Records")


# =========================================================
# WITHDRAWALS TABLE
# =========================================================

st.markdown("#### 💸 Withdrawals")

display_transaction_table(
    state_key="moniepoint_withdrawals",
    editor_key="moniepoint_withdrawal_editor",
    numeric_columns=[
        "Amount Withdrawn",
        "Amount Paid Out",
        "Charge"
    ],
    text_columns=[]
)


# =========================================================
# POS TRANSFERS TABLE
# =========================================================

st.markdown("#### 🔄 POS Transfers")

display_transaction_table(
    state_key="moniepoint_transfers",
    editor_key="moniepoint_transfer_editor",
    numeric_columns=[
        "Money Received",
        "Money Paid Out",
        "Charge"
    ],
    text_columns=[]
)


# =========================================================
# SALES TABLE
# =========================================================

st.markdown("#### 🛒 Sales")

display_transaction_table(
    state_key="moniepoint_sales",
    editor_key="moniepoint_sales_editor",
    numeric_columns=[
        "Amount",
        "Charge"
    ],
    text_columns=[
        "Transaction Type",
        "Details"
    ]
)


st.markdown('</div>', unsafe_allow_html=True)

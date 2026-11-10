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
You can edit individual cells, add rows, and delete transactions.
""")

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

st.session_state.setdefault("moniepoint_withdrawals", [])
st.session_state.setdefault("moniepoint_transfers", [])
st.session_state.setdefault("moniepoint_sales", [])

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

if st.session_state.moniepoint_withdrawals:

    withdrawal_df = pd.DataFrame(
        st.session_state.moniepoint_withdrawals
    )

    edited_withdrawal_df = st.data_editor(
        withdrawal_df,
        num_rows="dynamic",
        use_container_width=True,
        key="moniepoint_withdrawal_editor"
    )

    st.session_state.moniepoint_withdrawals = (
        edited_withdrawal_df.to_dict("records")
    )

    for i in range(len(st.session_state.moniepoint_withdrawals)):

        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button(
                "🗑 Delete",
                key=f"delete_mw_{i}"
            ):
                st.session_state.moniepoint_withdrawals.pop(i)
                st.rerun()

        with col2:
            if st.button(
                f"➕ Add Row Below Withdrawal {i + 1}",
                key=f"add_mw_{i}"
            ):
                columns = withdrawal_df.columns.tolist()

                new_row = {
                    column: "" for column in columns
                }

                st.session_state.moniepoint_withdrawals.insert(
                    i + 1,
                    new_row
                )

                st.rerun()

else:
    st.info("No Moniepoint withdrawals recorded yet.")

# =========================================================
# POS TRANSFERS TABLE
# =========================================================

st.markdown("#### 🔄 POS Transfers")

if st.session_state.moniepoint_transfers:

    transfer_df = pd.DataFrame(
        st.session_state.moniepoint_transfers
    )

    edited_transfer_df = st.data_editor(
        transfer_df,
        num_rows="dynamic",
        use_container_width=True,
        key="moniepoint_transfer_editor"
    )

    st.session_state.moniepoint_transfers = (
        edited_transfer_df.to_dict("records")
    )

    for i in range(len(st.session_state.moniepoint_transfers)):

        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button(
                "🗑 Delete",
                key=f"delete_mt_{i}"
            ):
                st.session_state.moniepoint_transfers.pop(i)
                st.rerun()

        with col2:
            if st.button(
                f"➕ Add Row Below Transfer {i + 1}",
                key=f"add_mt_{i}"
            ):
                columns = transfer_df.columns.tolist()

                new_row = {
                    column: "" for column in columns
                }

                st.session_state.moniepoint_transfers.insert(
                    i + 1,
                    new_row
                )

                st.rerun()

else:
    st.info("No Moniepoint transfers recorded yet.")

# =========================================================
# SALES TABLE
# =========================================================

st.markdown("#### 🛒 Sales")

if st.session_state.moniepoint_sales:

    sales_df = pd.DataFrame(
        st.session_state.moniepoint_sales
    )

    edited_sales_df = st.data_editor(
        sales_df,
        num_rows="dynamic",
        use_container_width=True,
        key="moniepoint_sales_editor"
    )

    st.session_state.moniepoint_sales = (
        edited_sales_df.to_dict("records")
    )

    for i in range(len(st.session_state.moniepoint_sales)):

        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button(
                "🗑 Delete",
                key=f"delete_ms_{i}"
            ):
                st.session_state.moniepoint_sales.pop(i)
                st.rerun()

        with col2:
            if st.button(
                f"➕ Add Row Below Sale {i + 1}",
                key=f"add_ms_{i}"
            ):
                columns = sales_df.columns.tolist()

                new_row = {
                    column: "" for column in columns
                }

                st.session_state.moniepoint_sales.insert(
                    i + 1,
                    new_row
                )

                st.rerun()

else:
    st.info("No Moniepoint sales recorded yet.")

st.markdown('</div>', unsafe_allow_html=True)

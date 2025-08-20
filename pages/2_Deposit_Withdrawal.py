import streamlit as st
import pandas as pd
import os
from datetime import datetime

# === Setup ===
st.set_page_config(page_title="Deposit & Withdrawal", layout="wide")

# Load CSS if available
try:
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.markdown('<div class="page-container">', unsafe_allow_html=True)
st.title("💳 Deposit & Withdrawal Transactions")
st.markdown("""
Record deposits, withdrawals, and other POS transactions below.
Manage today's records directly from the tables at the bottom.
""")

# === Session State Initialization ===
st.session_state.setdefault("deposits", [])
st.session_state.setdefault("withdrawals", [])
st.session_state.setdefault("other_pos", {})

# === Deposit Form ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("➕ Record Deposit Transaction")

with st.form("deposit_form", clear_on_submit=True):
    acc_no = st.text_input("Account Number")
    acc_name = st.text_input("Account Name")
    dep_amount = st.number_input("Amount Deposited", min_value=0.0, step=100.0)
    dep_charge = st.number_input("Charge", min_value=0.0, step=10.0)
    dep_submit = st.form_submit_button("Save Deposit")

    if dep_submit:
        adjusted_amount = dep_amount + 50  # Add ₦50 for export
        st.session_state.deposits.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Account Number": acc_no,
            "Account Name": acc_name,
            "Amount": adjusted_amount,          # For Excel export
            "Actual Amount": dep_amount,        # For internal summaries
            "Charge": dep_charge
        })
        st.success("Deposit transaction recorded.")

st.markdown('</div>', unsafe_allow_html=True)

# === Withdrawal Form ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("➖ Record Withdrawal Transaction")

with st.form("withdrawal_form", clear_on_submit=True):
    card_digits = st.text_input("Card Last 4 Digits")
    amt_withdrawn = st.number_input("Amount Withdrawn", min_value=0.0, step=100.0)
    amt_paid_out = st.number_input("Amount Paid Out", min_value=0.0, step=100.0)
    wd_charge = st.number_input("Charge", min_value=0.0, step=10.0)
    wd_submit = st.form_submit_button("Save Withdrawal")

    if wd_submit:
        st.session_state.withdrawals.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Card Last 4 Digits": card_digits,
            "Amount Withdrawn": amt_withdrawn,
            "Amount Paid Out": amt_paid_out,
            "Charge": wd_charge
        })
        st.success("Withdrawal transaction recorded.")

st.markdown('</div>', unsafe_allow_html=True)

# === Other POS Form ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("🏧 Record Other POS Terminal Transactions")

with st.form("other_pos_form", clear_on_submit=True):
    pos_name = st.text_input("POS Name (e.g. MoniePoint, Baxi)")
    pos_withdrawal = st.number_input("Total Withdrawal Paid Out", min_value=0.0, step=100.0)
    pos_deposit = st.number_input("Total Deposit/Sales", min_value=0.0, step=100.0)
    pos_submit = st.form_submit_button("Save POS Entry")

    if pos_submit:
        st.session_state.other_pos[pos_name] = {
            "Withdrawal": pos_withdrawal,
            "Deposit": pos_deposit
        }
        st.success(f"POS transaction for {pos_name} saved.")

st.markdown('</div>', unsafe_allow_html=True)


# === Transaction Tables ===
st.markdown("---")
st.subheader("📋 Today's Recorded Transactions")

# === Deposits Table ===
st.markdown("#### Deposits")
if st.session_state.deposits:
    deposit_df = pd.DataFrame(st.session_state.deposits)

    edited_deposit_df = st.data_editor(
        deposit_df,
        num_rows="dynamic",  # allows adding rows
        use_container_width=True
    )

    # Save back edits
    st.session_state.deposits = edited_deposit_df.to_dict("records")

    # Delete buttons
    for i in range(len(st.session_state.deposits)):
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button(f"🗑", key=f"del_dep_{i}"):
                st.session_state.deposits.pop(i)
                st.rerun()
        with col2:
            if st.button(f"➕ Add Row Below Deposit {i+1}", key=f"add_dep_{i}"):
                st.session_state.deposits.insert(i+1, {col: "" for col in deposit_df.columns})
                st.rerun()

else:
    st.info("No deposit transactions recorded today.")

# === Withdrawals Table ===
st.markdown("#### Withdrawals")
if st.session_state.withdrawals:
    withdrawal_df = pd.DataFrame(st.session_state.withdrawals)

    edited_withdrawal_df = st.data_editor(
        withdrawal_df,
        num_rows="dynamic",
        use_container_width=True
    )

    st.session_state.withdrawals = edited_withdrawal_df.to_dict("records")

    for i in range(len(st.session_state.withdrawals)):
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button(f"🗑", key=f"del_wd_{i}"):
                st.session_state.withdrawals.pop(i)
                st.rerun()
        with col2:
            if st.button(f"➕ Add Row Below Withdrawal {i+1}", key=f"add_wd_{i}"):
                st.session_state.withdrawals.insert(i+1, {col: "" for col in withdrawal_df.columns})
                st.rerun()
else:
    st.info("No withdrawal transactions recorded today.")

# === Other POS Table ===
st.markdown("#### Other POS Terminals Summary")
if st.session_state.other_pos:
    pos_df = pd.DataFrame([
        {"POS Name": k, "Withdrawal": v["Withdrawal"], "Deposit": v["Deposit"]}
        for k, v in st.session_state.other_pos.items()
    ])

    edited_pos_df = st.data_editor(
        pos_df,
        num_rows="dynamic",
        use_container_width=True
    )

    # Save edits back
    st.session_state.other_pos = {
        row["POS Name"]: {"Withdrawal": row["Withdrawal"], "Deposit": row["Deposit"]}
        for _, row in edited_pos_df.iterrows() if row["POS Name"]
    }

    for pos_name in list(st.session_state.other_pos.keys()):
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button(f"🗑", key=f"del_pos_{pos_name}"):
                del st.session_state.other_pos[pos_name]
                st.rerun()
        with col2:
            if st.button(f"➕ Add Row Below {pos_name}", key=f"add_pos_{pos_name}"):
                st.session_state.other_pos[f"{pos_name}_new"] = {"Withdrawal": 0, "Deposit": 0}
                st.rerun()
else:
    st.info("No POS terminals recorded today.")

st.markdown('</div>', unsafe_allow_html=True)

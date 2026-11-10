import streamlit as st

st.set_page_config(page_title="Reconciliation", layout="wide")

# Load CSS
try:
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Style file not found.")

st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("🔄 Reconciliation Summary")
st.markdown(
    "This page summarizes **Cash** and **Capital (System)** reconciliation for the day."
)


# ============================================================
# Utility Function
# ============================================================

def get_total(state_key):
    """
    Calculates the total amount from a session-state list.

    Expected format:
    [
        {"amount": 1000},
        {"amount": 2000}
    ]
    """
    items = st.session_state.get(state_key, [])

    if (
        isinstance(items, list)
        and len(items) > 0
        and isinstance(items[0], dict)
    ):
        return sum(float(i.get("amount", 0.0) or 0.0) for i in items)

    return sum(float(item or 0.0) for item in items)


# ============================================================
# 💵 CASH SUMMARY RECONCILIATION
# ============================================================

st.header("💵 Cash Summary")


# ============================================================
# 📈 CASH CREDIT SIDE / INFLOWS
# ============================================================

st.subheader("📈 Cash Inflows")

opening_cash = st.session_state.get("opening_cash", 0.0)
additional_cash = get_total("additional_cash")


# ------------------------------------------------------------
# Paga Deposits
# ------------------------------------------------------------

deposits = st.session_state.get("deposits", [])

# Use Actual Amount instead of Amount because Amount may include
# the ₦50 deposit charge/export amount.
total_deposits = sum(
    float(txn.get("Actual Amount", txn.get("Amount", 0.0)) or 0.0)
    for txn in deposits
)

deposit_charges = sum(
    float(txn.get("Charge", 0.0) or 0.0)
    for txn in deposits
)


# ------------------------------------------------------------
# Other POS Deposits
# ------------------------------------------------------------

other_pos_credit = sum(
    float(pos.get("Deposit", 0.0) or 0.0)
    for pos in st.session_state.get("other_pos", {}).values()
)


# ------------------------------------------------------------
# Moniepoint Transactions - Credit Side
# ------------------------------------------------------------

# Moniepoint Withdrawals
moniepoint_withdrawals = st.session_state.get(
    "moniepoint_withdrawals",
    []
)

moniepoint_withdrawal_charges = sum(
    float(txn.get("Charge", 0.0) or 0.0)
    for txn in moniepoint_withdrawals
)


# Moniepoint POS Transfers
moniepoint_transfers = st.session_state.get(
    "moniepoint_transfers",
    []
)

moniepoint_transfer_received = sum(
    float(txn.get("Money Received", 0.0) or 0.0)
    for txn in moniepoint_transfers
)

moniepoint_transfer_charges = sum(
    float(txn.get("Charge", 0.0) or 0.0)
    for txn in moniepoint_transfers
)


# Moniepoint Sales
moniepoint_sales = st.session_state.get(
    "moniepoint_sales",
    []
)

moniepoint_sales_amount = sum(
    float(txn.get("Amount", 0.0) or 0.0)
    for txn in moniepoint_sales
)

moniepoint_sales_charges = sum(
    float(txn.get("Charge", 0.0) or 0.0)
    for txn in moniepoint_sales
)


# ------------------------------------------------------------
# Display Cash Credit Entries
# ------------------------------------------------------------

st.write(f"**Opening Cash:** ₦{opening_cash:,.2f}")

st.write(f"**Additional Cash:** ₦{additional_cash:,.2f}")
for entry in st.session_state.get("additional_cash", []):
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )

st.write(f"**Paga Deposits (Actual):** ₦{total_deposits:,.2f}")
st.write(f"**Paga Deposit Charges:** ₦{deposit_charges:,.2f}")

st.write(f"**Other POS Deposits:** ₦{other_pos_credit:,.2f}")


# ------------------------------------------------------------
# Display Moniepoint Credit Entries
# ------------------------------------------------------------

st.write(
    f"**Moniepoint Withdrawal Charges:** "
    f"₦{moniepoint_withdrawal_charges:,.2f}"
)

st.write(
    f"**Moniepoint Transfer Money Received:** "
    f"₦{moniepoint_transfer_received:,.2f}"
)

st.write(
    f"**Moniepoint Transfer Charges:** "
    f"₦{moniepoint_transfer_charges:,.2f}"
)

st.write(
    f"**Moniepoint Sales:** "
    f"₦{moniepoint_sales_amount:,.2f}"
)

st.write(
    f"**Moniepoint Sales Charges:** "
    f"₦{moniepoint_sales_charges:,.2f}"
)


# ------------------------------------------------------------
# Total Cash Credit
# ------------------------------------------------------------

cash_credit_total = (
    opening_cash
    + additional_cash
    + total_deposits
    + deposit_charges
    + other_pos_credit
    + moniepoint_withdrawal_charges
    + moniepoint_transfer_received
    + moniepoint_transfer_charges
    + moniepoint_sales_amount
    + moniepoint_sales_charges
)

st.success(
    f"Total Cash Inflow: ₦{cash_credit_total:,.2f}"
)


# ============================================================
# 📉 CASH DEBIT SIDE / OUTFLOWS
# ============================================================

st.subheader("📉 Cash Outflows")

expenses = get_total("expenses")
branch_transfers = get_total("branch_transfers")


# ------------------------------------------------------------
# Paga Withdrawals
# ------------------------------------------------------------

withdrawals = st.session_state.get("withdrawals", [])

# Use Amount Paid Out because this is the actual cash given
# to the customer.
paga_withdrawals = sum(
    float(txn.get("Amount Paid Out", 0.0) or 0.0)
    for txn in withdrawals
)


# ------------------------------------------------------------
# Other POS Withdrawals
# ------------------------------------------------------------

other_pos_withdrawals = sum(
    float(pos.get("Withdrawal", 0.0) or 0.0)
    for pos in st.session_state.get("other_pos", {}).values()
)


# ------------------------------------------------------------
# Moniepoint Transactions - Debit Side
# ------------------------------------------------------------

# Moniepoint Withdrawals:
# Only Amount Paid Out affects the cash debit side.
moniepoint_withdrawal_paid_out = sum(
    float(txn.get("Amount Paid Out", 0.0) or 0.0)
    for txn in moniepoint_withdrawals
)


# Moniepoint POS Transfers:
# Only Money Paid Out affects the cash debit side.
moniepoint_transfer_paid_out = sum(
    float(txn.get("Money Paid Out", 0.0) or 0.0)
    for txn in moniepoint_transfers
)


# ------------------------------------------------------------
# Display Cash Debit Entries
# ------------------------------------------------------------

st.write(f"**Expenses:** ₦{expenses:,.2f}")
for entry in st.session_state.get("expenses", []):
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )

st.write(f"**Cash to Branches:** ₦{branch_transfers:,.2f}")
for entry in st.session_state.get("branch_transfers", []):
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )

st.write(
    f"**Paga Withdrawals (Cash Paid Out):** "
    f"₦{paga_withdrawals:,.2f}"
)

st.write(
    f"**Other POS Withdrawals:** "
    f"₦{other_pos_withdrawals:,.2f}"
)

st.write(
    f"**Moniepoint Withdrawals (Amount Paid Out):** "
    f"₦{moniepoint_withdrawal_paid_out:,.2f}"
)

st.write(
    f"**Moniepoint POS Transfers (Money Paid Out):** "
    f"₦{moniepoint_transfer_paid_out:,.2f}"
)


# ------------------------------------------------------------
# Total Cash Debit
# ------------------------------------------------------------

cash_debit_total = (
    expenses
    + branch_transfers
    + paga_withdrawals
    + other_pos_withdrawals
    + moniepoint_withdrawal_paid_out
    + moniepoint_transfer_paid_out
)

st.error(
    f"Total Cash Outflow: ₦{cash_debit_total:,.2f}"
)


# ============================================================
# 🧮 CASH RECONCILIATION RESULT
# ============================================================

st.subheader("🧮 Cash Reconciliation Result")

if st.button("🔍 Reconcile Cash Summary"):
    net_cash = cash_credit_total - cash_debit_total

    if net_cash >= 0:
        st.success(
            f"Cash Surplus: ₦{net_cash:,.2f}"
        )
    else:
        st.error(
            f"Cash Deficit: ₦{abs(net_cash):,.2f}"
        )


# ============================================================
# 🏛 CAPITAL (SYSTEM) RECONCILIATION
# IMPORTANT:
# No Moniepoint transaction is included in this section.
# ============================================================

st.header("🏛 Capital / System Summary")


# ============================================================
# 📥 CAPITAL OPENING SIDE
# ============================================================

st.subheader("📥 Opening Side")

capital_opening = st.session_state.get(
    "capital_opening_balances",
    []
)

external_cash_entries = st.session_state.get(
    "external_additional_cash",
    []
)

capital_inflows = st.session_state.get(
    "capital_inflows",
    []
)

opening_cash_entries = st.session_state.get(
    "opening_cash_capital",
    []
)


# ------------------------------------------------------------
# Opening POS Balances
# ------------------------------------------------------------

total_opening_bal = sum(
    float(entry["balance"] or 0.0)
    for entry in capital_opening
)

st.write("**POS Opening Balances:**")

for entry in capital_opening:
    st.markdown(
        f"- {entry['pos']}: ₦{entry['balance']:,.2f}"
    )


# ------------------------------------------------------------
# Opening Cash - System
# ------------------------------------------------------------

total_opening_cash = sum(
    float(entry["amount"] or 0.0)
    for entry in opening_cash_entries
)

st.write(
    f"**Opening Cash (System):** "
    f"₦{total_opening_cash:,.2f}"
)

for entry in opening_cash_entries:
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )


# ------------------------------------------------------------
# External Additional Cash
# ------------------------------------------------------------

total_external_cash = sum(
    float(entry["amount"] or 0.0)
    for entry in external_cash_entries
)

st.write(
    f"**External Additional Cash:** "
    f"₦{total_external_cash:,.2f}"
)

for entry in external_cash_entries:
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )


# ------------------------------------------------------------
# Capital Inflows
# ------------------------------------------------------------

total_inflows = sum(
    float(entry["amount"] or 0.0)
    for entry in capital_inflows
)

st.write(
    f"**Capital Inflows:** "
    f"₦{total_inflows:,.2f}"
)

for entry in capital_inflows:
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )


# ------------------------------------------------------------
# Total Capital Opening Side
# ------------------------------------------------------------

capital_opening_side = (
    total_opening_bal
    + total_opening_cash
    + total_external_cash
    + total_inflows
)

st.success(
    f"Total Opening Side: ₦{capital_opening_side:,.2f}"
)


# ============================================================
# 📤 CAPITAL CLOSING SIDE
# ============================================================

st.subheader("📤 Closing Side")

capital_closing = st.session_state.get(
    "capital_closing_balances",
    []
)

capital_outflows = st.session_state.get(
    "capital_outflows",
    []
)

closing_cash_entries = st.session_state.get(
    "closing_cash_capital",
    []
)


# ------------------------------------------------------------
# Closing POS Balances
# ------------------------------------------------------------

total_closing_bal = sum(
    float(entry["balance"] or 0.0)
    for entry in capital_closing
)

st.write("**POS Closing Balances:**")

for entry in capital_closing:
    st.markdown(
        f"- {entry['pos']}: ₦{entry['balance']:,.2f}"
    )


# ------------------------------------------------------------
# Closing Cash - System
# ------------------------------------------------------------

total_closing_cash = sum(
    float(entry["amount"] or 0.0)
    for entry in closing_cash_entries
)

st.write(
    f"**Closing Cash (System):** "
    f"₦{total_closing_cash:,.2f}"
)

for entry in closing_cash_entries:
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )


# ------------------------------------------------------------
# Capital Outflows
# ------------------------------------------------------------

total_outflows = sum(
    float(entry["amount"] or 0.0)
    for entry in capital_outflows
)

st.write(
    f"**Capital Outflows:** "
    f"₦{total_outflows:,.2f}"
)

for entry in capital_outflows:
    st.markdown(
        f"- ₦{entry['amount']:,.2f} — {entry['description']}"
    )


# ------------------------------------------------------------
# Total Capital Closing Side
# ------------------------------------------------------------

capital_closing_side = (
    total_closing_bal
    + total_closing_cash
    + total_outflows
)

st.error(
    f"Total Closing Side: ₦{capital_closing_side:,.2f}"
)


# ============================================================

# ============================================================
# 🧮 CAPITAL RECONCILIATION RESULT
# ============================================================

st.subheader("🧮 Capital Summary Result")

if st.button("🔍 Reconcile Capital Summary"):
    capital_result = (
        capital_opening_side - capital_closing_side
    )

    if capital_result >= 0:
        st.success(
            f"Capital Surplus: ₦{capital_result:,.2f}"
        )
    else:
        st.error(
            f"Capital Deficit: ₦{abs(capital_result):,.2f}"
        )

st.markdown('</div>', unsafe_allow_html=True)


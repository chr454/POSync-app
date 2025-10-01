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
st.markdown("This page summarizes **Cash** and **Capital (System)** reconciliation for the day.")

# === Utility Function ===
def get_total(state_key):
    items = st.session_state.get(state_key, [])
    if isinstance(items, list) and len(items) > 0 and isinstance(items[0], dict):
        return sum(i.get("amount", 0.0) for i in items)
    return sum(items)

# =============================
# 💵 CASH SUMMARY RECONCILIATION
# =============================
st.header("💵 Cash Summary")

# Credit Side
st.subheader("📈 Cash Inflows")
opening_cash = st.session_state.get("opening_cash", 0.0)
additional_cash = get_total("additional_cash")

# Deposits
deposits = st.session_state.get("deposits", [])
total_deposits = sum(txn.get("Actual Amount", 0.0) for txn in deposits)   # FIXED
deposit_charges = sum(txn.get("Charge", 0.0) for txn in deposits)

# Other POS Deposits
other_pos_credit = sum(pos.get("Deposit", 0.0) for pos in st.session_state.get("other_pos", {}).values())

st.write(f"**Opening Cash:** ₦{opening_cash:,.2f}")
st.write(f"**Additional Cash:** ₦{additional_cash:,.2f}")
for entry in st.session_state.get("additional_cash", []):
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")
st.write(f"**Paga Deposits (Actual):** ₦{total_deposits:,.2f}")
st.write(f"**Deposit Charges:** ₦{deposit_charges:,.2f}")
st.write(f"**Other POS Deposits:** ₦{other_pos_credit:,.2f}")

cash_credit_total = opening_cash + additional_cash + total_deposits + deposit_charges + other_pos_credit
st.success(f"Total Cash Inflow: ₦{cash_credit_total:,.2f}")

# Debit Side
st.subheader("📉 Cash Outflows")
expenses = get_total("expenses")
branch_transfers = get_total("branch_transfers")

# Withdrawals
withdrawals = st.session_state.get("withdrawals", [])
paga_withdrawals = sum(txn.get("Amount Paid Out", 0.0) for txn in withdrawals)   # FIXED

# Other POS Withdrawals
other_pos_withdrawals = sum(pos.get("Withdrawal", 0.0) for pos in st.session_state.get("other_pos", {}).values())

st.write(f"**Expenses:** ₦{expenses:,.2f}")
for entry in st.session_state.get("expenses", []):
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")
st.write(f"**Cash to Branches:** ₦{branch_transfers:,.2f}")
for entry in st.session_state.get("branch_transfers", []):
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")
st.write(f"**Paga Withdrawals (Cash Paid Out):** ₦{paga_withdrawals:,.2f}")
st.write(f"**Other POS Withdrawals:** ₦{other_pos_withdrawals:,.2f}")

cash_debit_total = expenses + branch_transfers + paga_withdrawals + other_pos_withdrawals
st.error(f"Total Cash Outflow: ₦{cash_debit_total:,.2f}")

# Result
st.subheader("🧮 Cash Reconciliation Result")
if st.button("🔍 Reconcile Cash Summary"):
    net_cash = cash_credit_total - cash_debit_total
    if net_cash >= 0:
        st.success(f"Cash Surplus: ₦{net_cash:,.2f}")
    else:
        st.error(f"Cash Deficit: ₦{net_cash:,.2f}")

# =============================
# 🏛 CAPITAL (SYSTEM) RECONCILIATION
# =============================
st.header("🏛 Capital / System Summary")

st.subheader("📥 Opening Side")
capital_opening = st.session_state.get("capital_opening_balances", [])
external_cash_entries = st.session_state.get("external_additional_cash", [])
capital_inflows = st.session_state.get("capital_inflows", [])
opening_cash_entries = st.session_state.get("opening_cash_capital", [])

# Opening POS
total_opening_bal = sum(entry["balance"] for entry in capital_opening)
st.write("**POS Opening Balances:**")
for entry in capital_opening:
    st.markdown(f"- {entry['pos']}: ₦{entry['balance']:,.2f}")

# Opening Cash (System)
total_opening_cash = sum(entry["amount"] for entry in opening_cash_entries)
st.write(f"**Opening Cash (System):** ₦{total_opening_cash:,.2f}")
for entry in opening_cash_entries:
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")

# External cash
total_external_cash = sum(entry["amount"] for entry in external_cash_entries)
st.write(f"**External Additional Cash:** ₦{total_external_cash:,.2f}")
for entry in external_cash_entries:
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")

# Inflows
total_inflows = sum(entry["amount"] for entry in capital_inflows)
st.write(f"**Capital Inflows:** ₦{total_inflows:,.2f}")
for entry in capital_inflows:
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")

capital_opening_side = total_opening_bal + total_opening_cash + total_external_cash + total_inflows
st.success(f"Total Opening Side: ₦{capital_opening_side:,.2f}")

st.subheader("📤 Closing Side")
capital_closing = st.session_state.get("capital_closing_balances", [])
capital_outflows = st.session_state.get("capital_outflows", [])
closing_cash_entries = st.session_state.get("closing_cash_capital", [])

# Closing POS
total_closing_bal = sum(entry["balance"] for entry in capital_closing)
st.write("**POS Closing Balances:**")
for entry in capital_closing:
    st.markdown(f"- {entry['pos']}: ₦{entry['balance']:,.2f}")

# Closing Cash (System)
total_closing_cash = sum(entry["amount"] for entry in closing_cash_entries)
st.write(f"**Closing Cash (System):** ₦{total_closing_cash:,.2f}")
for entry in closing_cash_entries:
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")

# Outflows
total_outflows = sum(entry["amount"] for entry in capital_outflows)
st.write(f"**Capital Outflows:** ₦{total_outflows:,.2f}")
for entry in capital_outflows:
    st.markdown(f"- ₦{entry['amount']:,.2f} — {entry['description']}")

capital_closing_side = total_closing_bal + total_closing_cash + total_outflows
st.error(f"Total Closing Side: ₦{capital_closing_side:,.2f}")

# Result
st.subheader("🧮 Capital Summary Result")
if st.button("🔍 Reconcile Capital Summary"):
    capital_result = capital_opening_side - capital_closing_side
    if capital_result >= 0:
        st.success(f"Capital Surplus: ₦{capital_result:,.2f}")
    else:
        st.error(f"Capital Deficit: ₦{capital_result:,.2f}")

st.markdown('</div>', unsafe_allow_html=True)

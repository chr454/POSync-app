import streamlit as st

st.set_page_config(page_title="Staff Inputs", layout="wide")

# ✅ Safe rerun trigger
def safe_rerun():
    st.rerun()  # Updated for latest Streamlit

# Load CSS if available
try:
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Style file not found. Skipping custom styling.")

st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("🧾 Staff Inputs")
st.markdown("""
#### This page is for authorized staff to manually enter and update key cash values for daily reconciliation.
Only staff can enter:
- Opening cash
- Additional cash collected during the day
- Expenses
- Money given to other branches
""")

# === OPENING CASH ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("Opening Cash")

st.session_state.setdefault("opening_cash", 0.0)

with st.form("opening_cash_form", clear_on_submit=True):
    input_opening_cash = st.number_input("Enter opening cash", min_value=0.0, step=100.0)
    submitted = st.form_submit_button("💾 Save Opening Cash")
    if submitted:
        st.session_state.opening_cash = input_opening_cash
        st.success(f"Opening cash of ₦{input_opening_cash:,.2f} saved.")

st.markdown('</div>', unsafe_allow_html=True)

# === ADDITIONAL CASH ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("Additional Cash (collected during the day)")

st.session_state.setdefault("additional_cash", [])

with st.form("additional_cash_form", clear_on_submit=True):
    new_cash = st.number_input("Amount", min_value=0.0, step=100.0, key="ac_amt")
    new_desc = st.text_input("Description", key="ac_desc")
    if st.form_submit_button("➕ Add Additional Cash"):
        if new_cash > 0 and new_desc:
            st.session_state.additional_cash.append({"amount": new_cash, "description": new_desc})
            st.success(f"Added ₦{new_cash:,.2f} — {new_desc}")

if st.session_state.additional_cash:
    st.markdown("##### Entries:")
    for i, entry in enumerate(st.session_state.additional_cash):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"₦{entry['amount']:,.2f} — {entry['description']}")
        with col2:
            if st.button("🗑", key=f"del_ac_{i}"):
                st.session_state.additional_cash.pop(i)
                safe_rerun()

st.markdown('</div>', unsafe_allow_html=True)

# === EXPENSES ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("Expenses")

st.session_state.setdefault("expenses", [])

with st.form("expenses_form", clear_on_submit=True):
    exp_amt = st.number_input("Amount", min_value=0.0, step=100.0, key="ex_amt")
    exp_desc = st.text_input("Description", key="ex_desc")
    if st.form_submit_button("➖ Add Expense"):
        if exp_amt > 0 and exp_desc:
            st.session_state.expenses.append({"amount": exp_amt, "description": exp_desc})
            st.success(f"Added ₦{exp_amt:,.2f} — {exp_desc}")

if st.session_state.expenses:
    st.markdown("##### Entries:")
    for i, entry in enumerate(st.session_state.expenses):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"₦{entry['amount']:,.2f} — {entry['description']}")
        with col2:
            if st.button("🗑", key=f"del_exp_{i}"):
                st.session_state.expenses.pop(i)
                safe_rerun()

st.markdown('</div>', unsafe_allow_html=True)

# === BRANCH TRANSFERS ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("Cash Sent to Other Branches")

st.session_state.setdefault("branch_transfers", [])

with st.form("branch_form", clear_on_submit=True):
    branch_amt = st.number_input("Amount", min_value=0.0, step=100.0, key="bt_amt")
    branch_desc = st.text_input("Description", key="bt_desc")
    if st.form_submit_button("🏢 Add Branch Transfer"):
        if branch_amt > 0 and branch_desc:
            st.session_state.branch_transfers.append({"amount": branch_amt, "description": branch_desc})
            st.success(f"Added ₦{branch_amt:,.2f} — {branch_desc}")

if st.session_state.branch_transfers:
    st.markdown("##### Entries:")
    for i, entry in enumerate(st.session_state.branch_transfers):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"₦{entry['amount']:,.2f} — {entry['description']}")
        with col2:
            if st.button("🗑", key=f"del_branch_{i}"):
                st.session_state.branch_transfers.pop(i)
                safe_rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

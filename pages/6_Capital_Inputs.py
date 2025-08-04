import streamlit as st

st.set_page_config(page_title="Capital Inputs", layout="wide")
st.title("🏛 Capital Summary Inputs")

st.markdown("""
Use this page to enter opening and closing balances for all POS terminals,
external additional cash, and capital inflows/outflows.
""")

# === Initialize State ===
if "capital_opening_balances" not in st.session_state:
    st.session_state.capital_opening_balances = []
if "capital_closing_balances" not in st.session_state:
    st.session_state.capital_closing_balances = []
if "external_additional_cash" not in st.session_state:
    st.session_state.external_additional_cash = []
if "capital_inflows" not in st.session_state:
    st.session_state.capital_inflows = []
if "capital_outflows" not in st.session_state:
    st.session_state.capital_outflows = []

# === POS Balances ===
st.subheader("🏦 POS Terminal Balances")

with st.form("pos_balances", clear_on_submit=True):
    pos_name = st.text_input("POS Terminal Name (e.g., MoniePoint, Opay)")
    opening = st.number_input("Opening Balance", min_value=0.0, step=100.0, format="%.2f")
    closing = st.number_input("Closing Balance", min_value=0.0, step=100.0, format="%.2f")
    submit = st.form_submit_button("💾 Save POS Entry")

    if submit and pos_name:
        st.session_state.capital_opening_balances.append({"pos": pos_name, "balance": opening})
        st.session_state.capital_closing_balances.append({"pos": pos_name, "balance": closing})
        st.success(f"Saved {pos_name} — Opening ₦{opening:,.2f}, Closing ₦{closing:,.2f}")

# === External Additional Cash ===
st.subheader("💸 External Additional Cash")

with st.form("external_cash_form", clear_on_submit=True):
    ext_cash_amt = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f", key="ext_cash_amt")
    ext_cash_desc = st.text_input("Description", key="ext_cash_desc")
    ext_submit = st.form_submit_button("➕ Add External Cash Entry")

    if ext_submit and ext_cash_amt > 0:
        st.session_state.external_additional_cash.append({
            "amount": ext_cash_amt,
            "description": ext_cash_desc
        })
        st.success("External cash entry saved.")

# === Capital Flows ===
st.subheader("🔁 Capital Flows")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Capital **Outflow**")
    with st.form("outflow_form", clear_on_submit=True):
        out_amt = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f", key="out_amt")
        out_desc = st.text_input("Description", key="out_desc")
        out_submit = st.form_submit_button("Add Capital Outflow")

        if out_submit and out_amt > 0:
            st.session_state.capital_outflows.append({
                "amount": out_amt,
                "description": out_desc
            })
            st.success("Capital outflow entry saved.")

with col2:
    st.markdown("#### Capital **Inflow**")
    with st.form("inflow_form", clear_on_submit=True):
        in_amt = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f", key="in_amt")
        in_desc = st.text_input("Description", key="in_desc")
        in_submit = st.form_submit_button("Add Capital Inflow")

        if in_submit and in_amt > 0:
            st.session_state.capital_inflows.append({
                "amount": in_amt,
                "description": in_desc
            })
            st.success("Capital inflow entry saved.")

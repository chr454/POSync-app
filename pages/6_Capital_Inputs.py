import streamlit as st
import pandas as pd

st.set_page_config(page_title="Capital Inputs", layout="wide")
st.title("🏛 Capital Summary Inputs")

st.markdown("""
Use this page to enter opening and closing balances for all POS terminals,
external additional cash, capital inflows/outflows, and cash balances.
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
if "opening_cash" not in st.session_state:
    st.session_state.opening_cash = 0.0
if "closing_cash" not in st.session_state:
    st.session_state.closing_cash = 0.0

# === Opening & Closing Cash ===
st.subheader("💵 Cash Balances")
st.session_state.opening_cash = st.number_input(
    "Opening Cash", min_value=0.0, step=100.0, format="%.2f",
    value=st.session_state.opening_cash
)
st.session_state.closing_cash = st.number_input(
    "Closing Cash", min_value=0.0, step=100.0, format="%.2f",
    value=st.session_state.closing_cash
)

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

if st.session_state.capital_opening_balances:
    df_open = pd.DataFrame(st.session_state.capital_opening_balances)
    df_close = pd.DataFrame(st.session_state.capital_closing_balances)
    st.write("**Saved POS Balances:**")
    st.dataframe(pd.concat([df_open, df_close], axis=1), use_container_width=True)
    for i, entry in enumerate(st.session_state.capital_opening_balances):
        if st.button(f"🗑 Delete {entry['pos']}", key=f"del_pos_{i}"):
            st.session_state.capital_opening_balances.pop(i)
            st.session_state.capital_closing_balances.pop(i)
            st.rerun()

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

if st.session_state.external_additional_cash:
    ext_df = pd.DataFrame(st.session_state.external_additional_cash)
    st.dataframe(ext_df, use_container_width=True)
    for i, entry in enumerate(st.session_state.external_additional_cash):
        if st.button(f"🗑 Delete Ext Cash {i+1}", key=f"del_ext_{i}"):
            st.session_state.external_additional_cash.pop(i)
            st.rerun()

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

    if st.session_state.capital_outflows:
        out_df = pd.DataFrame(st.session_state.capital_outflows)
        st.dataframe(out_df, use_container_width=True)
        for i, entry in enumerate(st.session_state.capital_outflows):
            if st.button(f"🗑 Delete Outflow {i+1}", key=f"del_out_{i}"):
                st.session_state.capital_outflows.pop(i)
                st.rerun()

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

    if st.session_state.capital_inflows:
        in_df = pd.DataFrame(st.session_state.capital_inflows)
        st.dataframe(in_df, use_container_width=True)
        for i, entry in enumerate(st.session_state.capital_inflows):
            if st.button(f"🗑 Delete Inflow {i+1}", key=f"del_in_{i}"):
                st.session_state.capital_inflows.pop(i)
                st.rerun()

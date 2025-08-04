import streamlit as st
import pandas as pd
import io
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Export Logs", layout="wide")

# Load CSS
try:
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Style file not found.")

st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("📤 Export Logs")
st.markdown("""
Use this page to export your recorded transactions and reconciliation data.
Files will be downloaded in Excel or PDF format for audit or backup purposes.
""")

# === Export Deposits ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("💰 Export Deposits")
if "deposits" in st.session_state and st.session_state.deposits:
    df = pd.DataFrame(st.session_state.deposits)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)

    st.download_button(
        label="⬇️ Download Deposits Excel",
        data=excel_buffer,
        file_name=f"deposits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No deposit data available to export.")
st.markdown('</div>', unsafe_allow_html=True)

# === Export Withdrawals ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("💸 Export Withdrawals")
if "withdrawals" in st.session_state and st.session_state.withdrawals:
    df = pd.DataFrame(st.session_state.withdrawals)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)

    st.download_button(
        label="⬇️ Download Withdrawals Excel",
        data=excel_buffer,
        file_name=f"withdrawals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No withdrawal data available to export.")
st.markdown('</div>', unsafe_allow_html=True)

# === Export Other POS Records ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("🏧 Export Other POS Records")
if "other_pos" in st.session_state and st.session_state.other_pos:
    df = pd.DataFrame([
        {"POS Name": k, **v} for k, v in st.session_state.other_pos.items()
    ])
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)

    st.download_button(
        label="⬇️ Download Other POS Excel",
        data=excel_buffer,
        file_name=f"other_pos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No other POS data available to export.")
st.markdown('</div>', unsafe_allow_html=True)

# === Export Reconciliation Summary as PDF ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("📄 Export Reconciliation Summary")

if st.button("📄 Generate Reconciliation PDF"):

    def get_total(key):
        items = st.session_state.get(key, [])
        if isinstance(items, list) and len(items) > 0 and isinstance(items[0], dict):
            return sum(i.get("amount", 0.0) for i in items)
        return sum(items)

    # === Cash Summary Calculations ===
    opening = st.session_state.get("opening_cash", 0.0)
    add_cash = get_total("additional_cash")
    deposit_amt = sum(txn["Amount"] for txn in st.session_state.get("deposits", []))
    deposit_chg = sum(txn["Charge"] for txn in st.session_state.get("deposits", []))
    other_deposits = sum(pos["Deposit"] for pos in st.session_state.get("other_pos", {}).values())
    expenses = get_total("expenses")
    branches = get_total("branch_transfers")
    payout = sum(txn["Amount Paid Out"] for txn in st.session_state.get("withdrawals", []))
    other_payouts = sum(pos["Withdrawal"] for pos in st.session_state.get("other_pos", {}).values())

    credit = opening + add_cash + deposit_amt + deposit_chg + other_deposits
    debit = expenses + branches + payout + other_payouts
    final_balance = credit - debit

    # === PDF Generation ===
    pdf = FPDF()
    pdf.add_font("DejaVu", "", "./Fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "./Fonts/dejavu-fonts-ttf-2.37/ttf/DejaVuSans-Bold.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(200, 10, txt="Reconciliation Summary", ln=1, align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    pdf.ln(5)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(200, 10, txt="CASH SUMMARY — CREDIT", ln=1)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Opening Cash: ₦{opening:,.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Additional Cash: ₦{add_cash:,.2f}", ln=1)
    for entry in st.session_state.get("additional_cash", []):
        pdf.cell(200, 10, txt=f"• ₦{entry['amount']:,.2f} — {entry['description']}", ln=1)
    pdf.cell(200, 10, txt=f"Paga Deposits: ₦{deposit_amt:,.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Deposit Charges: ₦{deposit_chg:,.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Other POS Deposits: ₦{other_deposits:,.2f}", ln=1)

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(200, 10, txt="CASH SUMMARY — DEBIT", ln=1)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Expenses: ₦{expenses:,.2f}", ln=1)
    for entry in st.session_state.get("expenses", []):
        pdf.cell(200, 10, txt=f"• ₦{entry['amount']:,.2f} — {entry['description']}", ln=1)
    pdf.cell(200, 10, txt=f"Cash to Branches: ₦{branches:,.2f}", ln=1)
    for entry in st.session_state.get("branch_transfers", []):
        pdf.cell(200, 10, txt=f"• ₦{entry['amount']:,.2f} — {entry['description']}", ln=1)
    pdf.cell(200, 10, txt=f"Paga Withdrawals: ₦{payout:,.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Other POS Withdrawals: ₦{other_payouts:,.2f}", ln=1)

    pdf.ln(5)
    label = "SURPLUS" if final_balance >= 0 else "DEFICIT"
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(200, 10, txt=f"FINAL CASH BALANCE: ₦{final_balance:,.2f} ({label})", ln=1, align='C')

    # Capital Summary
    opening_list = st.session_state.get("capital_opening_balances", [])
    closing_list = st.session_state.get("capital_closing_balances", [])
    external_list = st.session_state.get("external_additional_cash", [])
    capital_inflows_list = st.session_state.get("capital_inflows", [])
    capital_outflows_list = st.session_state.get("capital_outflows", [])

    cap_opening = sum(x["balance"] for x in opening_list)
    cap_closing = sum(x["balance"] for x in closing_list)
    external_cash = sum(x["amount"] for x in external_list)
    capital_inflows = sum(x["amount"] for x in capital_inflows_list)
    capital_outflows = sum(x["amount"] for x in capital_outflows_list)

    cap_open_total = cap_opening + external_cash + capital_inflows
    cap_close_total = cap_closing + capital_outflows
    cap_result = cap_open_total - cap_close_total

    pdf.add_page()
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(200, 10, txt="CAPITAL SUMMARY", ln=1, align='C')
    pdf.ln(5)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(200, 10, txt="OPENING SIDE", ln=1)
    pdf.set_font("DejaVu", "", 12)
    for entry in opening_list:
        pdf.cell(200, 10, txt=f"{entry['pos']} — ₦{entry['balance']:,.2f}", ln=1)
    for entry in external_list:
        pdf.cell(200, 10, txt=f"₦{entry['amount']:,.2f} — {entry['description']}", ln=1)
    for entry in capital_inflows_list:
        pdf.cell(200, 10, txt=f"₦{entry['amount']:,.2f} — {entry['description']}", ln=1)

    pdf.ln(3)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(200, 10, txt="CLOSING SIDE", ln=1)
    pdf.set_font("DejaVu", "", 12)
    for entry in closing_list:
        pdf.cell(200, 10, txt=f"{entry['pos']} — ₦{entry['balance']:,.2f}", ln=1)
    for entry in capital_outflows_list:
        pdf.cell(200, 10, txt=f"₦{entry['amount']:,.2f} — {entry['description']}", ln=1)

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    label = "SURPLUS" if cap_result >= 0 else "DEFICIT"
    pdf.cell(200, 10, txt=f"FINAL CAPITAL BALANCE: ₦{cap_result:,.2f} ({label})", ln=1, align='C')

    # Send as downloadable stream
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Download Reconciliation PDF",
        data=pdf_buffer,
        file_name=f"reconciliation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )

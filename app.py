import streamlit as st
from PIL import Image

# Load custom CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === Sidebar Branding ===
#st.sidebar.image("assets/posync-logo.png", use_column_width=True)
st.sidebar.title("📊 POSync")
st.sidebar.markdown("**Smart Reconciliation Dashboard**")
st.sidebar.divider()
st.sidebar.markdown("Use the **sidebar** to navigate pages.")

# === Page Content ===
st.markdown('<div class="page-container">', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>Welcome to <span style="color:#f47b20;">POSync</span></h1>
    <p>Your unified dashboard for managing POS deposits, withdrawals, and reconciliation reports.</p>
</div>
""", unsafe_allow_html=True)

# Summary Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><h3>Total Deposits</h3><p>₦0.00</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card"><h3>Total Withdrawals</h3><p>₦0.00</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card"><h3>Outstanding Transfers</h3><p>₦0.00</p></div>', unsafe_allow_html=True)

# Optional: Banner or Logo
st.image("assets/placeholder.jpeg", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

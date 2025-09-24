import streamlit as st
import pandas as pd

st.set_page_config(page_title="Compare Excel Files", layout="wide")

# Load CSS
try:
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("📊 Compare Excel Files")
st.markdown("""
Upload **two Excel/CSV files** and compare them.  
- You can apply multiple filters to narrow data.  
- You can compare **multiple columns at once**.  
- The tool checks row-by-row equality **regardless of order**.
""")

# === Upload Files ===
st.subheader("🔁 Upload Excel Files for Comparison")
file1 = st.file_uploader("Upload First File", type=["csv", "xls", "xlsx"])
file2 = st.file_uploader("Upload Second File", type=["csv", "xls", "xlsx"])

def load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

if file1 and file2:
    try:
        df1 = load_file(file1)
        df2 = load_file(file2)

        st.markdown("### ✅ File Preview")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**File 1 Preview:**")
            st.dataframe(df1.head())
        with col2:
            st.write("**File 2 Preview:**")
            st.dataframe(df2.head())

        # === Multi-filter Section ===
        st.markdown("### 🔍 Apply Filters (Optional)")
        with st.expander("Filter File 1"):
            for col in df1.columns:
                unique_vals = sorted(df1[col].dropna().unique())
                selected_vals = st.multiselect(f"Filter File 1 by {col}", unique_vals, key=f"f1_{col}")
                if selected_vals:
                    df1 = df1[df1[col].isin(selected_vals)]

        with st.expander("Filter File 2"):
            for col in df2.columns:
                unique_vals = sorted(df2[col].dropna().unique())
                selected_vals = st.multiselect(f"Filter File 2 by {col}", unique_vals, key=f"f2_{col}")
                if selected_vals:
                    df2 = df2[df2[col].isin(selected_vals)]

        # === Multi-column comparison ===
        st.subheader("🔎 Choose Columns to Compare")
        common_cols = list(set(df1.columns).intersection(set(df2.columns)))
        selected_cols = st.multiselect("Select columns to compare across both files", common_cols)

        if selected_cols and st.button("🔍 Compare Files"):
            # Reduce both DataFrames to selected columns only
            df1_comp = df1[selected_cols].copy()
            df2_comp = df2[selected_cols].copy()

            # Convert rows to sets of tuples (order-independent)
            set1 = set([tuple(x) for x in df1_comp.to_numpy()])
            set2 = set([tuple(x) for x in df2_comp.to_numpy()])

            st.markdown("### 🧾 Comparison Report")

            # Show unmatched rows
            in_file1_not_file2 = set1 - set2
            in_file2_not_file1 = set2 - set1

            if not in_file1_not_file2 and not in_file2_not_file1:
                st.success("🎉 The files are identical based on selected columns (row-by-row, order ignored).")
            else:
                if in_file1_not_file2:
                    st.warning("**Rows in File 1 not found in File 2:**")
                    st.dataframe(pd.DataFrame(list(in_file1_not_file2), columns=selected_cols))

                if in_file2_not_file1:
                    st.warning("**Rows in File 2 not found in File 1:**")
                    st.dataframe(pd.DataFrame(list(in_file2_not_file1), columns=selected_cols))

    except Exception as e:
        st.error(f"Error reading files: {e}")

st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Compare Excel Files", layout="wide")

# Load CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("📊 Compare Excel Files")
st.markdown("""
Use this tool to compare two Excel files.
You can filter specific rows based on any column and compare values column-by-column.
""")

# === Upload Files ===
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.subheader("🔁 Upload Excel Files for Comparison")
file1 = st.file_uploader("Upload First Excel File", type=["csv", "xls", "xlsx"])
file2 = st.file_uploader("Upload Second Excel File", type=["csv", "xls", "xlsx"])

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
        st.write("**First File:**")
        st.dataframe(df1.head())
        st.write("**Second File:**")
        st.dataframe(df2.head())

        # Optional Filtering Section
        st.markdown("### 🔍 Optional Filtering")

        filter_col1 = st.selectbox("Choose filter column from File 1 (optional)", ["None"] + list(df1.columns))
        selected_value1 = None
        if filter_col1 != "None":
            options1 = sorted(df1[filter_col1].dropna().unique())
            selected_value1 = st.multiselect(f"Select values in {filter_col1} from File 1", options1)
            if selected_value1:
                df1 = df1[df1[filter_col1].isin(selected_value1)]

        filter_col2 = st.selectbox("Choose filter column from File 2 (optional)", ["None"] + list(df2.columns))
        selected_value2 = None
        if filter_col2 != "None":
            options2 = sorted(df2[filter_col2].dropna().unique())
            selected_value2 = st.multiselect(f"Select values in {filter_col2} from File 2", options2)
            if selected_value2:
                df2 = df2[df2[filter_col2].isin(selected_value2)]

        # Column Selection
        st.subheader("🔎 Choose Columns to Compare")
        col1 = st.selectbox("Select column from File 1", df1.columns)
        col2 = st.selectbox("Select column from File 2", df2.columns)

        if st.button("🔍 Compare Columns"):
            col1_values = df1[col1].astype(str).tolist()
            col2_values = df2[col2].astype(str).tolist()

            set1 = set(col1_values)
            set2 = set(col2_values)

            st.markdown("### 🧾 Column Report")
            st.markdown(f"**All values from `{col1}` in File 1 ({len(col1_values)} total):**")
            st.dataframe(df1[[col1]])

            st.markdown(f"**All values from `{col2}` in File 2 ({len(col2_values)} total):**")
            st.dataframe(df2[[col2]])

            in_file1_not_file2 = set1 - set2
            in_file2_not_file1 = set2 - set1

            st.markdown("### ❌ Differences Detected")

            if in_file1_not_file2:
                st.warning(f"**Rows in File 1 with values in `{col1}` missing from File 2's `{col2}`:")
                mismatch1 = df1[df1[col1].astype(str).isin(in_file1_not_file2)]
                st.dataframe(mismatch1)
            else:
                st.success("No unmatched values in File 1.")

            if in_file2_not_file1:
                st.warning(f"**Rows in File 2 with values in `{col2}` missing from File 1's `{col1}`:")
                mismatch2 = df2[df2[col2].astype(str).isin(in_file2_not_file1)]
                st.dataframe(mismatch2)
            else:
                st.success("No unmatched values in File 2.")

    except Exception as e:
        st.error(f"Error reading files: {e}")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

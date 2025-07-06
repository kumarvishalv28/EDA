# # Save this as eda_streamlit_app.py

# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Config
# st.set_page_config(page_title="EDA Tool", layout="wide")
# st.title("📊 Exploratory Data Analysis Web App")

# # File Upload
# uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     st.success(f"Uploaded `{uploaded_file.name}` with shape {df.shape}")

#     # Show raw data
#     with st.expander("🔍 Preview Data"):
#         st.dataframe(df)

#     # Summary
#     st.header("📑 Data Summary")
#     st.write(df.describe(include="all"))

#     # Missing values
#     st.subheader("🌡️ Missing Value Heatmap")
#     fig1, ax1 = plt.subplots(figsize=(10, 5))
#     sns.heatmap(df.isnull(), cbar=False, cmap="viridis", ax=ax1)
#     st.pyplot(fig1)

#     # Correlation Heatmap
#     st.subheader("📌 Correlation Heatmap")
#     numeric_df = df.select_dtypes(include=['int64', 'float64'])
#     if not numeric_df.empty:
#         fig2, ax2 = plt.subplots(figsize=(10, 6))
#         sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax2)
#         st.pyplot(fig2)
#     else:
#         st.warning("No numeric columns to display correlation.")

#     # Univariate
#     st.subheader("📊 Univariate Plot")
#     column = st.selectbox("Select column", df.columns)
#     fig3, ax3 = plt.subplots()
#     if df[column].dtype == 'object':
#         sns.countplot(y=column, data=df, order=df[column].value_counts().index, ax=ax3)
#     else:
#         sns.histplot(df[column].dropna(), kde=True, ax=ax3)
#     st.pyplot(fig3)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="EDA Explorer", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #f7f9fc; }
    .css-18e3th9 { padding: 2rem 2rem 1rem 2rem; }
    .css-1d391kg { padding: 2rem 2rem 1rem 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Exploratory Data Analysis App")
st.markdown("Welcome to your **interactive and stylish EDA app**. Upload your dataset and start exploring! 🚀")

# Sidebar
st.sidebar.title("📂 Navigation")
section = st.sidebar.radio("Go to section", ["Upload", "Summary", "Missing Values", "Correlation", "Univariate Plot", "Pairplot & Boxplot", "Download Report"])

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if section == "Upload":
        st.subheader("📁 Dataset Preview")
        st.write("Showing first 10 rows of your dataset:")
        st.dataframe(df.head(10), use_container_width=True)

        with st.expander("📌 Basic Information", expanded=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("📦 Rows", df.shape[0])
            col2.metric("🧱 Columns", df.shape[1])
            col3.metric("⚠️ Missing Values", df.isnull().sum().sum())

    elif section == "Summary":
        st.subheader("📑 Dataset Summary")
        st.dataframe(df.describe(include="all").T, use_container_width=True)

    elif section == "Missing Values":
        st.subheader("🌡️ Missing Value Heatmap")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(df.isnull(), cbar=False, cmap="YlOrRd", ax=ax)
        st.pyplot(fig)

    elif section == "Correlation":
        st.subheader("📌 Correlation Heatmap (Numerical Columns Only)")
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if not numeric_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No numerical columns found for correlation matrix.")

    elif section == "Univariate Plot":
        st.subheader("📊 Univariate Analysis")
        column = st.selectbox("Select a column to plot", df.columns)

        fig, ax = plt.subplots()
        if df[column].dtype == "object":
            sns.countplot(y=column, data=df, order=df[column].value_counts().index, ax=ax, palette="pastel")
        else:
            sns.histplot(df[column].dropna(), kde=True, ax=ax, color="skyblue")
        st.pyplot(fig)

    elif section == "Pairplot & Boxplot":
        st.subheader("📈 Pairplot")
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if len(num_cols) >= 2:
            fig = sns.pairplot(df[num_cols].dropna())
            st.pyplot(fig)
        else:
            st.warning("Need at least 2 numerical columns for pairplot.")

        st.subheader("📦 Boxplot")
        box_col = st.selectbox("Select column for Boxplot", num_cols)
        fig2, ax2 = plt.subplots()
        sns.boxplot(x=df[box_col], ax=ax2, color='orange')
        st.pyplot(fig2)

    elif section == "Download Report":
        st.subheader("📤 Download Cleaned Data")
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False)
        st.download_button("Download CSV", buffer.getvalue(), file_name="cleaned_data.csv", mime="text/csv")

else:
    st.warning("👈 Please upload a CSV file from the sidebar to get started.")

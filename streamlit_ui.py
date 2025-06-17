import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Demo",page_icon="Computer",initial_sidebar_state="auto", layout="wide")
def main():
    st.title("Streamlit Feature Demo")
    st.write("This app demonstrates some core Streamlit features.")
  

    st.header("Interactive Widgets")
    name = st.text_input("Enter your name", "Data Scientist")
    if st.button("Greet"):
        st.success(f"Hello, {name}!")

    st.header("Data Display")
    df = pd.DataFrame(np.random.randn(10, 3), columns=list("ABC"))
    st.dataframe(df)
    st.header("Charting")
    st.line_chart(df)

    st.header("File Upload")
    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    uploaded_df = None
    if file is not None:
        if file.size > 5 * 1024 * 1024:
            st.error("File too large (max 5MB).")
        else:
            try:
                if file.name.endswith(".csv"):
                    uploaded_df = pd.read_csv(file)
                else:
                    uploaded_df = pd.read_excel(file)

                # Try to automatically convert object columns to numeric or bool
                for col in uploaded_df.columns:
                    if uploaded_df[col].dtype == object:
                        converted = pd.to_numeric(uploaded_df[col], errors="ignore")
                        if pd.api.types.is_numeric_dtype(converted):
                            uploaded_df[col] = converted
                            continue

                        lowered = uploaded_df[col].astype(str).str.lower().str.strip()
                        bool_map = {
                            "true": True,
                            "false": False,
                            "yes": True,
                            "no": False,
                            "1": True,
                            "0": False,
                        }
                        unique_vals = set(lowered.dropna().unique())
                        if unique_vals and unique_vals <= set(bool_map.keys()):
                            uploaded_df[col] = lowered.map(bool_map).astype("bool")

                st.subheader("Uploaded Data")
                st.dataframe(uploaded_df)

                numeric_cols = uploaded_df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    st.subheader("Create Chart from Uploaded Data")
                    x_axis = st.selectbox("X-axis", uploaded_df.columns.tolist())
                    y_axis = st.selectbox("Y-axis", numeric_cols)
                    chart_type = st.selectbox("Chart type", ["Line", "Bar", "Area"], index=0)
                    if x_axis and y_axis:
                        chart_df = uploaded_df[[x_axis, y_axis]].dropna()
                        if chart_type == "Line":
                            chart = alt.Chart(chart_df).mark_line().encode(x=x_axis, y=y_axis)
                        elif chart_type == "Bar":
                            chart = alt.Chart(chart_df).mark_bar().encode(x=x_axis, y=y_axis)
                        else:
                            chart = alt.Chart(chart_df).mark_area().encode(x=x_axis, y=y_axis)
                        st.altair_chart(chart, use_container_width=True)
            except Exception as e:
                st.error(f"Error processing file: {e}")


if __name__ == "__main__":
    main()

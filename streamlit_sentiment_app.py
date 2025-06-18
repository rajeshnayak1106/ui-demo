
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title
st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="wide")
st.title("Sentiment Analysis by Platform")

# Data from the image (approximated)
data = {
    "Platform": [
        "Websites", "Twitter", "Facebook", "Instagram", "TikTok",
        "YouTube", "Quynmet", "Forum", "Tripadvisor", "Reddit"
    ],
    "Positive": [60, 30, 40, 35, 33, 36, 30, 18, 22, 25],
    "Neutral": [25, 20, 20, 25, 27, 30, 28, 17, 23, 22],
    "Negative": [15, 50, 40, 40, 40, 34, 42, 65, 55, 53],
}

df = pd.DataFrame(data)
df.set_index("Platform", inplace=True)

# Display metadata
col1, col2 = st.columns(2)
with col1:
    st.metric("Most Positive Mentions", "Websites", "27,392")
with col2:
    st.metric("Most Negative Mentions", "Twitter", "14,183")

# Plotting
st.subheader("Sentiment Distribution Across Platforms")
fig, ax = plt.subplots(figsize=(12, 6))
df.plot(kind="barh", stacked=True, color=["mediumseagreen", "gray", "crimson"], ax=ax)
plt.xlabel("Mentions")
plt.ylabel("Platform")
plt.legend(title="Sentiment", loc="upper right")
st.pyplot(fig)

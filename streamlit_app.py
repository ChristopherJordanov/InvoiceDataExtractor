import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Invoice Data Extractor")
st.write(
    "Upload an invoice below and the data will be ready for you below "
)


# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)


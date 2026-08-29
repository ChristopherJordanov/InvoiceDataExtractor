import streamlit as st

from extractor import extract_text
from ai_extractor import extract_invoice_data


# Page configuration
st.set_page_config(
    page_title="Invoice Data Extractor",
    page_icon="📄",
    layout="wide"
)


# Header
st.title("Invoice Data Extractor")

st.write(
    "Upload an invoice and automatically extract its information."
)


# File upload
uploaded_file = st.file_uploader(
    "Upload an invoice",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Supported formats: PDF, PNG, JPG and JPEG"
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract invoice data", type="primary"):

        # Text extraction
        with st.spinner("Reading invoice..."):

            try:
                text = extract_text(uploaded_file)

            except Exception as e:
                st.error(f"Error while reading the invoice: {e}")
                st.stop()


        # Check extracted text
        if not text.strip():
            st.warning(
                "No text could be extracted from this invoice."
            )
            st.stop()


        # Show OCR text
        with st.expander("View extracted text"):

            st.text_area(
                "OCR Text",
                text,
                height=300
            )


        # AI integration
        with st.spinner("Analyzing invoice with AI..."):

            try:
                invoice_data = extract_invoice_data(text)

            except Exception as e:
                st.error(f"Error while analyzing the invoice: {e}")
                st.stop()

        # Display results
        st.subheader("Extracted invoice data")

        st.json(invoice_data.model_dump())
import streamlit as st
from extractor import extract_text

# Show title and description.
st.title("Invoice Data Extractor")
st.write(
    "Upload an invoice below and the data will be ready for you below "
)


# Let the user upload a file via `st.file_uploader`
uploaded_file = st.file_uploader(
    "Upload an invoice (.pdf, .png or .jpg)", type=("pdf", "png", "jpg")
)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Extract text"):
        with st.spinner("Reading invoice..."):
            try:
                text = extract_text(uploaded_file)

                if text.strip():
                    st.subheader("Extracted text")
                    st.text_area(
                        "Text",
                        text,
                        height=400
                    )
                else:
                    st.warning("No text could be extracted from this file.")

            except Exception as e:
                st.error(f"Error: {e}")

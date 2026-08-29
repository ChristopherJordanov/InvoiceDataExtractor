import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Invoice Data Extractor")
st.write(
    "Upload an invoice below and the data will be ready for you below "
)

openai_api_key = st.text_input("OpenAI API Key", type="password")


client = OpenAI(api_key=openai_api_key)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

if uploaded_file:

    # Process the uploaded file.
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document}",
        }
    ]

    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)

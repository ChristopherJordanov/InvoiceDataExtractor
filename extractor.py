import io

import fitz
import pytesseract

from PIL import Image

import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_pdf(file):
    pdf_bytes = file.read()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_text_from_image(file):
    image = Image.open(io.BytesIO(file.read()))

    text = pytesseract.image_to_string(
        image,
        lang="bul+eng"
    )

    return text


def extract_text(file):
    file_type = file.type

    if file_type == "application/pdf":
        return extract_text_from_pdf(file)

    if file_type in ["image/png", "image/jpeg"]:
        return extract_text_from_image(file)

    raise ValueError("Unsupported file type.")
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from models import InvoiceData


# Load environment variables
load_dotenv()


# OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_invoice_data(text):
    # AI extraction prompt
    prompt = f"""
You are an invoice data extraction system.

Extract information from the invoice text and return ONLY valid JSON.

Use exactly this structure:

{{
    "supplier": {{
        "name": null,
        "eik": null,
        "vat_number": null,
        "address": null,
        "iban": null,
        "bic": null
    }},
    "customer": {{
        "name": null,
        "eik": null,
        "vat_number": null,
        "address": null
    }},
    "invoice": {{
        "number": null,
        "date": null,
        "due_date": null,
        "currency": null
    }},
    "totals": {{
        "subtotal": null,
        "vat": null,
        "total": null
    }}
}}

Rules:
- Never invent information.
- Use null when information is missing.
- Preserve values from the invoice.
- Dates must use YYYY-MM-DD when possible.
- Numbers must be returned as numbers, not strings.
- Return ONLY JSON.

Invoice text:

{text}
"""

    # AI integration
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    # Parse AI response
    data = json.loads(response.output_text)

    # Validate response
    invoice_data = InvoiceData.model_validate(data)

    return invoice_data
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_invoice_data(text):
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
    - Preserve the values from the invoice.
    - Dates must use DD-MM-YYYY when possible.
    - Numbers must be returned as numbers, not strings.
    - Extract the supplier separately from the customer.
    - Return ONLY JSON.

    Invoice text:

    {text}
    """

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return json.loads(response.output_text)
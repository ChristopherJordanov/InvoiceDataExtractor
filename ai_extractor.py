import json
import os

from dotenv import load_dotenv
from openai import OpenAI



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

Analyze the invoice text and extract all available information.

Return ONLY valid JSON using exactly this structure:

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
        "currency": null
    }},
    "items": [
        {{
            "description": null,
            "quantity": null,
            "unit_price": null,
            "total_price": null
        }}
    ],
    "totals": {{
        "subtotal": null,
        "vat": null,
        "total": null
    }}
}}

Important rules:

1. Never invent information.
2. Use null when a value is not present or cannot be determined.
3. Extract the supplier's EIK/BULSTAT whenever present.
4. EIK/BULSTAT may appear under different names, including:
    - ЕИК
    - Булстат
    - БУЛСТАТ
    - UIC
    - Company ID
5. Do not confuse EIK/BULSTAT with VAT number.
6. A Bulgarian VAT number usually starts with BG followed by digits.
7. Extract IBAN exactly as shown on the invoice.
8. Extract every invoice item/product/service.
9. For every item extract:
    - description
    - quantity
    - unit price
    - VAT rate
    - total price
10. If there are multiple items, create a separate object for each item.
11. Do not combine multiple invoice items into one item.
12. Preserve the original product/service description as accurately as possible.
13. Numbers must be returned as numbers, not strings.
14. Dates should use YYYY-MM-DD when possible.
15. Return ONLY valid JSON.
16. If multiple IBANs are present, return all of them as a list.
17. If multiple BICs are present, return all of them as a list.
18. If only one IBAN/BIC is present, return it as a single string.
19. Never omit a clearly visible IBAN or BIC.

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

    return data
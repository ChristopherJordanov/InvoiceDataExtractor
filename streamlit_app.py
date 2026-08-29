import pandas as pd
import json
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
                st.error(
                    f"Error while analyzing the invoice: {e}"
                )
                st.stop()


        # Extract sections
        supplier = invoice_data.get("supplier", {})
        customer = invoice_data.get("customer", {})
        invoice = invoice_data.get("invoice", {})
        items = invoice_data.get("items", [])
        totals = invoice_data.get("totals", {})


        # Helper function
        def display_value(value):
            return value if value not in [None, ""] else "Not found"


        # Supplier and customer
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Supplier")

            st.write("**Name:**", display_value(supplier.get("name")))
            st.write("**EIK / BULSTAT:**", display_value(supplier.get("eik")))
            st.write("**VAT Number:**", display_value(supplier.get("vat_number")))
            st.write("**Address:**", display_value(supplier.get("address")))
            st.write("**IBAN:**", display_value(supplier.get("iban")))
            st.write("**BIC:**", display_value(supplier.get("bic")))

        with col2:
            st.subheader("Customer")

            st.write("**Name:**", display_value(customer.get("name")))
            st.write("**EIK / BULSTAT:**", display_value(customer.get("eik")))
            st.write("**VAT Number:**", display_value(customer.get("vat_number")))
            st.write("**Address:**", display_value(customer.get("address")))


        # Invoice information
        st.divider()

        st.subheader("Invoice")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Invoice Number",
                display_value(invoice.get("number"))
            )

        with col2:
            st.metric(
                "Date",
                display_value(invoice.get("date"))
            )

        with col3:
            st.metric(
                "Currency",
                display_value(invoice.get("currency"))
            )


        # Invoice items
        st.divider()

        st.subheader("Items")

        if items:

            items_table = pd.DataFrame(items)

            items_table = items_table.rename(
                columns={
                    "description": "Product / Service",
                    "quantity": "Quantity",
                    "unit_price": "Unit Price",
                    "vat_rate": "VAT %",
                    "total_price": "Total"
                }
            )

            st.dataframe(
                items_table,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No invoice items found.")


        # Totals
        st.divider()

        st.subheader("Totals")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Subtotal",
                display_value(totals.get("subtotal"))
            )

        with col2:
            st.metric(
                "VAT",
                display_value(totals.get("vat"))
            )

        with col3:
            st.metric(
                "Total",
                display_value(totals.get("total"))
            )


        # Raw JSON
        st.divider()

        with st.expander("View raw JSON"):
            st.json(invoice_data)

        # Export data
        st.divider()

        st.subheader("Export")

        col1, col2 = st.columns(2)

        with col1:
            json_data = json.dumps(
                invoice_data,
                indent=4,
                ensure_ascii=False
            )

            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="invoice_data.json",
                mime="application/json"
            )

        with col2:
            if items:
                csv_data = pd.DataFrame(items).to_csv(
                    index=False
                )

                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="invoice_items.csv",
                    mime="text/csv"
                )
            else:
                st.info("No items available for CSV export.")
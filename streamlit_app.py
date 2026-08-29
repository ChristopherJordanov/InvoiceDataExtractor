import io

import pandas as pd
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
    "Upload one or multiple invoices and automatically extract their information."
)


# File upload
uploaded_files = st.file_uploader(
    "Upload invoices",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
    help="Supported formats: PDF, PNG, JPG and JPEG"
)


if uploaded_files:

    st.success(f"{len(uploaded_files)} invoice(s) uploaded")

    if st.button("Extract invoice data", type="primary"):

        all_invoice_data = []

        # Process invoices
        for index, uploaded_file in enumerate(uploaded_files):

            st.write(
                f"Processing: **{uploaded_file.name}**"
            )

            with st.spinner(
                f"Reading {uploaded_file.name}..."
            ):

                try:
                    text = extract_text(uploaded_file)

                except Exception as e:
                    st.error(
                        f"Error while reading "
                        f"{uploaded_file.name}: {e}"
                    )
                    continue


            # Check extracted text
            if not text.strip():
                st.warning(
                    f"No text could be extracted from "
                    f"{uploaded_file.name}"
                )
                continue


            # AI integration
            with st.spinner(
                f"Analyzing {uploaded_file.name}..."
            ):

                try:
                    invoice_data = extract_invoice_data(text)

                except Exception as e:
                    st.error(
                        f"Error while analyzing "
                        f"{uploaded_file.name}: {e}"
                    )
                    continue


            # Add filename
            invoice_data["filename"] = uploaded_file.name

            all_invoice_data.append(invoice_data)

            st.success(
                f"{uploaded_file.name} processed successfully"
            )


        # Check results
        if not all_invoice_data:
            st.error(
                "No invoices could be processed."
            )
            st.stop()


        st.divider()

        st.subheader("Extracted Data")


        # Create tables
        invoice_rows = []
        item_rows = []
        supplier_rows = []
        customer_rows = []


        for invoice_data in all_invoice_data:

            supplier = invoice_data.get(
                "supplier", {}
            )

            customer = invoice_data.get(
                "customer", {}
            )

            invoice = invoice_data.get(
                "invoice", {}
            )

            totals = invoice_data.get(
                "totals", {}
            )

            filename = invoice_data.get(
                "filename"
            )


            # Invoice row
            invoice_rows.append({
                "File": filename,
                "Invoice Number": invoice.get("number"),
                "Date": invoice.get("date"),
                "Currency": invoice.get("currency"),
                "Subtotal": totals.get("subtotal"),
                "VAT": totals.get("vat"),
                "Total": totals.get("total")
            })


            # Supplier row
            supplier_rows.append({
                "File": filename,
                "Name": supplier.get("name"),
                "EIK / BULSTAT": supplier.get("eik"),
                "VAT Number": supplier.get("vat_number"),
                "Address": supplier.get("address"),
                "IBAN": supplier.get("iban"),
                "BIC": supplier.get("bic")
            })


            # Customer row
            customer_rows.append({
                "File": filename,
                "Name": customer.get("name"),
                "EIK / BULSTAT": customer.get("eik"),
                "VAT Number": customer.get("vat_number"),
                "Address": customer.get("address")
            })


            # Item rows
            for item in invoice_data.get(
                "items", []
            ):

                item_rows.append({
                    "File": filename,
                    "Invoice Number": invoice.get("number"),
                    "Product / Service": item.get(
                        "description"
                    ),
                    "Quantity": item.get(
                        "quantity"
                    ),
                    "Unit Price": item.get(
                        "unit_price"
                    ),
                    "VAT %": item.get(
                        "vat_rate"
                    ),
                    "Total": item.get(
                        "total_price"
                    )
                })


        # Convert to DataFrames
        invoices_df = pd.DataFrame(
            invoice_rows
        )

        items_df = pd.DataFrame(
            item_rows
        )

        suppliers_df = pd.DataFrame(
            supplier_rows
        )

        customers_df = pd.DataFrame(
            customer_rows
        )


        # Display results
        st.subheader("Invoices")

        st.dataframe(
            invoices_df,
            use_container_width=True,
            hide_index=True
        )


        st.subheader("Items")

        if not items_df.empty:

            st.dataframe(
                items_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No invoice items found."
            )


        # Excel export
        st.divider()

        st.subheader("Excel Export")

        excel_file = io.BytesIO()


        with pd.ExcelWriter(
            excel_file,
            engine="openpyxl"
        ) as writer:

            invoices_df.to_excel(
                writer,
                sheet_name="Invoices",
                index=False
            )

            items_df.to_excel(
                writer,
                sheet_name="Items",
                index=False
            )

            suppliers_df.to_excel(
                writer,
                sheet_name="Suppliers",
                index=False
            )

            customers_df.to_excel(
                writer,
                sheet_name="Customers",
                index=False
            )


        excel_file.seek(0)


        st.download_button(
            label="Download Excel",
            data=excel_file,
            file_name="invoice_data.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            type="primary"
        )
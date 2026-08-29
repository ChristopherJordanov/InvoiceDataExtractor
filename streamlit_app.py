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


# Custom styling
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
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


# Helper function
def display_value(value):
    if value is None or value == "":
        return "Not found"

    return value


if uploaded_files:

    st.success(
        f"{len(uploaded_files)} invoice(s) uploaded"
    )


    if st.button(
        "Extract invoice data",
        type="primary"
    ):

        all_invoice_data = []

        progress_bar = st.progress(0)

        status_text = st.empty()


        # Process invoices
        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            status_text.write(
                f"Processing **{uploaded_file.name}**..."
            )

            try:

                # Text extraction
                text = extract_text(
                    uploaded_file
                )

                if not text.strip():

                    st.warning(
                        f"No text could be extracted from "
                        f"{uploaded_file.name}"
                    )

                    continue


                # AI integration
                invoice_data = extract_invoice_data(
                    text
                )


                # Add filename
                invoice_data["filename"] = (
                    uploaded_file.name
                )


                all_invoice_data.append(
                    invoice_data
                )


                progress_bar.progress(
                    (index + 1) / len(uploaded_files)
                )

            except Exception as e:

                st.error(
                    f"Error processing "
                    f"{uploaded_file.name}: {e}"
                )


        status_text.empty()


        # Check results
        if not all_invoice_data:

            st.error(
                "No invoices could be processed."
            )

            st.stop()


        # Processing summary
        processed_count = len(
            all_invoice_data
        )

        failed_count = (
            len(uploaded_files)
            - processed_count
        )


        st.divider()

        st.subheader("Processing Summary")


        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Successfully processed",
                f"{processed_count}/{len(uploaded_files)}"
            )

        with col2:

            st.metric(
                "Failed",
                failed_count
            )


        # Invoice results
        for invoice_data in all_invoice_data:

            filename = invoice_data.get(
                "filename",
                "Unknown file"
            )

            supplier = invoice_data.get(
                "supplier",
                {}
            )

            customer = invoice_data.get(
                "customer",
                {}
            )

            invoice = invoice_data.get(
                "invoice",
                {}
            )

            items = invoice_data.get(
                "items",
                []
            )

            totals = invoice_data.get(
                "totals",
                {}
            )


            # Missing important fields
            missing_fields = []

            if not supplier.get("name"):
                missing_fields.append(
                    "Supplier name"
                )

            if not supplier.get("eik"):
                missing_fields.append(
                    "Supplier EIK / BULSTAT"
                )

            if not supplier.get("iban"):
                missing_fields.append(
                    "Supplier IBAN"
                )

            if not invoice.get("number"):
                missing_fields.append(
                    "Invoice number"
                )

            if not invoice.get("date"):
                missing_fields.append(
                    "Invoice date"
                )

            if not totals.get("total"):
                missing_fields.append(
                    "Total"
                )


            # Invoice header
            st.divider()

            st.subheader(
                f"📄 {filename}"
            )


            # Warning
            if missing_fields:

                st.warning(
                    "Missing information: "
                    + ", ".join(missing_fields)
                )

            else:

                st.success(
                    "All important fields were extracted."
                )


            # Supplier and customer
            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    "### Supplier"
                )

                st.write(
                    "**Name:**",
                    display_value(
                        supplier.get("name")
                    )
                )

                st.write(
                    "**EIK / BULSTAT:**",
                    display_value(
                        supplier.get("eik")
                    )
                )

                st.write(
                    "**VAT Number:**",
                    display_value(
                        supplier.get("vat_number")
                    )
                )

                st.write(
                    "**Address:**",
                    display_value(
                        supplier.get("address")
                    )
                )

                st.write(
                    "**IBAN:**",
                    display_value(
                        supplier.get("iban")
                    )
                )

                st.write(
                    "**BIC:**",
                    display_value(
                        supplier.get("bic")
                    )
                )


            with col2:

                st.markdown(
                    "### Customer"
                )

                st.write(
                    "**Name:**",
                    display_value(
                        customer.get("name")
                    )
                )

                st.write(
                    "**EIK / BULSTAT:**",
                    display_value(
                        customer.get("eik")
                    )
                )

                st.write(
                    "**VAT Number:**",
                    display_value(
                        customer.get("vat_number")
                    )
                )

                st.write(
                    "**Address:**",
                    display_value(
                        customer.get("address")
                    )
                )


            # Invoice information
            st.markdown(
                "### Invoice"
            )


            col1, col2, col3, col4 = st.columns(4)


            with col2:

                st.metric(
                    "Invoice Number",
                    display_value(
                        invoice.get("number")
                    )
                )


            with col3:

                st.metric(
                    "Date",
                    display_value(
                        invoice.get("date")
                    )
                )


            with col4:

                st.metric(
                    "Currency",
                    display_value(
                        invoice.get("currency")
                    )
                )


            # Items
            st.markdown(
                "### Items"
            )


            if items:

                items_table = pd.DataFrame(
                    items
                )

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

                st.info(
                    "No invoice items found."
                )


            # Totals
            st.markdown(
                "### Totals"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Subtotal",
                    display_value(
                        totals.get("subtotal")
                    )
                )


            with col2:

                st.metric(
                    "VAT",
                    display_value(
                        totals.get("vat")
                    )
                )


            with col3:

                st.metric(
                    "Total",
                    display_value(
                        totals.get("total")
                    )
                )


        # Excel export
        st.divider()

        st.subheader(
            "Excel Export"
        )


        invoice_rows = []
        item_rows = []
        supplier_rows = []
        customer_rows = []


        for invoice_data in all_invoice_data:

            filename = invoice_data.get(
                "filename"
            )

            supplier = invoice_data.get(
                "supplier",
                {}
            )

            customer = invoice_data.get(
                "customer",
                {}
            )

            invoice = invoice_data.get(
                "invoice",
                {}
            )

            totals = invoice_data.get(
                "totals",
                {}
            )


            # Invoice row
            invoice_rows.append({
                "File": filename,
                "Invoice Number": invoice.get(
                    "number"
                ),
                "Date": invoice.get(
                    "date"
                ),
                "Due Date": invoice.get(
                    "due_date"
                ),
                "Currency": invoice.get(
                    "currency"
                ),
                "Subtotal": totals.get(
                    "subtotal"
                ),
                "VAT": totals.get(
                    "vat"
                ),
                "Total": totals.get(
                    "total"
                )
            })


            # Supplier row
            supplier_rows.append({
                "File": filename,
                "Name": supplier.get(
                    "name"
                ),
                "EIK / BULSTAT": supplier.get(
                    "eik"
                ),
                "VAT Number": supplier.get(
                    "vat_number"
                ),
                "Address": supplier.get(
                    "address"
                ),
                "IBAN": supplier.get(
                    "iban"
                ),
                "BIC": supplier.get(
                    "bic"
                )
            })


            # Customer row
            customer_rows.append({
                "File": filename,
                "Name": customer.get(
                    "name"
                ),
                "EIK / BULSTAT": customer.get(
                    "eik"
                ),
                "VAT Number": customer.get(
                    "vat_number"
                ),
                "Address": customer.get(
                    "address"
                )
            })


            # Item rows
            for item in invoice_data.get(
                "items",
                []
            ):

                item_rows.append({
                    "File": filename,
                    "Invoice Number": invoice.get(
                        "number"
                    ),
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


        # DataFrames
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

        # Create Excel
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

        # Format Excel
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.worksheet.table import Table, TableStyleInfo

        workbook = writer.book

        for worksheet in workbook.worksheets:

            # Freeze header row
            worksheet.freeze_panes = "A2"

            # Header styling
            for cell in worksheet[1]:
                cell.font = Font(
                    bold=True,
                    color="FFFFFF"
                )

                cell.fill = PatternFill(
                    fill_type="solid",
                    fgColor="2563EB"
                )

                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

            # Automatic column width
            for column in worksheet.columns:

                max_length = 0

                column_letter = column[0].column_letter

                for cell in column:

                    if cell.value is not None:
                        cell_length = len(
                            str(cell.value)
                        )

                        max_length = max(
                            max_length,
                            cell_length
                        )

                worksheet.column_dimensions[
                    column_letter
                ].width = min(
                    max(max_length + 2, 12),
                    50
                )

            # Enable filters
            if worksheet.max_row > 1:

                last_cell = worksheet.cell(
                    row=worksheet.max_row,
                    column=worksheet.max_column
                ).coordinate

                table_reference = f"A1:{last_cell}"

                table = Table(
                    displayName=f"Table{worksheet.title}",
                    ref=table_reference
                )

                style = TableStyleInfo(
                    name="TableStyleMedium2",
                    showFirstColumn=False,
                    showLastColumn=False,
                    showRowStripes=True,
                    showColumnStripes=False
                )

                table.tableStyleInfo = style

                worksheet.add_table(table)

                # Vertical alignment
                for row in worksheet.iter_rows():

                    for cell in row:

                        cell.alignment = Alignment(
                            vertical="center"
                        )

                excel_file.seek(0)


        excel_file.seek(0)


        # Download Excel
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
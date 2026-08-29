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
    "Upload one or multiple invoices and automatically "
    "extract their information."
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

    if isinstance(value, list):
        return "\n".join(str(item) for item in value)

    return value

def normalize_value(value):
    if value is None:
        return None

    if isinstance(value, list):
        return ", ".join(
            str(item) for item in value
        )

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

                # OCR / text extraction
                text = extract_text(
                    uploaded_file
                )

                if not text.strip():

                    st.warning(
                        f"No text could be extracted from "
                        f"{uploaded_file.name}"
                    )

                    progress_bar.progress(
                        (index + 1) / len(uploaded_files)
                    )

                    continue


                # AI integration
                invoice_data = extract_invoice_data(
                    text
                )


                # Add original filename
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

                progress_bar.progress(
                    (index + 1) / len(uploaded_files)
                )


        status_text.empty()


        # Stop if nothing was processed
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


        # Display each invoice
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


            # Find missing important fields
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

            if totals.get("total") is None:
                missing_fields.append(
                    "Total"
                )


            # Invoice section
            st.divider()

            st.subheader(
                f"📄 {filename}"
            )


            # Extraction status
            if missing_fields:

                st.warning(
                    "Missing information: "
                    + ", ".join(missing_fields)
                )

            else:

                st.success(
                    "All important fields were extracted."
                )


            # Supplier / Customer
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


            with col1:

                st.metric(
                    "Invoice Number",
                    display_value(
                        invoice.get("number")
                    )
                )


            with col2:

                st.metric(
                    "Date",
                    display_value(
                        invoice.get("date")
                    )
                )


            with col3:

                st.metric(
                    "Due Date",
                    display_value(
                        invoice.get("due_date")
                    )
                )


            with col4:

                st.metric(
                    "Currency",
                    display_value(
                        invoice.get("currency")
                    )
                )


            # Invoice items
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

        st.subheader("Excel Export")


        def normalize_excel_value(value):
            """Convert lists into readable Excel values."""

            if value is None:
                return ""

            if isinstance(value, list):
                return ", ".join(
                    str(item) for item in value
                )

            return str(value)


        # Create one row per invoice
        excel_rows = []

        for invoice_data in all_invoice_data:

            filename = invoice_data.get(
                "filename",
                ""
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

            items = invoice_data.get(
                "items",
                []
            )

            # Format products
            products = []

            for item in items:

                description = item.get(
                    "description"
                )

                quantity = item.get(
                    "quantity"
                )

                unit_price = item.get(
                    "unit_price"
                )

                total_price = item.get(
                    "total_price"
                )

                product_text = (
                    f"{description or 'Unknown'}"
                )

                if quantity is not None:
                    product_text += (
                        f" | Qty: {quantity}"
                    )

                if unit_price is not None:
                    product_text += (
                        f" | Unit: {unit_price}"
                    )

                if total_price is not None:
                    product_text += (
                        f" | Total: {total_price}"
                    )

                products.append(
                    product_text
                )

            products_text = "\n".join(
                products
            )

            # Create invoice row
            excel_rows.append({

                "File": filename,

                "Invoice Number": normalize_excel_value(
                    invoice.get("number")
                ),

                "Date": normalize_excel_value(
                    invoice.get("date")
                ),

                "Due Date": normalize_excel_value(
                    invoice.get("due_date")
                ),

                "Currency": normalize_excel_value(
                    invoice.get("currency")
                ),

                "Supplier": normalize_excel_value(
                    supplier.get("name")
                ),

                "Supplier EIK / BULSTAT":
                    normalize_excel_value(
                        supplier.get("eik")
                    ),

                "Supplier VAT":
                    normalize_excel_value(
                        supplier.get("vat_number")
                    ),

                "Supplier Address":
                    normalize_excel_value(
                        supplier.get("address")
                    ),

                "IBAN":
                    normalize_excel_value(
                        supplier.get("iban")
                    ),

                "BIC":
                    normalize_excel_value(
                        supplier.get("bic")
                    ),

                "Customer":
                    normalize_excel_value(
                        customer.get("name")
                    ),

                "Customer EIK / BULSTAT":
                    normalize_excel_value(
                        customer.get("eik")
                    ),

                "Customer VAT":
                    normalize_excel_value(
                        customer.get("vat_number")
                    ),

                "Customer Address":
                    normalize_excel_value(
                        customer.get("address")
                    ),

                "Products / Services":
                    products_text,

                "Subtotal":
                    totals.get("subtotal"),

                "VAT":
                    totals.get("vat"),

                "Total":
                    totals.get("total")
            })

        # Create DataFrame
        excel_df = pd.DataFrame(
            excel_rows
        )

        # Create excel file

        excel_file = io.BytesIO()

        from openpyxl.styles import (
            Font,
            PatternFill,
            Alignment,
            Border,
            Side
        )

        from openpyxl.worksheet.table import (
            Table,
            TableStyleInfo
        )

        from openpyxl.utils import (
            get_column_letter
        )

        with pd.ExcelWriter(
                excel_file,
                engine="openpyxl"
        ) as writer:

            excel_df.to_excel(
                writer,
                sheet_name="Invoices",
                index=False
            )

            workbook = writer.book

            worksheet = workbook["Invoices"]

            # styling

            header_fill = PatternFill(
                fill_type="solid",
                fgColor="1F4E78"
            )

            header_font = Font(
                bold=True,
                color="FFFFFF",
                size=11
            )

            header_alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )

            body_alignment = Alignment(
                vertical="top",
                wrap_text=True
            )

            border = Border(
                bottom=Side(
                    style="thin",
                    color="D9E1F2"
                )
            )

            # Freeze first row
            worksheet.freeze_panes = "A2"

            # Hide gridlines
            worksheet.sheet_view.showGridLines = False

            # Header styling
            for cell in worksheet[1]:
                cell.fill = header_fill

                cell.font = header_font

                cell.alignment = header_alignment

            worksheet.row_dimensions[1].height = 30

            # Body styling
            for row in worksheet.iter_rows(
                    min_row=2
            ):

                for cell in row:
                    cell.alignment = body_alignment

                    cell.border = border

            # Column widths

            column_widths = {

                "File": 28,

                "Invoice Number": 22,

                "Date": 14,

                "Due Date": 14,

                "Currency": 12,

                "Supplier": 30,

                "Supplier EIK / BULSTAT": 22,

                "Supplier VAT": 22,

                "Supplier Address": 40,

                "IBAN": 34,

                "BIC": 18,

                "Customer": 30,

                "Customer EIK / BULSTAT": 22,

                "Customer VAT": 22,

                "Customer Address": 40,

                "Products / Services": 55,

                "Subtotal": 16,

                "VAT": 16,

                "Total": 16
            }

            for column_index in range(
                    1,
                    worksheet.max_column + 1
            ):

                header = worksheet.cell(
                    row=1,
                    column=column_index
                ).value

                column_letter = get_column_letter(
                    column_index
                )

                if header in column_widths:
                    worksheet.column_dimensions[
                        column_letter
                    ].width = column_widths[
                        header
                    ]

            # Number formatting

            for row in worksheet.iter_rows(
                    min_row=2
            ):

                for cell in row:

                    header = worksheet.cell(
                        row=1,
                        column=cell.column
                    ).value

                    if header in [
                        "Subtotal",
                        "VAT",
                        "Total"
                    ]:

                        if isinstance(
                                cell.value,
                                (int, float)
                        ):
                            cell.number_format = (
                                '#,##0.00'
                            )

            # Excel table

            if worksheet.max_row > 1:
                last_cell = worksheet.cell(
                    row=worksheet.max_row,
                    column=worksheet.max_column
                ).coordinate

                table = Table(
                    displayName="InvoiceTable",
                    ref=f"A1:{last_cell}"
                )

                table_style = TableStyleInfo(
                    name="TableStyleMedium2",
                    showFirstColumn=False,
                    showLastColumn=False,
                    showRowStripes=True,
                    showColumnStripes=False
                )

                table.tableStyleInfo = table_style

                worksheet.add_table(
                    table
                )

        excel_file.seek(0)


        # Download

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
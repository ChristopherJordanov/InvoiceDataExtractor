<h1 align="center" id="title">Invoice Data Extractor</h1>

<p id="description">An AI-powered Streamlit application that extracts structured information from invoices using OCR and artificial intelligence. Upload one or multiple PDF or image invoices and automatically extract important data such as invoice numbers, supplier and customer details, EIK / BULSTAT, IBAN, BIC, products, prices, VAT and totals, then export everything into a professionally formatted Excel file.</p>

<h2>Demo</h2>

https://extractinvoicedata.streamlit.app

<h2>Features</h2>

Here're some of the project's best features:

* Invoice Upload - Upload single or multiple invoices in PDF, PNG, JPG or JPEG format

* OCR Processing - Extract text from scanned invoices and image files using Tesseract OCR

* AI Data Extraction - Use OpenAI to identify and structure relevant invoice information

* Invoice Information - Extract invoice number, date, due date, currency, supplier, customer, EIK / BULSTAT, VAT number, IBAN and BIC

* Product Extraction - Identify products or services, quantities, unit prices, VAT rates and total prices

* Invoice Validation - Highlight important information that could not be extracted from an invoice

* Multi-Invoice Processing - Process multiple invoices in a single upload and combine their results

* Excel Export - Export all processed invoices into a single professionally formatted Excel spreadsheet with one invoice per row

* Smart Excel Formatting - Automatic column widths, filters, frozen headers, number formatting and structured Excel tables

* Responsive UI - Clean Streamlit interface with organized invoice information and extraction status

* Cloud Deployment - Deployed using Streamlit Community Cloud with secure API key handling

<h2>Built with</h2>

Technologies used in the project:

* Python

* Streamlit

* OpenAI API

* Tesseract OCR

* PyMuPDF

* Pandas

* OpenPyXL

<h2>What I Learned</h2>

* Integrating AI APIs into a Python application

* Extracting text from PDFs and images using OCR

* Processing and structuring unstructured invoice data

* Designing prompts for reliable AI-based data extraction

* Handling inconsistent AI responses and normalizing extracted data

* Processing multiple uploaded files in Streamlit

* Creating and formatting Excel files programmatically with Pandas and OpenPyXL

* Working with environment variables and securely handling API keys

* Building user-friendly interfaces with Streamlit

* Deploying an AI-powered application using Streamlit Community Cloud

from pydantic import BaseModel
from typing import Optional


# Supplier information
class Supplier(BaseModel):
    name: Optional[str] = None
    eik: Optional[str] = None
    vat_number: Optional[str] = None
    address: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None


# Customer information
class Customer(BaseModel):
    name: Optional[str] = None
    eik: Optional[str] = None
    vat_number: Optional[str] = None
    address: Optional[str] = None


# Invoice information
class Invoice(BaseModel):
    number: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[str] = None
    currency: Optional[str] = None


# Invoice totals
class Totals(BaseModel):
    subtotal: Optional[float] = None
    vat: Optional[float] = None
    total: Optional[float] = None


# Complete invoice
class InvoiceData(BaseModel):
    supplier: Supplier
    customer: Customer
    invoice: Invoice
    totals: Totals
from pydantic import BaseModel, field_validator
from typing import Optional


# Supplier information
class Supplier(BaseModel):
    name: Optional[str] = None
    eik: Optional[str] = None
    vat_number: Optional[str] = None
    address: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None

    @field_validator("eik", mode="before")
    @classmethod
    def convert_eik_to_string(cls, value):
        if value is not None:
            return str(value)
        return value


# Customer information
class Customer(BaseModel):
    name: Optional[str] = None
    eik: Optional[str] = None
    vat_number: Optional[str] = None
    address: Optional[str] = None

    @field_validator("eik", mode="before")
    @classmethod
    def convert_eik_to_string(cls, value):
        if value is not None:
            return str(value)
        return value


# Invoice item
class InvoiceItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


# Invoice information
class Invoice(BaseModel):
    number: Optional[str] = None
    date: Optional[str] = None
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
    items: list[InvoiceItem]
    totals: Totals
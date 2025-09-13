from datetime import datetime
from enum import Enum
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field


class AddUserTransactionRequest(BaseModel):
    transaction_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Transaction name",
        example="School supplies"
    )
    transaction_amount: Decimal = Field(
        ...,
        description="Transaction amount",
        example=200.99
    )
    currency_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        description="Three-letter currency code in uppercase (ISO 4217)",
        example="USD"
    )
    category_id: UUID = Field(
        ...,
        description="Category UUID"
    )
    
class CategoryType(str, Enum):
    income = "income"
    expense = "expense"

class RecurringFrequency(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

class AddUserRecurringTransactionRequest(BaseModel):
    transaction_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Transaction name",
        example="Monthly Rent"
    )
    transaction_amount: Decimal = Field(
        ...,
        description="Transaction amount",
        example=1000.00
    )
    currency_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        description="Three-letter currency code in uppercase (ISO 4217)",
        example="USD"
    )
    category_id: UUID = Field(
        ...,
        description="Category UUID"
    )
    frequency: RecurringFrequency = Field(
        ...,
        description="How often the transaction should repeat",
        example="monthly"
    )
    next_due_date: datetime | None = Field(
        None,
        description="When the first transaction should occur. If not provided, starts immediately.",
        example="2024-04-01T00:00:00Z"
    )
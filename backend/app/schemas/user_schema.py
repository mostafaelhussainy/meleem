from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal

class UpdateUserRequest(BaseModel):
    name: str | None = Field(
        None,
        min_length=2,
        max_length=100,
        description="User's full name",
        example="John Doe"
    )
    email: EmailStr | None = Field(
        None,
        description="User's email address",
        example="user@example.com"
    )
    currency_code: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        description="Three-letter currency code in uppercase (ISO 4217)",
        example="USD"
    )
    goal: Decimal | None = Field(
        None,
        description="User's financial goal amount",
        example=1000.00
    )
    savings: Decimal | None = Field(
        None,
        description="User's current savings amount",
        example=500.00
    )
    balance: Decimal | None = Field(
        None,
        description="User's current balance",
        example=100.00
    )

class UpdateUserResponse(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's full name",
        example="John Doe"
    )
    email: EmailStr = Field(
        ...,
        description="User's email address",
        example="user@example.com"
    )
    currency_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        description="Three-letter currency code in uppercase (ISO 4217)",
        example="USD"
    )
    goal: Decimal = Field(
        ...,
        description="User's financial goal amount",
        example=1000.00
    )
    savings: Decimal = Field(
        ...,
        description="User's current savings amount",
        example=500.00
    )
    balance: Decimal = Field(
        ...,
        description="User's current balance",
        example=100.00
    )

class UserDetailsResponse(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's full name",
        example="John Doe"
    )
    email: EmailStr = Field(
        ...,
        description="User's email address",
        example="user@example.com"
    )
    currency_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r'^[A-Z]{3}$',
        description="Three-letter currency code in uppercase (ISO 4217)",
        example="USD"
    )
    goal: Decimal = Field(
        ...,
        description="User's financial goal amount",
        example=1000.00
    )
    savings: Decimal = Field(
        ...,
        description="User's current savings amount",
        example=500.00
    )
    balance: Decimal = Field(
        ...,
        description="User's current balance",
        example=100.00
    )

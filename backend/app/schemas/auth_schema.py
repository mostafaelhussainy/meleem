from pydantic import BaseModel, EmailStr, Field, field_validator
from decimal import Decimal

from ..core.validators import validate_password

class RegisterUserRequest(BaseModel):
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
    password: str = Field(
        ...,
        description="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character, and be at least 8 characters long",
        example="StrongP@ss123"
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

    @field_validator("password")
    def check_password(cls, v: str) -> str:
        return validate_password(v)


class TokenResponse(BaseModel):
    token: str
    token_type: str

class LoginUserRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User's email address",
        example="user@example.com"
    )
    password: str = Field(
        ...,
        description="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character, and be at least 8 characters long",
        example="StrongP@ss123"
    )

    @field_validator("password")
    def check_password(cls, v: str) -> str:
        return validate_password(v)

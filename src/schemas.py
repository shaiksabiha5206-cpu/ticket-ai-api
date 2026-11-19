from pydantic import BaseModel, Field, field_validator
from typing import Literal
import re


class TicketRequest(BaseModel):
    customer_id: str = Field(..., min_length=1, max_length=100)
    subject: str = Field(..., min_length=5, max_length=255)
    message: str = Field(..., min_length=1, max_length=5000)
    urgency: Literal["low", "medium", "high"]
    email: str = Field(..., max_length=254)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        pattern = r"^[A-Za-z0-9._%+-]+@gmail\.com$"
        if not re.fullmatch(pattern, value):
            raise ValueError("EMAIL MUST BE LIKE NAME@GMAIL.COM")
        return value


class TicketResponse(BaseModel):
    ticket_id: str
    category: Literal["billing", "technical", "account"]
    suggested_action: str
    confidence_score: float
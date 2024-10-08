"""Module for Pydantic models."""
from typing import Optional

from pydantic import BaseModel
from pydantic import field_validator

from app import parse_exceptions

class IOUMessage(BaseModel):
    """Pydantic model for IOU messages."""
    conversation_id: int
    sender: str
    recipient: str
    amount: str
    description: Optional[str]

    @field_validator('sender', 'recipient')
    def remove_at_symbol(cls, username):
        """Remove the @ symbol"""
        return username.replace('@', '')

    @field_validator('amount')
    def validate_amount(cls, amount):
        """Validate that the amount is a number and turn it into a float"""
        amount_str = amount.replace('$', '')

        try:
            return float(amount_str)
        except ValueError as e:
            raise parse_exceptions.AmountException('Must be castable to float after removing $') from e

class IOUQuery(BaseModel):
    """Pydantic model for IOU queries."""
    conversation_id: int
    user1: str
    user2: str

    @field_validator('user1', 'user2')
    def remove_at_symbol(cls, username):
        """Remove the @ symbol"""
        return username.replace('@', '')


class IOUResponse(BaseModel):
    conversation_id: int
    user1: str
    user2: str
    amount: float

    @field_validator('amount')
    def round_amount(cls, amount):
        """Round amount to 2 decimal places"""
        return round(amount, 2)

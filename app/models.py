"""Module for Pydantic models."""

from typing import Optional
from pydantic import BaseModel, validator

from app import parse_exceptions

class IOUMessage(BaseModel):
    """Pydantic model for IOU messages."""
    conversation_id: int
    sender: str
    recipient: str
    amount: str
    description: Optional[str]

    @validator('sender', 'recipient')
    def remove_at_symbol(cls, username):
        """Remove the @ symbol"""
        return username.replace('@', '')
    
    @validator('amount')
    def validate_amount(cls, amount):
        """Validate that the amount is a number"""
        amount_str = amount.replace('$', '')

        try:
            _ = float(amount_str)
        except ValueError as e:
            raise parse_exceptions.AmountException('Must be a number') from e
        
        return amount_str


class IOUQuery(BaseModel):
    """Pydantic model for IOU queries."""
    conversation_id: int
    user1: str
    user2: str

    @validator('user1', 'user2')
    def remove_at_symbol(cls, username):
        """Remove the @ symbol"""
        return username.replace('@', '')


class IOUResponse(BaseModel):
    conversation_id: int
    user1: str
    user2: str
    amount: float

    @validator('amount')
    def round_amount(cls, amount):
        """Round amount to 2 decimal places"""        
        return round(amount, 2)
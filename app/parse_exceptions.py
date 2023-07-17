"""Custom exceptions for message parsing."""

class AmountException(Exception):
    """Exception raised when the amount is not a number."""
    pass

class ChatMemberException(Exception):
    """Exception raised when the chat member is not found."""
    pass

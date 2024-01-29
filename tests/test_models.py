import pytest

from app.models import IOUMessage
from app.models import IOUQuery
from app.parse_exceptions import AmountException

def test_iou_message_model():
    message = IOUMessage(
        conversation_id=1,
        sender='@user1',
        recipient='@user2',
        amount='$10.00',
        description='For lunch'
    )
    assert message.conversation_id == 1
    assert message.sender == 'user1'
    assert message.recipient == 'user2'
    assert message.amount == 10.
    assert message.description == 'For lunch'

    # Test validator for sender and recipient
    message = IOUMessage(
        conversation_id=1,
        sender='@@user1',
        recipient='@@user2',
        amount='$10.00',
        description='For lunch'
    )
    assert message.sender == 'user1'
    assert message.recipient == 'user2'

    # Test validator for amount
    with pytest.raises(AmountException):
        message = IOUMessage(
            conversation_id=1,
            sender='@user1',
            recipient='@user2',
            amount='ten dollars',
            description='For lunch'
        )

def test_iou_query_model():
    query = IOUQuery(
        conversation_id=1,
        user1='@user1',
        user2='@user2'
    )
    assert query.conversation_id == 1
    assert query.user1 == 'user1'
    assert query.user2 == 'user2'

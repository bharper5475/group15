import pytest
from pydantic import ValidationError

from ..schemas import orders as schema


def test_order_create_valid():
    """Basic happy-path validation for OrderCreate."""
    payload = schema.OrderCreate(
        customer_id=1,
        order_type="takeout",
        order_items=[
            schema.OrderItemCreate(menu_item_id=1, quantity=2),
            schema.OrderItemCreate(menu_item_id=2, quantity=1),
        ],
    )
    assert payload.order_type == "takeout"
    assert len(payload.order_items) == 2
    assert payload.order_items[0].quantity == 2


def test_order_create_invalid_order_type():
    """order_type other than takeout/delivery should fail validation."""
    with pytest.raises(ValidationError):
        schema.OrderCreate(
            customer_id=1,
            order_type="pickup",  # invalid
            order_items=[schema.OrderItemCreate(menu_item_id=1, quantity=1)],
        )


def test_order_create_requires_items():
    """order_items must not be empty."""
    with pytest.raises(ValidationError):
        schema.OrderCreate(
            customer_id=1,
            order_type="delivery",
            order_items=[],  # invalid
        )


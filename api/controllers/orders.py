from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
import uuid

from ..models import (
    orders as order_model,
    order_details as od_model,
    menu_items as menu_model,
    customers as customer_model,
)
from ..schemas import orders as schema


def _generate_tracking_number() -> str:
    """Generate a short unique-ish tracking number."""
    return "ORD-" + uuid.uuid4().hex[:8].upper()


def create(db: Session, request: schema.OrderCreate):
    """
    Create an order with one or more items.

    Sprint goals covered:
    - Create Order + OrderItem records
    - Auto-generate tracking number
    - Support takeout vs delivery (validated in schema)
    - Basic validation of customer + menu items
    """
    try:
        # 1) Ensure customer exists
        customer = (
            db.query(customer_model.Customer)
            .filter(customer_model.Customer.id == request.customer_id)
            .first()
        )
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer does not exist",
            )

        # 2) Compute total price and validate menu items
        total_price = 0.0
        for item in request.order_items:
            menu_item = (
                db.query(menu_model.MenuItem)
                .filter(
                    menu_model.MenuItem.id == item.menu_item_id,
                    menu_model.MenuItem.is_available == True,
                )
                .first()
            )
            if not menu_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Menu item {item.menu_item_id} not found or unavailable",
                )
            total_price += menu_item.price * item.quantity

        # 3) Generate tracking number
        tracking_number = _generate_tracking_number()

        # 4) Create Order row
        order = order_model.Order(
            tracking_number=tracking_number,
            customer_id=request.customer_id,
            order_type=request.order_type.lower(),  # "takeout" / "delivery"
            total_price=total_price,
            status=order_model.OrderStatus.PENDING,
            # promotion_id / payment_id can stay NULL for this sprint
        )
        db.add(order)
        db.flush()  # assigns order.id

        # 5) Create OrderDetail ("OrderItem") rows
        for item in request.order_items:
            menu_item = (
                db.query(menu_model.MenuItem)
                .filter(menu_model.MenuItem.id == item.menu_item_id)
                .first()
            )
            od = od_model.OrderDetail(
                order_id=order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                item_price=menu_item.price,
            )
            db.add(od)

        # 6) Commit and return
        db.commit()
        db.refresh(order)
        return order

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}",
        )


def read_all(db: Session):
    """Optional: list all orders (useful for debugging/demo)."""
    try:
        return db.query(order_model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}",
        )


def read_one(db: Session, item_id: int):
    """Optional: get a single order by ID."""
    try:
        item = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}",
        )


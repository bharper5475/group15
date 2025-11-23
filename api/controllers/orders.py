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

    - Validates customer exists
    - Validates all menu items exist and are available
    - Automatically computes total_price
    - Auto-generates tracking_number
    - Supports order_type: 'takeout' or 'delivery'
    """
    try:
        # Ensure customer exists (guest or otherwise)
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

        # Compute total price and validate menu items
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

        tracking_number = _generate_tracking_number()

        # Create Order row
        order = order_model.Order(
            tracking_number=tracking_number,
            customer_id=request.customer_id,
            order_type=request.order_type.lower(),
            total_price=total_price,
            status=order_model.OrderStatus.PENDING,
            # promotion_id / payment_id can remain NULL for now
        )
        db.add(order)
        db.flush()  # assign order.id

        # Create OrderDetail rows
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
    """List all orders."""
    try:
        return db.query(order_model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}",
        )


def read_one(db: Session, item_id: int):
    """Get a single order by ID."""
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


def update(db: Session, item_id: int, request: schema.OrderUpdate):
    """
    Update an existing order.

    We allow updating:
    - order_type ('takeout' / 'delivery')
    - status (enum)
    """
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        data = request.dict(exclude_unset=True)
        if "order_type" in data and data["order_type"] is not None:
            order.order_type = data["order_type"].lower()
        if "status" in data and data["status"] is not None:
            order.status = data["status"]

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


def delete(db: Session, item_id: int):
    """
    Delete an order.

    OrderDetails will be deleted as well because of the relationship
    cascade defined on Order.order_details.
    """
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        db.delete(order)
        db.commit()
        # Router returns 204, so we don't need to return a body
        return

    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}",
        )


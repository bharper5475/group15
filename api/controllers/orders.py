from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import uuid
from datetime import datetime

from ..models import (
    orders as order_model,
    order_details as od_model,
    menu_items as menu_model,
    customers as customer_model,
    recipes as recipe_model,
    resources as resource_model,
    promotions as promo_model
)
from ..schemas import orders as schema


def _generate_tracking_number() -> str:
    """Generate a short unique-ish tracking number."""
    return "ORD-" + uuid.uuid4().hex[:8].upper()


def create(db: Session, request: schema.OrderCreate):
    """
    Create an order with one or more items.
    Supports:
    - Registered customer orders
    - Guest checkout (auto-create customer)
    - Promotions
    - Inventory deduction
    """

    try:

        # CUSTOMER OR GUEST CHECKOUT
        if request.customer_id is None:
            # Guest checkout must include guest fields (already validated by schema, but double-check)
            if not (request.guest_name and request.guest_phone and request.guest_address):
                raise HTTPException(
                    status_code=400,
                    detail="Guest checkout requires name, phone, and address"
                )

            # Create a temporary guest customer
            guest = customer_model.Customer(
                name=request.guest_name,
                email=None,
                phone=request.guest_phone,
                address=request.guest_address,
            )
            db.add(guest)
            db.commit()
            db.refresh(guest)

            customer = guest
        else:
            # Registered customer
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

        # Compute total price + ingredient usage
        total_price = 0.0
        ingredient_usage = {}  # resource_id → amount needed

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

            # order total
            total_price += menu_item.price * item.quantity

            # recipe → ingredient usage
            recipes = (
                db.query(recipe_model.Recipe)
                .filter(recipe_model.Recipe.menu_item_id == item.menu_item_id)
                .all()
            )

            for recipe in recipes:
                needed = recipe.required_quantity * item.quantity
                ingredient_usage[recipe.resource_id] = (
                    ingredient_usage.get(recipe.resource_id, 0.0) + needed
                )

        # 3. Promo
        promotion_id = None

        if request.promotion_code:
            promo = (
                db.query(promo_model.Promotion)
                .filter(promo_model.Promotion.code == request.promotion_code)
                .first()
            )

            if not promo:
                raise HTTPException(status_code=400, detail="Invalid promotion code")

            if not promo.is_active:
                raise HTTPException(status_code=400, detail="Promotion code is inactive")

            if promo.expiration_date < datetime.now().date():
                raise HTTPException(status_code=400, detail="Promotion code has expired")

            promotion_id = promo.id
            discount = total_price * (promo.discount_percent / 100)
            total_price -= discount


        # Check inventory + deduct
        for resource_id, needed in ingredient_usage.items():
            ingredient = (
                db.query(resource_model.Resource)
                .filter(resource_model.Resource.id == resource_id)
                .with_for_update()
                .first()
            )

            if not ingredient:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ingredient resource {resource_id} not found"
                )

            if ingredient.quantity_available < needed:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Not enough '{ingredient.name}' in stock. "
                        f"Needed {needed} {ingredient.unit}, "
                        f"available {ingredient.quantity_available} {ingredient.unit}."
                    ),
                )

            ingredient.quantity_available -= needed


        #Create Order
        tracking_number = _generate_tracking_number()
        order = order_model.Order(
            tracking_number=tracking_number,
            customer_id=customer.id,  # Works for registered & guest
            order_type=request.order_type.lower(),
            total_price=total_price,
            status=order_model.OrderStatus.RECEIVED,
            promotion_id=promotion_id,
        )

        db.add(order)
        db.flush()  # assign order.id before adding details

        # ------------------------------------------------------------
        # 6. Create OrderDetail rows
        # ------------------------------------------------------------
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
        raise HTTPException(status_code=400, detail=f"Database error: {error}")


# READ FUNCTIONS
def read_all(db: Session):
    try:
        return db.query(order_model.Order).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__.get("orig", e)))


def read_one(db: Session, item_id: int):
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__.get("orig", e)))


def read_by_tracking_number(db: Session, tracking_number: str):
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.tracking_number == tracking_number)
            .first()
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__.get("orig", e)))


# UPDATE ORDER
def update(db: Session, item_id: int, request: schema.OrderUpdate):
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

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
        raise HTTPException(status_code=400, detail=str(e.__dict__.get("orig", e)))


# DELETE ORDER
def delete(db: Session, item_id: int):
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == item_id)
            .first()
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        db.delete(order)
        db.commit()
        return

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.__dict__.get("orig", e)))


# READ BY DATE RANGE
def read_by_date_range(db: Session, start: str, end: str):
    try:
        orders = (
            db.query(order_model.Order)
            .filter(func.date(order_model.Order.created_at) >= start)
            .filter(func.date(order_model.Order.created_at) <= end)
            .all()
        )
        return orders
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date range")

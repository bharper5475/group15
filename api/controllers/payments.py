import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models.payments import Payment
from api.models.orders import Order, OrderStatus
from api.models.promotions import Promotion
from api.schemas.payments import PaymentCreate


def apply_promotion(order_total: float, promotion: Promotion) -> float:
    """Apply percentage-based discount."""
    if not promotion.is_active:
        return order_total

    discount = (promotion.discount_percent / 100) * order_total
    return max(order_total - discount, 0)


def create(db: Session, request: PaymentCreate, order_id: int):
    # Validate order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    final_amount = order.total_price

    # Apply promotion if exists
    if order.promotion_id:
        promo = db.query(Promotion).filter(Promotion.id == order.promotion_id).first()
        if promo:
            final_amount = apply_promotion(final_amount, promo)

    # Validate amount matches
    if request.amount != final_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect payment amount. Expected {final_amount}",
        )

    transaction_id = uuid.uuid4().hex[:10]

    payment = Payment(
        payment_type=request.payment_type,
        status="Completed",
        amount=request.amount,
        masked_card_last4=request.masked_card_last4,
        transaction_id=transaction_id,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Link payment → order
    order.payment_id = payment.id
    order.status = OrderStatus.COMPLETED
    db.commit()

    return payment


def read_one(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def read_all(db: Session):
    return db.query(Payment).all()


def read_by_order(db: Session, order_id: int):
    """Get the payment for a specific order."""
    from api.models.orders import Order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not order.payment_id:
        raise HTTPException(status_code=404, detail="No payment found for this order")
    return db.query(Payment).filter(Payment.id == order.payment_id).first()


def update(db: Session, payment_id: int, request):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


def delete(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return {"message": f"Payment {payment_id} deleted"}


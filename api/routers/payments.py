from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.dependencies.database import get_db
from api.schemas.payments import PaymentCreate, PaymentRead, PaymentUpdate
from api.controllers import payments as controller

router = APIRouter(
    tags=["Payments"],
    prefix="/payments"
)


@router.get("/", response_model=list[PaymentRead])
def read_all_payments(db: Session = Depends(get_db)):
    return controller.read_all(db=db)


@router.post("/orders/{order_id}", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment_for_order(order_id: int, request: PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request, order_id=order_id)


@router.get("/orders/{order_id}", response_model=PaymentRead)
def read_payment_for_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_by_order(db=db, order_id=order_id)


@router.get("/{payment_id}", response_model=PaymentRead)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, payment_id=payment_id)


@router.put("/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: int, request: PaymentUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, payment_id=payment_id, request=request)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, payment_id=payment_id)


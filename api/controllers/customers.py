from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models.customers import Customer
from api.schemas.customers import CustomerCreate


def create(db: Session, request: CustomerCreate):
    new_customer = Customer(
        name=request.name,
        email=request.email,
        phone=request.phone,
        address=request.address,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def read_all(db: Session):
    return db.query(Customer).all()


def read_one(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def update(db: Session, customer_id: int, request: CustomerCreate):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.name = request.name
    customer.email = request.email
    customer.phone = request.phone
    customer.address = request.address

    db.commit()
    db.refresh(customer)
    return customer


def delete(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": f"Customer {customer_id} deleted"}


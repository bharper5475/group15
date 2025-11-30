from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas.customers import CustomerCreate, CustomerRead
from ..controllers import customers as controller

router = APIRouter(
    tags=["Customers"],
    prefix="/customers"
)


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(request: CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[CustomerRead])
def read_all_customers(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{customer_id}", response_model=CustomerRead)
def read_one_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, customer_id=customer_id)


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, request: CustomerCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, customer_id=customer_id, request=request)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, customer_id=customer_id)


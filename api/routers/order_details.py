from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import order_details as controller
from ..schemas import order_details as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Order Details"],
    prefix="/orderdetails"
)

@router.post("/", response_model=schema.OrderDetailRead, status_code=status.HTTP_201_CREATED)
def create_order_detail(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.OrderDetailRead])
def read_all_order_details(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.OrderDetailRead)
def read_one_order_detail(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.OrderDetailRead)
def update_order_detail(item_id: int, request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_detail(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)


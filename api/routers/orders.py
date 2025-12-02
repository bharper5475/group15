from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Orders"],
    prefix="/orders"
)

@router.post("/", response_model=schema.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.OrderRead])
def read_all_orders(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/tracking/{tracking_number}", response_model=schema.OrderRead)
def read_order_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking_number(db, tracking_number=tracking_number)

@router.get("/range", response_model=list[schema.OrderRead])
def get_orders_by_range(start: str, end: str, db: Session = Depends(get_db)):
    return controller.read_by_date_range(db, start, end)

@router.get("/{item_id}", response_model=schema.OrderRead)
def read_one_order(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.OrderRead)
def update_order(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
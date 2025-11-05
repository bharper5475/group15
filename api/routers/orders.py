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

@router.get("/{item_id}", response_model=schema.OrderRead)
def read_one_order(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.OrderRead)
def update_order(item_id: int, request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)


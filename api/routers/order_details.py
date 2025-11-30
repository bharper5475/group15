from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas.order_details import OrderDetailCreate, OrderDetailRead
from ..controllers import order_details as controller

router = APIRouter(
    tags=["Order Details"],
    prefix="/order_details"
)


@router.post("/", response_model=OrderDetailRead, status_code=status.HTTP_201_CREATED)
def create_order_detail(request: OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[OrderDetailRead])
def read_all_details(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{detail_id}", response_model=OrderDetailRead)
def read_one_detail(detail_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, detail_id=detail_id)


@router.put("/{detail_id}", response_model=OrderDetailRead)
def update_detail(detail_id: int, request: OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, detail_id=detail_id, request=request)


@router.delete("/{detail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_detail(detail_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, detail_id=detail_id)


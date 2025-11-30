from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from api.models.order_details import OrderDetail
from api.schemas.order_details import OrderDetailCreate


def create(db: Session, request: OrderDetailCreate):
    detail = OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=request.quantity,
        item_price=request.item_price,
    )

    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail


def read_all(db: Session):
    return db.query(OrderDetail).all()


def read_one(db: Session, detail_id: int):
    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return detail


def update(db: Session, detail_id: int, request: OrderDetailCreate):
    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")

    detail.menu_item_id = request.menu_item_id
    detail.quantity = request.quantity
    detail.item_price = request.item_price

    db.commit()
    db.refresh(detail)
    return detail


def delete(db: Session, detail_id: int):
    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")

    db.delete(detail)
    db.commit()
    return {"message": f"OrderDetail {detail_id} deleted"}


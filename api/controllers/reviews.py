from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import reviews as model
from ..models import menu_items as menu_model


def create(db: Session, request):

    menu_item = (
        db.query(menu_model.MenuItem)
        .filter(menu_model.MenuItem.id == request.menu_item_id)
        .first()
    )
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found",
        )

    new_review = model.Review(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        rating=request.rating,
        comment=request.comment,
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error
        )

    return new_review


def read_by_menu_item(db: Session, menu_item_id: int):


    menu_item = (
        db.query(menu_model.MenuItem)
        .filter(menu_model.MenuItem.id == menu_item_id)
        .first()
    )
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found",
        )

    try:
        reviews = (
            db.query(model.Review)
            .filter(model.Review.menu_item_id == menu_item_id)
            .all()
        )
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error
        )

    return reviews

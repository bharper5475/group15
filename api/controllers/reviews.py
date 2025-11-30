from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.models.reviews import Review
from api.schemas.reviews import ReviewCreate


def create(db: Session, request: ReviewCreate):
    review = Review(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        rating=request.rating,
        comment=request.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def read_all(db: Session):
    return db.query(Review).all()


def read_one(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


def read_by_menu_item(db: Session, menu_item_id: int):
    return db.query(Review).filter(Review.menu_item_id == menu_item_id).all()


def read_negative(db: Session):
    return db.query(Review).filter(Review.rating <= 2).all()


def update(db: Session, review_id: int, request: ReviewCreate):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.order_id = request.order_id
    review.menu_item_id = request.menu_item_id
    review.rating = request.rating
    review.comment = request.comment

    db.commit()
    db.refresh(review)
    return review


def delete(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": f"Review {review_id} deleted"}


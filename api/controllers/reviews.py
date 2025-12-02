from sqlalchemy.orm import Session
from sqlalchemy import func, case
from fastapi import HTTPException
from api.models.reviews import Review
from api.models.menu_items import MenuItem
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


def popularity_stats(db: Session):
    """
    Returns aggregated popularity + negativity stats per menu item.
    """

    results = (
        db.query(
            Review.menu_item_id,
            MenuItem.name.label("item_name"),
            func.avg(Review.rating).label("avg_rating"),
            func.count(Review.id).label("review_count"),
            func.sum(case((Review.rating <= 2, 1), else_=0)).label("negative_count")
        )
        .join(MenuItem, MenuItem.id == Review.menu_item_id)
        .group_by(Review.menu_item_id, MenuItem.name)
        .all()
    )

    # Convert SQL rows → dict format for router
    formatted = []
    for row in results:
        negative_pct = (
            (row.negative_count / row.review_count) * 100
            if row.review_count > 0 else 0
        )
        formatted.append({
            "menu_item_id": row.menu_item_id,
            "item_name": row.item_name,
            "avg_rating": float(row.avg_rating),
            "review_count": row.review_count,
            "negative_count": int(row.negative_count),
            "negative_percentage": round(negative_pct, 2),
        })

    # Sort by negativity descending
    formatted.sort(key=lambda x: x["negative_percentage"], reverse=True)

    return formatted

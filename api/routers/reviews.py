from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from api.dependencies.database import get_db
from api.schemas.reviews import ReviewCreate, ReviewRead
from api.controllers import reviews as controller

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews"
)


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(request: ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=List[ReviewRead])
def read_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{review_id}", response_model=ReviewRead)
def read_one_review(review_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, review_id)


@router.get("/menu/{menu_item_id}", response_model=List[ReviewRead])
def read_reviews_for_item(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.read_by_menu_item(db, menu_item_id)


@router.get("/negative", response_model=List[ReviewRead])
def read_negative_reviews(db: Session = Depends(get_db)):
    return controller.read_negative(db)


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, request: ReviewCreate, db: Session = Depends(get_db)):
    return controller.update(db, review_id, request)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, review_id)


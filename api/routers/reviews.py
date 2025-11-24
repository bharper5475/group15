from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import reviews as schema
from ..controllers import reviews as controller

router = APIRouter(
    tags=["Reviews"]
)

@router.post(
    "/reviews",
    response_model=schema.ReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    request: schema.ReviewCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new review for a menu item.
    """
    return controller.create(db, request)


@router.get(
    "/menu/{menu_item_id}/reviews",
    response_model=List[schema.ReviewRead],
    status_code=status.HTTP_200_OK,
)
def get_reviews_for_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    return controller.read_by_menu_item(db, menu_item_id)

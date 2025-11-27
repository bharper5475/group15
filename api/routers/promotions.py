from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import promotions as controller
from ..schemas import promotions as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions"
)

@router.post("/", response_model=schema.PromotionRead, status_code=status.HTTP_201_CREATED)
def create_menu_item(request: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)
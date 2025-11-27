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
def create_promotion(request: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.PromotionRead])
def read_all_promotions(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.PromotionRead)
def read_one_promotion(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)
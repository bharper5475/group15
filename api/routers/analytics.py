from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers.analytics import revenue_for_date

router = APIRouter(
    tags=["Analytics"],
    prefix="/analytics"
)

@router.get("/revenue")
def get_revenue(date: str, db: Session = Depends(get_db)):
    return revenue_for_date(db, date)

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from api.models.orders import Order

def revenue_for_date(db: Session, date_str: str):
    try:
        total = (
            db.query(func.sum(Order.total_price))
            .filter(func.date(Order.created_at) == date_str)
            .filter(Order.status != "CANCELLED")
            .scalar()
        )
        return {"date": date_str, "total_revenue": float(total or 0)}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Menu Items"],
    prefix="/menuitems"
)

@router.post("/", response_model=schema.MenuItemRead, status_code=status.HTTP_201_CREATED)
def create_menu_item(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.MenuItemRead])
def read_all_menu_items(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/search", response_model=list[schema.MenuItemRead])
def search_menu_items(category: str | None = None, db: Session = Depends(get_db)):
    return controller.search(db=db, category=category)

@router.get("/{item_id}", response_model=schema.MenuItemRead)
def read_one_menu_item(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.MenuItemRead)
def update_menu_item(item_id: int, request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

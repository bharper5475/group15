from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.controllers import resources as controller
from api.schemas import resources as schema
from api.dependencies.database import get_db

router = APIRouter(
    tags=["Resources"],
    prefix="/resources",
)


@router.post("/", response_model=schema.ResourceRead, status_code=status.HTTP_201_CREATED)
def create_resource(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.ResourceRead])
def read_all_resources(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{resource_id}", response_model=schema.ResourceRead)
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, resource_id=resource_id)


@router.put("/{resource_id}", response_model=schema.ResourceRead)
def update_resource(resource_id: int, request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, resource_id=resource_id)


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, resource_id=resource_id)


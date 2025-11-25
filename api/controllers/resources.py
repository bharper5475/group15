from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import resources as model


def create(db: Session, request):
    new_resource = model.Resource(
        name=request.name,
        quantity_available=request.quantity_available,
        unit=request.unit,
    )

    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
        return new_resource
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__.get("orig", e)),
        )


def read_all(db: Session):
    try:
        return db.query(model.Resource).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__.get("orig", e)),
        )


def read_one(db: Session, resource_id: int):
    resource = (
        db.query(model.Resource)
        .filter(model.Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    return resource


def update(db: Session, request, resource_id: int):
    resource_query = (
        db.query(model.Resource)
        .filter(model.Resource.id == resource_id)
    )

    resource = resource_query.first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    try:
        resource_query.update(
            {
                model.Resource.name: request.name,
                model.Resource.quantity_available: request.quantity_available,
                model.Resource.unit: request.unit,
            },
            synchronize_session=False,
        )
        db.commit()
        return resource_query.first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__.get("orig", e)),
        )


def delete(db: Session, resource_id: int):
    resource_query = (
        db.query(model.Resource)
        .filter(model.Resource.id == resource_id)
    )

    if not resource_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    try:
        resource_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__.get("orig", e)),
        )

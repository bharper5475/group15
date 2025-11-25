from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import recipes as model


def create(db: Session, request):
    """Create a new recipe row (link menu item ↔ ingredient)."""
    new_recipe = model.Recipe(
        menu_item_id=request.menu_item_id,
        resource_id=request.resource_id,
        required_quantity=request.required_quantity,
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except SQLAlchemyError as e:
        db.rollback()
        # handle unique constraint (one ingredient per menu item)
        error_text = str(e.__dict__.get("orig", e))
        if "uq_menuitem_resource" in error_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recipe for this menu item and ingredient already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_text,
        )


def read_all(db: Session):
    """Get all recipes."""
    try:
        return db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__.get("orig", e)),
        )


def read_one(db: Session, recipe_id: int):
    """Get one recipe by id."""
    recipe = (
        db.query(model.Recipe)
        .filter(model.Recipe.id == recipe_id)
        .first()
    )

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    return recipe


def update(db: Session, request, recipe_id: int):
    """Update a recipe row."""
    recipe_query = (
        db.query(model.Recipe)
        .filter(model.Recipe.id == recipe_id)
    )
    recipe = recipe_query.first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    try:
        recipe_query.update(
            {
                model.Recipe.menu_item_id: request.menu_item_id,
                model.Recipe.resource_id: request.resource_id,
                model.Recipe.required_quantity: request.required_quantity,
            },
            synchronize_session=False,
        )
        db.commit()
        return recipe_query.first()
    except SQLAlchemyError as e:
        db.rollback()
        error_text = str(e.__dict__.get("orig", e))
        if "uq_menuitem_resource" in error_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recipe for this menu item and ingredient already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_text,
        )


def delete(db: Session, recipe_id: int):
    """Delete a recipe row."""
    recipe_query = (
        db.query(model.Recipe)
        .filter(model.Recipe.id == recipe_id)
    )

    if not recipe_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    try:
        recipe_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__.get("orig", e)),
        )

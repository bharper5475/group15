from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Recipes"],
    prefix="/recipes",
)


@router.post(
    "/",
    response_model=schema.RecipeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_recipe(
    request: schema.RecipeCreate,
    db: Session = Depends(get_db),
):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.RecipeRead])
def read_all_recipes(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{recipe_id}", response_model=schema.RecipeRead)
def read_one_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    return controller.read_one(db=db, recipe_id=recipe_id)


@router.put("/{recipe_id}", response_model=schema.RecipeRead)
def update_recipe(
    recipe_id: int,
    request: schema.RecipeCreate,
    db: Session = Depends(get_db),
):
    return controller.update(db=db, request=request, recipe_id=recipe_id)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    return controller.delete(db=db, recipe_id=recipe_id)

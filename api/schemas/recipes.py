from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    menu_item_id: int
    resource_id: int
    required_quantity: float


class RecipeCreate(RecipeBase):
    pass


class RecipeRead(RecipeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

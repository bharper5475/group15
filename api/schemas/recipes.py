from pydantic import BaseModel

class RecipeBase(BaseModel):
    menu_item_id: int
    resource_id: int
    required_quantity: float

class RecipeCreate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    id: int
    class Config: from_attributes = True

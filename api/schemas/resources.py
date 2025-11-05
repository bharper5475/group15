from pydantic import BaseModel

class ResourceBase(BaseModel):
    name: str
    quantity_available: float
    unit: str

class ResourceCreate(ResourceBase):
    pass

class ResourceRead(ResourceBase):
    id: int
    class Config: from_attributes = True


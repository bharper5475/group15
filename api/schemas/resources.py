from pydantic import BaseModel, ConfigDict


class ResourceBase(BaseModel):
    name: str
    quantity_available: float
    unit: str


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


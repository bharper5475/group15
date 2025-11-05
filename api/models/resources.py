from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from api.dependencies.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    quantity_available = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)

    recipes = relationship("Recipe", back_populates="resource", cascade="all, delete-orphan")


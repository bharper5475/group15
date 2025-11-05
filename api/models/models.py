from sqlalchemy import (
        Column,
        Integer,
        String,
        Float,
        Boolean,
        ForeignKey,
        DateTime,
        Text,
        Enum,
        Date,
        func,
)
from sqlalchemy.orm import relationship
from api.dependencies import Base
import enum

# ENUMS

class OrderStatus(enum.Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for delivery"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

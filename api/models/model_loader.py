# Ensures all models are imported for SQLAlchemy table creation.

from api.models.customers import Customer
from api.models.menu_items import MenuItem
from api.models.resources import Resource
from api.models.recipes import Recipe
from api.models.promotions import Promotion
from api.models.payments import Payment
from api.models.orders import Order
from api.models.order_details import OrderDetail
from api.models.reviews import Review

def index():
    return "models loaded"


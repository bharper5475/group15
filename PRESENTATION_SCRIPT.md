# SLIME API Presentation Script
## SoftDash Linear Input Maintenance Exporter
### Group 15: Brad, Josias, Kenny, Maddy, Robert

**Total Time: 4-5 minutes**

---

## PART 1: INTRODUCTION (45-60 seconds)
**[Everyone on camera via Zoom]**

### Speaker 1 (Brad - Product Owner):
> "Hi everyone! We're Group 15, and today we're presenting SLIME - the SoftDash Linear Input Maintenance Exporter. This is a full-featured restaurant management API built with FastAPI and Python."

### Speaker 2 (Robert - Scrum Master):
> "Our system manages the complete restaurant workflow - from customers placing orders, to kitchen inventory management, to payment processing and customer feedback."

### Key Features to Mention:
- **10 Resource Modules**: Customers, Menu Items, Orders, Order Details, Payments, Promotions, Recipes, Resources (Inventory), Reviews, and Analytics
- **Full CRUD Operations** on all resources
- **Advanced Features**: Guest checkout, order tracking, promotion codes, inventory deduction, revenue analytics
- **Tech Stack**: FastAPI, SQLAlchemy, MySQL, Pydantic validation

---

## PART 2: LIVE DEMO (2.5-3 minutes)
**[Screen share Swagger UI at http://127.0.0.1:8000/docs]**

### Demo Flow - Follow This Order:

---

### DEMO STEP 1: Show the Swagger Overview (15 sec)
**Swagger Location**: Main `/docs` page

> "Here's our Swagger documentation. You can see all 10 modules organized by tags: Customers, Menu Items, Orders, Payments, Promotions, Recipes, Resources, Reviews, Order Details, and Analytics."

**Point out**: The organized tag structure and how each resource has full CRUD endpoints.

---

### DEMO STEP 2: Customers - Create & View (30 sec)
**Swagger Location**: `Customers` section

1. **GET /customers/** - Show existing customers
2. **POST /customers/** - Create a new customer:
```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "phone": "555-1234",
  "address": "123 Main Street"
}
```

> "Customers are the foundation - they can place orders and leave reviews. We support both registered customers AND guest checkout."

---

### DEMO STEP 3: Menu Items & Recipes (30 sec)
**Swagger Location**: `Menu Items` → `Recipes` → `Resources`

1. **GET /menuitems/** - Show the menu
2. **GET /recipes/** - Show recipes linking menu items to ingredients
3. **GET /resources/** - Show inventory/ingredients

> "Each menu item is linked to recipes, which specify the ingredients needed. When orders are placed, inventory is automatically deducted based on these recipes."

---

### DEMO STEP 4: Place an Order - THE MAIN FEATURE (45 sec)
**Swagger Location**: `Orders` section → **POST /orders/**

**Option A - Registered Customer Order:**
```json
{
  "customer_id": 1,
  "order_type": "delivery",
  "order_items": [
    {"menu_item_id": 1, "quantity": 2},
    {"menu_item_id": 2, "quantity": 1}
  ],
  "promotion_code": null
}
```

**Option B - Guest Checkout (highlight this!):**
```json
{
  "customer_id": null,
  "guest_name": "Walk-in Customer",
  "guest_phone": "555-9999",
  "guest_address": "456 Oak Ave",
  "order_type": "takeout",
  "order_items": [
    {"menu_item_id": 1, "quantity": 1}
  ]
}
```

> "Notice the response includes a **tracking number** like 'ORD-A1B2C3D4'. This allows customers to track their order status. The system also automatically calculates the total price and deducts ingredients from inventory."

**Point out in response:**
- `tracking_number` field
- `status: "RECEIVED"` 
- `total_price` calculated automatically
- `order_details` array with line items

---

### DEMO STEP 5: Order Tracking (20 sec)
**Swagger Location**: `Orders` → **GET /orders/tracking/{tracking_number}**

> "Customers can track their order using just the tracking number - no login required."

Use the tracking number from the previous step to demonstrate.

---

### DEMO STEP 6: Update Order Status (20 sec)
**Swagger Location**: `Orders` → **PUT /orders/{item_id}**

```json
{
  "status": "PREPARING"
}
```

> "Staff can update the order status through the lifecycle: RECEIVED → PENDING → PREPARING → OUT_FOR_DELIVERY → COMPLETED (or CANCELLED)"

---

### DEMO STEP 7: Payments (20 sec)
**Swagger Location**: `Payments` section → **POST /payments/orders/{order_id}**

```json
{
  "payment_method": "credit_card",
  "card_number": "4111111111111111"
}
```

> "Payments are linked to orders. We support multiple payment methods."

---

### DEMO STEP 8: Reviews & Analytics (30 sec)
**Swagger Location**: `Reviews` → `Analytics`

1. **POST /reviews/** - Create a review:
```json
{
  "order_id": 1,
  "menu_item_id": 1,
  "rating": 5,
  "comment": "Excellent food!"
}
```

2. **GET /reviews/negative** - Show negative reviews (rating ≤ 2)
3. **GET /reviews/popularity** - Show popularity stats per menu item
4. **GET /analytics/revenue?date=2025-12-01** - Show daily revenue

> "Reviews help track customer satisfaction. Our analytics endpoints let managers see revenue by date and identify poorly-rated items that need attention."

---

## PART 3: KEY CHALLENGES & LEARNING (45-60 seconds)
**[Back to camera view]**

### Challenge 1: Complex Order Creation
> "The biggest challenge was the order creation logic. It needed to handle registered customers AND guest checkout, validate menu items, apply promotions, calculate totals, AND deduct inventory - all in a single transaction with proper rollback on failure."

### Challenge 2: Database Relationships
> "Managing the relationships between Orders, OrderDetails, Recipes, and Resources required careful foreign key design. We learned how SQLAlchemy's ORM handles these relationships."

### Challenge 3: Missing Config File Issue
> "We encountered module import issues during development - for example, the config file wasn't being recognized. This taught us about Python package structure and relative imports."

### What We Learned:
- **FastAPI** makes building REST APIs fast with automatic Swagger docs
- **Pydantic** validation catches bad input before it hits the database
- **SQLAlchemy ORM** simplifies complex database operations
- **Proper project structure** with controllers/models/schemas/routers keeps code organized

---

## CLOSING (15 seconds)

> "Thank you for watching! Our full code is available in the GitHub repository. Any questions?"

---

# QUICK REFERENCE - Swagger Endpoints to Demo

| Feature | Endpoint | Method |
|---------|----------|--------|
| List Customers | `/customers/` | GET |
| Create Customer | `/customers/` | POST |
| List Menu Items | `/menuitems/` | GET |
| List Recipes | `/recipes/` | GET |
| List Inventory | `/resources/` | GET |
| **Create Order** | `/orders/` | **POST** |
| Track Order | `/orders/tracking/{tracking_number}` | GET |
| Update Order Status | `/orders/{item_id}` | PUT |
| Create Payment | `/payments/orders/{order_id}` | POST |
| Create Review | `/reviews/` | POST |
| Negative Reviews | `/reviews/negative` | GET |
| Popularity Stats | `/reviews/popularity` | GET |
| Revenue Analytics | `/analytics/revenue?date=YYYY-MM-DD` | GET |

---

# TIMING CHECKLIST

- [ ] Introduction: ~1 minute
- [ ] Demo: ~3 minutes  
- [ ] Challenges & Learning: ~1 minute
- [ ] **TOTAL: 4-5 minutes**

**TIP**: Practice the demo flow 2-3 times before recording. Have the JSON payloads ready to copy-paste.


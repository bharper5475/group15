-- SLIME Restaurant API Seed Data
-- This script populates the database with sample data to demonstrate all features

-- ========================================
-- RESOURCES (Ingredients)
-- ========================================
INSERT INTO resources (name, quantity_available, unit) VALUES
('Flour', 50.0, 'kg'),
('Tomato Sauce', 30.0, 'liters'),
('Mozzarella Cheese', 25.0, 'kg'),
('Pepperoni', 15.0, 'kg'),
('Ground Beef', 20.0, 'kg'),
('Lettuce', 10.0, 'kg'),
('Chicken Breast', 25.0, 'kg'),
('Rice', 40.0, 'kg'),
('Black Beans', 15.0, 'kg'),
('Tortilla', 100.0, 'pieces'),
('Olive Oil', 10.0, 'liters'),
('Garlic', 5.0, 'kg'),
('Onion', 10.0, 'kg'),
('Bell Pepper', 8.0, 'kg'),
('Mushrooms', 6.0, 'kg'),
('Tofu', 12.0, 'kg'),
('Soy Sauce', 5.0, 'liters'),
('Pasta', 20.0, 'kg'),
('Parmesan Cheese', 8.0, 'kg'),
('Basil', 2.0, 'kg');

-- ========================================
-- MENU ITEMS
-- ========================================
INSERT INTO menu_items (name, description, price, calories, category, is_available) VALUES
-- Pizzas
('Margherita Pizza', 'Classic pizza with tomato sauce, fresh mozzarella, and basil', 12.99, 850, 'Pizza', 1),
('Pepperoni Pizza', 'Loaded with pepperoni and melted mozzarella cheese', 14.99, 1050, 'Pizza', 1),
('Vegetarian Pizza', 'Bell peppers, mushrooms, onions, and olives on a crispy crust', 13.99, 780, 'Pizza,Vegetarian', 1),

-- Main Dishes
('Grilled Chicken Plate', 'Seasoned grilled chicken breast with rice and vegetables', 15.99, 650, 'Main,Healthy', 1),
('Beef Burrito', 'Large flour tortilla stuffed with seasoned beef, rice, beans, and cheese', 11.99, 920, 'Main,Mexican', 1),
('Chicken Burrito', 'Grilled chicken with rice, black beans, and fresh salsa', 11.99, 850, 'Main,Mexican', 1),
('Spaghetti Bolognese', 'Classic Italian pasta with rich meat sauce', 13.99, 780, 'Main,Italian', 1),
('Fettuccine Alfredo', 'Creamy parmesan sauce over fresh pasta', 12.99, 890, 'Main,Italian', 1),

-- Vegetarian Options
('Tofu Stir Fry', 'Crispy tofu with mixed vegetables in savory soy sauce', 10.99, 450, 'Main,Vegetarian,Healthy', 1),
('Veggie Rice Bowl', 'Seasoned rice topped with grilled vegetables and tofu', 9.99, 520, 'Main,Vegetarian,Healthy', 1),
('Garden Salad', 'Fresh mixed greens with cherry tomatoes and house dressing', 7.99, 180, 'Salad,Vegetarian,Healthy', 1),
('Caesar Salad', 'Crisp romaine lettuce with parmesan and caesar dressing', 8.99, 320, 'Salad,Vegetarian', 1),

-- Sides
('Garlic Bread', 'Toasted bread with garlic butter and herbs', 4.99, 280, 'Side', 1),
('French Fries', 'Crispy golden fries with sea salt', 3.99, 380, 'Side', 1),
('Rice and Beans', 'Traditional seasoned rice with black beans', 4.99, 350, 'Side,Vegetarian', 1),

-- Unavailable item for testing
('Seasonal Special', 'Limited time seasonal dish', 16.99, 700, 'Special', 0);

-- ========================================
-- RECIPES (Menu Item to Ingredient mappings)
-- ========================================
-- Margherita Pizza (menu_item_id = 1)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(1, 1, 0.3),   -- Flour
(1, 2, 0.15), -- Tomato Sauce
(1, 3, 0.2),  -- Mozzarella
(1, 20, 0.02); -- Basil

-- Pepperoni Pizza (menu_item_id = 2)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(2, 1, 0.3),   -- Flour
(2, 2, 0.15), -- Tomato Sauce
(2, 3, 0.2),  -- Mozzarella
(2, 4, 0.15); -- Pepperoni

-- Vegetarian Pizza (menu_item_id = 3)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(3, 1, 0.3),   -- Flour
(3, 2, 0.15), -- Tomato Sauce
(3, 3, 0.2),  -- Mozzarella
(3, 14, 0.1), -- Bell Pepper
(3, 15, 0.1), -- Mushrooms
(3, 13, 0.05); -- Onion

-- Grilled Chicken Plate (menu_item_id = 4)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(4, 7, 0.25), -- Chicken Breast
(4, 8, 0.15), -- Rice
(4, 11, 0.02); -- Olive Oil

-- Beef Burrito (menu_item_id = 5)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(5, 5, 0.2),  -- Ground Beef
(5, 10, 1),   -- Tortilla
(5, 8, 0.1),  -- Rice
(5, 9, 0.1),  -- Black Beans
(5, 3, 0.05); -- Mozzarella

-- Chicken Burrito (menu_item_id = 6)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(6, 7, 0.2),  -- Chicken
(6, 10, 1),   -- Tortilla
(6, 8, 0.1),  -- Rice
(6, 9, 0.1); -- Black Beans

-- Spaghetti Bolognese (menu_item_id = 7)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(7, 18, 0.2), -- Pasta
(7, 5, 0.15), -- Ground Beef
(7, 2, 0.15), -- Tomato Sauce
(7, 12, 0.02); -- Garlic

-- Fettuccine Alfredo (menu_item_id = 8)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(8, 18, 0.2), -- Pasta
(8, 19, 0.1), -- Parmesan
(8, 12, 0.02); -- Garlic

-- Tofu Stir Fry (menu_item_id = 9)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(9, 16, 0.2),  -- Tofu
(9, 17, 0.03), -- Soy Sauce
(9, 14, 0.1),  -- Bell Pepper
(9, 13, 0.05); -- Onion

-- Veggie Rice Bowl (menu_item_id = 10)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(10, 8, 0.15),  -- Rice
(10, 16, 0.15), -- Tofu
(10, 14, 0.1),  -- Bell Pepper
(10, 15, 0.08); -- Mushrooms

-- Garden Salad (menu_item_id = 11)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(11, 6, 0.15); -- Lettuce

-- Caesar Salad (menu_item_id = 12)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(12, 6, 0.15),  -- Lettuce
(12, 19, 0.03); -- Parmesan

-- Garlic Bread (menu_item_id = 13)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(13, 1, 0.1),  -- Flour
(13, 12, 0.02); -- Garlic

-- Rice and Beans (menu_item_id = 15)
INSERT INTO recipes (menu_item_id, resource_id, required_quantity) VALUES
(15, 8, 0.15), -- Rice
(15, 9, 0.1);  -- Black Beans

-- ========================================
-- PROMOTIONS
-- ========================================
INSERT INTO promotions (code, discount_percent, expiration_date, is_active) VALUES
('WELCOME10', 10.0, '2025-12-31', 1),
('SUMMER20', 20.0, '2025-08-31', 1),
('HOLIDAY15', 15.0, '2025-12-25', 1),
('VIP25', 25.0, '2025-06-30', 1),
('EXPIRED50', 50.0, '2024-01-01', 0),
('INACTIVE30', 30.0, '2025-12-31', 0);

-- ========================================
-- CUSTOMERS
-- ========================================
INSERT INTO customers (name, email, phone, address) VALUES
('John Smith', 'john.smith@email.com', '704-555-0101', '123 Main Street, Charlotte, NC 28202'),
('Sarah Johnson', 'sarah.j@email.com', '704-555-0102', '456 Oak Avenue, Charlotte, NC 28203'),
('Michael Brown', 'mbrown@email.com', '704-555-0103', '789 Pine Road, Charlotte, NC 28204'),
('Emily Davis', 'emily.d@email.com', '704-555-0104', '321 Elm Street, Charlotte, NC 28205'),
('David Wilson', 'dwilson@email.com', '704-555-0105', '654 Maple Lane, Charlotte, NC 28206'),
('Jessica Martinez', 'jmartinez@email.com', '704-555-0106', '987 Cedar Drive, Charlotte, NC 28207'),
('Christopher Lee', 'clee@email.com', '704-555-0107', '147 Birch Court, Charlotte, NC 28208'),
('Amanda Garcia', 'agarcia@email.com', '704-555-0108', '258 Walnut Way, Charlotte, NC 28209'),
('Guest User', NULL, '704-555-9999', '100 Guest Lane, Charlotte, NC 28210'),
('Regular Customer', 'regular@email.com', '704-555-0110', '200 Loyal Street, Charlotte, NC 28211');

-- ========================================
-- PAYMENTS
-- ========================================
INSERT INTO payments (payment_type, status, masked_card_last4, transaction_id, amount) VALUES
('Credit Card', 'Completed', '4242', 'txn_abc12345', 27.98),
('Credit Card', 'Completed', '1234', 'txn_def67890', 15.99),
('Debit Card', 'Completed', '5678', 'txn_ghi11223', 25.98),
('Credit Card', 'Completed', '9012', 'txn_jkl44556', 44.97),
('Credit Card', 'Completed', '3456', 'txn_mno77889', 11.99),
('Debit Card', 'Completed', '7890', 'txn_pqr00112', 35.97),
('Credit Card', 'Completed', '2345', 'txn_stu33445', 21.98);

-- ========================================
-- ORDERS
-- ========================================
-- Completed orders (various dates for revenue testing)
INSERT INTO orders (tracking_number, customer_id, promotion_id, payment_id, order_type, total_price, status, created_at) VALUES
('ORD-A1B2C3D4', 1, NULL, 1, 'delivery', 27.98, 'COMPLETED', '2025-11-28 12:30:00'),
('ORD-E5F6G7H8', 2, NULL, 2, 'takeout', 15.99, 'COMPLETED', '2025-11-28 14:15:00'),
('ORD-I9J0K1L2', 3, 1, 3, 'delivery', 25.98, 'COMPLETED', '2025-11-29 11:00:00'),
('ORD-M3N4O5P6', 4, NULL, 4, 'takeout', 44.97, 'COMPLETED', '2025-11-29 18:45:00'),
('ORD-Q7R8S9T0', 5, 2, 5, 'delivery', 11.99, 'COMPLETED', '2025-11-30 13:20:00'),
('ORD-U1V2W3X4', 6, NULL, 6, 'takeout', 35.97, 'COMPLETED', '2025-11-30 19:00:00'),
('ORD-Y5Z6A7B8', 7, NULL, 7, 'delivery', 21.98, 'COMPLETED', '2025-11-30 20:30:00');

-- Orders in various statuses (for tracking demonstration)
INSERT INTO orders (tracking_number, customer_id, promotion_id, payment_id, order_type, total_price, status, created_at) VALUES
('ORD-TRACK001', 8, NULL, NULL, 'delivery', 26.98, 'RECEIVED', NOW()),
('ORD-TRACK002', 9, 3, NULL, 'takeout', 22.99, 'PREPARING', NOW()),
('ORD-TRACK003', 10, NULL, NULL, 'delivery', 31.97, 'OUT_FOR_DELIVERY', NOW()),
('ORD-CANCEL01', 1, NULL, NULL, 'takeout', 12.99, 'CANCELLED', '2025-11-25 10:00:00');

-- ========================================
-- ORDER DETAILS
-- ========================================
-- Order 1 (ORD-A1B2C3D4): Margherita + Garlic Bread
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(1, 1, 2, 12.99),
(1, 13, 1, 4.99);

-- Order 2 (ORD-E5F6G7H8): Grilled Chicken
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(2, 4, 1, 15.99);

-- Order 3 (ORD-I9J0K1L2): Pepperoni Pizza
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(3, 2, 2, 14.99);

-- Order 4 (ORD-M3N4O5P6): Multiple items
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(4, 7, 2, 13.99),
(4, 11, 1, 7.99),
(4, 13, 2, 4.99);

-- Order 5 (ORD-Q7R8S9T0): Burrito
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(5, 5, 1, 11.99);

-- Order 6 (ORD-U1V2W3X4): Vegetarian order
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(6, 3, 1, 13.99),
(6, 9, 1, 10.99),
(6, 10, 1, 9.99);

-- Order 7 (ORD-Y5Z6A7B8): Pasta
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(7, 8, 1, 12.99),
(7, 12, 1, 8.99);

-- Order 8 (ORD-TRACK001): For tracking demo
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(8, 2, 1, 14.99),
(8, 6, 1, 11.99);

-- Order 9 (ORD-TRACK002): For tracking demo
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(9, 4, 1, 15.99),
(9, 11, 1, 7.99);

-- Order 10 (ORD-TRACK003): For tracking demo
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(10, 7, 1, 13.99),
(10, 8, 1, 12.99),
(10, 13, 1, 4.99);

-- Order 11 (Cancelled): 
INSERT INTO order_details (order_id, menu_item_id, quantity, item_price) VALUES
(11, 1, 1, 12.99);

-- ========================================
-- REVIEWS (Including negative reviews for complaint tracking)
-- ========================================
INSERT INTO reviews (order_id, menu_item_id, rating, comment, created_at) VALUES
-- Positive reviews
(1, 1, 5, 'Amazing pizza! The crust was perfect and toppings were fresh. Will definitely order again!', '2025-11-28 14:00:00'),
(2, 4, 4, 'Chicken was well seasoned and juicy. Good portion size.', '2025-11-28 16:30:00'),
(3, 2, 5, 'Best pepperoni pizza in town! Delivery was fast too.', '2025-11-29 13:00:00'),
(4, 7, 5, 'Authentic Italian taste. The bolognese sauce is incredible!', '2025-11-29 20:00:00'),

-- Mixed/Moderate reviews
(5, 5, 3, 'Burrito was okay but a bit small for the price. Taste was good though.', '2025-11-30 15:00:00'),

-- Negative reviews (for complaint tracking feature)
(6, 3, 2, 'Vegetarian pizza was undercooked. The crust was too doughy and vegetables were not fresh. Disappointed.', '2025-11-30 21:00:00'),
(7, 8, 1, 'Terrible experience. Pasta was overcooked and the alfredo sauce was bland. Would not recommend. Had to wait 45 minutes for delivery too.', '2025-11-30 22:00:00');

-- ========================================
-- End of Seed Data
-- ========================================


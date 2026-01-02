# Data Architecture

## Database Schema Design

### Overview
This platform uses a **relational database** (PostgreSQL/MySQL) with normalized tables to store business transaction data.

---

## Tables & Schema

### 1. `customers` Table
Stores customer information.

| Column Name    | Data Type    | Constraints          | Description                    |
|----------------|--------------|----------------------|--------------------------------|
| customer_id    | INT          | PRIMARY KEY, AUTO    | Unique customer identifier     |
| first_name     | VARCHAR(50)  | NOT NULL             | Customer first name            |
| last_name      | VARCHAR(50)  | NOT NULL             | Customer last name             |
| email          | VARCHAR(100) | UNIQUE, NOT NULL     | Customer email address         |
| phone          | VARCHAR(20)  | NULL                 | Contact number                 |
| city           | VARCHAR(50)  | NULL                 | Customer city                  |
| state          | VARCHAR(50)  | NULL                 | Customer state                 |
| country        | VARCHAR(50)  | DEFAULT 'India'      | Customer country               |
| created_at     | TIMESTAMP    | DEFAULT CURRENT_TIME | Account creation date          |

---

### 2. `products` Table
Stores product catalog information.

| Column Name    | Data Type     | Constraints          | Description                    |
|----------------|---------------|----------------------|--------------------------------|
| product_id     | INT           | PRIMARY KEY, AUTO    | Unique product identifier      |
| product_name   | VARCHAR(100)  | NOT NULL             | Product name                   |
| category       | VARCHAR(50)   | NOT NULL             | Product category               |
| price          | DECIMAL(10,2) | NOT NULL, CHECK > 0  | Product price (INR)            |
| stock_quantity | INT           | DEFAULT 0            | Available inventory            |
| created_at     | TIMESTAMP     | DEFAULT CURRENT_TIME | Product added date             |

---

### 3. `orders` Table
Stores order header information.

| Column Name    | Data Type     | Constraints              | Description                    |
|----------------|---------------|--------------------------|--------------------------------|
| order_id       | INT           | PRIMARY KEY, AUTO        | Unique order identifier        |
| customer_id    | INT           | FOREIGN KEY → customers  | Links to customer              |
| order_date     | DATE          | NOT NULL                 | Date order was placed          |
| order_status   | VARCHAR(20)   | DEFAULT 'Pending'        | Status: Pending/Completed/Cancelled |
| total_amount   | DECIMAL(10,2) | NOT NULL                 | Total order value (INR)        |
| created_at     | TIMESTAMP     | DEFAULT CURRENT_TIME     | Order creation timestamp       |

---

### 4. `order_items` Table
Stores individual line items for each order.

| Column Name    | Data Type     | Constraints              | Description                    |
|----------------|---------------|--------------------------|--------------------------------|
| order_item_id  | INT           | PRIMARY KEY, AUTO        | Unique line item identifier    |
| order_id       | INT           | FOREIGN KEY → orders     | Links to order                 |
| product_id     | INT           | FOREIGN KEY → products   | Links to product               |
| quantity       | INT           | NOT NULL, CHECK > 0      | Number of units ordered        |
| price_per_unit | DECIMAL(10,2) | NOT NULL                 | Price at time of order         |
| line_total     | DECIMAL(10,2) | COMPUTED (qty × price)   | Total for this line item       |

---

## Entity Relationship Diagram (ERD)
```
┌─────────────┐
│  customers  │
└──────┬──────┘
       │
       │ 1:N
       │
┌──────▼──────┐       ┌──────────────┐
│   orders    │──N:1──│ order_items  │
└─────────────┘       └──────┬───────┘
                             │
                             │ N:1
                             │
                      ┌──────▼──────┐
                      │  products   │
                      └─────────────┘
```

**Relationships:**
- 1 Customer → Many Orders (1:N)
- 1 Order → Many Order Items (1:N)
- 1 Product → Many Order Items (1:N)

---

## Data Quality Considerations

### Validation Rules:
- Email must be unique and valid format
- Phone numbers standardized to 10 digits
- Prices must be positive values
- Order dates cannot be in future
- Stock quantity cannot be negative

### Data Integrity:
- Foreign key constraints enforce referential integrity
- Cascading deletes where appropriate
- Transaction handling for multi-table operations

---

## Indexing Strategy

**Primary Indexes:**
- customer_id, product_id, order_id (automatic on PRIMARY KEY)

**Secondary Indexes (for query performance):**
- customers.email (for login lookups)
- orders.order_date (for date range queries)
- order_items.order_id (for order detail lookups)
- products.category (for category filtering)

---

*This schema follows database normalization principles (3NF) to minimize redundancy while maintaining query performance.*
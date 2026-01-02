# Data Quality Plan

## Overview

Real-world data is messy. This document outlines the data quality issues identified in our raw datasets and the validation/cleaning strategies to address them.

---

## Identified Data Quality Issues

### 1. **customers** Dataset Issues

| Issue Type          | Description                           | Example                              | Impact                    |
|---------------------|---------------------------------------|--------------------------------------|---------------------------|
| Duplicate Records   | Same customer_id appears multiple times | customer_id 1 appears twice        | Inflates customer count   |
| Missing Values      | NULL/empty values in important fields | Missing phone, missing email        | Incomplete customer profile|
| Invalid Format      | Email doesn't match valid pattern     | "sanjay@invalid" (no domain)        | Cannot contact customer   |
| Invalid Format      | Phone number too short/long           | "98765" (only 5 digits)             | Cannot contact customer   |

**Validation Rules:**
- ✅ customer_id must be unique
- ✅ first_name, last_name cannot be empty
- ✅ email must match pattern: `*@*.*`
- ✅ phone must be 10 digits (Indian standard)
- ✅ Remove exact duplicate rows

---

### 2. **products** Dataset Issues

| Issue Type          | Description                           | Example                              | Impact                    |
|---------------------|---------------------------------------|--------------------------------------|---------------------------|
| Missing Values      | Critical fields are NULL              | Missing price, missing product_name | Cannot sell product       |
| Invalid Values      | Negative or zero prices               | price = -500.00                     | Business logic error      |
| Invalid Values      | Negative stock quantity               | stock = -10                         | Inventory tracking broken |

**Validation Rules:**
- ✅ product_id must be unique
- ✅ product_name cannot be empty
- ✅ price must be > 0
- ✅ stock_quantity must be >= 0
- ✅ category cannot be empty

---

### 3. **orders** Dataset Issues

| Issue Type          | Description                           | Example                              | Impact                    |
|---------------------|---------------------------------------|--------------------------------------|---------------------------|
| Orphaned Records    | customer_id doesn't exist in customers| customer_id = 99                    | Referential integrity broken |
| Missing Values      | Critical fields NULL                  | Missing order_date                  | Cannot analyze trends     |
| Invalid Dates       | Future dates or impossible dates      | order_date = 2026-12-31             | Data quality issue        |
| Invalid Status      | Status not in allowed values          | "Invalid Status"                    | Reporting broken          |

**Validation Rules:**
- ✅ order_id must be unique
- ✅ customer_id must exist in customers table
- ✅ order_date cannot be NULL or in future
- ✅ order_status must be in: ['Pending', 'Completed', 'Cancelled']
- ✅ total_amount must be > 0

---

### 4. **order_items** Dataset Issues

| Issue Type          | Description                           | Example                              | Impact                    |
|---------------------|---------------------------------------|--------------------------------------|---------------------------|
| Orphaned Records    | order_id or product_id doesn't exist  | order_id = 9999                     | Referential integrity broken |
| Missing Values      | NULL price or quantity                | Missing price_per_unit              | Cannot calculate revenue  |
| Invalid Values      | Negative quantity                     | quantity = -3                       | Business logic error      |

**Validation Rules:**
- ✅ order_item_id must be unique
- ✅ order_id must exist in orders table
- ✅ product_id must exist in products table
- ✅ quantity must be > 0
- ✅ price_per_unit must be > 0

---

## Data Cleaning Strategy

### Phase 1: Validation & Logging
1. Read raw CSV files
2. Run validation checks on each row
3. Log all errors with row numbers and issue types
4. Generate validation report

### Phase 2: Cleaning & Transformation
1. Remove exact duplicate rows
2. Handle missing values:
   - **Critical fields:** Drop rows with missing values
   - **Optional fields:** Fill with default values or NULL
3. Fix formatting issues:
   - Standardize phone numbers (remove spaces/hyphens)
   - Validate email format
   - Trim whitespace
4. Remove invalid records:
   - Negative prices/quantities
   - Future dates
   - Invalid status values
   - Orphaned foreign keys

### Phase 3: Output Clean Data
1. Save cleaned data to separate files: `cleaned_customers.csv`, etc.
2. Generate cleaning summary report:
   - Total rows processed
   - Rows removed (with reasons)
   - Rows modified
   - Final clean row count

---

## Success Metrics

**Data Quality KPIs:**
- Zero duplicate records
- Zero orphaned foreign keys
- 100% valid email/phone formats
- 100% positive prices and quantities
- All dates within valid range

**Expected Results:**
- Customers: ~13-14 valid records (from 15 raw)
- Products: ~13-14 valid records (from 15 raw)
- Orders: ~12-13 valid records (from 14 raw)
- Order Items: ~12-13 valid records (from 14 raw)

---

## Implementation Plan

**Module Structure:**
```
src/
└── cleaning/
    ├── __init__.py
    ├── validators.py      # Validation functions
    ├── cleaners.py        # Cleaning functions
    └── main.py            # Orchestration
```

**Next Steps:**
1. Build validation functions (check email, phone, dates, etc.)
2. Build cleaning functions (remove duplicates, fix formats)
3. Create main pipeline script
4. Test with raw data
5. Generate cleaning report

---

*This plan follows industry best practices for data quality management in analytics pipelines.*
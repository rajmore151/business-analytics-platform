# Business Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **End-to-end data analytics platform demonstrating production-grade data engineering practices, SQL analytics, and business intelligence workflows.**

---

## 📊 Project Overview

A comprehensive analytics system built to process, clean, and analyze e-commerce business data. This platform solves real-world data quality challenges and generates actionable business insights through automated pipelines and SQL analytics.

**Built by:** [Raj Sudhir More](https://github.com/rajmore151) | EXTC Engineering Student  
**Tech Stack:** Python, SQL (SQLite), Pandas, Data Quality Engineering

---

## 🎯 Problem Statement

Modern businesses struggle with:
- ❌ Messy, inconsistent data (duplicates, missing values, invalid formats)
- ❌ Manual data processing (time-consuming, error-prone)
- ❌ Delayed insights (no automated reporting)
- ❌ Poor data quality (breaks analytics and decisions)

**This platform solves these challenges with automated data pipelines and quality controls.**

---

## ✨ Key Features

### 🔄 **Data Ingestion Pipeline**
- Automated CSV data loading with validation
- Schema verification and error logging
- Comprehensive data quality checks
- Handles 4 interconnected datasets (customers, products, orders, order items)

### 🧹 **Data Cleaning System**
- **Removes:** Duplicates, invalid records, orphaned foreign keys
- **Validates:** Email formats, phone numbers, prices, quantities, dates
- **Enforces:** Referential integrity across tables
- **Logs:** Every cleaning action with detailed reports

### 📈 **SQL Analytics Engine**
- Revenue analytics (total, daily, trends)
- Customer insights (top customers, lifetime value, segmentation)
- Product performance (best sellers, category analysis, inventory alerts)
- Order analytics (status summary, patterns)
- Advanced insights (RFM segmentation, cross-sell analysis)

### 📊 **Automated Reporting**
- Business intelligence reports
- Data quality summaries
- Validation error reports
- Cleaned datasets ready for analysis

---

## 🏗️ Architecture
```
Raw Data → Ingestion & Validation → Data Cleaning → SQL Database → Analytics → Business Insights
```

**Data Flow:**
1. **Load** raw CSV files with quality issues
2. **Validate** schema, data types, and business rules
3. **Clean** bad records while logging all actions
4. **Store** cleaned data in SQL database
5. **Analyze** using SQL queries
6. **Generate** automated business reports

---

## 📁 Project Structure
```
business-analytics-platform/
│
├── data/                           # Data directory
│   ├── raw_customers.csv           # Raw customer data (16 rows)
│   ├── raw_products.csv            # Raw product catalog (15 rows)
│   ├── raw_orders.csv              # Raw order records (14 rows)
│   ├── raw_order_items.csv         # Raw order line items (14 rows)
│   └── cleaned/                    # Cleaned data outputs
│       ├── cleaned_customers.csv   # (15 rows, 6.2% cleaned)
│       ├── cleaned_products.csv    # (12 rows, 20% cleaned)
│       ├── cleaned_orders.csv      # (11 rows, 21.4% cleaned)
│       ├── cleaned_order_items.csv # (11 rows, 21.4% cleaned)
│       ├── validation_errors.csv   # Detailed error log
│       └── cleaning_summary.csv    # Cleaning actions log
│
├── src/ingestion/                  # Core Python modules
│   ├── data_loader.py              # CSV ingestion with validation
│   ├── validators.py               # Data quality validation functions
│   ├── data_cleaner.py             # Data cleaning transformations
│   ├── cleaning_pipeline.py        # Orchestrates cleaning workflow
│   └── sql_analytics.py            # SQL analytics engine
│
├── sql/                            # SQL queries
│   └── analytics_queries.sql       # 15+ business analytics queries
│
├── docs/                           # Documentation
│   ├── problem_definition.md       # Business context & goals
│   ├── data_architecture.md        # Database schema & ERD
│   └── data_quality_plan.md        # Quality strategy & rules
│
├── tests/                          # Test scripts
│   ├── test_ingestion.py           # Test data loading
│   ├── test_cleaning.py            # Test cleaning pipeline
│   └── test_analytics.py           # Test SQL analytics
│
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── LICENSE                         # MIT License
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Clone repository
git clone https://github.com/rajmore151/business-analytics-platform.git
cd business-analytics-platform

# Install dependencies
pip install -r requirements.txt
```

### Run the Complete Pipeline
```bash
# Step 1: Test data ingestion
python test_ingestion.py

# Step 2: Run data cleaning pipeline
python test_cleaning.py

# Step 3: Generate analytics report
python test_analytics.py
```

---

## 📊 Sample Analytics Output

### Revenue Insights
- **Total Revenue:** ₹286,492
- **Completed Orders:** 8
- **Average Order Value:** ₹35,811.50
- **Peak Revenue Day:** January 1, 2025 (₹112,998)

### Customer Insights
- **Top Customer:** Arjun Reddy (₹89,999 lifetime value)
- **Highest Revenue City:** Bangalore (₹135,998)
- **Active Customers:** 15 across 9 cities

### Product Insights
- **Best Seller:** Apple iPhone 14 (₹89,999 revenue)
- **Top Category:** Electronics (98% of revenue)
- **Low Stock Alert:** 3 products below threshold

---

## 🎓 What This Project Demonstrates

### Technical Skills
✅ **Python Programming** - OOP, modules, error handling  
✅ **SQL Analytics** - Joins, aggregations, window functions  
✅ **Data Quality Engineering** - Validation, cleaning, integrity  
✅ **ETL Pipeline Design** - Extract, transform, load workflows  
✅ **Software Engineering** - Modular code, testing, documentation  

### Professional Practices
✅ **Clean Code** - Well-organized, readable, maintainable  
✅ **Version Control** - Git workflow with meaningful commits  
✅ **Documentation** - Clear architecture and usage guides  
✅ **Testing** - Comprehensive test coverage  
✅ **Production Thinking** - Error handling, logging, reporting  

---

## 🔄 Data Quality Results

| Dataset | Raw Rows | Clean Rows | Removed | Quality Score |
|---------|----------|------------|---------|---------------|
| Customers | 16 | 15 | 1 (6.2%) | 93.8% ✅ |
| Products | 15 | 12 | 3 (20%) | 80% ✅ |
| Orders | 14 | 11 | 3 (21.4%) | 78.6% ✅ |
| Order Items | 14 | 11 | 3 (21.4%) | 78.6% ✅ |

**Total Quality Improvement:** 49 clean records from 59 raw records

---

## 🛠️ Technologies Used

- **Language:** Python 3.13
- **Database:** SQLite (in-memory)
- **Data Processing:** Pandas, NumPy
- **SQL Engine:** sqlite3
- **Version Control:** Git & GitHub

---

## 📚 Learning Outcomes

Through building this project, I developed:
- End-to-end data pipeline architecture
- Real-world data quality management
- SQL-based business analytics
- Production-level Python development
- Professional software engineering practices

**This project represents the foundation of data engineering and analytics skills applicable to roles at companies like Atlan, Delphix, and modern data-driven organizations.**

---

## 🎯 Use Cases

This platform architecture can be adapted for:
- E-commerce analytics
- Retail business intelligence
- Customer behavior analysis
- Inventory management systems
- Sales performance tracking
- Data quality automation

---

## 📈 Future Enhancements

Potential additions (not yet implemented):
- PostgreSQL/MySQL integration for persistent storage
- REST API for analytics endpoints
- Interactive dashboards (Plotly/Streamlit)
- Automated email reports
- Machine learning predictions
- Real-time data streaming

---

## 👤 Author

**Raj Sudhir More**  
EXTC Engineering Student | Aspiring Data Engineer

- GitHub: [@rajmore151](https://github.com/rajmore151)
- LinkedIn: [Raj More](https://www.linkedin.com/in/raj-more-your-profile)
- Email: your.email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to my mentors and the data engineering community for guidance on industry best practices and modern data platform architecture.

---

**⭐ If you find this project useful, please consider giving it a star!**

---

*Last Updated: January 2026*
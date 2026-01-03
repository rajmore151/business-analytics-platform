"""
SQL Analytics Engine
Executes SQL queries on cleaned data for business insights
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

class SQLAnalytics:
    """Runs SQL analytics on cleaned datasets"""
    
    def __init__(self, cleaned_data_dir='data/cleaned'):
        """
        Initialize analytics engine
        
        Args:
            cleaned_data_dir: Directory with cleaned CSV files
        """
        self.cleaned_data_dir = cleaned_data_dir
        self.db_connection = None
        self.datasets = {}
    
    def setup_database(self):
        """Create in-memory SQLite database and load cleaned data"""
        print("\n[SETUP] Creating in-memory SQL database...")
        
        # Create in-memory SQLite database
        self.db_connection = sqlite3.connect(':memory:')
        
        # Load cleaned datasets
        dataset_files = {
            'customers': 'cleaned_customers.csv',
            'products': 'cleaned_products.csv',
            'orders': 'cleaned_orders.csv',
            'order_items': 'cleaned_order_items.csv'
        }
        
        for table_name, filename in dataset_files.items():
            filepath = os.path.join(self.cleaned_data_dir, filename)
            
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                df.to_sql(table_name, self.db_connection, index=False, if_exists='replace')
                self.datasets[table_name] = df
                print(f"  * Loaded {table_name}: {len(df)} rows")
            else:
                print(f"  x File not found: {filename}")
        
        print("[SETUP] Database ready for analytics")
    
    def execute_query(self, query, description=None):
        """
        Execute SQL query and return results
        
        Args:
            query: SQL query string
            description: Optional description of what query does
            
        Returns:
            pd.DataFrame: Query results
        """
        if description:
            print(f"\n--- {description} ---")
        
        try:
            result = pd.read_sql_query(query, self.db_connection)
            return result
        except Exception as e:
            print(f"[ERROR] Query failed: {str(e)}")
            return None
    
    def get_total_revenue(self):
        """Calculate total revenue metrics"""
        query = """
        SELECT 
            SUM(total_amount) AS total_revenue,
            COUNT(DISTINCT order_id) AS total_orders,
            AVG(total_amount) AS average_order_value
        FROM orders
        WHERE order_status = 'Completed'
        """
        return self.execute_query(query, "Total Revenue Summary")
    
    def get_revenue_by_date(self):
        """Get daily revenue breakdown"""
        query = """
        SELECT 
            order_date,
            COUNT(order_id) AS orders_count,
            SUM(total_amount) AS daily_revenue,
            AVG(total_amount) AS avg_order_value
        FROM orders
        WHERE order_status = 'Completed'
        GROUP BY order_date
        ORDER BY order_date DESC
        """
        return self.execute_query(query, "Revenue by Date")
    
    def get_top_customers(self, limit=10):
        """Get top customers by revenue"""
        query = f"""
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            c.city,
            COUNT(o.order_id) AS total_orders,
            SUM(o.total_amount) AS total_spent,
            AVG(o.total_amount) AS avg_order_value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_status = 'Completed'
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city
        ORDER BY total_spent DESC
        LIMIT {limit}
        """
        return self.execute_query(query, f"Top {limit} Customers by Revenue")
    
    def get_customer_distribution(self):
        """Get customer distribution by city"""
        query = """
        SELECT 
            c.city,
            c.state,
            COUNT(DISTINCT c.customer_id) AS customer_count,
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(o.total_amount), 0) AS total_revenue
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
            AND o.order_status = 'Completed'
        GROUP BY c.city, c.state
        ORDER BY total_revenue DESC
        """
        return self.execute_query(query, "Customer Distribution by City")
    
    def get_best_selling_products(self, limit=10):
        """Get best-selling products"""
        query = f"""
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            p.price,
            COUNT(oi.order_item_id) AS times_ordered,
            SUM(oi.quantity) AS total_quantity_sold,
            SUM(oi.quantity * oi.price_per_unit) AS total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_status = 'Completed'
        GROUP BY p.product_id, p.product_name, p.category, p.price
        ORDER BY total_revenue DESC
        LIMIT {limit}
        """
        return self.execute_query(query, f"Top {limit} Best-Selling Products")
    
    def get_category_performance(self):
        """Get product performance by category"""
        query = """
        SELECT 
            p.category,
            COUNT(DISTINCT p.product_id) AS products_count,
            SUM(oi.quantity) AS total_units_sold,
            SUM(oi.quantity * oi.price_per_unit) AS category_revenue,
            AVG(oi.price_per_unit) AS avg_product_price
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_status = 'Completed'
        GROUP BY p.category
        ORDER BY category_revenue DESC
        """
        return self.execute_query(query, "Product Performance by Category")
    
    def get_low_stock_products(self, threshold=50):
        """Get products with low inventory"""
        query = f"""
        SELECT 
            product_id,
            product_name,
            category,
            stock_quantity,
            price
        FROM products
        WHERE stock_quantity < {threshold}
        ORDER BY stock_quantity ASC
        """
        return self.execute_query(query, f"Low Stock Products (< {threshold} units)")
    
    def get_order_status_summary(self):
        """Get summary of orders by status"""
        query = """
        SELECT 
            order_status,
            COUNT(order_id) AS order_count,
            SUM(total_amount) AS total_value,
            AVG(total_amount) AS avg_order_value
        FROM orders
        GROUP BY order_status
        ORDER BY order_count DESC
        """
        return self.execute_query(query, "Orders Status Summary")
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        print("\n" + "="*70)
        print("BUSINESS ANALYTICS REPORT")
        print("="*70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "="*70)
        print("1. REVENUE ANALYTICS")
        print("="*70)
        
        revenue = self.get_total_revenue()
        if revenue is not None and not revenue.empty:
            print(revenue.to_string(index=False))
        
        revenue_by_date = self.get_revenue_by_date()
        if revenue_by_date is not None and not revenue_by_date.empty:
            print("\n" + revenue_by_date.to_string(index=False))
        
        print("\n" + "="*70)
        print("2. CUSTOMER ANALYTICS")
        print("="*70)
        
        top_customers = self.get_top_customers(5)
        if top_customers is not None and not top_customers.empty:
            print(top_customers.to_string(index=False))
        
        customer_dist = self.get_customer_distribution()
        if customer_dist is not None and not customer_dist.empty:
            print("\n" + customer_dist.to_string(index=False))
        
        print("\n" + "="*70)
        print("3. PRODUCT ANALYTICS")
        print("="*70)
        
        best_products = self.get_best_selling_products(5)
        if best_products is not None and not best_products.empty:
            print(best_products.to_string(index=False))
        
        category_perf = self.get_category_performance()
        if category_perf is not None and not category_perf.empty:
            print("\n" + category_perf.to_string(index=False))
        
        low_stock = self.get_low_stock_products()
        if low_stock is not None and not low_stock.empty:
            print("\n" + low_stock.to_string(index=False))
        
        print("\n" + "="*70)
        print("4. ORDER ANALYTICS")
        print("="*70)
        
        order_summary = self.get_order_status_summary()
        if order_summary is not None and not order_summary.empty:
            print(order_summary.to_string(index=False))
        
        print("\n" + "="*70)
        print("REPORT COMPLETE")
        print("="*70)
    
    def close(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()
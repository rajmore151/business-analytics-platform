"""
Data Cleaning Module
Handles data cleaning and transformation
"""

import pandas as pd
import numpy as np
from .validators import DataValidator

class DataCleaner:
    """Cleans and transforms raw data based on validation rules"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.cleaning_log = []
    
    # ========== CUSTOMER CLEANING ==========
    
    def clean_customers(self, df):
        """
        Clean customers dataset
        
        Args:
            df: Raw customers dataframe
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("\n[CLEANING] Customers dataset...")
        
        original_count = len(df)
        df_clean = df.copy()
        
        # Remove exact duplicates
        duplicates = df_clean.duplicated(keep='first')
        df_clean = df_clean[~duplicates]
        self.log_cleaning('customers', 'duplicates_removed', duplicates.sum())
        
        # Remove rows with duplicate customer_id (keep first)
        id_duplicates = df_clean.duplicated(subset=['customer_id'], keep='first')
        df_clean = df_clean[~id_duplicates]
        self.log_cleaning('customers', 'duplicate_ids_removed', id_duplicates.sum())
        
        # Remove rows with missing critical fields
        critical_fields = ['customer_id', 'first_name', 'last_name']
        missing_critical = df_clean[critical_fields].isna().any(axis=1)
        df_clean = df_clean[~missing_critical]
        self.log_cleaning('customers', 'missing_critical_removed', missing_critical.sum())
        
        # Validate and remove invalid emails
        if 'email' in df_clean.columns:
            invalid_email = ~df_clean['email'].apply(self.validator.validate_email)
            for idx in df_clean[invalid_email].index:
                self.validator.log_validation_error(
                    'customers', idx, 'email', 'invalid_format', 
                    df_clean.loc[idx, 'email']
                )
        
        # Validate and remove invalid phone numbers
        if 'phone' in df_clean.columns:
            invalid_phone = ~df_clean['phone'].apply(self.validator.validate_phone)
            for idx in df_clean[invalid_phone].index:
                self.validator.log_validation_error(
                    'customers', idx, 'phone', 'invalid_format',
                    df_clean.loc[idx, 'phone']
                )
        
        # Trim whitespace from string columns
        string_cols = df_clean.select_dtypes(include=['object']).columns
        for col in string_cols:
            df_clean[col] = df_clean[col].str.strip()
        
        final_count = len(df_clean)
        print(f"[CLEANING] Customers: {original_count} -> {final_count} rows ({original_count - final_count} removed)")
        
        return df_clean
    
    # ========== PRODUCT CLEANING ==========
    
    def clean_products(self, df):
        """
        Clean products dataset
        
        Args:
            df: Raw products dataframe
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("\n[CLEANING] Products dataset...")
        
        original_count = len(df)
        df_clean = df.copy()
        
        # Remove rows with missing product_name
        missing_name = df_clean['product_name'].isna()
        df_clean = df_clean[~missing_name]
        self.log_cleaning('products', 'missing_product_name', missing_name.sum())
        
        # Remove rows with invalid price
        invalid_price = ~df_clean['price'].apply(self.validator.validate_price)
        df_clean = df_clean[~invalid_price]
        self.log_cleaning('products', 'invalid_price_removed', invalid_price.sum())
        
        # Fix negative stock quantities (set to 0)
        if 'stock_quantity' in df_clean.columns:
            negative_stock = df_clean['stock_quantity'] < 0
            df_clean.loc[negative_stock, 'stock_quantity'] = 0
            self.log_cleaning('products', 'negative_stock_fixed', negative_stock.sum())
        
        # Remove duplicate product_ids
        id_duplicates = df_clean.duplicated(subset=['product_id'], keep='first')
        df_clean = df_clean[~id_duplicates]
        self.log_cleaning('products', 'duplicate_ids_removed', id_duplicates.sum())
        
        final_count = len(df_clean)
        print(f"[CLEANING] Products: {original_count} -> {final_count} rows ({original_count - final_count} removed)")
        
        return df_clean
    
    # ========== ORDER CLEANING ==========
    
    def clean_orders(self, df, customers_df):
        """
        Clean orders dataset
        
        Args:
            df: Raw orders dataframe
            customers_df: Cleaned customers dataframe (for FK check)
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("\n[CLEANING] Orders dataset...")
        
        original_count = len(df)
        df_clean = df.copy()
        
        # Remove rows with missing order_date
        missing_date = df_clean['order_date'].isna()
        df_clean = df_clean[~missing_date]
        self.log_cleaning('orders', 'missing_order_date', missing_date.sum())
        
        # Remove rows with future dates
        invalid_date = ~df_clean['order_date'].apply(self.validator.validate_date)
        df_clean = df_clean[~invalid_date]
        self.log_cleaning('orders', 'future_dates_removed', invalid_date.sum())
        
        # Remove orders with invalid status
        invalid_status = ~df_clean['order_status'].apply(self.validator.validate_order_status)
        df_clean = df_clean[~invalid_status]
        self.log_cleaning('orders', 'invalid_status_removed', invalid_status.sum())
        
        # Remove orders with orphaned customer_id
        valid_customer_ids = set(customers_df['customer_id'])
        orphaned = ~df_clean['customer_id'].isin(valid_customer_ids)
        df_clean = df_clean[~orphaned]
        self.log_cleaning('orders', 'orphaned_customer_id', orphaned.sum())
        
        # Remove duplicate order_ids
        id_duplicates = df_clean.duplicated(subset=['order_id'], keep='first')
        df_clean = df_clean[~id_duplicates]
        self.log_cleaning('orders', 'duplicate_ids_removed', id_duplicates.sum())
        
        final_count = len(df_clean)
        print(f"[CLEANING] Orders: {original_count} -> {final_count} rows ({original_count - final_count} removed)")
        
        return df_clean
    
    # ========== ORDER ITEMS CLEANING ==========
    
    def clean_order_items(self, df, orders_df, products_df):
        """
        Clean order_items dataset
        
        Args:
            df: Raw order_items dataframe
            orders_df: Cleaned orders dataframe (for FK check)
            products_df: Cleaned products dataframe (for FK check)
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("\n[CLEANING] Order Items dataset...")
        
        original_count = len(df)
        df_clean = df.copy()
        
        # Remove rows with invalid quantity
        invalid_qty = ~df_clean['quantity'].apply(self.validator.validate_quantity)
        df_clean = df_clean[~invalid_qty]
        self.log_cleaning('order_items', 'invalid_quantity_removed', invalid_qty.sum())
        
        # Remove rows with invalid price
        invalid_price = ~df_clean['price_per_unit'].apply(self.validator.validate_price)
        df_clean = df_clean[~invalid_price]
        self.log_cleaning('order_items', 'invalid_price_removed', invalid_price.sum())
        
        # Remove items with orphaned order_id
        valid_order_ids = set(orders_df['order_id'])
        orphaned_orders = ~df_clean['order_id'].isin(valid_order_ids)
        df_clean = df_clean[~orphaned_orders]
        self.log_cleaning('order_items', 'orphaned_order_id', orphaned_orders.sum())
        
        # Remove items with orphaned product_id
        valid_product_ids = set(products_df['product_id'])
        orphaned_products = ~df_clean['product_id'].isin(valid_product_ids)
        df_clean = df_clean[~orphaned_products]
        self.log_cleaning('order_items', 'orphaned_product_id', orphaned_products.sum())
        
        final_count = len(df_clean)
        print(f"[CLEANING] Order Items: {original_count} -> {final_count} rows ({original_count - final_count} removed)")
        
        return df_clean
    
    # ========== LOGGING ==========
    
    def log_cleaning(self, dataset, action, count):
        """Log cleaning action"""
        log_entry = {
            'dataset': dataset,
            'action': action,
            'rows_affected': count
        }
        self.cleaning_log.append(log_entry)
    
    def get_cleaning_report(self):
        """Get cleaning summary as DataFrame"""
        return pd.DataFrame(self.cleaning_log)
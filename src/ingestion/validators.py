"""
Data Validation Functions
Contains all validation logic for data quality checks
"""

import re
import pandas as pd
from datetime import datetime

class DataValidator:
    """Validates data quality across different datasets"""
    
    def __init__(self):
        self.validation_errors = []
    
    # ========== EMAIL VALIDATION ==========
    
    def validate_email(self, email):
        """
        Check if email format is valid
        
        Args:
            email: Email string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(email) or email == '':
            return False
        
        # Simple email regex: must have @ and .
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))
    
    # ========== PHONE VALIDATION ==========
    
    def validate_phone(self, phone):
        """
        Check if phone number is valid (10 digits for India)
        
        Args:
            phone: Phone string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(phone) or phone == '':
            return False
        
        # Remove any non-digit characters
        phone_digits = re.sub(r'\D', '', str(phone))
        
        # Must be exactly 10 digits
        return len(phone_digits) == 10
    
    # ========== PRICE VALIDATION ==========
    
    def validate_price(self, price):
        """
        Check if price is valid (must be positive)
        
        Args:
            price: Price value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(price):
            return False
        
        try:
            price_float = float(price)
            return price_float > 0
        except (ValueError, TypeError):
            return False
    
    # ========== QUANTITY VALIDATION ==========
    
    def validate_quantity(self, quantity):
        """
        Check if quantity is valid (must be positive integer)
        
        Args:
            quantity: Quantity value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(quantity):
            return False
        
        try:
            qty_int = int(quantity)
            return qty_int > 0
        except (ValueError, TypeError):
            return False
    
    # ========== DATE VALIDATION ==========
    
    def validate_date(self, date_str):
        """
        Check if date is valid (not in future, not null)
        
        Args:
            date_str: Date string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if pd.isna(date_str) or date_str == '':
            return False
        
        try:
            date_obj = pd.to_datetime(date_str)
            today = pd.Timestamp.now()
            
            # Date cannot be in future
            return date_obj <= today
        except:
            return False
    
    # ========== STATUS VALIDATION ==========
    
    def validate_order_status(self, status):
        """
        Check if order status is valid
        
        Args:
            status: Status string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        valid_statuses = ['Pending', 'Completed', 'Cancelled']
        return status in valid_statuses
    
    # ========== DUPLICATE DETECTION ==========
    
    def find_duplicates(self, df, id_column):
        """
        Find duplicate IDs in dataframe
        
        Args:
            df: Dataframe to check
            id_column: Name of ID column
            
        Returns:
            pd.DataFrame: Rows with duplicate IDs
        """
        duplicates = df[df.duplicated(subset=[id_column], keep=False)]
        return duplicates
    
    # ========== MISSING VALUE CHECK ==========
    
    def find_missing_values(self, df, required_columns):
        """
        Find rows with missing required values
        
        Args:
            df: Dataframe to check
            required_columns: List of columns that cannot be null
            
        Returns:
            pd.DataFrame: Rows with missing required values
        """
        missing_mask = df[required_columns].isna().any(axis=1)
        return df[missing_mask]
    
    # ========== REFERENTIAL INTEGRITY ==========
    
    def check_foreign_key(self, df, fk_column, reference_df, ref_column):
        """
        Check if foreign key values exist in reference table
        
        Args:
            df: Dataframe with foreign key
            fk_column: Foreign key column name
            reference_df: Reference dataframe
            ref_column: Reference column name
            
        Returns:
            pd.DataFrame: Rows with orphaned foreign keys
        """
        valid_ids = set(reference_df[ref_column].dropna())
        orphaned = df[~df[fk_column].isin(valid_ids)]
        return orphaned
    
    # ========== VALIDATION REPORT ==========
    
    def log_validation_error(self, dataset, row_index, column, issue, value):
        """
        Log a validation error
        
        Args:
            dataset: Name of dataset
            row_index: Row number
            column: Column name
            issue: Description of issue
            value: Problematic value
        """
        error = {
            'dataset': dataset,
            'row': row_index,
            'column': column,
            'issue': issue,
            'value': str(value)[:50]  # Truncate long values
        }
        self.validation_errors.append(error)
    
    def get_error_report(self):
        """
        Get all validation errors as DataFrame
        
        Returns:
            pd.DataFrame: Error report
        """
        return pd.DataFrame(self.validation_errors)
    
    def get_error_summary(self):
        """
        Get summary of errors by type
        
        Returns:
            pd.DataFrame: Error counts by issue type
        """
        if not self.validation_errors:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.validation_errors)
        summary = df.groupby(['dataset', 'issue']).size().reset_index(name='count')
        return summary
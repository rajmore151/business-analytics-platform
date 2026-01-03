"""
Data Loader Module
Handles reading CSV files and basic validation
"""

import pandas as pd
import os
from datetime import datetime

class DataLoader:
    """Loads and validates raw CSV data files"""
    
    def __init__(self, data_dir='data'):
        """
        Initialize DataLoader
        
        Args:
            data_dir (str): Directory containing CSV files
        """
        self.data_dir = data_dir
        self.validation_log = []
        
    def load_csv(self, filename):
        """
        Load a CSV file from the data directory
        
        Args:
            filename (str): Name of CSV file to load
            
        Returns:
            pd.DataFrame: Loaded dataframe or None if error
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                error_msg = f"File not found: {filepath}"
                self.log_error(filename, error_msg)
                return None
            
            # Load CSV
            df = pd.read_csv(filepath)
            
            # Log success
            self.log_info(filename, f"Successfully loaded {len(df)} rows")
            
            return df
            
        except Exception as e:
            error_msg = f"Error loading {filename}: {str(e)}"
            self.log_error(filename, error_msg)
            return None
    
    def validate_not_empty(self, df, dataset_name):
        """
        Check if dataframe is not empty
        
        Args:
            df (pd.DataFrame): Dataframe to validate
            dataset_name (str): Name of dataset for logging
            
        Returns:
            bool: True if valid, False otherwise
        """
        if df is None or df.empty:
            self.log_error(dataset_name, "Dataset is empty")
            return False
        
        self.log_info(dataset_name, f"Dataset has {len(df)} rows")
        return True
    
    def validate_required_columns(self, df, dataset_name, required_columns):
        """
        Check if all required columns exist
        
        Args:
            df (pd.DataFrame): Dataframe to validate
            dataset_name (str): Name of dataset
            required_columns (list): List of required column names
            
        Returns:
            bool: True if all columns exist, False otherwise
        """
        if df is None:
            return False
            
        missing_cols = set(required_columns) - set(df.columns)
        
        if missing_cols:
            self.log_error(dataset_name, f"Missing columns: {missing_cols}")
            return False
        
        self.log_info(dataset_name, "All required columns present")
        return True
    
    def log_info(self, source, message):
        """Log informational message"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': 'INFO',
            'source': source,
            'message': message
        }
        self.validation_log.append(log_entry)
        print(f"[INFO] {source}: {message}")
    
    def log_error(self, source, message):
        """Log error message"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': 'ERROR',
            'source': source,
            'message': message
        }
        self.validation_log.append(log_entry)
        print(f"[ERROR] {source}: {message}")
    
    def get_validation_report(self):
        """
        Get full validation log as DataFrame
        
        Returns:
            pd.DataFrame: Validation log
        """
        return pd.DataFrame(self.validation_log)
    
    def load_all_datasets(self):
        """
        Load all raw datasets
        
        Returns:
            dict: Dictionary of dataframes
        """
        datasets = {}
        
        # Define files and their required columns
        file_configs = {
            'customers': {
                'filename': 'raw_customers.csv',
                'required_columns': ['customer_id', 'first_name', 'last_name', 'email']
            },
            'products': {
                'filename': 'raw_products.csv',
                'required_columns': ['product_id', 'product_name', 'category', 'price']
            },
            'orders': {
                'filename': 'raw_orders.csv',
                'required_columns': ['order_id', 'customer_id', 'order_date', 'total_amount']
            },
            'order_items': {
                'filename': 'raw_order_items.csv',
                'required_columns': ['order_item_id', 'order_id', 'product_id', 'quantity']
            }
        }
        
        # Load each dataset
        for dataset_name, config in file_configs.items():
            print(f"\n--- Loading {dataset_name} ---")
            
            # Load CSV
            df = self.load_csv(config['filename'])
            
            # Validate
            if df is not None:
                self.validate_not_empty(df, dataset_name)
                self.validate_required_columns(df, dataset_name, config['required_columns'])
            
            datasets[dataset_name] = df
        
        return datasets
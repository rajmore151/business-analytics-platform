"""
Data Cleaning Pipeline
Orchestrates the complete data cleaning workflow
"""

import pandas as pd
import os
from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from datetime import datetime

class CleaningPipeline:
    """Manages end-to-end data cleaning process"""
    
    def __init__(self, raw_data_dir='data', clean_data_dir='data/cleaned'):
        """
        Initialize pipeline
        
        Args:
            raw_data_dir: Directory with raw CSV files
            clean_data_dir: Directory to save cleaned CSV files
        """
        self.raw_data_dir = raw_data_dir
        self.clean_data_dir = clean_data_dir
        self.loader = DataLoader(data_dir=raw_data_dir)
        self.cleaner = DataCleaner()
        
        # Create cleaned data directory if it doesn't exist
        os.makedirs(clean_data_dir, exist_ok=True)
    
    def run(self):
        """
        Execute complete cleaning pipeline
        
        Returns:
            dict: Cleaned datasets
        """
        print("\n" + "="*70)
        print("DATA CLEANING PIPELINE STARTED")
        print("="*70)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Load raw data
        print("\n[STEP 1] Loading raw datasets...")
        raw_datasets = self.loader.load_all_datasets()
        
        # Check if all datasets loaded
        if any(df is None for df in raw_datasets.values()):
            print("\n[ERROR] Failed to load some datasets. Aborting.")
            return None
        
        # Step 2: Clean datasets (in dependency order)
        print("\n[STEP 2] Cleaning datasets...")
        
        cleaned_datasets = {}
        
        # 2a. Clean customers (no dependencies)
        cleaned_datasets['customers'] = self.cleaner.clean_customers(
            raw_datasets['customers']
        )
        
        # 2b. Clean products (no dependencies)
        cleaned_datasets['products'] = self.cleaner.clean_products(
            raw_datasets['products']
        )
        
        # 2c. Clean orders (depends on customers)
        cleaned_datasets['orders'] = self.cleaner.clean_orders(
            raw_datasets['orders'],
            cleaned_datasets['customers']
        )
        
        # 2d. Clean order_items (depends on orders and products)
        cleaned_datasets['order_items'] = self.cleaner.clean_order_items(
            raw_datasets['order_items'],
            cleaned_datasets['orders'],
            cleaned_datasets['products']
        )
        
        # Step 3: Save cleaned data
        print("\n[STEP 3] Saving cleaned datasets...")
        self.save_cleaned_data(cleaned_datasets)
        
        # Step 4: Generate reports
        print("\n[STEP 4] Generating reports...")
        self.generate_reports(raw_datasets, cleaned_datasets)
        
        print("\n" + "="*70)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*70)
        
        return cleaned_datasets
    
    def save_cleaned_data(self, cleaned_datasets):
        """
        Save cleaned datasets to CSV files
        
        Args:
            cleaned_datasets: Dictionary of cleaned dataframes
        """
        for name, df in cleaned_datasets.items():
            filename = f"cleaned_{name}.csv"
            filepath = os.path.join(self.clean_data_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"  ✓ Saved: {filename} ({len(df)} rows)")
    
    def generate_reports(self, raw_datasets, cleaned_datasets):
        """
        Generate cleaning summary reports
        
        Args:
            raw_datasets: Original datasets
            cleaned_datasets: Cleaned datasets
        """
        # Summary statistics
        print("\n--- Data Quality Summary ---")
        print(f"{'Dataset':<15} {'Raw Rows':<12} {'Clean Rows':<12} {'Removed':<10} {'% Removed':<10}")
        print("-" * 70)
        
        for name in raw_datasets.keys():
            raw_count = len(raw_datasets[name])
            clean_count = len(cleaned_datasets[name])
            removed = raw_count - clean_count
            pct_removed = (removed / raw_count * 100) if raw_count > 0 else 0
            
            print(f"{name:<15} {raw_count:<12} {clean_count:<12} {removed:<10} {pct_removed:>6.1f}%")
        
        # Cleaning actions log
        print("\n--- Cleaning Actions Log ---")
        cleaning_report = self.cleaner.get_cleaning_report()
        if not cleaning_report.empty:
            print(cleaning_report.to_string(index=False))
        
        # Validation errors
        print("\n--- Validation Errors Detected ---")
        error_report = self.cleaner.validator.get_error_report()
        if not error_report.empty:
            error_summary = self.cleaner.validator.get_error_summary()
            print(error_summary.to_string(index=False))
            
            # Save detailed error report
            error_filepath = os.path.join(self.clean_data_dir, 'validation_errors.csv')
            error_report.to_csv(error_filepath, index=False)
            print(f"\n  ✓ Detailed error report saved: validation_errors.csv")
        else:
            print("  No validation errors found.")
        
        # Save cleaning summary
        summary_filepath = os.path.join(self.clean_data_dir, 'cleaning_summary.csv')
        cleaning_report.to_csv(summary_filepath, index=False)
        print(f"\n  ✓ Cleaning summary saved: cleaning_summary.csv")
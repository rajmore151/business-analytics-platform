"""
Test script for data cleaning pipeline
"""

from src.ingestion.cleaning_pipeline import CleaningPipeline

def main():
    print("\n" + "="*70)
    print("RUNNING DATA CLEANING PIPELINE TEST")
    print("="*70)
    
    # Initialize pipeline
    pipeline = CleaningPipeline(
        raw_data_dir='data',
        clean_data_dir='data/cleaned'
    )
    
    # Run complete pipeline
    cleaned_datasets = pipeline.run()
    
    # Verify outputs
    if cleaned_datasets:
        print("\n" + "="*70)
        print("VERIFICATION: Cleaned Datasets")
        print("="*70)
        
        for name, df in cleaned_datasets.items():
            print(f"\n{name.upper()}:")
            print(f"  Rows: {len(df)}")
            print(f"  Columns: {list(df.columns)}")
            print(f"  Sample data:")
            print(df.head(3).to_string(index=False))
        
        print("\n" + "="*70)
        print("TEST COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nCleaned files saved in: data/cleaned/")
        print("  - cleaned_customers.csv")
        print("  - cleaned_products.csv")
        print("  - cleaned_orders.csv")
        print("  - cleaned_order_items.csv")
        print("  - validation_errors.csv")
        print("  - cleaning_summary.csv")
    else:
        print("\n[ERROR] Pipeline failed to complete.")

if __name__ == "__main__":
    main()

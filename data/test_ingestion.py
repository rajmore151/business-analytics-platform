"""
Test script for data ingestion module
"""

from src.ingestion.data_loader import DataLoader

def main():
    print("="*60)
    print("TESTING DATA INGESTION MODULE")
    print("="*60)
    
    # Initialize data loader
    loader = DataLoader(data_dir='data')
    
    # Load all datasets
    datasets = loader.load_all_datasets()
    
    # Print summary
    print("\n" + "="*60)
    print("LOADING SUMMARY")
    print("="*60)
    
    for name, df in datasets.items():
        if df is not None:
            print(f"{name}: {len(df)} rows, {len(df.columns)} columns")
        else:
            print(f"{name}: FAILED TO LOAD")
    
    # Show validation report
    print("\n" + "="*60)
    print("VALIDATION LOG")
    print("="*60)
    
    report = loader.get_validation_report()
    print(report.to_string(index=False))
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
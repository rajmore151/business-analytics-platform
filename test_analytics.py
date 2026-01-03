"""
Test script for SQL analytics engine
"""

from src.ingestion.sql_analytics import SQLAnalytics

def main():
    print("\n" + "="*70)
    print("TESTING SQL ANALYTICS ENGINE")
    print("="*70)
    
    # Initialize analytics engine
    analytics = SQLAnalytics(cleaned_data_dir='data/cleaned')
    
    # Setup database
    analytics.setup_database()
    
    # Generate full analytics report
    analytics.generate_analytics_report()
    
    # Close connection
    analytics.close()
    
    print("\n" + "="*70)
    print("ANALYTICS TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

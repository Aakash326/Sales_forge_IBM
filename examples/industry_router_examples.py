#!/usr/bin/env python3
"""
IndustryRouter Usage Examples

This script demonstrates various usage patterns for the IndustryRouter class.
Run this script to see examples of industry detection and database routing.

Usage:
    python examples/industry_router_examples.py

Prerequisites:
    1. Set up Supabase database using database/supabase_setup.sql
    2. Configure environment variables in .env file
    3. Install dependencies: pip install -r requirements_supabase.txt
"""

import sys
import os
import json
import asyncio
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from src.agents.industry_router import IndustryRouter, create_industry_router, quick_query
except ImportError as e:
    print(f"Error importing IndustryRouter: {e}")
    print("Make sure you've installed the required dependencies and set up your environment properly.")
    sys.exit(1)


def print_separator(title: str):
    """Print a formatted separator for examples"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_result(result: dict, title: str):
    """Pretty print a result dictionary"""
    print(f"\n🎯 {title}")
    print("-" * 40)
    print(f"Industry: {result.get('industry', 'N/A')}")
    print(f"Database Table: {result.get('database_table', 'N/A')}")
    print(f"Processing Time: {result.get('processing_time', 'N/A')}")
    print(f"Results Count: {len(result.get('results', []))}")
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
    
    if result.get('results'):
        print("\n📊 Sample Results:")
        for i, company in enumerate(result['results'][:3], 1):
            print(f"  {i}. {company.get('company_name', 'N/A')} "
                  f"(Score: {company.get('performance_score', 'N/A')}, "
                  f"Location: {company.get('location', 'N/A')})")
        
        if len(result['results']) > 3:
            print(f"  ... and {len(result['results']) - 3} more results")


def example_basic_usage():
    """Example 1: Basic IndustryRouter usage"""
    print_separator("Example 1: Basic IndustryRouter Usage")
    
    # Test data for different industries
    test_cases = [
        {
            "title": "Finance Company Query",
            "data": {
                "company_name": "Goldman Sachs",
                "industry": "Finance",
                "query": "What are the top-performing finance companies in NY?"
            }
        },
        {
            "title": "Healthcare Company Query", 
            "data": {
                "company_name": "Johnson & Johnson",
                "industry": "Healthcare",
                "query": "Find pharmaceutical companies with high performance"
            }
        },
        {
            "title": "Technology Company Query",
            "data": {
                "company_name": "Apple Inc.",
                "industry": "Technology", 
                "query": "List top tech companies in California"
            }
        }
    ]
    
    try:
        # Initialize IndustryRouter
        router = IndustryRouter()
        
        for test_case in test_cases:
            print(f"\n🔍 Testing: {test_case['title']}")
            print(f"Input: {test_case['data']}")
            
            result = router.route_query(test_case['data'])
            print_result(result, test_case['title'])
            
    except Exception as e:
        print(f"❌ Error in basic usage example: {e}")
        print("Make sure your Supabase credentials are correctly configured in .env file")


def example_industry_detection():
    """Example 2: Industry detection capabilities"""
    print_separator("Example 2: Industry Detection Capabilities")
    
    detection_test_cases = [
        # Explicit industry field
        {"company_name": "Random Corp", "industry": "fintech"},
        
        # Company name-based detection
        {"company_name": "Microsoft Corporation"},
        {"company_name": "JPMorgan Chase"},
        {"company_name": "Pfizer Inc."},
        
        # Query-based detection
        {"query": "Find software companies"},
        {"query": "Banking and financial services"},
        {"query": "Medical device companies"},
        
        # Combined detection
        {"company_name": "TechCorp", "query": "artificial intelligence platform"},
        {"company_name": "MedDevice Inc.", "query": "healthcare technology"},
        
        # Edge cases
        {"company_name": "XYZ Corp"},  # Should fail to detect
        {"query": "General business consulting"},  # Should fail to detect
    ]
    
    try:
        router = IndustryRouter()
        
        for i, test_data in enumerate(detection_test_cases, 1):
            print(f"\n🔍 Test Case {i}: {test_data}")
            
            # Test just the detection method
            detected_industry = router.detect_industry(test_data)
            print(f"Detected Industry: {detected_industry or 'Not detected'}")
            
            if detected_industry:
                table = router.get_database_table(detected_industry)
                print(f"Target Table: {table}")
            
    except Exception as e:
        print(f"❌ Error in industry detection example: {e}")


def example_advanced_filtering():
    """Example 3: Advanced filtering and querying"""
    print_separator("Example 3: Advanced Filtering and Querying")
    
    advanced_queries = [
        {
            "title": "Finance Companies in New York (High Performance)",
            "data": {
                "industry": "finance",
                "location": "New York",
                "min_performance": 90,
                "limit": 5,
                "sort_by": "performance_score",
                "sort_order": "desc"
            }
        },
        {
            "title": "Healthcare Companies (Sorted by Name)",
            "data": {
                "industry": "healthcare", 
                "min_performance": 85,
                "sort_by": "company_name",
                "sort_order": "asc",
                "limit": 10
            }
        },
        {
            "title": "Tech Companies in California",
            "data": {
                "query": "technology companies",
                "location": "CA",
                "min_performance": 88
            }
        },
        {
            "title": "Specific Company Search",
            "data": {
                "company_name": "Apple",
                "industry": "technology"
            }
        }
    ]
    
    try:
        router = IndustryRouter()
        
        for query_case in advanced_queries:
            print(f"\n🔍 {query_case['title']}")
            print(f"Query Parameters: {query_case['data']}")
            
            result = router.route_query(query_case['data'])
            print_result(result, query_case['title'])
            
    except Exception as e:
        print(f"❌ Error in advanced filtering example: {e}")


def example_utility_functions():
    """Example 4: Utility functions and factory methods"""
    print_separator("Example 4: Utility Functions")
    
    try:
        # Method 1: Factory function
        print("🏭 Using factory function:")
        router1 = create_industry_router()
        stats1 = router1.get_statistics()
        print(f"Router created - Supported industries: {stats1['supported_industries']}")
        
        # Method 2: Quick query utility
        print("\n⚡ Using quick query utility:")
        test_data = {
            "company_name": "Tesla Inc.",
            "query": "electric vehicle technology"
        }
        
        result = quick_query(test_data)
        print_result(result, "Quick Query Result")
        
        # Method 3: Connection testing
        print("\n🔌 Testing connection:")
        connection_status = router1.test_connection()
        print(f"Connection Status: {'✅ Connected' if connection_status['connected'] else '❌ Failed'}")
        
        if connection_status['connected']:
            for table, status in connection_status['tables_status'].items():
                if status['accessible']:
                    print(f"  • {table}: ✅ Accessible ({status['sample_count']} sample records)")
                else:
                    print(f"  • {table}: ❌ Error - {status.get('error', 'Unknown')}")
        else:
            print(f"Connection Error: {connection_status.get('error', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error in utility functions example: {e}")


def example_performance_monitoring():
    """Example 5: Performance monitoring and statistics"""
    print_separator("Example 5: Performance Monitoring")
    
    try:
        router = IndustryRouter()
        
        # Run several queries to generate statistics
        test_queries = [
            {"company_name": "Microsoft", "industry": "technology"},
            {"query": "banking services", "location": "NY"},
            {"industry": "healthcare", "min_performance": 90},
            {"company_name": "InvalidCompany", "industry": "unknown"},  # This should fail
            {"query": "pharmaceutical research"}
        ]
        
        print("🏃‍♂️ Running multiple queries for performance testing...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            result = router.route_query(query)
            print(f"Result: {result['industry']} -> {len(result.get('results', []))} results in {result['processing_time']}")
        
        # Get performance statistics
        print("\n📊 Performance Statistics:")
        stats = router.get_statistics()
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Successful Queries: {stats['successful_queries']}")
        print(f"Failed Queries: {stats['failed_queries']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Average Response Time: {stats['average_response_time_seconds']}s")
        
        print(f"\n🗺️  Table Mappings:")
        for industry, table in stats['table_mappings'].items():
            print(f"  • {industry.title()}: {table}")
            
    except Exception as e:
        print(f"❌ Error in performance monitoring example: {e}")


def example_error_handling():
    """Example 6: Error handling scenarios"""
    print_separator("Example 6: Error Handling")
    
    error_test_cases = [
        {
            "title": "Empty Input",
            "data": {}
        },
        {
            "title": "Invalid Input Type",
            "data": "not_a_dict"
        },
        {
            "title": "Unknown Industry",
            "data": {"industry": "agriculture", "company_name": "Farm Corp"}
        },
        {
            "title": "No Detectable Industry",
            "data": {"company_name": "Random Corp", "query": "generic business"}
        }
    ]
    
    try:
        router = IndustryRouter()
        
        for test_case in error_test_cases:
            print(f"\n🧪 Testing: {test_case['title']}")
            
            try:
                result = router.route_query(test_case['data'])
                print_result(result, test_case['title'])
                
                if result.get('error'):
                    print(f"✅ Error handled gracefully: {result['error']}")
                    
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
        
    except Exception as e:
        print(f"❌ Error in error handling example: {e}")


async def example_async_usage():
    """Example 7: Async usage patterns (if applicable)"""
    print_separator("Example 7: Async Usage Patterns")
    
    # Note: Current implementation is sync, but showing how it could be used in async context
    def run_async_queries():
        try:
            router = IndustryRouter()
            
            # Simulate async-like batch processing
            queries = [
                {"industry": "finance", "location": "NY"},
                {"industry": "healthcare", "min_performance": 85},
                {"industry": "technology", "location": "CA"}
            ]
            
            print("🔄 Running batch queries...")
            results = []
            
            for i, query in enumerate(queries, 1):
                print(f"Processing query {i}/{len(queries)}: {query}")
                result = router.route_query(query)
                results.append(result)
                print(f"✅ Query {i} completed: {len(result.get('results', []))} results")
            
            print(f"\n📈 Batch Summary:")
            print(f"Total Queries: {len(results)}")
            total_results = sum(len(r.get('results', [])) for r in results)
            print(f"Total Results: {total_results}")
            
            successful = sum(1 for r in results if r.get('industry') != 'error')
            print(f"Success Rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
            
        except Exception as e:
            print(f"❌ Error in async usage example: {e}")
    
    run_async_queries()


def main():
    """Run all examples"""
    print("🚀 IndustryRouter Examples")
    print(f"Started at: {datetime.now().isoformat()}")
    
    examples = [
        ("Basic Usage", example_basic_usage),
        ("Industry Detection", example_industry_detection),
        ("Advanced Filtering", example_advanced_filtering),
        ("Utility Functions", example_utility_functions),
        ("Performance Monitoring", example_performance_monitoring),
        ("Error Handling", example_error_handling),
        ("Async Patterns", example_async_usage)
    ]
    
    for name, example_func in examples:
        try:
            example_func()
        except KeyboardInterrupt:
            print(f"\n⏸️  Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Failed to run {name}: {e}")
            continue
    
    print_separator("Examples Complete")
    print(f"✅ All examples completed at: {datetime.now().isoformat()}")
    print("\n📝 Next Steps:")
    print("1. Review the results above")
    print("2. Modify the examples for your specific use case") 
    print("3. Integration the IndustryRouter into your application")
    print("4. Set up monitoring and logging as needed")


if __name__ == "__main__":
    main()
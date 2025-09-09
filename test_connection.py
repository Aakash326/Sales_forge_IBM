#!/usr/bin/env python3
"""
Quick Supabase Connection Test

This script tests the connection to your Supabase instance and
verifies the IndustryRouter system is working properly.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

def test_basic_connection():
    """Test basic Supabase connection"""
    print("🔌 Testing Supabase Connection...")
    
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            print("❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY in .env file")
            return False
        
        print(f"   URL: {url}")
        print(f"   Key: {key[:20]}...")
        
        # Create client
        supabase = create_client(url, key)
        
        # Test basic query - try to access a simple table or create one
        print("   Testing basic query...")
        
        # Try a simple query that should work even without our tables
        response = supabase.table('_temp_test').select('*').limit(1).execute()
        print("✅ Basic connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_database_setup():
    """Test if our database tables exist"""
    print("\n🗄️  Testing Database Setup...")
    
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY') 
        supabase = create_client(url, key)
        
        tables_to_check = [
            'finance_companies',
            'healthcare_companies', 
            'tech_companies'
        ]
        
        results = {}
        
        for table in tables_to_check:
            try:
                print(f"   Checking {table}...")
                response = supabase.table(table).select('id').limit(1).execute()
                
                if response.data is not None:
                    # Get count
                    count_response = supabase.table(table).select('id', count='exact').execute()
                    count = count_response.count if hasattr(count_response, 'count') else len(response.data)
                    results[table] = {'exists': True, 'count': count}
                    print(f"   ✅ {table}: Found with sample data")
                else:
                    results[table] = {'exists': False, 'count': 0}
                    print(f"   ⚠️  {table}: Table exists but no data")
                    
            except Exception as e:
                results[table] = {'exists': False, 'error': str(e)}
                print(f"   ❌ {table}: {str(e)}")
        
        # Summary
        existing_tables = sum(1 for r in results.values() if r.get('exists', False))
        print(f"\n📊 Database Summary: {existing_tables}/3 tables ready")
        
        if existing_tables == 0:
            print("\n⚠️  No tables found. You need to run the SQL setup in Supabase.")
            print("   Go to your Supabase dashboard → SQL Editor")
            print("   Copy and paste the contents of database/supabase_setup.sql")
        
        return existing_tables > 0
        
    except Exception as e:
        print(f"❌ Database setup test failed: {str(e)}")
        return False

def test_industry_router():
    """Test the IndustryRouter class"""
    print("\n🎯 Testing IndustryRouter...")
    
    try:
        from src.agents.industry_router import IndustryRouter
        
        # Initialize router
        print("   Initializing IndustryRouter...")
        router = IndustryRouter()
        
        # Test connection method
        print("   Testing connection...")
        connection_status = router.test_connection()
        
        if connection_status['connected']:
            print("   ✅ IndustryRouter connected successfully!")
            
            # Show table status
            for table, status in connection_status['tables_status'].items():
                if status['accessible']:
                    print(f"      • {table}: ✅ Accessible")
                else:
                    print(f"      • {table}: ❌ {status.get('error', 'Not accessible')}")
        else:
            print(f"   ❌ Connection failed: {connection_status.get('error', 'Unknown error')}")
            return False
        
        # Test industry detection
        print("   Testing industry detection...")
        test_cases = [
            {'company_name': 'Goldman Sachs', 'expected': 'finance'},
            {'company_name': 'Microsoft Corporation', 'expected': 'technology'},
            {'company_name': 'Johnson & Johnson', 'expected': 'healthcare'},
        ]
        
        for test_case in test_cases:
            detected = router.detect_industry(test_case)
            expected = test_case['expected']
            if detected == expected:
                print(f"      • {test_case['company_name']}: ✅ {detected}")
            else:
                print(f"      • {test_case['company_name']}: ❌ Got {detected}, expected {expected}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import failed: {str(e)}")
        print("   Make sure the src/agents/industry_router.py file exists")
        return False
    except Exception as e:
        print(f"   ❌ IndustryRouter test failed: {str(e)}")
        return False

def test_sample_queries():
    """Test sample queries if everything is set up"""
    print("\n🔍 Testing Sample Queries...")
    
    try:
        from src.agents.industry_router import IndustryRouter
        
        router = IndustryRouter()
        
        # Test queries
        test_queries = [
            {
                'name': 'Finance Companies Query',
                'data': {'industry': 'finance', 'limit': 3}
            },
            {
                'name': 'Tech Companies in CA',
                'data': {'industry': 'technology', 'location': 'CA', 'limit': 2}
            },
            {
                'name': 'High Performance Healthcare',
                'data': {'industry': 'healthcare', 'min_performance': 90, 'limit': 2}
            }
        ]
        
        for query in test_queries:
            print(f"   Running: {query['name']}")
            try:
                result = router.route_query(query['data'])
                
                if result['industry'] != 'error':
                    count = len(result.get('results', []))
                    time_taken = result.get('processing_time', 'N/A')
                    print(f"      ✅ {count} results in {time_taken}")
                    
                    # Show first result if available
                    if result.get('results'):
                        first = result['results'][0]
                        name = first.get('company_name', 'N/A')
                        score = first.get('performance_score', 'N/A')
                        location = first.get('location', 'N/A')
                        print(f"         Sample: {name} (Score: {score}, Location: {location})")
                else:
                    print(f"      ❌ Query failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"      ❌ Query failed: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample queries failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Supabase IndustryRouter Connection Test")
    print("=" * 50)
    print(f"Started at: {datetime.now().isoformat()}")
    
    tests = [
        ("Basic Connection", test_basic_connection),
        ("Database Setup", test_database_setup), 
        ("IndustryRouter", test_industry_router),
        ("Sample Queries", test_sample_queries)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except KeyboardInterrupt:
            print(f"\n⏸️  Test interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ {test_name} failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your IndustryRouter is ready to use.")
        print("\n📚 Next steps:")
        print("   • Run examples: python examples/industry_router_examples.py")
        print("   • Run full tests: python tests/test_industry_router.py")
        print("   • Integrate into your workflows")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
        
        if any("Database Setup" in name and not success for name, success in results):
            print("\n💡 Quick fix for database issues:")
            print("   1. Go to https://supabase.com/dashboard")
            print("   2. Open your project")
            print("   3. Go to SQL Editor")
            print("   4. Copy & paste contents of database/supabase_setup.sql")
            print("   5. Run the SQL commands")
            print("   6. Run this test again")

if __name__ == "__main__":
    main()
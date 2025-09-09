#!/usr/bin/env python3
"""
Gmail Integration Test Script for Sales Forge

This script tests the complete Gmail integration workflow:
1. Database connection and company retrieval
2. Gmail API authentication
3. Email generation and sending
4. Error handling and reporting

Usage:
    python test_gmail_integration.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test environment variables and file requirements"""
    print("🔧 Testing Environment Setup...")
    
    issues = []
    
    # Check required environment variables
    required_vars = {
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': os.getenv('SUPABASE_ANON_KEY'),
        'GMAIL_CREDENTIALS_PATH': os.getenv('GMAIL_CREDENTIALS_PATH', 'client_secret.json'),
        'GMAIL_TOKEN_PATH': os.getenv('GMAIL_TOKEN_PATH', 'gmail_token.json'),
    }
    
    for var_name, var_value in required_vars.items():
        if not var_value:
            issues.append(f"Missing {var_name} in environment")
            print(f"   ❌ {var_name}: Not set")
        else:
            print(f"   ✅ {var_name}: Configured")
    
    # Check file existence
    gmail_creds_path = required_vars['GMAIL_CREDENTIALS_PATH']
    if gmail_creds_path and not os.path.exists(gmail_creds_path):
        issues.append(f"Gmail credentials file not found: {gmail_creds_path}")
        print(f"   ❌ Gmail credentials: File not found ({gmail_creds_path})")
    else:
        print(f"   ✅ Gmail credentials: File exists")
    
    if issues:
        print(f"\n⚠️  Environment issues found:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    
    print("   ✅ Environment setup looks good!")
    return True

def test_database_connection():
    """Test Supabase database connection"""
    print("\n🗄️  Testing Database Connection...")
    
    try:
        from src.agents.industry_router import IndustryRouter
        
        # Initialize router without email to test DB only
        router = IndustryRouter(enable_email=False)
        
        # Test connection
        connection_status = router.test_connection()
        
        if not connection_status['connected']:
            print(f"   ❌ Database connection failed: {connection_status.get('error')}")
            return False
        
        print("   ✅ Database connected successfully")
        
        # Test table access
        tables_status = connection_status.get('tables_status', {})
        accessible_tables = sum(1 for status in tables_status.values() if status.get('accessible'))
        total_tables = len(tables_status)
        
        print(f"   📊 Tables accessible: {accessible_tables}/{total_tables}")
        
        for table_name, status in tables_status.items():
            if status.get('accessible'):
                print(f"      ✅ {table_name}")
            else:
                print(f"      ❌ {table_name}: {status.get('error', 'Not accessible')}")
        
        return accessible_tables > 0
        
    except ImportError as e:
        print(f"   ❌ Import failed: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Database test failed: {str(e)}")
        return False

def test_gmail_client_initialization():
    """Test Gmail client initialization"""
    print("\n📧 Testing Gmail Client Initialization...")
    
    try:
        from src.integrations.gmail_client import GmailClient
        
        # Get credentials path from environment
        credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'client_secret.json')
        token_path = os.getenv('GMAIL_TOKEN_PATH', 'gmail_token.json')
        
        print(f"   Using credentials: {credentials_path}")
        print(f"   Token path: {token_path}")
        
        # Initialize client
        gmail_client = GmailClient(
            credentials_path=credentials_path,
            token_path=token_path
        )
        
        print("   ✅ Gmail client initialized")
        
        # Test authentication (this might prompt for OAuth)
        print("   🔐 Testing Gmail authentication...")
        print("   📝 Note: This may open a browser window for OAuth authentication")
        
        auth_success = gmail_client.authenticate()
        
        if auth_success:
            print("   ✅ Gmail authentication successful")
            return True
        else:
            print("   ❌ Gmail authentication failed")
            return False
            
    except ImportError as e:
        print(f"   ❌ Gmail import failed: {str(e)}")
        print("   💡 Install Google API client: pip install google-api-python-client google-auth-oauthlib")
        return False
    except Exception as e:
        print(f"   ❌ Gmail initialization failed: {str(e)}")
        return False

def test_industry_router_with_email():
    """Test IndustryRouter with email functionality enabled"""
    print("\n🎯 Testing IndustryRouter with Email Integration...")
    
    try:
        from src.agents.industry_router import IndustryRouter
        
        # Initialize with email enabled
        router = IndustryRouter(enable_email=True)
        
        # Check email enablement
        if not router.email_enabled:
            print("   ❌ Email functionality not enabled in router")
            return False
        
        print("   ✅ IndustryRouter with email initialized")
        
        # Test a simple query
        print("   🔍 Testing company query...")
        test_query = {
            "industry": "technology",
            "limit": 1
        }
        
        result = router.route_query(test_query)
        
        if result.get('industry') == 'error':
            print(f"   ❌ Query failed: {result.get('error')}")
            return False
        
        companies_found = len(result.get('results', []))
        print(f"   ✅ Query successful: {companies_found} companies found")
        
        if companies_found == 0:
            print("   ⚠️  No companies found for email test")
            return True
        
        # Test email generation (without sending)
        print("   📝 Testing email content generation...")
        test_company = result['results'][0]
        
        # Generate contact email
        contact_email = router._generate_contact_email(test_company)
        contact_name = router._extract_contact_name(test_company)
        pain_points = router._identify_pain_points(test_company)
        
        print(f"      Company: {test_company.get('company_name')}")
        print(f"      Generated email: {contact_email}")
        print(f"      Contact name: {contact_name}")
        print(f"      Pain points: {len(pain_points)} identified")
        
        # Generate outreach content
        lead_data = {
            "contact_email": contact_email,
            "company_name": test_company.get('company_name'),
            "contact_name": contact_name,
            "industry": test_company.get('industry'),
            "pain_points": pain_points
        }
        
        outreach_content = router._generate_default_outreach_content(lead_data)
        
        print(f"      Subject: {outreach_content.get('email_subject', '')[:50]}...")
        print(f"      Email length: {len(outreach_content.get('personalized_email', ''))} characters")
        
        print("   ✅ Email content generation successful")
        return True
        
    except Exception as e:
        print(f"   ❌ IndustryRouter test failed: {str(e)}")
        return False

def test_email_sending_simulation():
    """Test email sending simulation (dry run)"""
    print("\n📤 Testing Email Sending Simulation...")
    
    try:
        from src.agents.industry_router import IndustryRouter
        
        router = IndustryRouter(enable_email=True)
        
        if not router.email_enabled:
            print("   ❌ Email not enabled, skipping send test")
            return False
        
        # Get a company to test with
        result = router.route_query({
            "industry": "technology",
            "limit": 1
        })
        
        if not result.get('results'):
            print("   ❌ No companies found for email test")
            return False
        
        print("   🎯 Found test company for email simulation")
        
        # Create test outreach content
        test_outreach = {
            "email_subject": "Test Email - Sales Forge Integration",
            "personalized_email": """Hi there,

This is a test email from the Sales Forge platform integration testing.

If you received this email, it means our Gmail integration is working correctly.

This is an automated test - please ignore this email.

Best regards,
Sales Forge Test System""",
            "value_proposition": "Testing Gmail integration",
            "call_to_action": "No action required - this is a test"
        }
        
        print("   📝 Test email content prepared")
        print("   ⚠️  This is a simulation - no actual email will be sent")
        
        # For safety, we'll simulate the email sending process
        print("   🔄 Simulating email send process...")
        
        companies = result['results']
        company = companies[0]
        
        # Generate all the data that would be used
        contact_email = router._generate_contact_email(company)
        contact_name = router._extract_contact_name(company)
        
        lead_data = {
            "contact_email": contact_email,
            "company_name": company.get('company_name'),
            "contact_name": contact_name,
            "industry": company.get('industry')
        }
        
        print(f"   📧 Would send to: {contact_email}")
        print(f"   📛 Contact name: {contact_name}")
        print(f"   🏢 Company: {lead_data['company_name']}")
        print(f"   📧 Subject: {test_outreach['email_subject']}")
        
        # This is where we would actually send the email:
        # send_result = router.gmail_client.send_sales_outreach_email(
        #     lead_data=lead_data,
        #     outreach_content=test_outreach,
        #     template_type="test"
        # )
        
        print("   ✅ Email simulation completed successfully")
        print("   💡 To actually send emails, modify this test and remove the simulation")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Email simulation failed: {str(e)}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n📚 Next Steps:")
    print("=" * 30)
    
    print("1. 🔐 Gmail OAuth Setup:")
    print("   • Run the demo script to complete OAuth flow")
    print("   • First run will open browser for Google authentication")
    print("   • Subsequent runs will use saved token")
    
    print("\n2. 🧪 Test Email Sending:")
    print("   • Run: python examples/email_outreach_demo.py")
    print("   • Start with test emails to your own email address")
    print("   • Verify email templates and content")
    
    print("\n3. 🚀 Production Integration:")
    print("   • Integrate router.route_and_email() into your workflows")
    print("   • Customize email templates in the GmailClient")
    print("   • Set up proper rate limiting for bulk emails")
    print("   • Monitor Gmail API quotas and limits")
    
    print("\n4. 📊 Monitoring:")
    print("   • Check router.get_statistics() for email metrics")
    print("   • Monitor Gmail sent folder for actual deliveries")
    print("   • Set up error logging for failed sends")

def main():
    """Run all integration tests"""
    print("🧪 Gmail Integration Test Suite")
    print("===============================")
    print(f"Started at: {datetime.now().isoformat()}")
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Database Connection", test_database_connection),
        ("Gmail Client Init", test_gmail_client_initialization),
        ("IndustryRouter + Email", test_industry_router_with_email),
        ("Email Simulation", test_email_sending_simulation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except KeyboardInterrupt:
            print(f"\n⏸️  Test interrupted by user")
            break
        except Exception as e:
            print(f"\n💥 {test_name}: CRASHED - {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📋 TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Gmail integration is ready to use.")
        show_next_steps()
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("\n💡 Common fixes:")
        print("   • Check your .env file configuration")
        print("   • Ensure client_secret.json is in the right location")
        print("   • Run the Supabase database setup if tables are missing")
        print("   • Install required packages: pip install google-api-python-client google-auth-oauthlib")
    
    print(f"\nTesting completed at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
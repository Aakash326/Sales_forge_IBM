#!/usr/bin/env python3
"""
Gmail Email Outreach Demo for Sales Forge Platform

This script demonstrates how to use the IndustryRouter with Gmail integration
to find companies and send personalized outreach emails.

Prerequisites:
1. Set up Gmail API credentials (client_secret.json)
2. Configure environment variables in .env file
3. Have Supabase database with company data

Usage:
    python examples/email_outreach_demo.py
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.industry_router import IndustryRouter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def demo_basic_email_outreach():
    """Demonstrate basic email outreach functionality"""
    print("🚀 Gmail Email Outreach Demo")
    print("=" * 50)
    
    try:
        # Initialize IndustryRouter with email enabled
        print("📧 Initializing IndustryRouter with Gmail integration...")
        router = IndustryRouter(enable_email=True)
        
        # Test connection first
        print("🔌 Testing connections...")
        connection_status = router.test_connection()
        
        if not connection_status['connected']:
            print(f"❌ Database connection failed: {connection_status.get('error')}")
            return False
        
        email_status = "✅ Enabled" if router.email_enabled else "❌ Disabled"
        print(f"   Database: ✅ Connected")
        print(f"   Gmail API: {email_status}")
        
        if not router.email_enabled:
            print("\n⚠️  Gmail integration not available. Check your credentials.")
            print("   Make sure you have:")
            print("   • client_secret.json file")
            print("   • GMAIL_CREDENTIALS_PATH in .env")
            return False
        
        print("\n📊 Running company queries and sending emails...")
        
        # Demo 1: Technology companies in California
        print("\n1️⃣ Finding tech companies in California...")
        tech_query = {
            "industry": "technology",
            "location": "CA",
            "limit": 2
        }
        
        # Custom outreach content for tech companies
        tech_outreach = {
            "email_subject": "AI & Technology Partnership Opportunity",
            "personalized_email": """Hi there,

I hope this message finds you well. I've been researching innovative technology companies in California, and your company caught my attention.

We're seeing incredible success helping tech companies like yours with:
• Advanced AI implementation strategies
• Cloud infrastructure optimization  
• Scalable development frameworks

Recent results with similar companies:
✓ 50% faster deployment cycles
✓ 75% reduction in infrastructure costs
✓ 90% improvement in system reliability

Would you be interested in a brief 20-minute discussion about how we could help accelerate your technology initiatives?

I'm available for a call this week.

Best regards,
Tech Solutions Team

P.S. I'd love to share how we helped a similar company reduce their cloud costs by $2M annually.""",
            "value_proposition": "AI implementation and cloud optimization",
            "call_to_action": "Schedule a 20-minute technology consultation"
        }
        
        result = router.route_and_email(
            input_data=tech_query,
            outreach_content=tech_outreach,
            template_type="tech_focused"
        )
        
        print_email_results("Tech Companies (CA)", result)
        
        # Demo 2: High-performance finance companies
        print("\n2️⃣ Finding high-performance finance companies...")
        finance_query = {
            "industry": "finance", 
            "min_performance": 90,
            "limit": 2
        }
        
        # Use default outreach content for finance
        result = router.route_and_email(
            input_data=finance_query,
            template_type="roi_focused"
        )
        
        print_email_results("Finance Companies (High Performance)", result)
        
        # Demo 3: Healthcare companies with custom targeting
        print("\n3️⃣ Finding healthcare companies...")
        healthcare_query = {
            "industry": "healthcare",
            "location": "NY", 
            "limit": 1
        }
        
        # Custom healthcare outreach
        healthcare_outreach = {
            "email_subject": "Healthcare Innovation Partnership",
            "personalized_email": """Hello,

I hope you're having a great day. I've been researching leading healthcare organizations, and I'm impressed by your commitment to patient care.

We specialize in helping healthcare organizations achieve:
• Enhanced patient data security
• Streamlined compliance processes
• Improved operational workflows

Our recent healthcare clients have seen:
✓ 40% reduction in compliance overhead
✓ 60% improvement in data processing speed
✓ 85% increase in patient satisfaction scores

Would you be open to a 15-minute conversation about optimizing your healthcare operations?

Looking forward to hearing from you.

Best regards,
Healthcare Solutions Team

P.S. We recently helped a similar organization save $500K annually in compliance costs.""",
            "value_proposition": "Healthcare compliance and operational optimization",
            "call_to_action": "Schedule a healthcare consultation"
        }
        
        result = router.route_and_email(
            input_data=healthcare_query,
            outreach_content=healthcare_outreach,
            template_type="strategic_proposal"
        )
        
        print_email_results("Healthcare Companies (NY)", result)
        
        # Show overall statistics
        print("\n📈 Overall Statistics:")
        stats = router.get_statistics()
        print(f"   Total queries: {stats['total_queries']}")
        print(f"   Success rate: {stats['success_rate']:.1f}%")
        print(f"   Emails sent: {stats.get('emails_sent', 0)}")
        print(f"   Email failures: {stats.get('email_failures', 0)}")
        print(f"   Avg response time: {stats['average_response_time_seconds']}s")
        
        print("\n✅ Email outreach demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False


def print_email_results(category: str, result: dict):
    """Print formatted results for email outreach"""
    
    query_data = result.get('query_metadata', {})
    email_data = result.get('email_results', {})
    
    print(f"   📋 {category}:")
    print(f"      Companies found: {query_data.get('total_results', 0)}")
    print(f"      Processing time: {result.get('processing_time', 'N/A')}")
    
    if email_data:
        sent = email_data.get('sent_count', 0)
        failed = email_data.get('failed_count', 0)
        success_rate = email_data.get('success_rate', 0)
        
        print(f"      Emails sent: {sent}")
        print(f"      Email failures: {failed}")
        print(f"      Email success rate: {success_rate:.1f}%")
        
        # Show first successful email
        results = email_data.get('results', [])
        successful_results = [r for r in results if r.get('success')]
        
        if successful_results:
            first_success = successful_results[0]
            company = first_success.get('company_name', 'Unknown')
            email = first_success.get('contact_email', 'Unknown')
            print(f"      ✉️  Sample: {company} ({email})")


def demo_individual_email_functions():
    """Demonstrate individual email-related functions"""
    print("\n🔧 Individual Function Demos")
    print("=" * 30)
    
    try:
        router = IndustryRouter(enable_email=True)
        
        if not router.email_enabled:
            print("❌ Gmail not enabled, skipping individual demos")
            return
        
        # Demo: Send emails to specific companies
        print("\n📤 Sending emails to specific companies...")
        
        # Get some companies first
        query_result = router.route_query({
            "industry": "technology",
            "limit": 1
        })
        
        if query_result.get('results'):
            companies = query_result['results']
            
            # Custom outreach for specific targeting
            custom_outreach = {
                "email_subject": "Exclusive Partnership Invitation",
                "personalized_email": "Hi there,\n\nSpecial invitation for an exclusive partnership opportunity.\n\nBest regards,\nPartnership Team"
            }
            
            # Send emails using the dedicated method
            email_result = router.send_outreach_emails(
                companies=companies,
                outreach_content=custom_outreach,
                template_type="strategic_proposal"
            )
            
            print(f"   Individual email sending:")
            print(f"   • Sent: {email_result.get('sent_count', 0)}")
            print(f"   • Failed: {email_result.get('failed_count', 0)}")
            print(f"   • Success rate: {email_result.get('success_rate', 0):.1f}%")
            
        else:
            print("   No companies found for individual demo")
            
        print("✅ Individual function demo completed!")
        
    except Exception as e:
        print(f"❌ Individual demo failed: {str(e)}")


def main():
    """Main demo function"""
    print("🎯 Sales Forge Gmail Integration Demo")
    print("====================================")
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Make sure your .env file is configured correctly")
        return
    
    # Check Gmail credentials
    gmail_creds_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'client_secret.json')
    if not os.path.exists(gmail_creds_path):
        print(f"⚠️  Gmail credentials not found at: {gmail_creds_path}")
        print("   Email functionality will be limited")
    
    print("✅ Prerequisites checked")
    
    # Run demos
    try:
        # Main email outreach demo
        success = demo_basic_email_outreach()
        
        if success:
            # Additional demos
            demo_individual_email_functions()
            
            print(f"\n🎉 All demos completed successfully!")
            print("\n📚 Next steps:")
            print("   • Review sent emails in your Gmail")
            print("   • Modify outreach templates for your use case")
            print("   • Integrate into your agent workflows")
            print("   • Set up automation for regular outreach")
        else:
            print(f"\n⚠️  Demo had issues. Check the output above.")
            
    except KeyboardInterrupt:
        print(f"\n⏸️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
    
    print(f"\nDemo completed at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
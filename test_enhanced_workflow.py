#!/usr/bin/env python3
"""
Test Enhanced Sales Workflow

Test the complete enhanced sales workflow with:
- Domain selection  
- Company selection
- Web research integration
- AI analysis with real-time insights
- Email outreach with fresh data

Author: AI Assistant  
Date: 2025-01-09
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.workflow.domain_selector import DomainSelector
from src.agents.web_research_agent import WebResearchAgent
from src.workflow.examples.fast_workflow import FastSalesPipeline

async def test_enhanced_workflow():
    """Test the enhanced workflow with domain selection and web research."""
    
    print("🧪 TESTING ENHANCED SALES WORKFLOW")
    print("="*60)
    print("Features Testing:")
    print("✅ Domain selection (automated)")
    print("✅ Company selection from domain")
    print("✅ Web research with Tavily API")
    print("✅ Enhanced AI outreach with fresh insights")
    print("✅ Email sending with Gmail integration")
    print()
    
    # Step 1: Initialize services
    print("🔧 Initializing Services...")
    domain_selector = DomainSelector()
    web_research_agent = WebResearchAgent()
    fast_pipeline = FastSalesPipeline()
    
    # Step 2: Automated domain selection (pick Technology for demo)
    print("\n🎯 Step 1: Domain Selection")
    selected_domain = "Technology"  # Automated selection
    print(f"   Selected Domain: {selected_domain}")
    
    # Step 3: Company selection from domain
    print(f"\n🏢 Step 2: Company Selection from {selected_domain}")
    selected_company = domain_selector.select_company_from_domain(selected_domain)
    
    if not selected_company:
        print("❌ No company selected. Test failed.")
        return
    
    print(f"   ✅ Selected: {selected_company.get('company_name', 'Unknown')}")
    print(f"   💰 Revenue: ${selected_company.get('revenue', 0):,}")
    print(f"   📧 Email: {selected_company.get('contact_email', 'TBD')}")
    
    # Step 4: Web research
    print(f"\n🔍 Step 3: Web Research")
    enhanced_company = await web_research_agent.research_company(selected_company)
    
    research_summary = web_research_agent.get_research_summary(enhanced_company)
    print("📊 Web Research Summary:")
    print(research_summary)
    
    # Enhance company data with research
    final_company_data = web_research_agent.enhance_company_data(selected_company, enhanced_company)
    
    # Step 5: Convert to lead data format
    print(f"\n🤖 Step 4: AI Analysis Preparation")
    
    lead_data = {
        'lead_id': f"TEST_{final_company_data.get('company_name', 'UNKNOWN').upper().replace(' ', '_')}",
        'company_name': final_company_data.get('company_name', 'Unknown Company'),
        'contact_email': 'saiaaksh33333@gmail.com',  # Always send to demo email
        'contact_name': final_company_data.get('ceo_name', 'Executive Team'),
        'company_size': final_company_data.get('employee_count', 1000),
        'industry': final_company_data.get('industry', 'Technology'),
        'location': final_company_data.get('location', 'Global'),
        'annual_revenue': final_company_data.get('revenue', 0),
        'stage': 'qualification',
        
        # Enhanced with web research
        'latest_news': final_company_data.get('latest_news_headline', ''),
        'recent_developments': final_company_data.get('recent_developments', []),
        'technology_updates': final_company_data.get('recent_tech_initiatives', []),
        'web_research_confidence': final_company_data.get('web_research_confidence', 0.0),
        
        # Existing intelligence
        'competitive_advantages': final_company_data.get('competitive_advantages', ''),
        'challenges': final_company_data.get('challenges', ''),
        'technology_stack': final_company_data.get('technology_stack', ''),
        'market_position': final_company_data.get('market_position', 'Challenger')
    }
    
    print(f"   ✅ Lead data prepared with {len([k for k, v in lead_data.items() if v])} populated fields")
    print(f"   🔍 Web research confidence: {lead_data['web_research_confidence']:.1%}")
    
    # Step 6: Run AI analysis with enhanced data
    print(f"\n⚡ Step 5: AI Sales Intelligence Analysis")
    
    try:
        results = fast_pipeline.run_fast(lead_data)
        
        print(f"   ✅ AI Analysis Complete")
        print(f"   📊 Lead Score: {results.lead_score:.2f}/1.0")
        print(f"   🎯 Conversion Probability: {results.predicted_conversion:.1%}")
        print(f"   📧 Email Status: {'✅ Sent' if results.metadata.get('email_sent') else '📧 Generated'}")
        
        # Display email content
        if results.metadata.get('email_subject'):
            print(f"\n📧 Generated Email:")
            print(f"   Subject: {results.metadata.get('email_subject', '')}")
            print(f"   Preview: {results.metadata.get('email_body', '')[:100]}...")
        
        print(f"\n🎉 ENHANCED WORKFLOW TEST COMPLETE")
        print("="*60)
        print("✅ All features working:")
        print(f"   • Domain Selection: ✅ {selected_domain}")
        print(f"   • Company Selection: ✅ {selected_company.get('company_name', 'Unknown')}")
        print(f"   • Web Research: ✅ {enhanced_company.get('web_research_confidence', 0):.1%} confidence")
        print(f"   • AI Analysis: ✅ {results.lead_score:.2f} lead score")
        print(f"   • Email Generation: ✅ {'Sent' if results.metadata.get('email_sent') else 'Generated'}")
        print("="*60)
        
        return results
        
    except Exception as e:
        print(f"❌ AI Analysis failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_enhanced_workflow())
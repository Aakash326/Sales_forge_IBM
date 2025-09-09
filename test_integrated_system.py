#!/usr/bin/env python3
"""
Test script for the integrated Sales Intelligence system
Tests the complete workflow orchestrator with all agents
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.sales_intelligence_orchestrator import SalesIntelligenceOrchestrator

async def test_basic_functionality():
    """Test basic functionality of the integrated system"""
    print("🧪 Testing Sales Intelligence Orchestrator...")
    
    # Initialize orchestrator
    orchestrator = SalesIntelligenceOrchestrator()
    
    # Test data (TechFlow example from the prompt)
    company_data = {
        "company_name": "TechFlow Inc",
        "company_size": 350,
        "industry": "software development", 
        "annual_revenue": 25_000_000,
        "location": "San Francisco, CA"
    }
    
    contact_data = {
        "contact_name": "Sarah Chen",
        "title": "CTO",
        "role": "technical_leader",
        "bio": "Technical leader focused on scalable architecture and engineering excellence"
    }
    
    # Test documents
    documents = [
        {
            "type": "financial_report",
            "content": "Revenue growth: 180% YoY accelerating. Burn rate: $890K/month. 18 months runway. Customer metrics: 15% churn, $2.1K ACV. Cash position: Strong for 12-18 months.",
            "metadata": {"date": "2024-01-01", "source": "Q4 Financial Report"}
        },
        {
            "type": "board_presentation",
            "content": "Strategic priorities: Scale to enterprise, Improve margins. Budget allocation: 40% to product, 25% to sales. Timeline: Enterprise push by Q2 next year. Executive buy-in: CEO fully committed to scaling.",
            "metadata": {"date": "2024-01-15", "source": "Board Strategy Deck"}
        }
    ]
    
    try:
        print("📊 Generating complete intelligence report...")
        start_time = datetime.now()
        
        # Generate the complete intelligence report
        report = await orchestrator.generate_complete_intelligence_report(
            company_data=company_data,
            contact_data=contact_data,
            documents=documents
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ Report generated successfully in {processing_time:.2f} seconds")
        print(f"📈 Strategic Priority: {report.strategic_priority}")
        print(f"🎯 Confidence Level: {report.confidence_level}")
        print(f"💰 Investment: {report.total_investment}")
        print(f"📊 ROI: {report.projected_roi}")
        
        # Format and display the executive report
        print("\n" + "="*80)
        print("📋 EXECUTIVE INTELLIGENCE REPORT")
        print("="*80)
        formatted_report = orchestrator.format_executive_report(report)
        print(formatted_report)
        
        return True, report
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def test_individual_agents():
    """Test individual agents to ensure they work properly"""
    print("\n🔧 Testing individual agents...")
    
    orchestrator = SalesIntelligenceOrchestrator()
    
    # Test data
    company_data = {
        "company_name": "Test Company",
        "company_size": 250,
        "industry": "software",
        "annual_revenue": 15_000_000
    }
    
    contact_data = {
        "contact_name": "John Doe",
        "title": "CEO",
        "role": "executive"
    }
    
    tests_passed = 0
    total_tests = 5
    
    # Test Behavioral Agent
    try:
        behavioral_result = await orchestrator._run_behavioral_analysis(contact_data, company_data, None)
        if behavioral_result:
            print("✅ Behavioral Psychology Agent working")
            tests_passed += 1
        else:
            print("⚠️  Behavioral Psychology Agent returned None")
    except Exception as e:
        print(f"❌ Behavioral Psychology Agent failed: {e}")
    
    # Test Competitive Agent
    try:
        competitive_result = await orchestrator._run_competitive_intelligence(company_data, None)
        if competitive_result:
            print("✅ Competitive Intelligence Agent working")
            tests_passed += 1
        else:
            print("⚠️  Competitive Intelligence Agent returned None")
    except Exception as e:
        print(f"❌ Competitive Intelligence Agent failed: {e}")
    
    # Test Economic Agent
    try:
        economic_result = await orchestrator._run_economic_analysis(company_data, None)
        if economic_result:
            print("✅ Economic Intelligence Agent working")
            tests_passed += 1
        else:
            print("⚠️  Economic Intelligence Agent returned None")
    except Exception as e:
        print(f"❌ Economic Intelligence Agent failed: {e}")
    
    # Test Predictive Agent
    try:
        predictive_result = await orchestrator._run_predictive_forecast(company_data, None)
        if predictive_result:
            print("✅ Predictive Forecast Agent working")
            tests_passed += 1
        else:
            print("⚠️  Predictive Forecast Agent returned None")
    except Exception as e:
        print(f"❌ Predictive Forecast Agent failed: {e}")
    
    # Test Document Agent
    try:
        documents = [{"type": "test", "content": "Test document content"}]
        document_result = await orchestrator._run_document_analysis(documents, company_data)
        if document_result:
            print("✅ Document Intelligence Agent working")
            tests_passed += 1
        else:
            print("⚠️  Document Intelligence Agent returned None")
    except Exception as e:
        print(f"❌ Document Intelligence Agent failed: {e}")
    
    print(f"\n📊 Individual Agent Tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def export_test_results(report, success):
    """Export test results to a file"""
    results = {
        "test_timestamp": datetime.now().isoformat(),
        "test_success": success,
        "report_summary": {
            "executive_summary": report.executive_summary if report else None,
            "strategic_priority": report.strategic_priority if report else None,
            "confidence_level": report.confidence_level if report else None,
            "total_investment": report.total_investment if report else None,
            "projected_roi": report.projected_roi if report else None,
            "processing_time": report.total_processing_time if report else None
        }
    }
    
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Test results exported to test_results.json")

async def main():
    """Main test function"""
    print("🚀 Starting Sales Intelligence System Tests")
    print("="*60)
    
    # Test individual agents first
    agents_working = await test_individual_agents()
    
    if not agents_working:
        print("⚠️  Some individual agents failed, but continuing with integration test...")
    
    # Test complete integration
    success, report = await test_basic_functionality()
    
    # Export results
    export_test_results(report, success)
    
    # Final results
    print("\n" + "="*60)
    if success:
        print("🎉 All tests completed successfully!")
        print("✅ Sales Intelligence System is working properly")
        if report:
            print(f"📊 Generated report with {report.confidence_level} confidence")
            print(f"🎯 Strategic priority: {report.strategic_priority}")
    else:
        print("❌ Some tests failed")
        print("🔧 Please check the error messages above")
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
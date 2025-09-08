#!/usr/bin/env python3
"""
Simple demo runner for Strategic Sales Intelligence Workflow
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append('.')

async def run_quick_demo():
    """Run a quick strategic workflow demo"""
    
    from src.workflow.examples.strategic_workflow import StrategicSalesWorkflow
    
    # Simple test prospect
    test_prospect = {
        "lead_id": "DEMO_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "cto@techflow.com", 
        "contact_name": "Sarah Chen",
        "company_size": 850,
        "industry": "Enterprise Software",
        "location": "Austin, TX",
        "annual_revenue": 75000000,  # $75M revenue
        "stage": "qualification"
    }
    
    print("🚀 Strategic Sales Intelligence Demo")
    print("=" * 50)
    print(f"Target: {test_prospect['company_name']}")
    print(f"Size: {test_prospect['company_size']} employees")
    print(f"Industry: {test_prospect['industry']}")
    print()
    
    try:
        workflow = StrategicSalesWorkflow()
        result = await workflow.run_complete_strategic_workflow(test_prospect)
        
        print("\n✅ Demo completed successfully!")
        return result
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(run_quick_demo())
import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
load_dotenv(os.path.join(project_root, '.env'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

from src.workflow.sales_pipeline import SalesPipeline
from src.workflow.states.lead_states import LeadState

def run_sample_workflow():
    """Run a sample sales pipeline workflow"""
    
    # Initialize the pipeline
    pipeline = SalesPipeline()
    
    # Sample lead data
    sample_lead = {
        "lead_id": "lead_123456",
        "company_name": "TechCorp Solutions",
        "contact_email": "john.doe@techcorp.com",
        "contact_name": "John Doe",
        "company_size": 250,
        "industry": "Software Technology",
        "location": "San Francisco, CA"
    }
    
    print(f"Starting sales pipeline for {sample_lead['company_name']}")
    
    # Run the workflow
    try:
        result = pipeline.run(sample_lead)
        
        print("\n=== Workflow Completed ===")
        print(f"Final Stage: {result.get('stage', 'Unknown')}")
        print(f"Lead Score: {result.get('lead_score', 0):.2f}")
        print(f"Engagement Level: {result.get('engagement_level', 0):.2f}")
        print(f"Qualification Score: {result.get('qualification_score', 0):.2f}")
        
        if result.get('assigned_rep'):
            print(f"Assigned Rep: {result['assigned_rep']}")
        
        # Display key insights
        if result.get('pain_points'):
            print(f"\nPain Points Identified: {', '.join(result['pain_points'])}")
        
        if result.get('recommended_approach'):
            print(f"Recommended Approach: {result['recommended_approach']}")
        
        return result
        
    except Exception as e:
        print(f"Workflow failed: {e}")
        return None

def run_multiple_leads():
    """Run workflow for multiple sample leads"""
    
    sample_leads = [
        {
            "lead_id": "lead_001",
            "company_name": "Enterprise Corp",
            "contact_email": "cto@enterprise.com",
            "contact_name": "Sarah Johnson",
            "company_size": 1500,
            "industry": "Financial Technology",
            "annual_revenue": 500_000_000
        },
        {
            "lead_id": "lead_002", 
            "company_name": "StartupInc",
            "contact_email": "founder@startup.com",
            "contact_name": "Mike Chen",
            "company_size": 25,
            "industry": "E-commerce",
            "annual_revenue": 2_000_000
        },
        {
            "lead_id": "lead_003",
            "company_name": "MidSize Manufacturing",
            "contact_email": "ops@midsize.com",
            "contact_name": "Lisa Rodriguez",
            "company_size": 400,
            "industry": "Manufacturing",
            "annual_revenue": 50_000_000
        }
    ]
    
    pipeline = SalesPipeline()
    results = []
    
    for lead_data in sample_leads:
        print(f"\n{'='*50}")
        print(f"Processing: {lead_data['company_name']}")
        print(f"{'='*50}")
        
        try:
            result = pipeline.run(lead_data)
            results.append(result)
            
            print(f"✅ Completed - Stage: {result.get('stage', 'Unknown')}")
            print(f"   Score: {result.get('lead_score', 0):.2f}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            results.append(None)
    
    # Summary
    print(f"\n{'='*50}")
    print("PIPELINE SUMMARY")
    print(f"{'='*50}")
    
    successful = [r for r in results if r is not None]
    print(f"Processed: {len(successful)}/{len(sample_leads)} leads")
    
    if successful:
        avg_score = sum(r.get('lead_score', 0) for r in successful) / len(successful)
        print(f"Average Lead Score: {avg_score:.2f}")
        
        # Stage distribution
        stages = {}
        for result in successful:
            stage = result.get('stage', 'unknown')
            stages[stage] = stages.get(stage, 0) + 1
        
        print("\nStage Distribution:")
        for stage, count in stages.items():
            print(f"  {stage}: {count}")
    
    return results

if __name__ == "__main__":
    print("Sales Pipeline Workflow Examples")
    print("=" * 40)
    
    # Run single lead example
    print("\n1. Single Lead Example:")
    run_sample_workflow()
    
    # Run multiple leads example
    print("\n\n2. Multiple Leads Example:")
    run_multiple_leads()

#!/usr/bin/env python3
"""
Simple test script for the sales pipeline without heavy dependencies
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_lead_state():
    """Test the LeadState model"""
    try:
        from src.workflow.states.lead_states import LeadState
        
        print("Testing LeadState creation...")
        
        # Create a lead state
        lead_data = {
            "lead_id": "test_123",
            "company_name": "Test Company",
            "contact_email": "test@testcompany.com",
            "contact_name": "John Doe",
            "company_size": 100,
            "industry": "Technology"
        }
        
        lead = LeadState(**lead_data)
        
        print(f"✅ Lead created successfully:")
        print(f"   Company: {lead.company_name}")
        print(f"   Contact: {lead.contact_name}")
        print(f"   Stage: {lead.stage}")
        print(f"   Score: {lead.lead_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing LeadState: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scoring_logic():
    """Test the scoring logic components"""
    try:
        from src.workflow.edges.scoring_logic import ScoringLogic
        from src.workflow.states.lead_states import LeadState
        
        print("\nTesting scoring logic...")
        
        scoring = ScoringLogic()
        
        # Create test lead
        lead = LeadState(
            lead_id="test_score",
            company_name="Test Corp",
            contact_email="test@test.com",
            company_size=500,
            industry="Technology",
            engagement_level=0.7
        )
        
        # Test scoring
        score = scoring._score_company_size(500)
        print(f"✅ Company size scoring works: {score}")
        
        industry_score = scoring._score_industry_fit("Technology")
        print(f"✅ Industry fit scoring works: {industry_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing scoring logic: {e}")
        return False

def test_conditional_routing():
    """Test the conditional routing logic"""
    try:
        from src.workflow.edges.conditional_routing import ConditionalRouter
        from src.workflow.states.lead_states import LeadState
        
        print("\nTesting conditional routing...")
        
        router = ConditionalRouter()
        
        # Create test lead
        lead = LeadState(
            lead_id="test_route",
            company_name="Test Corp",
            contact_email="test@test.com",
            research_completed=True,
            engagement_level=0.8
        )
        
        # Test routing
        route = router.route_after_research(lead)
        print(f"✅ Research routing works: {route}")
        
        route = router.route_after_outreach(lead)
        print(f"✅ Outreach routing works: {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing conditional routing: {e}")
        return False

def main():
    """Main test function"""
    
    print("Sales Forge - Core Components Test")
    print("=" * 40)
    
    tests = [
        test_lead_state,
        test_scoring_logic,
        test_conditional_routing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'=' * 40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All core components working correctly!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
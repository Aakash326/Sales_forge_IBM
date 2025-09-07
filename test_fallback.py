#!/usr/bin/env python3
"""
Test script that forces fallback mode for quick testing without API calls
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_fallback_pipeline():
    """Test pipeline in fallback mode"""
    
    # Temporarily disable API key to force fallback mode
    original_key = os.environ.get('OPENAI_API_KEY')
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        from src.workflow.sales_pipeline import SalesPipeline
        
        print("Sales Forge - Fallback Mode Test")
        print("=" * 40)
        
        # Initialize pipeline (will use fallback mode without API key)
        pipeline = SalesPipeline()
        
        # Sample lead data
        lead_data = {
            "lead_id": "test_fallback_123",
            "company_name": "Fallback Test Corp",
            "contact_email": "test@fallbacktest.com",
            "contact_name": "Test Contact",
            "company_size": 500,
            "industry": "Technology",
            "location": "San Francisco, CA"
        }
        
        print(f"Testing pipeline for {lead_data['company_name']}")
        
        # Run the workflow
        result = pipeline.run(lead_data)
        
        print("\n=== Fallback Test Results ===")
        print(f"Final Stage: {result.get('stage', 'Unknown')}")
        print(f"Lead Score: {result.get('lead_score', 0):.2f}")
        print(f"Engagement Level: {result.get('engagement_level', 0):.2f}")
        print(f"Research Completed: {result.get('research_completed', False)}")
        
        if result.get('pain_points'):
            print(f"Pain Points: {', '.join(result['pain_points'])}")
        
        if result.get('predicted_conversion'):
            print(f"Predicted Conversion: {result['predicted_conversion']:.2f}")
        
        if result.get('recommended_approach'):
            print(f"Recommended Approach: {result['recommended_approach']}")
        
        print("\n✅ Fallback pipeline test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in fallback test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restore original API key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key

def main():
    """Main test function"""
    
    success = test_fallback_pipeline()
    
    if success:
        print("\n🎉 All fallback tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
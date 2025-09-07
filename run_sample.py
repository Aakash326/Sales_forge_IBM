#!/usr/bin/env python3
"""
Sales Forge - Sample Workflow Runner

Run this script to test the sales pipeline with sample data.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Main entry point for running sample workflows"""
    
    try:
        from src.workflow.examples.sample_workflow import run_sample_workflow, run_multiple_leads
        
        print("Sales Forge - AI-Powered Sales Pipeline")
        print("=" * 50)
        
        print("\n🚀 Running single lead example...")
        result = run_sample_workflow()
        
        if result:
            print("\n✅ Single lead workflow completed successfully!")
        else:
            print("\n❌ Single lead workflow failed!")
            
        print("\n" + "="*50)
        print("🚀 Running multiple leads example...")
        results = run_multiple_leads()
        
        successful_count = sum(1 for r in results if r is not None)
        print(f"\n✅ Processed {successful_count}/{len(results)} leads successfully!")
        
    except Exception as e:
        print(f"❌ Error running sample workflows: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
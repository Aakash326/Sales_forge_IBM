#!/usr/bin/env python3
"""
Sales Forge - Fast Execution Options

Choose your speed vs depth preference:
1. Ultra-Fast (30 seconds) - Mathematical analysis
2. Fast (1-2 minutes) - AI-enhanced analysis  
3. Full Pipeline (10-20 minutes) - Complete AI crews
"""

import sys
import os
from datetime import datetime

def main():
    """Main menu for different pipeline speeds"""
    
    print("🚀 Sales Forge - Speed Options")
    print("=" * 40)
    print("1. ⚡ Ultra-Fast Analysis (30s)")
    print("2. 🔥 Fast AI Analysis (1-2m)")
    print("3. 📧 Medium Content Pipeline (3-5m)")
    print("4. 🤖 Full AI Pipeline (10-20m)")
    print("5. 📊 Test Core Components")
    print()
    
    choice = input("Select option (1-5): ").strip()
    
    if choice == "1":
        print("\n⚡ Starting Ultra-Fast Analysis...")
        os.system(f"python '{os.path.dirname(__file__)}/src/workflow/examples/ultra_fast_workflow.py'")
    
    elif choice == "2":
        print("\n🔥 Starting Fast AI Analysis...")
        os.system(f"python '{os.path.dirname(__file__)}/src/workflow/examples/fast_workflow.py'")
    
    elif choice == "3":
        print("\n📧 Starting Medium Content Pipeline...")
        os.system(f"python '{os.path.dirname(__file__)}/src/workflow/examples/medium_workflow.py'")
    
    elif choice == "4":
        print("\n🤖 Starting Full AI Pipeline...")
        os.system(f"python '{os.path.dirname(__file__)}/run_sample.py'")
    
    elif choice == "5":
        print("\n📊 Testing Core Components...")
        os.system(f"python '{os.path.dirname(__file__)}/test_simple.py'")
    
    else:
        print("Invalid choice. Please select 1-5.")
        return main()

if __name__ == "__main__":
    main()
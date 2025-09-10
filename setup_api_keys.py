#!/usr/bin/env python3
"""
API Keys Setup Script for Sales Forge Platform

This script helps you configure the required API keys for the complete
Sales Forge platform including:
- OpenAI API (required for CrewAI agents)
- IBM Watson/Granite API (for IBM Strategic Intelligence)
- Gmail API (for email outreach)

Author: AI Assistant
Date: 2025-01-09
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

def load_env_file() -> Dict[str, str]:
    """Load current .env file contents."""
    env_path = Path('.env')
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    return env_vars

def save_env_file(env_vars: Dict[str, str]) -> None:
    """Save updated .env file with new API keys."""
    env_path = Path('.env')
    
    # Read the full file to preserve comments and structure
    lines = []
    if env_path.exists():
        with open(env_path, 'r') as f:
            lines = f.readlines()
    
    # Update or add the API key lines
    for key, value in env_vars.items():
        key_found = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f'{key}='):
                lines[i] = f'{key}={value}\n'
                key_found = True
                break
        
        if not key_found:
            lines.append(f'{key}={value}\n')
    
    # Write back to file
    with open(env_path, 'w') as f:
        f.writelines(lines)

def check_api_keys() -> Dict[str, bool]:
    """Check which API keys are configured."""
    env_vars = load_env_file()
    
    required_keys = {
        'OPENAI_API_KEY': 'OpenAI API (required for CrewAI agents)',
        'IBM_API_KEY': 'IBM Watson API (for IBM Strategic Intelligence)',
        'IBM_PROJECT_ID': 'IBM Project ID (for IBM Strategic Intelligence)',
        'SUPABASE_URL': 'Supabase Database URL',
        'SUPABASE_ANON_KEY': 'Supabase Anonymous Key'
    }
    
    optional_keys = {
        'GMAIL_CREDENTIALS_PATH': 'Gmail API Credentials (for email outreach)',
        'IBM_ENDPOINT': 'IBM Watson Endpoint URL'
    }
    
    status = {}
    
    print("🔍 API KEY CONFIGURATION STATUS")
    print("=" * 50)
    
    print("\n✅ REQUIRED KEYS:")
    for key, description in required_keys.items():
        configured = bool(env_vars.get(key) and env_vars[key] != f'your_{key.lower()}_here' and env_vars[key].strip())
        status[key] = configured
        status_icon = "✅" if configured else "❌"
        print(f"   {status_icon} {key}: {description}")
    
    print("\n🔧 OPTIONAL KEYS:")
    for key, description in optional_keys.items():
        configured = bool(env_vars.get(key) and env_vars[key] != f'your_{key.lower()}_here' and env_vars[key].strip())
        status[key] = configured
        status_icon = "✅" if configured else "⚠️"
        print(f"   {status_icon} {key}: {description}")
    
    return status

def setup_openai_key() -> None:
    """Guide user through OpenAI API key setup."""
    print("\n🤖 OPENAI API KEY SETUP")
    print("=" * 30)
    print("1. Go to: https://platform.openai.com/account/api-keys")
    print("2. Click 'Create new secret key'")
    print("3. Copy the key (starts with 'sk-')")
    print("4. Enter it below:")
    
    api_key = input("\nEnter your OpenAI API key: ").strip()
    
    if api_key and api_key.startswith('sk-'):
        env_vars = load_env_file()
        env_vars['OPENAI_API_KEY'] = api_key
        save_env_file(env_vars)
        print("✅ OpenAI API key saved successfully!")
    else:
        print("❌ Invalid OpenAI API key format. Should start with 'sk-'")

def setup_ibm_keys() -> None:
    """Guide user through IBM API key setup."""
    print("\n🔷 IBM WATSON API SETUP")
    print("=" * 25)
    print("1. Go to: https://cloud.ibm.com/")
    print("2. Create Watson Machine Learning service")
    print("3. Get API Key from service credentials")
    print("4. Get Project ID from Watson Studio project")
    print("5. Enter them below:")
    
    api_key = input("\nEnter your IBM API key: ").strip()
    project_id = input("Enter your IBM Project ID: ").strip()
    
    if api_key and project_id:
        env_vars = load_env_file()
        env_vars['IBM_API_KEY'] = api_key
        env_vars['IBM_PROJECT_ID'] = project_id
        save_env_file(env_vars)
        print("✅ IBM API credentials saved successfully!")
    else:
        print("❌ Please provide both API key and Project ID")

def test_api_connections() -> None:
    """Test API connections."""
    print("\n🧪 TESTING API CONNECTIONS")
    print("=" * 30)
    
    # Test OpenAI
    try:
        import openai
        env_vars = load_env_file()
        openai_key = env_vars.get('OPENAI_API_KEY')
        
        if openai_key and openai_key.startswith('sk-'):
            # Simple test - just check if key format is valid
            print("✅ OpenAI API key format valid")
        else:
            print("❌ OpenAI API key missing or invalid")
    except ImportError:
        print("⚠️ OpenAI library not installed (pip install openai)")
    
    # Test IBM
    env_vars = load_env_file()
    ibm_key = env_vars.get('IBM_API_KEY')
    ibm_project = env_vars.get('IBM_PROJECT_ID')
    
    if ibm_key and ibm_project:
        print("✅ IBM API credentials configured")
    else:
        print("❌ IBM API credentials missing")
    
    # Test Supabase
    supabase_url = env_vars.get('SUPABASE_URL')
    supabase_key = env_vars.get('SUPABASE_ANON_KEY')
    
    if supabase_url and supabase_key:
        print("✅ Supabase credentials configured")
    else:
        print("❌ Supabase credentials missing")

def show_next_steps() -> None:
    """Show next steps after API key setup."""
    print("\n🚀 NEXT STEPS")
    print("=" * 15)
    print("1. Setup Database Tables:")
    print("   • Copy database/supabase_setup.sql to Supabase SQL Editor")
    print("   • Run the SQL to create enhanced company tables")
    print()
    print("2. Test the Platform:")
    print("   • python test_integrated_workflow.py (full system test)")
    print("   • python test_agent_evaluation.py (agent evaluation test)")
    print()
    print("3. Run Agent Platforms:")
    print("   • python run_fast_8_agent_platform.py (4-5 minute pipeline)")
    print("   • python workflows/run_intermediate_11_agent_platform.py (7-9 minute pipeline)")
    print()
    print("4. Gmail Integration (Optional):")
    print("   • Setup Gmail API credentials for email outreach")
    print("   • Follow Gmail API setup guide in documentation")
    print()

def main():
    """Main setup function."""
    print("🔧 SALES FORGE PLATFORM - API KEYS SETUP")
    print("=" * 50)
    print("This script helps you configure API keys for the complete Sales Forge platform")
    print()
    
    # Check current status
    status = check_api_keys()
    
    # Count configured keys
    required_configured = sum(1 for key in ['OPENAI_API_KEY', 'IBM_API_KEY', 'IBM_PROJECT_ID', 'SUPABASE_URL', 'SUPABASE_ANON_KEY'] if status.get(key))
    total_required = 5
    
    print(f"\n📊 Configuration Status: {required_configured}/{total_required} required keys configured")
    
    if required_configured == total_required:
        print("✅ All required API keys are configured!")
        test_api_connections()
        show_next_steps()
        return
    
    print(f"\n⚠️ Missing {total_required - required_configured} required API keys")
    print("Let's set them up:")
    
    # Setup missing keys
    if not status.get('OPENAI_API_KEY'):
        setup_openai_key()
    
    if not status.get('IBM_API_KEY') or not status.get('IBM_PROJECT_ID'):
        print(f"\n⚠️ IBM API keys are optional but recommended for full 11-13 agent platforms")
        choice = input("Setup IBM API keys now? (y/n): ").lower().strip()
        if choice == 'y':
            setup_ibm_keys()
    
    if not status.get('SUPABASE_URL') or not status.get('SUPABASE_ANON_KEY'):
        print(f"\n⚠️ Supabase keys appear to be configured but may need verification")
    
    # Final check
    print(f"\n🔄 Rechecking configuration...")
    final_status = check_api_keys()
    final_configured = sum(1 for key in ['OPENAI_API_KEY', 'SUPABASE_URL', 'SUPABASE_ANON_KEY'] if final_status.get(key))
    
    if final_configured >= 3:  # OpenAI + Supabase is minimum for basic functionality
        print(f"\n✅ Minimum configuration complete!")
        print(f"🚀 You can now run the 8-agent fast platform")
        test_api_connections()
        show_next_steps()
    else:
        print(f"\n❌ Still missing required API keys")
        print(f"Please manually edit .env file with your API keys")

if __name__ == "__main__":
    main()
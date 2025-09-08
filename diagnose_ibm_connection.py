#!/usr/bin/env python3
"""
IBM watsonx Connection Diagnostics
Helps troubleshoot connection issues with detailed error analysis
"""

import os
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ dotenv not available, install with: pip install python-dotenv")

def check_credentials():
    """Check if credentials are properly configured"""
    print("🔍 CREDENTIAL VERIFICATION")
    print("=" * 50)
    
    api_key = os.getenv('IBM_WATSONX_API_KEY')
    project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
    url = os.getenv('IBM_WATSONX_URL')
    
    issues = []
    
    if not api_key or api_key == 'your_watsonx_api_key_here':
        issues.append("❌ API Key not set or still has placeholder value")
    else:
        print(f"✅ API Key found: {api_key[:20]}...")
        
        # Check API key format
        if len(api_key) < 40:
            issues.append("⚠️ API Key seems too short (should be ~44 characters)")
        if not api_key.replace('-', '').replace('_', '').isalnum():
            issues.append("⚠️ API Key contains unexpected characters")
    
    if not project_id or project_id == 'your_watsonx_project_id_here':
        issues.append("❌ Project ID not set or still has placeholder value")
    else:
        print(f"✅ Project ID found: {project_id}")
        
        # Check project ID format (should be UUID-like)
        if len(project_id) != 36 or project_id.count('-') != 4:
            issues.append("⚠️ Project ID doesn't look like a valid UUID")
    
    if not url:
        issues.append("❌ URL not set")
    else:
        print(f"✅ URL: {url}")
    
    if issues:
        print("\n🚨 ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("\n✅ All credentials appear to be configured correctly")
        return True

def test_ibm_cloud_connection():
    """Test basic IBM Cloud connectivity"""
    print("\n🌐 IBM CLOUD CONNECTIVITY TEST")
    print("=" * 50)
    
    try:
        import requests
        
        # Test general connectivity to IBM Cloud
        print("📡 Testing connectivity to IBM Cloud...")
        response = requests.get("https://cloud.ibm.com", timeout=10)
        if response.status_code == 200:
            print("✅ IBM Cloud is accessible")
        else:
            print(f"⚠️ IBM Cloud returned status {response.status_code}")
        
        # Test watsonx URL
        url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        print(f"📡 Testing watsonx endpoint: {url}")
        response = requests.get(url, timeout=10)
        print(f"✅ watsonx endpoint responded with status {response.status_code}")
        
    except requests.RequestException as e:
        print(f"❌ Network connectivity issue: {e}")
        print("Check your internet connection")
        return False
    except ImportError:
        print("⚠️ requests library not available")
    
    return True

def test_watsonx_auth():
    """Test watsonx authentication step by step"""
    print("\n🔐 WATSONX AUTHENTICATION TEST")
    print("=" * 50)
    
    api_key = os.getenv('IBM_WATSONX_API_KEY')
    project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
    url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
    
    try:
        from ibm_watsonx_ai import Credentials
        
        print("📡 Step 1: Creating credentials object...")
        try:
            credentials = Credentials(url=url, api_key=api_key)
            print("✅ Credentials object created successfully")
        except Exception as e:
            print(f"❌ Failed to create credentials: {e}")
            return False
        
        print("📡 Step 2: Testing authentication...")
        try:
            # Try to access a simple endpoint to verify auth
            from ibm_watsonx_ai import APIClient
            client = APIClient(credentials)
            print("✅ API Client created successfully")
            
            # Try to get version info
            try:
                version_info = client.version
                print(f"✅ Connected to watsonx version: {version_info}")
            except Exception as version_error:
                print(f"⚠️ Could not get version info: {version_error}")
            
        except Exception as auth_error:
            print(f"❌ Authentication failed: {auth_error}")
            
            # Analyze the error
            error_str = str(auth_error).lower()
            if "401" in error_str or "unauthorized" in error_str:
                print("🔍 ANALYSIS: Authentication Error (401)")
                print("   Possible causes:")
                print("   • Invalid API key")
                print("   • API key expired or revoked")
                print("   • Account not properly set up for watsonx")
                print("   • Wrong region/URL")
            elif "404" in error_str:
                print("🔍 ANALYSIS: Resource Not Found (404)")
                print("   Possible causes:")
                print("   • Project ID is incorrect")
                print("   • Project doesn't exist or was deleted")
                print("   • Project is in a different region")
                print("   • User doesn't have access to the project")
            elif "403" in error_str or "forbidden" in error_str:
                print("🔍 ANALYSIS: Permission Error (403)")
                print("   Possible causes:")
                print("   • User doesn't have the required permissions")
                print("   • watsonx service not enabled in the account")
                print("   • Trial period expired")
            
            return False
    
    except ImportError as e:
        print(f"❌ IBM watsonx library not properly installed: {e}")
        print("Try: pip install ibm-watsonx-ai")
        return False
    
    return True

def test_model_availability():
    """Test if Granite models are available"""
    print("\n🤖 MODEL AVAILABILITY TEST")
    print("=" * 50)
    
    api_key = os.getenv('IBM_WATSONX_API_KEY')
    project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
    url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
    
    try:
        from ibm_watsonx_ai import APIClient, Credentials
        
        credentials = Credentials(url=url, api_key=api_key)
        client = APIClient(credentials)
        
        print("📡 Checking available foundation models...")
        try:
            # Get available models
            models = client.foundation_models.get_model_specs()
            
            granite_models = [m for m in models if 'granite' in m.get('model_id', '').lower()]
            
            if granite_models:
                print(f"✅ Found {len(granite_models)} Granite models:")
                for model in granite_models[:5]:  # Show first 5
                    model_id = model.get('model_id', 'Unknown')
                    print(f"   • {model_id}")
                if len(granite_models) > 5:
                    print(f"   ... and {len(granite_models) - 5} more")
            else:
                print("⚠️ No Granite models found")
                print("Available models:")
                for model in models[:5]:
                    model_id = model.get('model_id', 'Unknown')  
                    print(f"   • {model_id}")
            
        except Exception as model_error:
            print(f"❌ Could not list models: {model_error}")
            return False
            
    except Exception as e:
        print(f"❌ Error during model check: {e}")
        return False
    
    return True

def suggest_solutions():
    """Suggest solutions based on common issues"""
    print("\n💡 SUGGESTED SOLUTIONS")
    print("=" * 50)
    
    print("🔧 If authentication failed (401/404 errors):")
    print("   1. Double-check your API key and Project ID")
    print("   2. Make sure you copied them completely (no extra spaces)")
    print("   3. Verify you're using the correct region URL")
    print("   4. Check if your IBM Cloud account is properly verified")
    print("   5. Ensure watsonx service is enabled in your account")
    print()
    
    print("🔧 If project not found (404 errors):")
    print("   1. Go to https://dataplatform.cloud.ibm.com/projects")
    print("   2. Verify your project exists and you have access")
    print("   3. Copy the Project ID from the project's 'Manage' tab")
    print("   4. Make sure the project is in the same region as your URL")
    print()
    
    print("🔧 If permission errors (403 errors):")
    print("   1. Check if you have 'Editor' or 'Admin' role in the project")
    print("   2. Verify watsonx.ai service is provisioned")
    print("   3. Check if your trial/free tier limits are exceeded")
    print()
    
    print("🔧 General troubleshooting:")
    print("   1. Try creating a new API key")
    print("   2. Create a fresh watsonx project")
    print("   3. Verify your IBM Cloud account email is confirmed")
    print("   4. Check IBM Cloud status page for service issues")
    print()
    
    print("🆘 If nothing works:")
    print("   • The integration works in fallback mode without credentials")
    print("   • Use fallback mode for development and testing")
    print("   • Contact IBM Support for account-specific issues")

def main():
    """Main diagnostic function"""
    print("🩺 IBM watsonx Connection Diagnostics")
    print("=" * 60)
    print("This tool will help diagnose connection issues with IBM watsonx")
    print()
    
    # Step 1: Check credentials
    creds_ok = check_credentials()
    
    # Step 2: Test connectivity 
    if creds_ok:
        conn_ok = test_ibm_cloud_connection()
        
        # Step 3: Test authentication
        if conn_ok:
            auth_ok = test_watsonx_auth()
            
            # Step 4: Test models (if auth worked)
            if auth_ok:
                test_model_availability()
    
    # Always show suggestions
    suggest_solutions()
    
    print("\n📋 SUMMARY")
    print("=" * 50)
    print("If diagnostic tests passed:")
    print("   • Your IBM watsonx integration should work!")
    print("   • Run: python test_ibm_integration.py")
    print()
    print("If diagnostic tests failed:")
    print("   • Follow the suggested solutions above")
    print("   • Use fallback mode for development")
    print("   • The integration works without real credentials")

if __name__ == "__main__":
    main()
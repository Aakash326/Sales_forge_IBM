#!/usr/bin/env python3
"""
IBM watsonx Credentials Setup Guide
Interactive script to help you get and configure IBM watsonx credentials
"""

import os
import webbrowser
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🪨 IBM watsonx Credentials Setup Guide")
    print("=" * 50)
    print("This guide will help you set up IBM Granite LLMs integration")
    print()

def check_existing_credentials():
    """Check if credentials are already configured"""
    print("🔍 Checking existing configuration...")
    
    api_key = os.getenv('IBM_WATSONX_API_KEY')
    project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
    url = os.getenv('IBM_WATSONX_URL')
    
    if api_key and api_key != 'your_watsonx_api_key_here':
        print(f"   ✅ API Key: Configured ({api_key[:8]}...)")
    else:
        print(f"   ❌ API Key: Not configured")
    
    if project_id and project_id != 'your_watsonx_project_id_here':
        print(f"   ✅ Project ID: Configured ({project_id[:8]}...)")
    else:
        print(f"   ❌ Project ID: Not configured")
    
    if url and url != 'your_watsonx_url_here':
        print(f"   ✅ URL: {url}")
    else:
        print(f"   ❌ URL: Not configured")
    
    print()
    
    if api_key and project_id and url and \
       api_key != 'your_watsonx_api_key_here' and \
       project_id != 'your_watsonx_project_id_here':
        print("🎉 Credentials are already configured!")
        test_choice = input("Would you like to test the connection? (y/n): ").lower().strip()
        if test_choice == 'y':
            test_credentials()
        return True
    
    return False

def show_signup_instructions():
    """Show instructions for signing up to IBM Cloud"""
    print("📋 Step 1: Create IBM Cloud Account")
    print("=" * 40)
    print("If you don't have an IBM Cloud account:")
    print("1. Go to https://cloud.ibm.com")
    print("2. Click 'Create an account' (free tier available)")
    print("3. Complete the registration process")
    print("4. Verify your email address")
    print()
    
    open_browser = input("Would you like me to open IBM Cloud in your browser? (y/n): ").lower().strip()
    if open_browser == 'y':
        try:
            webbrowser.open('https://cloud.ibm.com')
            print("✅ Opening IBM Cloud in your browser...")
        except:
            print("❌ Couldn't open browser. Please visit: https://cloud.ibm.com")
    print()

def show_watsonx_setup_instructions():
    """Show watsonx setup instructions"""
    print("📋 Step 2: Set up watsonx Project")
    print("=" * 40)
    print("Once logged into IBM Cloud:")
    print("1. Navigate to the watsonx platform")
    print("2. Click 'Create project' or select an existing project")
    print("3. Choose 'Create an empty project'")
    print("4. Give your project a name (e.g., 'Sales Forge AI')")
    print("5. Select a storage service (IBM Cloud Object Storage)")
    print("6. Click 'Create'")
    print()
    
    print("🔑 Step 3: Get API Credentials")
    print("=" * 40)
    print("In your watsonx project:")
    print("1. Go to the 'Manage' tab")
    print("2. Click 'Access control'")
    print("3. Navigate to 'API keys'")
    print("4. Click 'New' to create an API key")
    print("5. Give it a name (e.g., 'Sales Forge Integration')")
    print("6. Copy the API key (you won't see it again!)")
    print("7. Also copy your Project ID from the project overview")
    print()

def collect_credentials():
    """Collect credentials from user"""
    print("📝 Step 4: Enter Your Credentials")
    print("=" * 40)
    
    api_key = input("Enter your IBM watsonx API key: ").strip()
    if not api_key:
        print("❌ API key cannot be empty")
        return None
    
    project_id = input("Enter your watsonx Project ID: ").strip()
    if not project_id:
        print("❌ Project ID cannot be empty")
        return None
    
    print("\n🌍 Select your region:")
    print("1. US South (Dallas) - https://us-south.ml.cloud.ibm.com")
    print("2. Europe (Frankfurt) - https://eu-de.ml.cloud.ibm.com")
    print("3. Asia Pacific (Tokyo) - https://jp-tok.ml.cloud.ibm.com")
    print("4. Europe (London) - https://eu-gb.ml.cloud.ibm.com")
    
    region_choice = input("Select region (1-4) [default: 1]: ").strip()
    
    region_urls = {
        '1': 'https://us-south.ml.cloud.ibm.com',
        '2': 'https://eu-de.ml.cloud.ibm.com', 
        '3': 'https://jp-tok.ml.cloud.ibm.com',
        '4': 'https://eu-gb.ml.cloud.ibm.com'
    }
    
    url = region_urls.get(region_choice, region_urls['1'])
    
    return {
        'api_key': api_key,
        'project_id': project_id,
        'url': url
    }

def update_env_file(credentials):
    """Update .env file with credentials"""
    print("\n💾 Updating .env file...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found. Please make sure you're in the project directory.")
        return False
    
    # Read current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update IBM credentials
    updated_lines = []
    for line in lines:
        if line.startswith('IBM_WATSONX_API_KEY='):
            updated_lines.append(f'IBM_WATSONX_API_KEY={credentials["api_key"]}\n')
        elif line.startswith('IBM_WATSONX_PROJECT_ID='):
            updated_lines.append(f'IBM_WATSONX_PROJECT_ID={credentials["project_id"]}\n')
        elif line.startswith('IBM_WATSONX_URL='):
            updated_lines.append(f'IBM_WATSONX_URL={credentials["url"]}\n')
        else:
            updated_lines.append(line)
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("✅ .env file updated successfully!")
    return True

def test_credentials():
    """Test the IBM watsonx connection"""
    print("\n🧪 Testing IBM watsonx Connection...")
    print("=" * 40)
    
    try:
        import sys
        sys.path.insert(0, 'src')
        
        from ibm_integrations.granite_client import create_granite_client
        
        # Create client with watsonx backend
        client = create_granite_client(
            model_name="granite-3.0-8b-instruct",
            backend="watsonx"
        )
        
        if client.backend == "watsonx":
            print("✅ watsonx backend initialized successfully")
            
            # Test simple generation
            print("🔄 Testing text generation...")
            response = client.generate(
                "Hello, this is a test of IBM Granite integration.",
                max_tokens=50
            )
            
            if response and response.content:
                print("✅ Text generation successful!")
                print(f"   Model: {response.model}")
                print(f"   Response: {response.content[:100]}...")
                print("🎉 IBM watsonx integration is working!")
                return True
            else:
                print("❌ Text generation failed")
                
        else:
            print(f"⚠️  Using fallback backend: {client.backend}")
            print("This might indicate credential issues")
            
    except ImportError:
        print("❌ IBM integration not properly installed")
        print("Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("Check your credentials and try again")
    
    return False

def show_next_steps():
    """Show what to do next"""
    print("\n🚀 Next Steps")
    print("=" * 40)
    print("Now that your credentials are configured:")
    print()
    print("1. Test the integration:")
    print("   python test_ibm_integration.py")
    print()
    print("2. Try the examples:")
    print("   python examples/granite_quickstart.py")
    print("   python examples/ibm_integration_demo.py")
    print()
    print("3. Start using IBM agents in your code:")
    print("   python examples/start_ibm_agents_guide.py")
    print()
    print("4. Read the documentation:")
    print("   Open IBM_INTEGRATION_README.md")
    print()

def show_cost_warning():
    """Show cost warning"""
    print("💰 Important Cost Information")
    print("=" * 40)
    print("⚠️  IBM watsonx is a paid service after free tier")
    print()
    print("Cost optimization tips:")
    print("• Start with smaller models (granite-3.0-2b-instruct)")
    print("• Set token limits in your .env file")
    print("• Monitor usage in IBM Cloud dashboard")
    print("• Use fallback mode for development/testing")
    print()
    print("Free tier includes some credits to get started.")
    print("Check IBM Cloud pricing for current rates.")
    print()

def main():
    """Main setup flow"""
    print_banner()
    
    # Check existing credentials
    if check_existing_credentials():
        show_next_steps()
        return
    
    print("🎯 Let's get you set up with IBM watsonx!")
    print()
    
    # Show cost warning first
    show_cost_warning()
    proceed = input("Do you want to continue with setup? (y/n): ").lower().strip()
    if proceed != 'y':
        print("Setup cancelled. You can run this script again anytime.")
        return
    
    # Guided setup
    show_signup_instructions()
    
    input("Press Enter when you have your IBM Cloud account ready...")
    
    show_watsonx_setup_instructions()
    
    input("Press Enter when you have your API key and Project ID...")
    
    # Collect credentials
    credentials = collect_credentials()
    if not credentials:
        print("❌ Setup incomplete. Please try again.")
        return
    
    # Update .env file
    if not update_env_file(credentials):
        return
    
    # Test connection
    print()
    test_choice = input("Would you like to test the connection now? (y/n): ").lower().strip()
    if test_choice == 'y':
        if test_credentials():
            print()
            show_next_steps()
        else:
            print()
            print("❌ Connection test failed. Please check your credentials.")
            print("You can run this setup script again to update them.")
    else:
        print()
        show_next_steps()

if __name__ == "__main__":
    main()
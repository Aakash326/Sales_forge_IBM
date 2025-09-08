#!/usr/bin/env python3
"""
IBM Integration Installation and Setup Script
Installs dependencies and tests the IBM Granite LLMs integration
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("🔧 Installing IBM Integration Requirements...")
    
    try:
        # Install main requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Main requirements installed successfully")
        
        # Try to install optional packages individually
        optional_packages = [
            "ibm-watsonx-ai>=1.2.0",
            "transformers>=4.36.0", 
            "torch>=2.0.0",
            "accelerate>=0.25.0"
        ]
        
        for package in optional_packages:
            try:
                print(f"Installing {package}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {package} installed")
                else:
                    print(f"⚠️  {package} installation failed - will use fallback mode")
            except subprocess.CalledProcessError:
                print(f"⚠️  {package} installation failed - will use fallback mode")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking Environment Configuration...")
    
    required_vars = [
        "IBM_WATSONX_API_KEY",
        "IBM_WATSONX_PROJECT_ID",
        "IBM_WATSONX_URL"
    ]
    
    optional_vars = [
        "WATSONX_ORCHESTRATE_WORKSPACE_ID",
        "WATSONX_ORCHESTRATE_API_KEY",
        "HF_TOKEN"
    ]
    
    print("Required variables (for production):")
    for var in required_vars:
        value = os.getenv(var)
        status = "✅ Set" if value else "⚠️  Not set (will use fallback mode)"
        print(f"  {var}: {status}")
    
    print("\nOptional variables:")
    for var in optional_vars:
        value = os.getenv(var)
        status = "✅ Set" if value else "⚪ Not set"
        print(f"  {var}: {status}")
    
    # Check if any production vars are set
    has_watsonx = any(os.getenv(var) for var in required_vars)
    
    if has_watsonx:
        print("\n✅ Production environment detected")
    else:
        print("\n📝 Development environment - using fallback mode")
        print("   To enable full functionality, set IBM watsonx environment variables")

def test_imports():
    """Test that all imports work"""
    print("\n🧪 Testing Imports...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Test core imports
        print("Testing Granite client...")
        from ibm_integrations.granite_client import create_granite_client
        print("✅ Granite client import successful")
        
        print("Testing Granite models...")
        from ibm_integrations.granite_models import GraniteModelRegistry
        print("✅ Granite models import successful")
        
        print("Testing ADK agent manager...")
        from ibm_integrations.adk_agent_manager import ADKAgentManager
        print("✅ ADK agent manager import successful")
        
        print("Testing watsonx ADK client...")
        from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client
        print("✅ watsonx ADK client import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🚀 Testing Basic Functionality...")
    
    try:
        from ibm_integrations.granite_client import create_granite_client
        from ibm_integrations.granite_models import GraniteModelRegistry
        
        # Test model registry
        registry = GraniteModelRegistry()
        stats = registry.get_model_stats()
        print(f"✅ Model registry loaded: {stats['total_models']} models available")
        
        # Test Granite client creation
        client = create_granite_client(
            model_name="granite-3.0-8b-instruct",
            backend="fallback"  # Use fallback mode for testing
        )
        print(f"✅ Granite client created with backend: {client.backend}")
        
        # Test simple generation
        response = client.generate(
            "Hello, this is a test of IBM Granite integration",
            max_tokens=50
        )
        print(f"✅ Text generation successful")
        print(f"   Model: {response.model}")
        print(f"   Response: {response.content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_adk_integration():
    """Test ADK integration"""
    print("\n🤖 Testing ADK Integration...")
    
    try:
        from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client
        from ibm_integrations.adk_agent_manager import ADKAgentManager
        from ibm_integrations.granite_client import create_granite_client
        
        # Create clients
        granite_client = create_granite_client(backend="fallback")
        adk_client = create_watsonx_adk_client(local_mode=True, granite_client=granite_client)
        
        print("✅ ADK client created successfully")
        
        # Test agent creation
        research_agent = adk_client.create_sales_research_agent()
        print(f"✅ Research agent created: {research_agent.name}")
        
        # Test agent manager
        manager = ADKAgentManager(granite_client=granite_client)
        status = manager.get_agent_status()
        print(f"✅ Agent manager status: {status['basic_agents']} basic agents")
        
        return True
        
    except Exception as e:
        print(f"❌ ADK integration test failed: {e}")
        return False

def create_sample_env_file():
    """Create sample environment file"""
    print("\n📝 Creating Sample Environment File...")
    
    env_content = """# IBM watsonx Configuration
# Get these from https://cloud.ibm.com -> watsonx
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# watsonx Orchestrate Configuration (optional)
# Get these from watsonx Orchestrate workspace
WATSONX_ORCHESTRATE_WORKSPACE_ID=your_workspace_id_here
WATSONX_ORCHESTRATE_API_KEY=your_orchestrate_api_key_here

# Optional: Hugging Face token for direct model access
HF_TOKEN=your_huggingface_token_here

# Application Settings
LOG_LEVEL=INFO
ENABLE_SAFETY_CHECKS=true
DEFAULT_MODEL=granite-3.0-8b-instruct
"""
    
    env_file = Path(".env.example")
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Sample environment file created: {env_file}")
    print("   Copy .env.example to .env and add your credentials")

def main():
    """Main installation and setup"""
    print("🚀 IBM Granite LLMs & watsonx ADK Integration Setup")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Installation failed. Please check error messages above.")
        return False
    
    # Step 2: Check environment
    check_environment()
    
    # Step 3: Test imports
    if not test_imports():
        print("❌ Import tests failed. Please check installation.")
        return False
    
    # Step 4: Test basic functionality
    if not test_basic_functionality():
        print("❌ Basic functionality tests failed.")
        return False
    
    # Step 5: Test ADK integration
    if not test_adk_integration():
        print("❌ ADK integration tests failed.")
        return False
    
    # Step 6: Create sample environment file
    create_sample_env_file()
    
    # Success message
    print("\n🎉 IBM Integration Setup Complete!")
    print("=" * 60)
    print("\n📚 Next Steps:")
    print("   1. Copy .env.example to .env and add your IBM watsonx credentials")
    print("   2. Run: python examples/granite_quickstart.py")
    print("   3. Run: python examples/ibm_integration_demo.py") 
    print("   4. Explore: python examples/adk_agents_demo.py")
    print("   5. Configure: python examples/configuration_guide.py")
    
    print("\n💡 Current Status:")
    print("   ✅ Integration installed and working in fallback mode")
    print("   ⚠️  Add IBM watsonx credentials for full functionality")
    print("   📖 Check IBM_INTEGRATION_README.md for detailed documentation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
IBM Integration Configuration Guide
Shows how to configure Granite LLMs and watsonx ADK for production use
"""

import os
import json
from pathlib import Path

def show_environment_variables():
    """Show required environment variables"""
    print("🔧 Environment Variables Configuration")
    print("=" * 50)
    
    required_vars = {
        "IBM_WATSONX_API_KEY": "Your IBM watsonx API key",
        "IBM_WATSONX_PROJECT_ID": "Your watsonx project ID", 
        "IBM_WATSONX_URL": "watsonx URL (default: https://us-south.ml.cloud.ibm.com)",
        "WATSONX_ORCHESTRATE_WORKSPACE_ID": "Your watsonx Orchestrate workspace ID",
        "WATSONX_ORCHESTRATE_API_KEY": "Your watsonx Orchestrate API key"
    }
    
    optional_vars = {
        "HF_TOKEN": "Hugging Face token for direct model access",
        "IBM_CLOUD_API_KEY": "IBM Cloud API key for additional services"
    }
    
    print("📋 Required Environment Variables:")
    print("-" * 40)
    
    for var, description in required_vars.items():
        current_value = os.getenv(var)
        status = "✅ Set" if current_value else "❌ Not set"
        print(f"{var:<35} {status}")
        print(f"  Description: {description}")
        if current_value:
            masked_value = current_value[:8] + "..." if len(current_value) > 8 else current_value
            print(f"  Current value: {masked_value}")
        print()
    
    print("📋 Optional Environment Variables:")
    print("-" * 40)
    
    for var, description in optional_vars.items():
        current_value = os.getenv(var)
        status = "✅ Set" if current_value else "⚪ Optional"
        print(f"{var:<35} {status}")
        print(f"  Description: {description}")
        print()

def show_configuration_files():
    """Show configuration file examples"""
    print("📁 Configuration Files")
    print("=" * 50)
    
    # watsonx configuration
    watsonx_config = {
        "watsonx": {
            "url": "https://us-south.ml.cloud.ibm.com",
            "api_key": "${IBM_WATSONX_API_KEY}",
            "project_id": "${IBM_WATSONX_PROJECT_ID}"
        },
        "models": {
            "default_model": "granite-3.0-8b-instruct",
            "fallback_model": "granite-3.0-2b-instruct",
            "safety_model": "granite-guardian-3.0-2b"
        },
        "features": {
            "enable_safety": True,
            "enable_function_calling": True,
            "enable_rag": True
        }
    }
    
    print("📄 config/watsonx_config.json")
    print(json.dumps(watsonx_config, indent=2))
    print()
    
    # ADK configuration
    adk_config = {
        "adk": {
            "workspace_id": "${WATSONX_ORCHESTRATE_WORKSPACE_ID}",
            "api_key": "${WATSONX_ORCHESTRATE_API_KEY}",
            "region": "us-south",
            "local_mode": False
        },
        "agents": {
            "research_agent": {
                "model": "granite-3.0-8b-instruct",
                "temperature": 0.3,
                "max_tokens": 2048
            },
            "scoring_agent": {
                "model": "granite-3.0-2b-instruct", 
                "temperature": 0.2,
                "max_tokens": 1536
            },
            "outreach_agent": {
                "model": "granite-3.0-8b-instruct",
                "temperature": 0.7,
                "max_tokens": 2048
            }
        }
    }
    
    print("📄 config/adk_config.json")
    print(json.dumps(adk_config, indent=2))
    print()

def show_setup_instructions():
    """Show step-by-step setup instructions"""
    print("🚀 Setup Instructions")
    print("=" * 50)
    
    steps = [
        {
            "title": "1. IBM Cloud Account Setup",
            "instructions": [
                "Create an IBM Cloud account at https://cloud.ibm.com",
                "Navigate to the watsonx platform",
                "Create a new watsonx project",
                "Copy your API key and project ID"
            ]
        },
        {
            "title": "2. watsonx Orchestrate Setup", 
            "instructions": [
                "Access watsonx Orchestrate from IBM Cloud",
                "Create or access your workspace",
                "Generate API credentials",
                "Note your workspace ID"
            ]
        },
        {
            "title": "3. Environment Configuration",
            "instructions": [
                "Create a .env file in your project root",
                "Add all required environment variables",
                "Source the .env file or restart your terminal",
                "Verify variables are loaded correctly"
            ]
        },
        {
            "title": "4. Install Dependencies",
            "instructions": [
                "pip install ibm-watsonx-ai>=1.2.0",
                "pip install ibm-watsonx-orchestrate-adk>=1.0.0",
                "pip install transformers>=4.36.0 torch>=2.0.0",
                "Verify installations with import tests"
            ]
        },
        {
            "title": "5. Test Configuration",
            "instructions": [
                "Run: python examples/granite_quickstart.py",
                "Run: python examples/ibm_integration_demo.py",
                "Check logs for any configuration issues",
                "Verify all backends are working"
            ]
        }
    ]
    
    for step in steps:
        print(f"📋 {step['title']}")
        print("-" * 40)
        for instruction in step['instructions']:
            print(f"   • {instruction}")
        print()

def show_model_selection_guide():
    """Show model selection guide"""
    print("🎯 Model Selection Guide")
    print("=" * 50)
    
    model_recommendations = {
        "Research & Analysis": {
            "model": "granite-3.0-8b-instruct",
            "reason": "Best balance of capability and cost for complex analysis",
            "use_cases": ["Company research", "Market analysis", "Competitive intelligence"],
            "cost_tier": "Medium"
        },
        "Lead Scoring": {
            "model": "granite-3.0-2b-instruct", 
            "reason": "Fast and cost-effective for classification tasks",
            "use_cases": ["Lead qualification", "Quick scoring", "Priority ranking"],
            "cost_tier": "Low"
        },
        "Content Generation": {
            "model": "granite-3.0-8b-instruct",
            "reason": "Superior language capabilities for personalized content",
            "use_cases": ["Email outreach", "LinkedIn messages", "Proposal writing"],
            "cost_tier": "Medium"
        },
        "Code & Technical": {
            "model": "granite-code-8b-instruct",
            "reason": "Specialized for technical and coding tasks",
            "use_cases": ["API integration", "Script generation", "Technical documentation"],
            "cost_tier": "Medium"
        },
        "Real-time Processing": {
            "model": "granite-3.0-1b-a400m",
            "reason": "Ultra-fast inference for real-time applications",
            "use_cases": ["Chatbots", "Instant recommendations", "Live scoring"],
            "cost_tier": "Low"
        },
        "Safety & Moderation": {
            "model": "granite-guardian-3.0-2b",
            "reason": "Specialized safety model for content moderation",
            "use_cases": ["Content filtering", "Risk assessment", "Compliance checks"],
            "cost_tier": "Low"
        }
    }
    
    print("📊 Model Recommendations by Use Case:")
    print("-" * 60)
    
    for use_case, info in model_recommendations.items():
        print(f"\n🎯 {use_case}")
        print(f"   Recommended Model: {info['model']}")
        print(f"   Reason: {info['reason']}")
        print(f"   Cost Tier: {info['cost_tier']}")
        print(f"   Use Cases: {', '.join(info['use_cases'])}")

def show_deployment_options():
    """Show deployment configuration options"""
    print("🏗️ Deployment Options")
    print("=" * 50)
    
    deployment_configs = {
        "Development": {
            "description": "Local development with fallback modes",
            "config": {
                "backend": "fallback",
                "local_mode": True,
                "enable_safety": False,
                "cost_optimization": "maximum"
            },
            "pros": ["No API costs", "Fast iteration", "Works offline"],
            "cons": ["Limited capabilities", "Mock responses only"]
        },
        "Testing": {
            "description": "Hybrid setup with watsonx API and local ADK",
            "config": {
                "backend": "watsonx",
                "local_mode": True,
                "enable_safety": True,
                "cost_optimization": "balanced"
            },
            "pros": ["Real model responses", "Cost controlled", "Full feature testing"],
            "cons": ["Requires API keys", "Network dependent"]
        },
        "Production": {
            "description": "Full cloud deployment with watsonx Orchestrate",
            "config": {
                "backend": "watsonx",
                "local_mode": False,
                "enable_safety": True,
                "cost_optimization": "performance"
            },
            "pros": ["Full capabilities", "Scalable", "Team collaboration"],
            "cons": ["Higher costs", "More complex setup"]
        }
    }
    
    print("📋 Deployment Configuration Options:")
    print("-" * 50)
    
    for env, info in deployment_configs.items():
        print(f"\n🏷️  {env} Environment")
        print(f"   Description: {info['description']}")
        print(f"   Configuration:")
        for key, value in info['config'].items():
            print(f"     {key}: {value}")
        print(f"   Pros: {', '.join(info['pros'])}")
        print(f"   Cons: {', '.join(info['cons'])}")

def show_troubleshooting_guide():
    """Show troubleshooting guide"""
    print("🔍 Troubleshooting Guide")
    print("=" * 50)
    
    common_issues = {
        "Authentication Failed": {
            "symptoms": ["401 Unauthorized errors", "Invalid credentials messages"],
            "causes": ["Expired API key", "Wrong project ID", "Incorrect URL"],
            "solutions": [
                "Verify IBM_WATSONX_API_KEY is correct",
                "Check IBM_WATSONX_PROJECT_ID matches your project",
                "Ensure IBM_WATSONX_URL is correct for your region",
                "Regenerate API key if expired"
            ]
        },
        "Model Not Available": {
            "symptoms": ["Model not found errors", "Unsupported model messages"],
            "causes": ["Model not deployed in region", "Typo in model name", "Model deprecated"],
            "solutions": [
                "Check available models in your watsonx instance",
                "Verify model name spelling (e.g., granite-3.0-8b-instruct)", 
                "Use fallback models if primary unavailable",
                "Check model availability in your region"
            ]
        },
        "ADK Connection Issues": {
            "symptoms": ["ADK client initialization fails", "Workspace not found"],
            "causes": ["Wrong workspace ID", "Insufficient permissions", "Network issues"],
            "solutions": [
                "Verify WATSONX_ORCHESTRATE_WORKSPACE_ID is correct",
                "Check user permissions for watsonx Orchestrate",
                "Test network connectivity to IBM Cloud",
                "Use local_mode=True for development"
            ]
        },
        "Performance Issues": {
            "symptoms": ["Slow response times", "Timeout errors", "High costs"],
            "causes": ["Large model selection", "High token limits", "Inefficient prompts"],
            "solutions": [
                "Use smaller models for simple tasks (granite-3.0-2b-instruct)",
                "Reduce max_tokens parameter",
                "Optimize prompts for clarity and brevity",
                "Implement caching for repeated requests"
            ]
        }
    }
    
    print("🚨 Common Issues and Solutions:")
    print("-" * 50)
    
    for issue, details in common_issues.items():
        print(f"\n⚠️  {issue}")
        print(f"   Symptoms: {', '.join(details['symptoms'])}")
        print(f"   Likely causes: {', '.join(details['causes'])}")
        print(f"   Solutions:")
        for solution in details['solutions']:
            print(f"     • {solution}")

def create_sample_env_file():
    """Create a sample .env file"""
    print("📝 Sample .env File")
    print("=" * 50)
    
    env_content = """# IBM watsonx Configuration
IBM_WATSONX_API_KEY=your_watsonx_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# watsonx Orchestrate Configuration  
WATSONX_ORCHESTRATE_WORKSPACE_ID=your_workspace_id_here
WATSONX_ORCHESTRATE_API_KEY=your_orchestrate_api_key_here

# Optional: Hugging Face (for direct model access)
HF_TOKEN=your_huggingface_token_here

# Optional: IBM Cloud
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here

# Application Settings
LOG_LEVEL=INFO
ENABLE_SAFETY_CHECKS=true
DEFAULT_MODEL=granite-3.0-8b-instruct
FALLBACK_MODEL=granite-3.0-2b-instruct"""
    
    print("📄 Copy this to your .env file:")
    print("-" * 40)
    print(env_content)
    print()
    
    # Write to file
    env_file = Path(__file__).parent.parent / ".env.example"
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Sample .env file created at: {env_file}")

def main():
    """Main configuration guide"""
    print("🔧 IBM Integration Configuration Guide")
    print("=" * 60)
    print()
    
    show_environment_variables()
    show_configuration_files()
    show_setup_instructions()
    show_model_selection_guide()
    show_deployment_options()
    show_troubleshooting_guide()
    create_sample_env_file()
    
    print("\n🎉 Configuration Guide Complete!")
    print("\n📚 Additional Resources:")
    print("   • IBM watsonx Documentation: https://www.ibm.com/docs/en/watsonx-as-a-service")
    print("   • watsonx Orchestrate ADK: https://github.com/IBM/ibm-watsonx-orchestrate-adk")
    print("   • Granite Models: https://huggingface.co/ibm-granite")

if __name__ == "__main__":
    main()
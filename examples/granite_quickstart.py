#!/usr/bin/env python3
"""
IBM Granite LLMs Quick Start Guide
Simple examples to get started with Granite models
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ibm_integrations.granite_client import create_granite_client
from ibm_integrations.granite_models import GraniteModelRegistry

def basic_granite_example():
    """Basic Granite LLM usage example"""
    print("🪨 Basic Granite LLM Example")
    print("=" * 40)
    
    # Create Granite client (will use fallback mode if watsonx not configured)
    client = create_granite_client(
        model_name="granite-3.0-8b-instruct",
        backend="watsonx"  # Will fallback to simulation mode
    )
    
    # Simple text generation
    prompt = "Explain the benefits of using IBM Granite models for enterprise AI"
    response = client.generate(prompt, max_tokens=512, temperature=0.7)
    
    print(f"Model: {response.model}")
    print(f"Backend: {response.backend}")
    print(f"Response:\n{response.content}")
    print(f"Tokens used: {response.tokens_used}")
    print()

def chat_interface_example():
    """Chat interface example"""
    print("💬 Chat Interface Example")
    print("=" * 40)
    
    client = create_granite_client(model_name="granite-3.0-8b-instruct")
    
    # Chat conversation
    messages = [
        {"role": "system", "content": "You are a helpful B2B sales assistant."},
        {"role": "user", "content": "How do I qualify enterprise leads effectively?"},
        {"role": "assistant", "content": "To qualify enterprise leads effectively, use frameworks like BANT..."},
        {"role": "user", "content": "What's the best way to personalize outreach?"}
    ]
    
    response = client.chat(messages, max_tokens=512)
    
    print("Chat Response:")
    print(response.content)
    print()

def template_example():
    """Template-based generation example"""
    print("📝 Template Example")
    print("=" * 40)
    
    client = create_granite_client(model_name="granite-3.0-8b-instruct")
    
    # Research template
    template_vars = {
        "company_name": "Acme Corp",
        "context": "Technology consulting firm looking to expand AI capabilities"
    }
    
    response = client.generate_with_template(
        template_type="research",
        template_vars=template_vars,
        max_tokens=1024,
        temperature=0.3
    )
    
    print("Research Analysis:")
    print(response.content)
    print()

def model_selection_example():
    """Model selection example"""
    print("🎯 Model Selection Example")
    print("=" * 40)
    
    registry = GraniteModelRegistry()
    
    # Show available models
    stats = registry.get_model_stats()
    print(f"Available models: {stats['total_models']}")
    print(f"Model families: {stats['families']}")
    print(f"Supported backends: {stats['backends']}")
    print()
    
    # Get recommendations for different tasks
    tasks = ["research", "scoring", "outreach", "code"]
    
    for task in tasks:
        recommended_model = registry.get_recommended_model(task, backend="watsonx")
        print(f"Best model for {task}: {recommended_model}")
    
    print()

def safety_example():
    """Content safety example"""
    print("🛡️ Safety Example")
    print("=" * 40)
    
    client = create_granite_client(
        model_name="granite-3.0-8b-instruct",
        enable_safety=True
    )
    
    # Generate content and check safety
    prompt = "Write a professional email to a potential client about our new AI product"
    response = client.generate(prompt, max_tokens=512)
    
    print("Generated content:")
    print(response.content[:200] + "...")
    print(f"Safety check - Is safe: {response.is_safe()}")
    
    if response.safety_check:
        print(f"Risk level: {response.safety_check.get('risk_level', 'unknown')}")
    
    print()

async def function_calling_example():
    """Function calling example"""
    print("🔧 Function Calling Example")
    print("=" * 40)
    
    client = create_granite_client(
        model_name="granite-3.0-8b-instruct",
        enable_function_calling=True
    )
    
    # Define available tools
    tools = [
        {
            "name": "get_company_info",
            "description": "Get company information and business details",
            "parameters": {
                "company_name": "string",
                "include_financials": "boolean"
            }
        }
    ]
    
    messages = [
        {"role": "user", "content": "I need information about IBM including their financial data"}
    ]
    
    response = client.chat_with_tools(
        messages=messages,
        tools=tools,
        max_tokens=512
    )
    
    print("Response:")
    print(response.content)
    
    if response.function_call:
        print(f"\nFunction called: {response.function_call['name']}")
        print(f"Parameters: {response.function_call['parameters']}")
    
    print()

def cost_optimization_example():
    """Cost optimization example"""
    print("💰 Cost Optimization Example")
    print("=" * 40)
    
    registry = GraniteModelRegistry()
    
    # Show cost-effective model choices
    print("Cost-effective model recommendations:")
    
    task_configs = [
        ("research", "high", "For comprehensive company analysis"),
        ("scoring", "low", "For quick lead qualification"), 
        ("outreach", "medium", "For personalized campaign creation"),
        ("ultra_fast", "low", "For real-time processing")
    ]
    
    for task, cost_tier, description in task_configs:
        # Get models by cost tier and capability
        available_models = []
        for model_name, model_info in registry.models.items():
            if (task in model_info.use_cases or 
                task == "ultra_fast" and "ultra_fast" in model_info.use_cases) and \
               model_info.cost_tier == cost_tier:
                available_models.append(model_name)
        
        if available_models:
            recommended = available_models[0]
            model_info = registry.models[recommended]
            print(f"  {task.upper()}: {recommended}")
            print(f"    Cost tier: {model_info.cost_tier}")
            print(f"    Use case: {description}")
            print(f"    Max tokens: {model_info.max_tokens}")
            print()

def main():
    """Run all examples"""
    print("🚀 IBM Granite LLMs Quick Start Examples")
    print("=" * 50)
    print()
    
    # Basic examples
    basic_granite_example()
    chat_interface_example()
    template_example()
    model_selection_example()
    safety_example()
    cost_optimization_example()
    
    # Async example
    print("Running async function calling example...")
    asyncio.run(function_calling_example())
    
    print("✅ All examples completed!")
    print("\nNext Steps:")
    print("1. Configure IBM watsonx credentials for full functionality")
    print("2. Explore the comprehensive demo: python examples/ibm_integration_demo.py")
    print("3. Check out the ADK agents in examples/adk_agents_demo.py")

if __name__ == "__main__":
    main()
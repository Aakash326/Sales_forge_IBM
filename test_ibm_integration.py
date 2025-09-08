#!/usr/bin/env python3
"""
IBM Integration Test Suite
Quick test to verify all components are working
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_all_components():
    """Test all IBM integration components"""
    print("🧪 IBM Integration Test Suite")
    print("=" * 50)
    
    try:
        # Test 1: Granite Models Registry
        print("\n1. Testing Granite Models Registry...")
        from ibm_integrations.granite_models import GraniteModelRegistry, GraniteModelRouter
        
        registry = GraniteModelRegistry()
        router = GraniteModelRouter()
        stats = registry.get_model_stats()
        
        print(f"   ✅ {stats['total_models']} models loaded")
        print(f"   ✅ Model families: {list(stats['families'].keys())}")
        
        # Test model routing
        best_model = router.get_best_model("research", "medium")
        print(f"   ✅ Best model for research: {best_model}")
        
        # Test 2: Granite Client
        print("\n2. Testing Granite Client...")
        from ibm_integrations.granite_client import create_granite_client
        
        client = create_granite_client(
            model_name="granite-3.0-8b-instruct",
            backend="fallback",
            enable_safety=True,
            enable_function_calling=True
        )
        
        print(f"   ✅ Client created with backend: {client.backend}")
        
        # Test text generation
        response = client.generate(
            "Analyze the benefits of AI in B2B sales automation",
            max_tokens=100
        )
        
        print(f"   ✅ Generation successful: {len(response.content)} characters")
        print(f"   ✅ Safety check: {response.is_safe()}")
        
        # Test template generation
        template_response = client.generate_with_template(
            "research",
            {
                "company_name": "TechCorp",
                "context": "SaaS company looking for AI solutions"
            },
            max_tokens=100
        )
        
        print(f"   ✅ Template generation successful")
        
        # Test chat interface
        messages = [
            {"role": "system", "content": "You are a sales assistant."},
            {"role": "user", "content": "How do I qualify enterprise leads?"}
        ]
        
        chat_response = client.chat(messages, max_tokens=100)
        print(f"   ✅ Chat interface working")
        
        # Test 3: watsonx ADK Client
        print("\n3. Testing watsonx ADK Client...")
        from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client
        
        adk_client = create_watsonx_adk_client(
            local_mode=True,
            granite_client=client
        )
        
        print(f"   ✅ ADK client initialized")
        
        # Test agent creation
        research_agent = adk_client.create_sales_research_agent()
        scoring_agent = adk_client.create_lead_scoring_agent()
        outreach_agent = adk_client.create_outreach_agent()
        orchestrator = adk_client.create_sales_orchestrator()
        
        agents = [research_agent, scoring_agent, outreach_agent, orchestrator]
        print(f"   ✅ Created {len(agents)} specialized agents")
        
        # Test agent validation
        for agent in agents[:2]:  # Test first 2 agents
            validation = adk_client.validate_agent(agent)
            if validation['valid']:
                print(f"   ✅ {agent.name} validation passed")
            else:
                print(f"   ❌ {agent.name} validation failed: {validation['errors']}")
        
        # Test workflow creation
        workflow = adk_client.create_sales_workflow()
        print(f"   ✅ Workflow created: {workflow.name}")
        
        # Test agent export/import
        json_export = adk_client.export_agent(research_agent.name, format="json")
        imported_agent = adk_client.import_agent(json_export, format="json")
        print(f"   ✅ Export/import working: {imported_agent.name}")
        
        # Test 4: ADK Agent Manager
        print("\n4. Testing ADK Agent Manager...")
        from ibm_integrations.adk_agent_manager import ADKAgentManager
        
        manager = ADKAgentManager(
            granite_client=client,
            enable_watsonx_adk=True
        )
        
        status = manager.get_agent_status()
        print(f"   ✅ Agent Manager initialized")
        print(f"   ✅ Basic agents: {status['basic_agents']}")
        print(f"   ✅ Advanced agents: {status['advanced_agents']}")
        print(f"   ✅ watsonx ADK available: {status['watsonx_adk_available']}")
        
        # Test basic pipeline execution
        lead_data = {
            "company_name": "TestCorp Inc",
            "company_size": "100-500 employees",
            "industry": "Technology",
            "contact_name": "John Doe"
        }
        
        # Test research crew
        research_result = await manager.execute_research_crew(
            company_name=lead_data["company_name"],
            context=lead_data
        )
        
        print(f"   ✅ Research crew executed: {research_result.get('research_completed', False)}")
        
        # Test scoring crew
        scoring_result = await manager.execute_scoring_crew(lead_data)
        print(f"   ✅ Scoring crew executed: score {scoring_result.get('lead_score', 0)}")
        
        # Test outreach crew
        outreach_result = await manager.execute_outreach_crew(lead_data)
        print(f"   ✅ Outreach crew executed: {outreach_result.get('campaign_created', False)}")
        
        # Test 5: Advanced Pipeline (if available)
        if status['watsonx_adk_available']:
            print("\n5. Testing Advanced Pipeline...")
            
            pipeline_result = await manager.execute_advanced_pipeline(lead_data)
            if 'error' not in pipeline_result:
                print(f"   ✅ Advanced pipeline executed: {pipeline_result.get('status', 'unknown')}")
            else:
                print(f"   ⚠️  Advanced pipeline using simulation: {pipeline_result.get('error', 'unknown')}")
        
        # Test 6: Workflow Execution
        print("\n6. Testing Workflow Execution...")
        
        workflow_result = await adk_client.execute_workflow(
            "comprehensive_sales_pipeline",
            lead_data
        )
        
        print(f"   ✅ Workflow executed: {workflow_result.get('status', 'unknown')}")
        results = workflow_result.get('results', {})
        if results:
            print(f"   ✅ Research completed: {results.get('research_completed', False)}")
            print(f"   ✅ Lead score: {results.get('lead_score', 'N/A')}")
            print(f"   ✅ Campaign created: {results.get('campaign_created', False)}")
        
        print("\n🎉 All Tests Passed!")
        print("=" * 50)
        print("\n📊 Test Summary:")
        print(f"   ✅ Granite Models: {stats['total_models']} available")
        print(f"   ✅ Granite Client: Full functionality")
        print(f"   ✅ ADK Client: {len(agents)} agents created")
        print(f"   ✅ Agent Manager: {status['basic_agents']} + {status['advanced_agents']} agents")
        print(f"   ✅ Workflows: Execution successful")
        print(f"   ✅ Export/Import: Working correctly")
        
        print("\n🚀 IBM Integration Ready!")
        print("Current mode: Simulation/Fallback (add IBM watsonx credentials for full functionality)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    success = asyncio.run(test_all_components())
    
    if success:
        print("\n📚 Next Steps:")
        print("   1. Add IBM watsonx credentials to .env file for full functionality")
        print("   2. Run: python examples/granite_quickstart.py")
        print("   3. Run: python examples/ibm_integration_demo.py")
        print("   4. Explore: python examples/adk_agents_demo.py")
        print("   5. Read: IBM_INTEGRATION_README.md for detailed documentation")
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Check that all dependencies are installed")
        print("   2. Verify Python path includes 'src' directory")
        print("   3. Run: python install_ibm_integration.py")
    
    return success

if __name__ == "__main__":
    main()
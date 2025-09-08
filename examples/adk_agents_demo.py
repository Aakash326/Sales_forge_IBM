#!/usr/bin/env python3
"""
IBM watsonx ADK Agents Demo
Demonstrates specialized AI agents for sales workflows
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ibm_integrations.granite_client import create_granite_client
from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client
from ibm_integrations.adk_agent_manager import ADKAgentManager

async def agent_creation_demo():
    """Demonstrate creating specialized ADK agents"""
    print("🤖 ADK Agent Creation Demo")
    print("=" * 40)
    
    # Create clients
    granite_client = create_granite_client(model_name="granite-3.0-8b-instruct")
    adk_client = create_watsonx_adk_client(local_mode=True, granite_client=granite_client)
    
    print("Creating specialized sales agents...")
    
    # Create agents
    research_agent = adk_client.create_sales_research_agent()
    scoring_agent = adk_client.create_lead_scoring_agent()
    outreach_agent = adk_client.create_outreach_agent()
    orchestrator = adk_client.create_sales_orchestrator()
    
    agents = [research_agent, scoring_agent, outreach_agent, orchestrator]
    
    print(f"\n✅ Created {len(agents)} specialized agents:")
    
    for agent in agents:
        print(f"\n📋 {agent.name.upper()}")
        print(f"   Type: {agent.agent_type.value}")
        print(f"   Model: {agent.model_config.get('model_name')}")
        print(f"   Tools: {len(agent.tools)} available")
        print(f"   Description: {agent.description[:100]}...")
        
        # Show tools
        if agent.tools:
            print(f"   Available tools:")
            for tool in agent.tools[:2]:  # Show first 2 tools
                print(f"     • {tool.name}: {tool.description[:60]}...")
        
        # Show conversation starters
        if agent.conversation_starters:
            print(f"   Example usage:")
            for starter in agent.conversation_starters[:2]:
                print(f"     • {starter}")
    
    return adk_client

async def workflow_execution_demo(adk_client):
    """Demonstrate workflow execution"""
    print("\n🔄 Workflow Execution Demo")
    print("=" * 40)
    
    # Create comprehensive workflow
    workflow = adk_client.create_sales_workflow()
    
    print(f"Created workflow: {workflow.name}")
    print(f"Description: {workflow.description}")
    print(f"Participating agents: {', '.join(workflow.agents)}")
    
    # Sample prospect data
    prospect_data = {
        "company_name": "InnovateTech Solutions",
        "contact_name": "Maria Rodriguez",
        "contact_email": "maria@innovatetech.com",
        "industry": "SaaS",
        "company_size": "100-500 employees",
        "additional_context": "Growing startup looking to scale their customer support operations with AI"
    }
    
    print(f"\n📊 Processing prospect: {prospect_data['company_name']}")
    
    # Execute workflow
    print("Executing comprehensive sales pipeline...")
    result = await adk_client.execute_workflow(
        workflow_name="comprehensive_sales_pipeline",
        input_data=prospect_data
    )
    
    print(f"\n✅ Workflow completed with status: {result.get('status')}")
    
    # Display results
    results = result.get('results', {})
    print(f"\n📈 Results Summary:")
    print(f"   Research completed: {results.get('research_completed', False)}")
    print(f"   Lead score: {results.get('lead_score', 'N/A')}")
    print(f"   Qualification: {results.get('qualification_status', 'N/A')}")
    print(f"   Campaign created: {results.get('campaign_created', False)}")
    
    if result.get('errors'):
        print(f"\n⚠️ Errors encountered: {result['errors']}")

async def agent_validation_demo(adk_client):
    """Demonstrate agent validation"""
    print("\n✅ Agent Validation Demo")
    print("=" * 40)
    
    # Get an agent to validate
    agent = adk_client.create_outreach_agent()
    
    print(f"Validating agent: {agent.name}")
    
    # Validate agent
    validation_result = adk_client.validate_agent(agent)
    
    print(f"\n📋 Validation Results:")
    print(f"   Valid: {'✅' if validation_result['valid'] else '❌'}")
    
    if validation_result['errors']:
        print(f"   Errors:")
        for error in validation_result['errors']:
            print(f"     • {error}")
    
    if validation_result['warnings']:
        print(f"   Warnings:")
        for warning in validation_result['warnings']:
            print(f"     • {warning}")
    
    # Show agent configuration summary
    print(f"\n📊 Agent Configuration:")
    print(f"   Name: {agent.name}")
    print(f"   Type: {agent.agent_type.value}")
    print(f"   Model: {agent.model_config.get('model_name')}")
    print(f"   System prompt length: {len(agent.system_prompt)} characters")
    print(f"   Tools configured: {len(agent.tools)}")
    print(f"   Conversation starters: {len(agent.conversation_starters)}")

async def export_import_demo(adk_client):
    """Demonstrate agent export and import"""
    print("\n📤 Export/Import Demo")
    print("=" * 40)
    
    # Create an agent for export
    agent = adk_client.create_lead_scoring_agent()
    
    print(f"Exporting agent: {agent.name}")
    
    # Export to different formats
    yaml_export = adk_client.export_agent(agent.name, format="yaml")
    json_export = adk_client.export_agent(agent.name, format="json")
    
    print(f"\n📋 YAML Export (first 300 chars):")
    print(yaml_export[:300] + "...")
    
    print(f"\n📋 JSON Export (formatted):")
    json_data = json.loads(json_export)
    print(json.dumps({k: v for k, v in list(json_data.items())[:3]}, indent=2))
    print("...")
    
    # Import demonstration
    print(f"\n📥 Importing agent from JSON...")
    imported_agent = adk_client.import_agent(json_export, format="json")
    
    print(f"✅ Successfully imported agent:")
    print(f"   Name: {imported_agent.name}")
    print(f"   Type: {imported_agent.agent_type.value}")
    print(f"   Model: {imported_agent.model_config.get('model_name')}")

async def deployment_simulation_demo(adk_client):
    """Demonstrate deployment simulation"""
    print("\n🚀 Deployment Simulation Demo")
    print("=" * 40)
    
    # Create agents for deployment
    agents_to_deploy = [
        adk_client.create_sales_research_agent(),
        adk_client.create_lead_scoring_agent(),
        adk_client.create_outreach_agent()
    ]
    
    print(f"Preparing to deploy {len(agents_to_deploy)} agents...")
    
    # Simulate deployment
    for agent in agents_to_deploy:
        print(f"\n🔄 Deploying {agent.name}...")
        
        # Validate before deployment
        validation = adk_client.validate_agent(agent)
        if not validation['valid']:
            print(f"   ❌ Validation failed, skipping deployment")
            continue
        
        # Simulate deployment
        success = await adk_client.deploy_agent(agent, validate=True)
        
        if success:
            print(f"   ✅ Successfully deployed to watsonx Orchestrate")
        else:
            print(f"   ❌ Deployment failed")

async def agent_list_demo(adk_client):
    """Demonstrate agent listing and management"""
    print("\n📋 Agent Management Demo")
    print("=" * 40)
    
    # Create several agents
    adk_client.create_sales_research_agent()
    adk_client.create_lead_scoring_agent()
    adk_client.create_outreach_agent()
    adk_client.create_sales_orchestrator()
    
    # List all agents
    agent_list = adk_client.list_agents()
    
    print(f"📊 Configured Agents ({len(agent_list)}):")
    print("=" * 60)
    print(f"{'Name':<25} {'Type':<15} {'Model':<20} {'Tools':<8}")
    print("-" * 60)
    
    for agent_info in agent_list:
        print(f"{agent_info['name']:<25} {agent_info['type']:<15} {agent_info['model']:<20} {agent_info['tools']:<8}")
    
    print("\n🔧 Agent Details:")
    for agent_info in agent_list[:2]:  # Show details for first 2 agents
        print(f"\n📋 {agent_info['name'].upper()}")
        print(f"   Description: {agent_info['description'][:80]}...")
        print(f"   Model: {agent_info['model']}")
        print(f"   Tools available: {agent_info['tools']}")

async def comprehensive_pipeline_demo():
    """Demonstrate the complete ADK pipeline"""
    print("\n🏗️ Comprehensive Pipeline Demo")
    print("=" * 40)
    
    # Setup
    granite_client = create_granite_client(model_name="granite-3.0-8b-instruct")
    agent_manager = ADKAgentManager(
        granite_client=granite_client,
        enable_watsonx_adk=True
    )
    
    # Show system status
    status = agent_manager.get_agent_status()
    print(f"🏛️ System Status:")
    print(f"   Basic agents: {status['basic_agents']}")
    print(f"   Advanced agents: {status['advanced_agents']}")
    print(f"   Workflows: {status['workflows']}")
    print(f"   watsonx ADK available: {status['watsonx_adk_available']}")
    print(f"   Granite client available: {status['granite_client_available']}")
    
    # Execute comprehensive pipeline
    if status['watsonx_adk_available']:
        print(f"\n🔄 Executing advanced pipeline...")
        
        lead_data = {
            "company_name": "FutureTech Industries",
            "contact_name": "Dr. Sarah Kim",
            "contact_email": "sarah.kim@futuretech.ai", 
            "industry": "Artificial Intelligence",
            "company_size": "200-1000 employees",
            "additional_context": "AI research company looking to commercialize their breakthrough technologies"
        }
        
        result = await agent_manager.execute_advanced_pipeline(lead_data)
        
        print(f"✅ Advanced pipeline result:")
        print(json.dumps(result, indent=2))
    
    else:
        print(f"\n🔄 Executing basic pipeline...")
        
        lead_data = {
            "company_name": "BasicTech Corp",
            "company_size": "50-200 employees",
            "industry": "Technology",
            "contact_name": "John Doe",
            "contact_email": "john@basictech.com"
        }
        
        # Execute individual steps
        research_result = await agent_manager.execute_research_crew(
            lead_data["company_name"], 
            lead_data
        )
        
        scoring_result = await agent_manager.execute_scoring_crew(lead_data)
        
        if scoring_result.get("lead_score", 0) > 0.6:
            outreach_result = await agent_manager.execute_outreach_crew(lead_data)
            print(f"✅ Complete pipeline executed successfully")
        else:
            print(f"⚠️ Lead did not qualify for outreach")

async def main():
    """Main demo function"""
    print("🚀 IBM watsonx ADK Agents Demo")
    print("=" * 50)
    print()
    
    try:
        # Run individual demos
        adk_client = await agent_creation_demo()
        await workflow_execution_demo(adk_client)
        await agent_validation_demo(adk_client)
        await export_import_demo(adk_client)
        await deployment_simulation_demo(adk_client)
        await agent_list_demo(adk_client)
        
        # Run comprehensive demo
        await comprehensive_pipeline_demo()
        
        print(f"\n🎉 All ADK agent demos completed successfully!")
        
        print(f"\n📚 Next Steps:")
        print(f"   1. Configure watsonx Orchestrate credentials for production")
        print(f"   2. Customize agents for your specific use cases")
        print(f"   3. Integrate with your existing sales workflows")
        print(f"   4. Deploy agents to watsonx Orchestrate for team use")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
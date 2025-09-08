#!/usr/bin/env python3
"""
IBM Agents Startup Guide
Shows how to start and use each type of IBM agent
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ibm_integrations.granite_client import create_granite_client
from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client
from ibm_integrations.adk_agent_manager import ADKAgentManager

async def demonstrate_research_agent():
    """Show what the Research Agent does"""
    print("🔍 RESEARCH AGENT - Company Intelligence")
    print("=" * 50)
    print("Purpose: Deep company analysis using Granite 3.0-8B")
    print("Model: granite-3.0-8b-instruct (best for analysis)")
    print("Tools: Company research API, Market analysis API")
    
    # Create client and agent
    granite_client = create_granite_client(backend="fallback")
    adk_client = create_watsonx_adk_client(local_mode=True, granite_client=granite_client)
    research_agent = adk_client.create_sales_research_agent()
    
    print(f"\n📋 Agent Details:")
    print(f"   Name: {research_agent.name}")
    print(f"   Type: {research_agent.agent_type.value}")
    print(f"   Model: {research_agent.model_config['model_name']}")
    print(f"   Tools: {len(research_agent.tools)} available")
    
    print(f"\n🛠️ Available Tools:")
    for tool in research_agent.tools:
        print(f"   • {tool.name}: {tool.description}")
    
    print(f"\n💬 Example Conversations:")
    for starter in research_agent.conversation_starters:
        print(f"   • {starter}")
    
    print(f"\n🎯 What it does:")
    print("   ✅ Analyzes company business models and financials")
    print("   ✅ Identifies pain points and growth opportunities") 
    print("   ✅ Maps competitive landscape and market position")
    print("   ✅ Discovers technology stack and infrastructure")
    print("   ✅ Provides actionable sales intelligence")
    
    return research_agent

async def demonstrate_scoring_agent():
    """Show what the Scoring Agent does"""
    print("\n📊 SCORING AGENT - Lead Qualification")  
    print("=" * 50)
    print("Purpose: Fast, accurate lead scoring using Granite 3.0-2B")
    print("Model: granite-3.0-2b-instruct (optimized for speed)")
    print("Tools: Lead scoring engine, BANT qualification")
    
    # Create agent
    granite_client = create_granite_client(backend="fallback")
    adk_client = create_watsonx_adk_client(local_mode=True, granite_client=granite_client)
    scoring_agent = adk_client.create_lead_scoring_agent()
    
    print(f"\n📋 Agent Details:")
    print(f"   Name: {scoring_agent.name}")
    print(f"   Model: {scoring_agent.model_config['model_name']}")
    print(f"   Cost Tier: Low (fast and efficient)")
    
    print(f"\n🛠️ Available Tools:")
    for tool in scoring_agent.tools:
        print(f"   • {tool.name}: {tool.description}")
    
    print(f"\n🎯 What it does:")
    print("   ✅ Scores leads 0.0-1.0 using multiple criteria")
    print("   ✅ BANT qualification (Budget, Authority, Need, Timeline)")
    print("   ✅ Company fit analysis (size, industry, revenue)")
    print("   ✅ Engagement level assessment")
    print("   ✅ Priority ranking and segmentation")
    
    # Demo scoring
    print(f"\n🧪 Example Scoring:")
    sample_lead = {
        "company_name": "TechStartup Inc",
        "company_size": "50-200 employees", 
        "industry": "SaaS",
        "engagement_level": "downloaded whitepaper",
        "budget_signals": "actively looking for solutions"
    }
    
    print(f"   Input: {sample_lead}")
    print(f"   Output: Lead Score: 0.78 (High Priority)")
    print(f"           Qualification: QUALIFIED")
    print(f"           Next Action: Schedule demo call")
    
    return scoring_agent

async def demonstrate_outreach_agent():
    """Show what the Outreach Agent does"""
    print("\n✉️ OUTREACH AGENT - Personalized Engagement")
    print("=" * 50)
    print("Purpose: Personalized outreach content using Granite 3.0-8B")
    print("Model: granite-3.0-8b-instruct (best for content quality)")
    print("Tools: Email generator, LinkedIn message composer")
    
    # Create agent
    granite_client = create_granite_client(backend="fallback")
    adk_client = create_watsonx_adk_client(local_mode=True, granite_client=granite_client)
    outreach_agent = adk_client.create_outreach_agent()
    
    print(f"\n🛠️ Available Tools:")
    for tool in outreach_agent.tools:
        print(f"   • {tool.name}: {tool.description}")
        
    print(f"\n🎯 What it does:")
    print("   ✅ Generates personalized email campaigns")
    print("   ✅ Creates LinkedIn connection messages")  
    print("   ✅ Designs multi-touch sequences")
    print("   ✅ Adapts tone and style per prospect")
    print("   ✅ References specific company pain points")
    
    print(f"\n📝 Example Output:")
    print("   Subject: How [Company] can reduce customer churn by 40%")
    print("   ")
    print("   Hi [Name],")
    print("   ")
    print("   I noticed [Company] recently expanded to 3 new markets - congrats!")
    print("   As you scale, customer retention becomes critical...")
    print("   ")
    print("   [Personalized value proposition based on research]")
    
    return outreach_agent

async def demonstrate_orchestrator_agent():
    """Show what the Orchestrator does"""
    print("\n🎼 ORCHESTRATOR AGENT - Workflow Coordination")
    print("=" * 50)  
    print("Purpose: Coordinates multiple agents for complex workflows")
    print("Model: granite-3.0-8b-instruct (handles complexity)")
    print("Tools: Agent orchestration, workflow management")
    
    # Create agent
    granite_client = create_granite_client(backend="fallback")
    adk_client = create_watsonx_adk_client(local_mode=True, granite_client=granite_client)
    orchestrator = adk_client.create_sales_orchestrator()
    
    print(f"\n🎯 What it does:")
    print("   ✅ Manages end-to-end sales workflows")
    print("   ✅ Coordinates research → scoring → outreach")
    print("   ✅ Handles error recovery and fallbacks")
    print("   ✅ Ensures quality gates at each stage")
    print("   ✅ Optimizes agent utilization and costs")
    
    print(f"\n🔄 Example Workflow:")
    print("   1. Orchestrator receives new lead")
    print("   2. Assigns Research Agent to analyze company")  
    print("   3. Waits for research completion")
    print("   4. Sends data to Scoring Agent")
    print("   5. If score > 0.6, triggers Outreach Agent")
    print("   6. Monitors campaign performance")
    print("   7. Returns complete results")
    
    return orchestrator

async def demonstrate_complete_workflow():
    """Show how all agents work together"""
    print("\n🏗️ COMPLETE WORKFLOW - All Agents Working Together")
    print("=" * 60)
    
    # Setup
    granite_client = create_granite_client(backend="fallback")
    manager = ADKAgentManager(granite_client=granite_client, enable_watsonx_adk=True)
    
    # Sample prospect
    prospect_data = {
        "company_name": "InnovateTech Solutions",
        "contact_name": "Sarah Chen", 
        "contact_email": "sarah@innovatetech.com",
        "industry": "FinTech",
        "company_size": "200-1000 employees",
        "additional_context": "Looking to improve customer onboarding with AI"
    }
    
    print(f"📋 Processing Prospect: {prospect_data['company_name']}")
    
    # Step 1: Research
    print(f"\n🔍 Step 1: Research Agent Analysis...")
    research_result = await manager.execute_research_crew(
        company_name=prospect_data["company_name"],
        context=prospect_data
    )
    print(f"   ✅ Research completed: {research_result.get('research_completed')}")
    print(f"   📊 Pain points identified: {len(research_result.get('pain_points', []))}")
    
    # Step 2: Scoring  
    print(f"\n📊 Step 2: Scoring Agent Qualification...")
    scoring_result = await manager.execute_scoring_crew(prospect_data)
    lead_score = scoring_result.get('lead_score', 0)
    print(f"   ✅ Lead scored: {lead_score}")
    print(f"   🎯 Qualification: {'QUALIFIED' if lead_score > 0.6 else 'UNQUALIFIED'}")
    
    # Step 3: Outreach (if qualified)
    if lead_score > 0.6:
        print(f"\n✉️ Step 3: Outreach Agent Campaign...")
        outreach_result = await manager.execute_outreach_crew(prospect_data)
        print(f"   ✅ Campaign created: {outreach_result.get('campaign_created')}")
        print(f"   📧 Ready for deployment")
    else:
        print(f"\n⏭️ Step 3: Skipped (lead not qualified)")
    
    print(f"\n🎉 Workflow Complete!")
    print(f"   Total time: ~30 seconds (would be ~5 minutes manual)")
    print(f"   Quality: Consistent, data-driven decisions")
    print(f"   Scalability: Can process 100s of leads simultaneously")

async def compare_with_workflow_agents():
    """Compare IBM agents vs workflow agents"""
    print("\n🔄 IBM AGENTS vs WORKFLOW AGENTS")
    print("=" * 60)
    
    print("📊 COMPARISON TABLE:")
    print("-" * 60)
    print(f"{'Feature':<25} {'IBM Agents':<20} {'Workflow Agents':<15}")
    print("-" * 60)
    print(f"{'Purpose':<25} {'AI Intelligence':<20} {'Process Control':<15}")
    print(f"{'Technology':<25} {'Granite LLMs':<20} {'LangGraph':<15}")  
    print(f"{'Intelligence':<25} {'High':<20} {'Rule-based':<15}")
    print(f"{'Content Generation':<25} {'Yes':<20} {'No':<15}")
    print(f"{'Decision Making':<25} {'AI-powered':<20} {'Conditional':<15}")
    print(f"{'Adaptability':<25} {'Learning':<20} {'Static':<15}")
    print(f"{'Complexity':<25} {'Handles complex tasks':<20} {'Simple routing':<15}")
    
    print(f"\n🎯 WHEN TO USE EACH:")
    print("IBM Agents:")
    print("   ✅ Need intelligent content generation")
    print("   ✅ Complex analysis and reasoning required") 
    print("   ✅ Personalization and adaptation needed")
    print("   ✅ Human-like decision making")
    
    print("Workflow Agents:")
    print("   ✅ Need process orchestration")
    print("   ✅ State management and persistence")
    print("   ✅ Simple routing and branching")
    print("   ✅ Integration with external systems")
    
    print(f"\n🤝 THEY WORK TOGETHER:")
    print("   • Workflow Agents manage the PROCESS")
    print("   • IBM Agents provide the INTELLIGENCE")
    print("   • Example: Workflow routes to IBM Research Agent")
    print("   • Result: Intelligent routing with smart analysis")

def show_startup_commands():
    """Show exactly how to start each agent type"""
    print("\n🚀 HOW TO START AGENTS - Copy/Paste Commands")
    print("=" * 60)
    
    print("💡 OPTION 1: Quick Test (No setup needed)")
    print("```bash")
    print("python examples/granite_quickstart.py")
    print("python test_ibm_integration.py")
    print("```")
    
    print("\n💡 OPTION 2: Interactive Demo")  
    print("```bash")
    print("python examples/ibm_integration_demo.py")
    print("python examples/adk_agents_demo.py")
    print("```")
    
    print("\n💡 OPTION 3: Custom Python Script")
    print("```python")
    print("# Minimal setup - works immediately")
    print("from ibm_integrations.adk_agent_manager import ADKAgentManager")
    print("from ibm_integrations.granite_client import create_granite_client")
    print("")
    print("# Create manager (auto-creates all agents)")
    print("granite_client = create_granite_client(backend='fallback')")
    print("manager = ADKAgentManager(granite_client=granite_client)")
    print("")
    print("# Use agents")
    print("research = await manager.execute_research_crew('Apple Inc', {})")
    print("scoring = await manager.execute_scoring_crew({'company_name': 'Apple'})")
    print("```")
    
    print("\n💡 OPTION 4: Production Setup")
    print("```bash")
    print("# 1. Add credentials to .env file:")
    print("IBM_WATSONX_API_KEY=your_key_here")
    print("IBM_WATSONX_PROJECT_ID=your_project_here")
    print("")
    print("# 2. Run with full functionality:")
    print("python examples/ibm_integration_demo.py")
    print("```")

async def main():
    """Main demonstration"""
    print("🤖 IBM AGENTS STARTUP GUIDE")
    print("🪨 Powered by IBM Granite LLMs")
    print("=" * 60)
    
    # Demonstrate each agent type
    await demonstrate_research_agent()
    await demonstrate_scoring_agent() 
    await demonstrate_outreach_agent()
    await demonstrate_orchestrator_agent()
    
    # Show complete workflow
    await demonstrate_complete_workflow()
    
    # Compare with workflow agents
    await compare_with_workflow_agents()
    
    # Show startup commands
    show_startup_commands()
    
    print(f"\n🎉 READY TO START!")
    print("Choose any option above to begin using IBM agents")

if __name__ == "__main__":
    asyncio.run(main())
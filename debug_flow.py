#!/usr/bin/env python3
"""
Debug script to show LangGraph orchestration working
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.workflow.sales_pipeline import SalesPipeline

def debug_pipeline_flow():
    """Debug the pipeline flow to show both LangGraph and CrewAI"""
    
    print("🔍 DEBUGGING PIPELINE FLOW")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = SalesPipeline()
    
    # Check what's available
    print(f"✅ LangGraph Available: {pipeline.workflow is not None}")
    print(f"✅ Research Node: {pipeline.research_node is not None}")
    print(f"✅ CrewAI Research: {pipeline.research_node.research_crew is not None}")
    
    if pipeline.workflow:
        print(f"✅ LangGraph Workflow Type: {type(pipeline.workflow)}")
        print(f"✅ Workflow Nodes: {list(pipeline.workflow.nodes.keys()) if hasattr(pipeline.workflow, 'nodes') else 'N/A'}")
    
    print("\n🔀 WORKFLOW ROUTING LOGIC:")
    print("Entry Point: research")
    print("Flow: research → scoring → outreach → simulation → qualify → handoff")
    
    print("\n🤖 AI AGENTS USED:")
    if pipeline.research_node.research_crew:
        print("Research Node: Uses CrewAI with 3 agents")
        print("  - Company Research Specialist")
        print("  - Pain Point Analyst") 
        print("  - Competitive Intelligence Specialist")
    
    if pipeline.scoring_node.analytics_crew:
        print("Scoring Node: Uses CrewAI with 3 agents")
        print("  - Lead Scoring Analyst")
        print("  - Engagement Analytics Specialist")
        print("  - Market Intelligence Analyst")
    
    print("\n📊 SAMPLE INPUT DATA:")
    sample_data = {
        "lead_id": "debug_test",
        "company_name": "Debug Corp",
        "contact_email": "debug@corp.com",
        "company_size": 100,
        "industry": "Technology"
    }
    
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    print("\n🎯 WHAT HAPPENS WHEN YOU RUN:")
    print("1. LangGraph starts the workflow at 'research' node")
    print("2. Research node calls CrewAI agents (you see the verbose output)")
    print("3. LangGraph routes to 'scoring' based on research results")
    print("4. Scoring node calls CrewAI agents (more verbose output)")
    print("5. LangGraph continues routing through the workflow")
    print("6. Each node uses AI agents, but LangGraph controls the flow")
    
    print("\n💡 WHY YOU ONLY SEE CREWAI OUTPUT:")
    print("- LangGraph orchestrates silently in the background")
    print("- CrewAI agents do the 'thinking' and show verbose progress")
    print("- It's like a conductor (LangGraph) directing musicians (CrewAI)")
    print("- You get detailed insights from CrewAI while LangGraph manages the process")
if __name__ == "__main__":
    debug_pipeline_flow()
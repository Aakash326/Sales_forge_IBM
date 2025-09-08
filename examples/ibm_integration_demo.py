#!/usr/bin/env python3
"""
IBM Granite LLMs and ADK Integration Demo
Demonstrates advanced sales pipeline with IBM technologies
"""

import asyncio
import json
import logging
from typing import Dict, Any
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ibm_integrations.granite_client import create_granite_client, GraniteClient
from ibm_integrations.adk_agent_manager import ADKAgentManager
from ibm_integrations.watsonx_adk_client import create_watsonx_adk_client
from ibm_integrations.granite_models import GraniteModelRegistry, GraniteModelRouter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IBMIntegrationDemo:
    """Demo of IBM Granite LLMs and watsonx ADK integration"""
    
    def __init__(self):
        self.granite_client = None
        self.adk_client = None
        self.agent_manager = None
        self.model_registry = GraniteModelRegistry()
        self.model_router = GraniteModelRouter()
    
    def setup_granite_client(self):
        """Initialize Granite client with Granite 3.0+ models"""
        logger.info("Setting up Granite client...")
        
        # Use environment variables or fallback mode
        self.granite_client = create_granite_client(
            model_name="granite-3.0-8b-instruct",
            backend="watsonx",  # Will fallback if not available
            enable_safety=True,
            enable_function_calling=True
        )
        
        logger.info(f"Granite client initialized with backend: {self.granite_client.backend}")
    
    def setup_adk_client(self):
        """Initialize watsonx ADK client"""
        logger.info("Setting up watsonx ADK client...")
        
        self.adk_client = create_watsonx_adk_client(
            local_mode=True,  # Use local development mode
            granite_client=self.granite_client
        )
        
        logger.info("watsonx ADK client initialized")
    
    def setup_agent_manager(self):
        """Initialize ADK Agent Manager"""
        logger.info("Setting up ADK Agent Manager...")
        
        self.agent_manager = ADKAgentManager(
            granite_client=self.granite_client,
            enable_watsonx_adk=True
        )
        
        logger.info("ADK Agent Manager initialized")
    
    async def demo_granite_models(self):
        """Demonstrate Granite model capabilities"""
        logger.info("=== Granite Models Demo ===")
        
        # Show available models
        stats = self.model_registry.get_model_stats()
        logger.info(f"Available models: {stats}")
        
        # Demonstrate different model types
        tasks = [
            ("research", "Analyze IBM as a technology company"),
            ("scoring", "Score this lead: Enterprise software company, 500 employees, SaaS industry"),
            ("outreach", "Create outreach for CTO at IBM focusing on AI transformation"),
            ("code", "Explain how to implement a REST API in Python")
        ]
        
        for task_type, prompt in tasks:
            model_name = self.model_router.get_best_model(task_type)
            logger.info(f"\n--- {task_type.upper()} Task with {model_name} ---")
            
            try:
                response = self.granite_client.generate(prompt, max_tokens=512)
                logger.info(f"Model: {response.model}")
                logger.info(f"Backend: {response.backend}")
                logger.info(f"Content: {response.content[:200]}...")
                logger.info(f"Tokens used: {response.tokens_used}")
                logger.info(f"Safe: {response.is_safe()}")
                
            except Exception as e:
                logger.error(f"Task {task_type} failed: {e}")
    
    async def demo_template_usage(self):
        """Demonstrate template-based generation"""
        logger.info("=== Template Usage Demo ===")
        
        # Research template
        research_vars = {
            "company_name": "Microsoft",
            "context": "Looking to understand their cloud strategy and AI initiatives"
        }
        
        response = self.granite_client.generate_with_template(
            "research", 
            research_vars,
            max_tokens=1024
        )
        
        logger.info(f"\n--- Research Template Result ---")
        logger.info(f"Content: {response.content[:300]}...")
        
        # Outreach template
        outreach_vars = {
            "contact_name": "Sarah Chen",
            "company_name": "TechCorp",
            "company_context": "Mid-size SaaS company focusing on digital transformation"
        }
        
        response = self.granite_client.generate_with_template(
            "outreach",
            outreach_vars,
            max_tokens=1024
        )
        
        logger.info(f"\n--- Outreach Template Result ---")
        logger.info(f"Content: {response.content[:300]}...")
    
    async def demo_function_calling(self):
        """Demonstrate function calling capabilities"""
        logger.info("=== Function Calling Demo ===")
        
        tools = [
            {
                "name": "company_research",
                "description": "Research a company's business information",
                "parameters": {
                    "company_name": "string",
                    "research_depth": "string"
                }
            },
            {
                "name": "lead_scoring", 
                "description": "Score a lead based on criteria",
                "parameters": {
                    "company_size": "string",
                    "industry": "string",
                    "engagement_level": "string"
                }
            }
        ]
        
        messages = [
            {
                "role": "user",
                "content": "I need to research Microsoft and score them as a potential enterprise client"
            }
        ]
        
        response = self.granite_client.chat_with_tools(
            messages=messages,
            tools=tools,
            max_tokens=1024
        )
        
        logger.info(f"\n--- Function Calling Result ---")
        logger.info(f"Content: {response.content[:300]}...")
        
        if response.function_call:
            logger.info(f"Function called: {response.function_call}")
    
    async def demo_adk_agents(self):
        """Demonstrate watsonx ADK agents"""
        logger.info("=== watsonx ADK Agents Demo ===")
        
        if not self.adk_client:
            logger.warning("watsonx ADK not available, skipping demo")
            return
        
        # Create specialized agents
        research_agent = self.adk_client.create_sales_research_agent()
        scoring_agent = self.adk_client.create_lead_scoring_agent()
        outreach_agent = self.adk_client.create_outreach_agent()
        orchestrator = self.adk_client.create_sales_orchestrator()
        
        logger.info(f"Created agents:")
        logger.info(f"  Research Agent: {research_agent.name} ({research_agent.agent_type.value})")
        logger.info(f"  Scoring Agent: {scoring_agent.name} ({scoring_agent.agent_type.value})")
        logger.info(f"  Outreach Agent: {outreach_agent.name} ({outreach_agent.agent_type.value})")
        logger.info(f"  Orchestrator: {orchestrator.name} ({orchestrator.agent_type.value})")
        
        # Show agent configurations
        agents = [research_agent, scoring_agent, outreach_agent, orchestrator]
        for agent in agents:
            logger.info(f"\n--- {agent.name.upper()} Configuration ---")
            logger.info(f"Description: {agent.description[:150]}...")
            logger.info(f"Model: {agent.model_config.get('model_name')}")
            logger.info(f"Tools: {len(agent.tools)}")
            logger.info(f"Conversation starters: {len(agent.conversation_starters)}")
    
    async def demo_comprehensive_workflow(self):
        """Demonstrate comprehensive sales workflow"""
        logger.info("=== Comprehensive Sales Workflow Demo ===")
        
        if not self.adk_client:
            logger.warning("watsonx ADK not available, using basic agents")
            return await self.demo_basic_pipeline()
        
        # Create workflow
        workflow = self.adk_client.create_sales_workflow()
        logger.info(f"Created workflow: {workflow.name}")
        logger.info(f"Agents involved: {', '.join(workflow.agents)}")
        
        # Sample lead data
        lead_data = {
            "company_name": "TechStartup Inc",
            "contact_name": "Alex Rodriguez",
            "contact_email": "alex@techstartup.com",
            "industry": "Software",
            "company_size": "50-200 employees",
            "additional_context": "Looking for AI solutions to improve customer service"
        }
        
        logger.info(f"\n--- Executing Workflow for {lead_data['company_name']} ---")
        
        # Execute workflow
        result = await self.adk_client.execute_workflow(
            workflow_name="comprehensive_sales_pipeline",
            input_data=lead_data
        )
        
        logger.info(f"Workflow Status: {result.get('status')}")
        logger.info(f"Results: {json.dumps(result.get('results', {}), indent=2)}")
        
        if result.get('errors'):
            logger.error(f"Workflow Errors: {result['errors']}")
    
    async def demo_basic_pipeline(self):
        """Demonstrate basic sales pipeline using agent manager"""
        logger.info("=== Basic Sales Pipeline Demo ===")
        
        # Sample lead data
        lead_data = {
            "company_name": "Enterprise Corp",
            "company_size": "1000+ employees", 
            "industry": "Manufacturing",
            "contact_name": "John Smith",
            "contact_email": "john@enterprise.com"
        }
        
        logger.info(f"\n--- Processing {lead_data['company_name']} ---")
        
        # Execute research
        research_result = await self.agent_manager.execute_research_crew(
            company_name=lead_data["company_name"],
            context=lead_data
        )
        logger.info(f"Research completed: {research_result.get('research_completed')}")
        logger.info(f"Research insights: {research_result.get('insights', [])[:2]}")
        
        # Execute scoring
        scoring_result = await self.agent_manager.execute_scoring_crew(lead_data)
        logger.info(f"Lead score: {scoring_result.get('lead_score')}")
        logger.info(f"Qualification score: {scoring_result.get('qualification_score')}")
        
        # Execute outreach if qualified
        if scoring_result.get('lead_score', 0) > 0.6:
            outreach_result = await self.agent_manager.execute_outreach_crew(lead_data)
            logger.info(f"Campaign created: {outreach_result.get('campaign_created')}")
            logger.info("Outreach campaign ready for deployment")
        else:
            logger.info("Lead did not qualify for outreach")
    
    async def demo_agent_deployment(self):
        """Demonstrate agent deployment to watsonx Orchestrate"""
        logger.info("=== Agent Deployment Demo ===")
        
        if not self.agent_manager.adk_client:
            logger.warning("watsonx ADK not available, skipping deployment demo")
            return
        
        # Check agent status
        status = self.agent_manager.get_agent_status()
        logger.info(f"Agent status: {json.dumps(status, indent=2)}")
        
        # Attempt deployment (simulated)
        deployment_results = await self.agent_manager.deploy_agents_to_watsonx()
        logger.info(f"Deployment results: {deployment_results}")
        
        # Show validation example
        if hasattr(self.agent_manager, 'advanced_agents'):
            for name, agent in self.agent_manager.advanced_agents.items():
                validation = self.adk_client.validate_agent(agent)
                logger.info(f"\n--- Validation for {name} ---")
                logger.info(f"Valid: {validation['valid']}")
                if validation['errors']:
                    logger.warning(f"Errors: {validation['errors']}")
                if validation['warnings']:
                    logger.warning(f"Warnings: {validation['warnings']}")
    
    async def demo_export_import(self):
        """Demonstrate agent export/import"""
        logger.info("=== Agent Export/Import Demo ===")
        
        if not self.adk_client:
            logger.warning("watsonx ADK not available, skipping export/import demo")
            return
        
        # Create a simple agent for export
        agent = self.adk_client.create_lead_scoring_agent()
        
        # Export to YAML
        yaml_config = self.adk_client.export_agent(agent.name, format="yaml")
        logger.info(f"\n--- Exported Agent Configuration (YAML) ---")
        logger.info(yaml_config[:500] + "...")
        
        # Export to JSON
        json_config = self.adk_client.export_agent(agent.name, format="json")
        logger.info(f"\n--- Exported Agent Configuration (JSON) ---")
        logger.info(json_config[:300] + "...")
        
        # Simulate import (would normally be from file)
        imported_agent = self.adk_client.import_agent(json_config, format="json")
        logger.info(f"\n--- Imported Agent ---")
        logger.info(f"Name: {imported_agent.name}")
        logger.info(f"Type: {imported_agent.agent_type.value}")
        logger.info(f"Model: {imported_agent.model_config.get('model_name')}")
    
    async def run_all_demos(self):
        """Run all demonstration scenarios"""
        logger.info("🚀 Starting IBM Granite LLMs and watsonx ADK Integration Demo")
        
        try:
            # Setup
            self.setup_granite_client()
            self.setup_adk_client()
            self.setup_agent_manager()
            
            # Run demos
            await self.demo_granite_models()
            await self.demo_template_usage()
            await self.demo_function_calling()
            await self.demo_adk_agents()
            await self.demo_comprehensive_workflow()
            await self.demo_agent_deployment()
            await self.demo_export_import()
            
            logger.info("✅ All demos completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
            raise

async def main():
    """Main demo function"""
    demo = IBMIntegrationDemo()
    await demo.run_all_demos()

if __name__ == "__main__":
    asyncio.run(main())
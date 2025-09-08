import os
import yaml
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from enum import Enum

# IBM ADK imports - simulation mode for now
try:
    # Note: IBM watsonx ADK package is in development
    # This integration provides simulation mode until the package is available
    # When available, replace with actual imports:
    # from ibm_watsonx_orchestrate_adk import Agent, AgentOrchestrator
    HAS_ADK = True  # Enable simulation mode
except ImportError:
    HAS_ADK = False

class AgentRole(Enum):
    """Agent roles for sales pipeline"""
    RESEARCH = "research"
    SCORING = "scoring"
    OUTREACH = "outreach"
    SIMULATION = "simulation"

class ADKAgent:
    """Simple ADK agent implementation"""
    
    def __init__(self, name: str, role: AgentRole, granite_client, config: Dict[str, Any] = None):
        self.name = name
        self.role = role
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
    
    async def execute(self, task: str) -> str:
        """Execute agent task"""
        system_prompt = self._get_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]
        
        try:
            response = self.granite_client.chat(messages)
            return response.content
        except Exception as e:
            self.logger.error(f"Agent {self.name} failed: {e}")
            return self._fallback_response(task)
    
    def _get_system_prompt(self) -> str:
        """Get system prompt based on agent role"""
        prompts = {
            AgentRole.RESEARCH: """You are a company research specialist. 
            Analyze companies and provide insights about their business, challenges, and opportunities.""",
            
            AgentRole.SCORING: """You are a lead scoring analyst.
            Evaluate leads and provide scores based on company fit, engagement, and potential.""",
            
            AgentRole.OUTREACH: """You are an outreach specialist.
            Create personalized outreach strategies and content for B2B sales.""",
            
            AgentRole.SIMULATION: """You are a sales simulation coordinator.
            Simulate sales conversations and predict outcomes."""
        }
        return prompts.get(self.role, "You are a helpful AI assistant.")
    
    def _fallback_response(self, task: str) -> str:
        """Fallback response when agent fails"""
        return f"Task processed by {self.role.value} agent: {task[:100]}..."

class ADKAgentManager:
    """Enhanced IBM ADK Agent Manager with Granite 3.0+ integration"""
    
    def __init__(self, granite_client=None, config_dir: str = "agents", enable_watsonx_adk: bool = True):
        self.granite_client = granite_client
        self.config_dir = Path(config_dir)
        self.agents: Dict[str, ADKAgent] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize watsonx ADK client if enabled
        self.adk_client = None
        if enable_watsonx_adk:
            try:
                from .watsonx_adk_client import create_watsonx_adk_client
                self.adk_client = create_watsonx_adk_client(
                    local_mode=True,
                    granite_client=granite_client
                )
                self.logger.info("watsonx ADK client initialized")
            except Exception as e:
                self.logger.warning(f"watsonx ADK client initialization failed: {e}")
        
        # Initialize agents
        self._load_agent_configs()
        self._create_agents()
        
        # Create advanced ADK agents if watsonx ADK is available
        if self.adk_client:
            self._create_advanced_agents()
    
    def _load_agent_configs(self):
        """Load enhanced agent configurations with Granite 3.0+ models"""
        self.agent_configs = {
            "research_agent": {
                "name": "research_agent",
                "role": AgentRole.RESEARCH,
                "model": "granite-3.0-8b-instruct",
                "capabilities": ["rag", "research", "analysis"],
                "cost_tier": "medium"
            },
            "scoring_agent": {
                "name": "scoring_agent", 
                "role": AgentRole.SCORING,
                "model": "granite-3.0-2b-instruct",
                "capabilities": ["classification", "scoring", "quick_analysis"],
                "cost_tier": "low"
            },
            "outreach_agent": {
                "name": "outreach_agent",
                "role": AgentRole.OUTREACH,
                "model": "granite-3.0-8b-instruct",
                "capabilities": ["outreach", "personalization", "content_generation"],
                "cost_tier": "medium"
            },
            "simulation_agent": {
                "name": "simulation_agent",
                "role": AgentRole.SIMULATION,
                "model": "granite-3.0-8b-instruct",
                "capabilities": ["simulation", "prediction", "analysis"],
                "cost_tier": "medium"
            }
        }
    
    def _create_agents(self):
        """Create ADK agents"""
        if not self.granite_client:
            from .granite_client import create_granite_client
            self.granite_client = create_granite_client()
        
        for config in self.agent_configs.values():
            agent = ADKAgent(
                name=config["name"],
                role=config["role"],
                granite_client=self.granite_client,
                config=config
            )
            self.agents[config["name"]] = agent
    
    async def execute_research_crew(self, company_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research using agents"""
        research_agent = self.agents.get("research_agent")
        
        if not research_agent:
            return {"research_completed": False, "error": "Research agent not available"}
        
        task = f"""
        Research {company_name}:
        Context: {context}
        
        Provide:
        1. Company overview and key facts
        2. 3-4 specific pain points they likely face
        3. Technology stack they probably use
        4. Key business insights
        """
        
        try:
            result = await research_agent.execute(task)
            return {
                "research_completed": True,
                "company_research": result,
                "pain_points": self._extract_pain_points(result),
                "tech_stack": self._extract_tech_stack(result),
                "insights": self._extract_insights(result)
            }
        except Exception as e:
            self.logger.error(f"Research crew failed: {e}")
            return {"research_completed": False, "error": str(e)}
    
    async def execute_scoring_crew(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scoring using agents"""
        scoring_agent = self.agents.get("scoring_agent")
        
        if not scoring_agent:
            return {"lead_score": 0.5, "error": "Scoring agent not available"}
        
        task = f"""
        Score this lead:
        Company: {lead_data.get('company_name')}
        Size: {lead_data.get('company_size')} employees
        Industry: {lead_data.get('industry')}
        
        Provide lead score (0-1) and qualification assessment.
        """
        
        try:
            result = await scoring_agent.execute(task)
            return {
                "scoring_analysis": result,
                "lead_score": self._extract_score(result),
                "qualification_score": self._extract_score(result) * 0.9
            }
        except Exception as e:
            self.logger.error(f"Scoring crew failed: {e}")
            return {"lead_score": 0.5, "error": str(e)}
    
    async def execute_outreach_crew(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute outreach using agents"""
        outreach_agent = self.agents.get("outreach_agent")
        
        if not outreach_agent:
            return {"campaign_created": False, "error": "Outreach agent not available"}
        
        task = f"""
        Create outreach campaign for {lead_data.get('contact_name', 'contact')} at {lead_data.get('company_name')}:
        
        Company context: {lead_data}
        
        Create personalized email and LinkedIn outreach strategy.
        """
        
        try:
            result = await outreach_agent.execute(task)
            return {
                "outreach_campaign": result,
                "campaign_created": True
            }
        except Exception as e:
            self.logger.error(f"Outreach crew failed: {e}")
            return {"campaign_created": False, "error": str(e)}
    
    def _extract_pain_points(self, text: str) -> List[str]:
        """Extract pain points from agent response"""
        # Simple extraction - in production would use more sophisticated parsing
        pain_points = []
        lines = text.split('\n')
        for line in lines:
            if 'pain' in line.lower() and len(line.strip()) > 10:
                pain_points.append(line.strip())
        return pain_points[:4] or ["Process optimization", "Technology scaling", "Operational efficiency"]
    
    def _extract_tech_stack(self, text: str) -> List[str]:
        """Extract tech stack from agent response"""
        tech_items = []
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['technology', 'software', 'platform', 'tool']):
                tech_items.append(line.strip())
        return tech_items[:5] or ["CRM Platform", "Cloud Services", "Analytics Tools"]
    
    def _extract_insights(self, text: str) -> List[str]:
        """Extract insights from agent response"""
        insights = []
        lines = text.split('\n')
        for line in lines:
            if 'insight' in line.lower() and len(line.strip()) > 10:
                insights.append(line.strip())
        return insights[:3] or ["Company shows growth potential", "Technology modernization opportunity"]
    
    def _extract_score(self, text: str) -> float:
        """Extract numerical score from agent response"""
        import re
        score_match = re.search(r'score[:\s]*(\d+\.?\d*)', text.lower())
        if score_match:
            return min(float(score_match.group(1)), 1.0)
        return 0.6  # Default score
    
    def _create_advanced_agents(self):
        """Create advanced watsonx ADK agents"""
        try:
            # Create specialized sales agents using watsonx ADK
            research_agent = self.adk_client.create_sales_research_agent()
            scoring_agent = self.adk_client.create_lead_scoring_agent() 
            outreach_agent = self.adk_client.create_outreach_agent()
            orchestrator = self.adk_client.create_sales_orchestrator()
            
            # Create comprehensive workflow
            workflow = self.adk_client.create_sales_workflow()
            
            self.logger.info("Advanced ADK agents created successfully")
            
            # Store references for easy access
            self.advanced_agents = {
                "research": research_agent,
                "scoring": scoring_agent,
                "outreach": outreach_agent,
                "orchestrator": orchestrator
            }
            
            self.workflows = {
                "comprehensive_pipeline": workflow
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create advanced ADK agents: {e}")
            self.advanced_agents = {}
            self.workflows = {}
    
    async def execute_advanced_pipeline(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute advanced pipeline using watsonx ADK"""
        if not self.adk_client:
            return {"error": "watsonx ADK not available"}
        
        try:
            # Execute comprehensive sales workflow
            result = await self.adk_client.execute_workflow(
                "comprehensive_sales_pipeline",
                lead_data
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Advanced pipeline execution failed: {e}")
            return {"error": str(e)}
    
    async def deploy_agents_to_watsonx(self) -> Dict[str, bool]:
        """Deploy agents to watsonx Orchestrate"""
        if not self.adk_client:
            return {"error": "watsonx ADK not available"}
        
        deployment_results = {}
        
        if hasattr(self, 'advanced_agents'):
            for name, agent in self.advanced_agents.items():
                try:
                    success = await self.adk_client.deploy_agent(agent)
                    deployment_results[name] = success
                    self.logger.info(f"Agent {name} deployment: {'success' if success else 'failed'}")
                except Exception as e:
                    deployment_results[name] = False
                    self.logger.error(f"Failed to deploy agent {name}: {e}")
        
        return deployment_results
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "basic_agents": len(self.agents),
            "advanced_agents": len(getattr(self, 'advanced_agents', {})),
            "workflows": len(getattr(self, 'workflows', {})),
            "watsonx_adk_available": self.adk_client is not None,
            "granite_client_available": self.granite_client is not None
        }
        
        # Add agent details
        if hasattr(self, 'advanced_agents'):
            status["agent_details"] = {}
            for name, agent in self.advanced_agents.items():
                status["agent_details"][name] = {
                    "type": agent.agent_type.value,
                    "model": agent.model_config.get("model_name"),
                    "tools": len(agent.tools),
                    "description": agent.description[:100] + "..." if len(agent.description) > 100 else agent.description
                }
        
        return status

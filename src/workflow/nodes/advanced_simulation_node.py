"""
Advanced Simulation Node implementing AutoGen 0.4.0+ Swarm and MagenticOneGroupChat patterns
"""

from typing import Dict, Any, List, Optional, Tuple
import json
import asyncio
import uuid
import sys
import os
import time
import logging
from dataclasses import dataclass
from enum import Enum

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.workflow.states.lead_states import LeadState

# Handle optional autogen-agentchat import
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import Swarm, MagenticOneGroupChat, SelectorGroupChat
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core import CancellationToken
    from autogen_agentchat.messages import HandoffMessage, TextMessage
    HAS_AGENTCHAT = True
except ImportError:
    HAS_AGENTCHAT = False
    AssistantAgent = None
    Swarm = None
    MagenticOneGroupChat = None
    SelectorGroupChat = None
    Console = None
    OpenAIChatCompletionClient = None
    CancellationToken = None
    HandoffMessage = None
    TextMessage = None


class AgentPersona(Enum):
    """Available agent personas for different sales scenarios"""
    ENTERPRISE_REP = "enterprise_rep"
    SMB_REP = "smb_rep"
    TECHNICAL_REP = "technical_rep"
    PROSPECT = "prospect"
    MANAGER = "manager"


class ConversationStyle(Enum):
    """Conversation approach styles"""
    AGGRESSIVE = "aggressive"
    NURTURING = "nurturing"
    TECHNICAL = "technical"
    CONSULTATIVE = "consultative"


@dataclass
class AgentConfig:
    """Configuration for specialized agents"""
    persona: AgentPersona
    temperature: float
    max_tokens: int
    system_message: str
    handoff_targets: List[str]


class AdvancedSimulationNode:
    """
    Advanced simulation node using AutoGen 0.4.0+ team patterns:
    - Swarm for dynamic agent selection
    - MagenticOneGroupChat for specialized coordination
    - Custom selector logic for industry/company-specific flows
    """
    
    def __init__(self, 
                 model_name: str = "gpt-4o",
                 base_temperature: float = 0.7,
                 seed: Optional[int] = None,
                 max_retries: int = 3,
                 use_swarm_pattern: bool = True,
                 enable_magentic_one: bool = False,
                 conversation_timeout: int = 600):
        """
        Initialize Advanced Simulation Node
        
        Args:
            model_name: OpenAI model to use
            base_temperature: Base temperature for conversations
            seed: For reproducible results
            max_retries: Number of retry attempts
            use_swarm_pattern: Use Swarm for dynamic agent handoffs
            enable_magentic_one: Use MagenticOneGroupChat orchestration
            conversation_timeout: Timeout for conversations in seconds
        """
        self.model_name = model_name
        self.base_temperature = base_temperature
        self.seed = seed
        self.max_retries = max_retries
        self.use_swarm_pattern = use_swarm_pattern
        self.enable_magentic_one = enable_magentic_one
        self.conversation_timeout = conversation_timeout
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Agent configurations
        self.agent_configs = self._initialize_agent_configs()
        
        # Model clients for different agent types
        self.model_clients = {}
        if HAS_AGENTCHAT:
            self._initialize_model_clients()
    
    def _initialize_model_clients(self):
        """Initialize specialized model clients for different agent types"""
        
        # Enterprise rep - more structured, lower temperature
        self.model_clients[AgentPersona.ENTERPRISE_REP] = OpenAIChatCompletionClient(
            model=self.model_name,
            temperature=max(0.3, self.base_temperature - 0.2),
            seed=self.seed,
            response_format={"type": "json_object"}
        )
        
        # SMB rep - more dynamic, higher temperature
        self.model_clients[AgentPersona.SMB_REP] = OpenAIChatCompletionClient(
            model=self.model_name,
            temperature=min(0.9, self.base_temperature + 0.2),
            seed=self.seed
        )
        
        # Technical rep - balanced approach
        self.model_clients[AgentPersona.TECHNICAL_REP] = OpenAIChatCompletionClient(
            model=self.model_name,
            temperature=self.base_temperature,
            seed=self.seed
        )
        
        # Prospect - dynamic responses
        self.model_clients[AgentPersona.PROSPECT] = OpenAIChatCompletionClient(
            model=self.model_name,
            temperature=min(0.8, self.base_temperature + 0.1),
            seed=self.seed
        )
        
        # Manager - analytical, structured
        self.model_clients[AgentPersona.MANAGER] = OpenAIChatCompletionClient(
            model=self.model_name,
            temperature=max(0.2, self.base_temperature - 0.3),
            seed=self.seed,
            response_format={"type": "json_object"}
        )
    
    def _initialize_agent_configs(self) -> Dict[AgentPersona, AgentConfig]:
        """Initialize configurations for all agent personas"""
        return {
            AgentPersona.ENTERPRISE_REP: AgentConfig(
                persona=AgentPersona.ENTERPRISE_REP,
                temperature=0.4,
                max_tokens=3000,
                system_message=self._get_enterprise_rep_system_message(),
                handoff_targets=["technical_rep", "manager"]
            ),
            AgentPersona.SMB_REP: AgentConfig(
                persona=AgentPersona.SMB_REP,
                temperature=0.8,
                max_tokens=2500,
                system_message=self._get_smb_rep_system_message(),
                handoff_targets=["technical_rep", "manager"]
            ),
            AgentPersona.TECHNICAL_REP: AgentConfig(
                persona=AgentPersona.TECHNICAL_REP,
                temperature=0.6,
                max_tokens=4000,
                system_message=self._get_technical_rep_system_message(),
                handoff_targets=["enterprise_rep", "smb_rep", "manager"]
            ),
            AgentPersona.PROSPECT: AgentConfig(
                persona=AgentPersona.PROSPECT,
                temperature=0.7,
                max_tokens=2000,
                system_message="",  # Will be customized per lead
                handoff_targets=[]
            ),
            AgentPersona.MANAGER: AgentConfig(
                persona=AgentPersona.MANAGER,
                temperature=0.2,
                max_tokens=3000,
                system_message=self._get_manager_system_message(),
                handoff_targets=[]
            )
        }
    
    async def execute(self, state: LeadState) -> LeadState:
        """Execute advanced sales simulation for the lead"""
        
        if not HAS_AGENTCHAT:
            return self._fallback_simulation(state)
        
        try:
            # Analyze lead and determine optimal simulation approach
            simulation_strategy = self._analyze_lead_requirements(state)
            
            # Run simulation based on strategy
            if self.enable_magentic_one and simulation_strategy["use_orchestrator"]:
                simulation_results = await self._run_magentic_one_simulation(state, simulation_strategy)
            elif self.use_swarm_pattern:
                simulation_results = await self._run_swarm_simulation(state, simulation_strategy)
            else:
                simulation_results = await self._run_selector_group_chat(state, simulation_strategy)
            
            # Update state with results
            self._update_state_with_results(state, simulation_results, simulation_strategy)
            
        except Exception as e:
            self.logger.error(f"Advanced simulation failed for {state.company_name}: {str(e)}")
            state.metadata["simulation_error"] = str(e)
            state.recommended_approach = "Standard discovery call approach"
            state.predicted_conversion = 0.3
        
        return state
    
    def _analyze_lead_requirements(self, state: LeadState) -> Dict[str, Any]:
        """Analyze lead characteristics to determine optimal simulation strategy"""
        
        strategy = {
            "primary_rep_persona": AgentPersona.SMB_REP,
            "conversation_style": ConversationStyle.CONSULTATIVE,
            "use_orchestrator": False,
            "max_turns": 8,
            "engagement_approach": "nurturing",
            "technical_depth": "standard"
        }
        
        # Determine company size category
        company_size = state.company_size or 100
        
        if company_size >= 1000:
            strategy.update({
                "primary_rep_persona": AgentPersona.ENTERPRISE_REP,
                "conversation_style": ConversationStyle.CONSULTATIVE,
                "use_orchestrator": True,
                "max_turns": 12,
                "engagement_approach": "structured",
                "technical_depth": "deep"
            })
        elif company_size >= 500:
            strategy.update({
                "primary_rep_persona": AgentPersona.SMB_REP,
                "max_turns": 10,
                "technical_depth": "moderate"
            })
        
        # Adjust based on industry
        if state.industry:
            industry_lower = state.industry.lower()
            if any(tech_term in industry_lower for tech_term in ['software', 'tech', 'saas', 'ai', 'data']):
                strategy.update({
                    "primary_rep_persona": AgentPersona.TECHNICAL_REP,
                    "conversation_style": ConversationStyle.TECHNICAL,
                    "technical_depth": "deep"
                })
        
        # Adjust based on engagement level
        if state.engagement_level > 0.7:
            strategy.update({
                "engagement_approach": "aggressive",
                "max_turns": min(strategy["max_turns"] + 2, 15)
            })
        elif state.engagement_level < 0.3:
            strategy.update({
                "engagement_approach": "nurturing",
                "conversation_style": ConversationStyle.NURTURING
            })
        
        return strategy
    
    async def _run_swarm_simulation(self, state: LeadState, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation using Swarm pattern for dynamic agent handoffs"""
        
        # Create specialized agents
        agents = self._create_swarm_agents(state, strategy)
        
        # Create swarm team
        swarm_team = Swarm(agents)
        
        # Create initial context message
        initial_message = self._create_swarm_initial_message(state, strategy)
        
        # Run the swarm simulation
        start_time = time.time()
        
        try:
            cancellation_token = CancellationToken() if CancellationToken else None
            
            if cancellation_token:
                chat_result = await asyncio.wait_for(
                    swarm_team.run(task=initial_message, cancellation_token=cancellation_token),
                    timeout=self.conversation_timeout
                )
            else:
                chat_result = await swarm_team.run(task=initial_message)
                
        except asyncio.TimeoutError:
            self.logger.warning(f"Swarm simulation timed out for {state.company_name}")
            raise Exception(f"Simulation timeout after {self.conversation_timeout} seconds")
        
        response_time = time.time() - start_time
        
        # Parse results
        return self._parse_swarm_results(chat_result, state, strategy, response_time)
    
    async def _run_magentic_one_simulation(self, state: LeadState, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation using MagenticOneGroupChat for orchestrated coordination"""
        
        if not self.enable_magentic_one:
            raise ValueError("MagenticOne not enabled")
        
        # Create agents for MagenticOne orchestration
        agents = self._create_magentic_agents(state, strategy)
        
        # Create MagenticOne team
        magentic_team = MagenticOneGroupChat(
            participants=agents,
            max_turns=strategy["max_turns"]
        )
        
        # Create task for orchestrator
        task_description = self._create_magentic_task(state, strategy)
        
        # Run orchestrated simulation
        start_time = time.time()
        
        try:
            chat_result = await asyncio.wait_for(
                magentic_team.run(task=task_description),
                timeout=self.conversation_timeout
            )
        except asyncio.TimeoutError:
            self.logger.warning(f"MagenticOne simulation timed out for {state.company_name}")
            raise Exception(f"Simulation timeout after {self.conversation_timeout} seconds")
        
        response_time = time.time() - start_time
        
        # Parse orchestrated results
        return self._parse_magentic_results(chat_result, state, strategy, response_time)
    
    async def _run_selector_group_chat(self, state: LeadState, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation using SelectorGroupChat with custom selection logic"""
        
        # Create agents
        agents = self._create_selector_agents(state, strategy)
        
        # Create custom selector
        selector = self._create_custom_selector(state, strategy)
        
        # Create selector group chat
        team = SelectorGroupChat(
            participants=agents,
            selector=selector,
            max_turns=strategy["max_turns"]
        )
        
        # Create initial message
        initial_message = self._create_selector_initial_message(state, strategy)
        
        # Run simulation
        start_time = time.time()
        chat_result = await team.run(task=initial_message)
        response_time = time.time() - start_time
        
        return self._parse_selector_results(chat_result, state, strategy, response_time)
    
    def _create_swarm_agents(self, state: LeadState, strategy: Dict[str, Any]) -> List[AssistantAgent]:
        """Create agents for Swarm pattern with handoff capabilities"""
        
        agents = []
        
        # Primary sales rep based on strategy
        primary_persona = strategy["primary_rep_persona"]
        primary_agent = self._create_sales_agent(primary_persona, state, strategy)
        agents.append(primary_agent)
        
        # Technical rep for technical discussions
        if strategy["technical_depth"] != "standard":
            technical_agent = self._create_sales_agent(AgentPersona.TECHNICAL_REP, state, strategy)
            agents.append(technical_agent)
        
        # Prospect agent
        prospect_agent = self._create_prospect_agent(state, strategy)
        agents.append(prospect_agent)
        
        # Manager for analysis
        manager_agent = self._create_manager_agent(state, strategy)
        agents.append(manager_agent)
        
        return agents
    
    def _create_sales_agent(self, persona: AgentPersona, state: LeadState, strategy: Dict[str, Any]) -> AssistantAgent:
        """Create a specialized sales agent based on persona"""
        
        config = self.agent_configs[persona]
        system_message = config.system_message.format(
            company_name=state.company_name,
            industry=state.industry or "technology",
            company_size=state.company_size or "unknown",
            pain_points=", ".join(state.pain_points) if state.pain_points else "standard challenges",
            engagement_approach=strategy["engagement_approach"],
            technical_depth=strategy["technical_depth"]
        )
        
        # Add handoff instructions for Swarm
        if self.use_swarm_pattern:
            system_message += f"""\\n\\nHandoff Instructions:
            You can hand off the conversation to other agents when appropriate:
            - Hand off to 'technical_rep' for technical deep-dives
            - Hand off to 'manager' for final analysis and recommendations
            
            Use the handoff function when you need specialized expertise.
            """
        
        return AssistantAgent(
            name=persona.value,
            model_client=self.model_clients[persona],
            system_message=system_message
        )
    
    def _create_prospect_agent(self, state: LeadState, strategy: Dict[str, Any]) -> AssistantAgent:
        """Create a realistic prospect agent"""
        
        prospect_persona = self._create_prospect_persona(state, strategy)
        
        return AssistantAgent(
            name="prospect",
            model_client=self.model_clients[AgentPersona.PROSPECT],
            system_message=prospect_persona
        )
    
    def _create_manager_agent(self, state: LeadState, strategy: Dict[str, Any]) -> AssistantAgent:
        """Create sales manager agent for analysis"""
        
        manager_message = self.agent_configs[AgentPersona.MANAGER].system_message
        if strategy["conversation_style"] == ConversationStyle.TECHNICAL:
            manager_message += "\\n\\nFocus on technical fit and implementation considerations in your analysis."
        
        return AssistantAgent(
            name="sales_manager",
            model_client=self.model_clients[AgentPersona.MANAGER],
            system_message=manager_message
        )
    
    def _create_prospect_persona(self, state: LeadState, strategy: Dict[str, Any]) -> str:
        """Create detailed prospect persona based on lead data and strategy"""
        
        persona = f"""
        You are {state.contact_name or 'the decision maker'} at {state.company_name}.
        
        Company Profile:
        - Company: {state.company_name}
        - Industry: {state.industry or 'Technology'}
        - Size: {state.company_size or 100} employees
        - Your role: {self._get_prospect_role(state)}
        
        Current Situation:
        """
        
        if state.pain_points:
            persona += f"- Key challenges: {', '.join(state.pain_points)}\\n"
        else:
            persona += "- Generally satisfied but open to improvements\\n"
            
        if state.tech_stack:
            persona += f"- Current tech stack: {', '.join(state.tech_stack)}\\n"
        
        # Add persona characteristics based on strategy
        engagement_style = self._get_prospect_engagement_style(state, strategy)
        persona += f"""
        
        Communication Style: {engagement_style}
        
        Decision-Making Factors:
        - ROI and business impact are critical
        - Implementation complexity is a concern
        - Budget approval process: {self._get_budget_process(state)}
        - Timeline considerations: {self._get_timeline_pressure(state)}
        
        Conversation Approach:
        - Ask specific questions about capabilities
        - Share relevant challenges when solution seems promising
        - Raise realistic objections based on past experiences
        - Request concrete examples and case studies
        - Focus on practical implementation details
        
        Respond naturally as this person would in a real sales conversation.
        Be realistic - not too easy or too difficult to convince.
        """
        
        return persona
    
    def _get_prospect_role(self, state: LeadState) -> str:
        """Determine prospect's role based on company size"""
        if not state.company_size:
            return "Technology decision maker"
        
        if state.company_size >= 1000:
            return "VP of Technology / IT Director"
        elif state.company_size >= 500:
            return "Engineering Manager / IT Manager"
        else:
            return "CTO / Technical Lead"
    
    def _get_prospect_engagement_style(self, state: LeadState, strategy: Dict[str, Any]) -> str:
        """Determine how engaged and responsive the prospect should be"""
        
        base_engagement = state.engagement_level if state.engagement_level else 0.5
        
        if base_engagement > 0.7:
            return "Highly engaged, asks detailed questions, shows strong interest"
        elif base_engagement > 0.4:
            return "Moderately engaged, somewhat skeptical but open to discussion"
        else:
            return "Low engagement, busy and distracted, needs compelling reasons to continue"
    
    def _get_budget_process(self, state: LeadState) -> str:
        """Determine budget approval process complexity"""
        company_size = state.company_size or 100
        
        if company_size >= 1000:
            return "Complex approval process, multiple stakeholders, formal procurement"
        elif company_size >= 500:
            return "Moderate approval process, needs manager approval for significant spend"
        else:
            return "Direct decision-making authority, flexible budget discussions"
    
    def _get_timeline_pressure(self, state: LeadState) -> str:
        """Determine timeline urgency"""
        if state.engagement_level and state.engagement_level > 0.7:
            return "Looking to implement soon, has urgency"
        elif state.pain_points and len(state.pain_points) > 2:
            return "Some urgency due to current challenges"
        else:
            return "No immediate timeline pressure, evaluating options"
    
    def _create_swarm_initial_message(self, state: LeadState, strategy: Dict[str, Any]) -> str:
        """Create initial message for Swarm simulation"""
        
        return f"""
        Initiate a sales discovery call simulation for {state.company_name}.
        
        Context:
        - Company: {state.company_name} ({state.company_size or 'Unknown'} employees)
        - Industry: {state.industry or 'Technology'}
        - Engagement level: {state.engagement_level or 0.5}
        - Strategy: {strategy['engagement_approach']} approach
        
        {strategy['primary_rep_persona'].value.replace('_', ' ').title()}: Begin the conversation with a professional introduction and discovery questions.
        
        Prospect: Respond authentically as the contact from {state.company_name}.
        
        All agents: Use handoffs when appropriate to leverage specialized expertise.
        
        Sales Manager: Observe the conversation and provide final analysis.
        
        Begin the simulation now.
        """
    
    def _create_magentic_task(self, state: LeadState, strategy: Dict[str, Any]) -> str:
        """Create task description for MagenticOne orchestration"""
        
        return f"""
        Orchestrate a comprehensive sales simulation for {state.company_name}.
        
        Objective: Conduct a realistic discovery call that:
        1. Identifies the prospect's key challenges and requirements
        2. Assesses product-market fit and technical alignment
        3. Determines engagement level and buying readiness
        4. Uncovers potential objections and concerns
        5. Establishes next steps and follow-up approach
        
        Company Context:
        - Name: {state.company_name}
        - Industry: {state.industry or 'Technology'}
        - Size: {state.company_size or 'Unknown'} employees
        - Known challenges: {', '.join(state.pain_points) if state.pain_points else 'To be discovered'}
        - Current engagement: {state.engagement_level or 0.5}/1.0
        
        Orchestration Requirements:
        - Coordinate between sales rep, prospect, and technical experts as needed
        - Ensure natural conversation flow with realistic objections
        - Gather sufficient information for accurate conversion prediction
        - Provide actionable recommendations for next steps
        
        Success Metrics:
        - Realistic conversation dynamics
        - Accurate assessment of buying readiness
        - Clear identification of success factors and risks
        - Actionable next steps recommendation
        """
    
    def _create_selector_initial_message(self, state: LeadState, strategy: Dict[str, Any]) -> str:
        """Create initial message for selector group chat"""
        
        return f"""
        Begin sales discovery simulation for {state.company_name}.
        
        The selector will determine the optimal speaking order based on:
        - Conversation flow and context
        - Required expertise for each topic
        - Prospect engagement and questions
        
        Start with introductions and proceed with discovery.
        """
    
    def _create_custom_selector(self, state: LeadState, strategy: Dict[str, Any]):
        """Create custom selector logic for agent coordination"""
        
        def custom_select_speaker(messages, participants):
            """Custom logic to select next speaker based on conversation context"""
            
            if not messages:
                # Start with primary rep
                return strategy['primary_rep_persona'].value
            
            last_message = messages[-1]
            last_speaker = getattr(last_message, 'source', '') if hasattr(last_message, 'source') else ''
            
            # Simple logic - can be enhanced
            if 'technical' in str(last_message).lower():
                return 'technical_rep'
            elif 'analysis' in str(last_message).lower() or len(messages) >= strategy['max_turns'] - 2:
                return 'sales_manager'
            elif 'prospect' in last_speaker:
                return strategy['primary_rep_persona'].value
            else:
                return 'prospect'
        
        return custom_select_speaker
    
    def _create_magentic_agents(self, state: LeadState, strategy: Dict[str, Any]) -> List[AssistantAgent]:
        """Create agents optimized for MagenticOne orchestration"""
        # Similar to swarm agents but optimized for orchestration
        return self._create_swarm_agents(state, strategy)
    
    def _create_selector_agents(self, state: LeadState, strategy: Dict[str, Any]) -> List[AssistantAgent]:
        """Create agents for selector group chat"""
        return self._create_swarm_agents(state, strategy)
    
    def _parse_swarm_results(self, chat_result, state: LeadState, strategy: Dict[str, Any], response_time: float) -> Dict[str, Any]:
        """Parse results from Swarm simulation"""
        return self._parse_simulation_results(chat_result, state, "swarm", response_time)
    
    def _parse_magentic_results(self, chat_result, state: LeadState, strategy: Dict[str, Any], response_time: float) -> Dict[str, Any]:
        """Parse results from MagenticOne simulation"""
        return self._parse_simulation_results(chat_result, state, "magentic_one", response_time)
    
    def _parse_selector_results(self, chat_result, state: LeadState, strategy: Dict[str, Any], response_time: float) -> Dict[str, Any]:
        """Parse results from selector group chat"""
        return self._parse_simulation_results(chat_result, state, "selector", response_time)
    
    def _parse_simulation_results(self, chat_result, state: LeadState, simulation_type: str, response_time: float) -> Dict[str, Any]:
        """Common parsing logic for all simulation types"""
        
        # Extract messages
        conversation_messages = []
        if hasattr(chat_result, 'messages'):
            conversation_messages = chat_result.messages
        elif hasattr(chat_result, 'task_result') and hasattr(chat_result.task_result, 'messages'):
            conversation_messages = chat_result.task_result.messages
        
        # Default results
        results = {
            "conversion_probability": 0.3,
            "recommended_approach": "Follow up with technical demo",
            "conversation_summary": f"Advanced {simulation_type} simulation completed",
            "insights": [],
            "objections": [],
            "success_factors": [],
            "risk_factors": [],
            "simulation_metadata": {
                "type": simulation_type,
                "response_time": response_time,
                "message_count": len(conversation_messages)
            }
        }
        
        # Analyze conversation content
        full_conversation = " ".join([
            str(msg.content) if hasattr(msg, 'content') else str(msg)
            for msg in conversation_messages
        ])
        
        # Enhanced analysis based on advanced patterns
        results = self._analyze_advanced_conversation(full_conversation, state, results)
        
        return results
    
    def _analyze_advanced_conversation(self, conversation: str, state: LeadState, results: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced conversation analysis for sophisticated pattern detection"""
        
        conversation_lower = conversation.lower()
        
        # Sentiment and engagement analysis
        positive_signals = ['interested', 'sounds good', 'exactly', 'perfect', 'impressed', 'excited']
        negative_signals = ['not interested', 'already have', 'too expensive', 'not now', 'complicated']
        
        positive_count = sum(1 for signal in positive_signals if signal in conversation_lower)
        negative_count = sum(1 for signal in negative_signals if signal in conversation_lower)
        
        # Adjust conversion probability based on signals
        signal_adjustment = (positive_count * 0.1) - (negative_count * 0.15)
        results['conversion_probability'] += signal_adjustment
        
        # Technical engagement analysis
        technical_terms = ['integration', 'api', 'security', 'scalability', 'implementation', 'architecture']
        technical_engagement = sum(1 for term in technical_terms if term in conversation_lower)
        
        if technical_engagement > 2:
            results['insights'].append("High technical engagement - prospect has technical requirements")
            results['conversion_probability'] += 0.1
            results['recommended_approach'] = "Schedule technical deep-dive with engineering team"
        
        # Urgency indicators
        urgency_terms = ['urgent', 'asap', 'quickly', 'soon', 'deadline', 'timeline']
        urgency_level = sum(1 for term in urgency_terms if term in conversation_lower)
        
        if urgency_level > 1:
            results['success_factors'].append("Time-sensitive opportunity")
            results['conversion_probability'] += 0.15
        
        # Budget discussion analysis
        budget_terms = ['budget', 'cost', 'price', 'investment', 'roi', 'value']
        budget_discussion = sum(1 for term in budget_terms if term in conversation_lower)
        
        if budget_discussion > 2:
            if any(negative in conversation_lower for negative in ['expensive', 'too much', 'costly']):
                results['objections'].append("Budget constraints")
                results['recommended_approach'] = "Focus on ROI demonstration and flexible pricing"
            else:
                results['success_factors'].append("Budget discussion initiated")
        
        # Competition mentions
        competition_terms = ['competitor', 'alternative', 'currently using', 'comparing']
        competition_mentions = sum(1 for term in competition_terms if term in conversation_lower)
        
        if competition_mentions > 0:
            results['risk_factors'].append("Competitive evaluation in progress")
            results['recommended_approach'] = "Provide competitive differentiation materials"
        
        # Decision-making insights
        decision_terms = ['decision', 'approval', 'stakeholder', 'team', 'board', 'committee']
        decision_complexity = sum(1 for term in decision_terms if term in conversation_lower)
        
        if decision_complexity > 2:
            results['insights'].append("Complex decision-making process identified")
            results['recommended_approach'] = "Map stakeholder engagement strategy"
        
        # Ensure probability bounds
        results['conversion_probability'] = max(0.0, min(1.0, results['conversion_probability']))
        
        # Generate summary based on analysis
        if results['conversion_probability'] > 0.7:
            results['conversation_summary'] = f"Highly positive {results.get('simulation_metadata', {}).get('type', 'advanced')} simulation with strong buying signals"
        elif results['conversion_probability'] > 0.4:
            results['conversation_summary'] = f"Promising {results.get('simulation_metadata', {}).get('type', 'advanced')} simulation with moderate interest"
        else:
            results['conversation_summary'] = f"Challenging {results.get('simulation_metadata', {}).get('type', 'advanced')} simulation requiring nurturing approach"
        
        return results
    
    def _update_state_with_results(self, state: LeadState, results: Dict[str, Any], strategy: Dict[str, Any]):
        """Update lead state with advanced simulation results"""
        
        state.simulation_completed = True
        state.predicted_conversion = results["conversion_probability"]
        state.recommended_approach = results["recommended_approach"]
        
        # Enhanced metadata with strategy and advanced analysis
        state.metadata["advanced_simulation_results"] = {
            "simulation_id": str(uuid.uuid4()),
            "strategy_used": strategy,
            "simulation_type": results.get("simulation_metadata", {}).get("type", "unknown"),
            "conversation_summary": results["conversation_summary"],
            "key_insights": results["insights"],
            "objections_identified": results["objections"],
            "success_factors": results["success_factors"],
            "risk_factors": results["risk_factors"],
            "performance_metrics": results.get("simulation_metadata", {}),
            "agent_configurations": {
                "model_name": self.model_name,
                "base_temperature": self.base_temperature,
                "seed": self.seed,
                "use_swarm_pattern": self.use_swarm_pattern,
                "enable_magentic_one": self.enable_magentic_one
            }
        }
    
    def _fallback_simulation(self, state: LeadState) -> LeadState:
        """Fallback when AutoGen is not available"""
        
        self.logger.warning(f"AutoGen not available, using fallback for {state.company_name}")
        
        state.simulation_completed = True
        state.predicted_conversion = 0.3
        state.recommended_approach = "Standard discovery call approach"
        
        state.metadata["simulation_results"] = {
            "simulation_id": str(uuid.uuid4()),
            "conversation_summary": f"Fallback simulation for {state.company_name}",
            "key_insights": ["Advanced simulation unavailable - AutoGen not installed"],
            "objections_identified": ["Technology constraints"],
            "success_factors": ["Basic lead qualification completed"],
            "risk_factors": ["Limited simulation capability"]
        }
        
        return state
    
    # System message templates for different agent personas
    def _get_enterprise_rep_system_message(self) -> str:
        return """
        You are an experienced enterprise sales representative specializing in large B2B accounts.
        
        Your Expertise:
        - Complex stakeholder navigation
        - Enterprise buying processes
        - ROI and business case development
        - Implementation planning for large organizations
        - Risk mitigation strategies
        
        Your Approach:
        - Professional and consultative
        - Focus on business outcomes and strategic value
        - Ask about governance, compliance, and security requirements
        - Understand multi-stakeholder decision processes
        - Present solutions in terms of enterprise benefits
        
        Company Context: {company_name} ({company_size} employees) in {industry}
        Known challenges: {pain_points}
        Engagement approach: {engagement_approach}
        Technical depth required: {technical_depth}
        
        Conduct a discovery call that uncovers enterprise-level requirements and builds confidence in your solution's ability to serve large organizations.
        """
    
    def _get_smb_rep_system_message(self) -> str:
        return """
        You are an energetic SMB sales representative who excels at building relationships with growing companies.
        
        Your Expertise:
        - Quick rapport building
        - Understanding growth challenges
        - Agile implementation approaches
        - Cost-effective solution positioning
        - Flexible engagement models
        
        Your Approach:
        - Friendly and responsive
        - Focus on immediate value and quick wins
        - Ask about growth plans and scaling challenges
        - Emphasize speed to value and ease of implementation
        - Be flexible on pricing and terms
        
        Company Context: {company_name} ({company_size} employees) in {industry}
        Known challenges: {pain_points}
        Engagement approach: {engagement_approach}
        Technical depth required: {technical_depth}
        
        Conduct a discovery call that resonates with a growing company's needs for efficient, scalable solutions.
        """
    
    def _get_technical_rep_system_message(self) -> str:
        return """
        You are a technical sales specialist with deep product knowledge and engineering background.
        
        Your Expertise:
        - Technical architecture discussions
        - Integration requirements and capabilities
        - Security and compliance frameworks
        - Performance and scalability analysis
        - Implementation methodology
        
        Your Approach:
        - Technically accurate and detailed
        - Ask probing questions about current tech stack
        - Discuss integration patterns and data flows
        - Address security, performance, and reliability concerns
        - Provide technical proof points and documentation
        
        Company Context: {company_name} ({company_size} employees) in {industry}
        Known challenges: {pain_points}
        Engagement approach: {engagement_approach}
        Technical depth required: {technical_depth}
        
        Conduct a discovery call that thoroughly explores technical requirements and demonstrates deep product expertise.
        """
    
    def _get_manager_system_message(self) -> str:
        return """
        You are an experienced sales manager analyzing this conversation for strategic insights.
        
        Your Analysis Framework:
        1. Conversion Probability Assessment (0.0-1.0)
        2. Key Buying Signals and Engagement Level
        3. Identified Pain Points and Business Impact
        4. Technical Requirements and Complexity
        5. Decision-Making Process and Timeline
        6. Competitive Landscape and Positioning
        7. Risk Factors and Potential Objections
        8. Success Factors and Relationship Building
        9. Recommended Next Steps and Strategy
        10. Resource Requirements and Support Needs
        
        Provide your analysis in structured JSON format with:
        - conversion_probability: number between 0.0 and 1.0
        - recommended_approach: string describing next steps
        - insights: array of key observations
        - objections: array of concerns raised
        - success_factors: array of positive indicators
        - risk_factors: array of potential challenges
        - conversation_summary: string summarizing the interaction
        
        Be analytical, objective, and provide actionable recommendations for the sales team.
        """
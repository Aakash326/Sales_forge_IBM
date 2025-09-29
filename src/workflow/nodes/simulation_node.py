from typing import Dict, Any, List, Optional
import json
import asyncio
import uuid
import sys
import os
import time
import logging
from dataclasses import dataclass
from enum import Enum
from pydantic import ValidationError

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.workflow.states.lead_states import LeadState
from src.workflow.schemas.simulation_schemas import (
    SimulationResults, ConversationMetrics, ObjectionAnalysis, 
    NextStepRecommendations, EngagementScoring, validate_simulation_results
)

# Handle optional autogen-agentchat import
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core import CancellationToken
    HAS_AGENTCHAT = True
except ImportError:
    HAS_AGENTCHAT = False
    AssistantAgent = None
    RoundRobinGroupChat = None
    OpenAIChatCompletionClient = None
    CancellationToken = None

class CompanySize(Enum):
    """Company size categories for simulation optimization"""
    STARTUP = "startup"
    SMB = "smb"
    ENTERPRISE = "enterprise"

@dataclass
class ModelUsageStats:
    """Track model usage and costs"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    response_time: float = 0.0
    retry_count: int = 0

class SimulationNode:
    """Node that coordinates sales simulations using AgentChat API"""
    
    def __init__(self, 
                 model_name: str = "gpt-4o-mini",
                 temperature: float = 0.7,
                 seed: Optional[int] = None,
                 max_retries: int = 3,
                 use_json_mode: bool = True,
                 enable_usage_tracking: bool = True):
        """
        Initialize SimulationNode with enhanced model configuration
        
        Args:
            model_name: OpenAI model to use
            temperature: Controls randomness (0.0-2.0)
            seed: For reproducible results
            max_retries: Number of retry attempts on failure
            use_json_mode: Enable JSON object response format
            enable_usage_tracking: Track token usage and costs
        """
        self.model_name = model_name
        self.temperature = temperature
        self.seed = seed
        self.max_retries = max_retries
        self.use_json_mode = use_json_mode
        self.enable_usage_tracking = enable_usage_tracking
        self.usage_stats = ModelUsageStats()
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize model client for autogen-agentchat
        self.model_client = None
        if HAS_AGENTCHAT:
            client_config = {
                "model": model_name,
                "temperature": temperature,
            }
            
            if seed is not None:
                client_config["seed"] = seed
                
            if use_json_mode:
                client_config["response_format"] = {"type": "json_object"}
                
            self.model_client = OpenAIChatCompletionClient(**client_config)
        
    async def execute(self, state: LeadState) -> LeadState:
        """Execute sales simulation for the lead"""
        
        if not HAS_AGENTCHAT:
            # Fallback simulation when agentchat is not available
            print(f"AgentChat not available, using fallback simulation for {state.company_name}")
            state.simulation_completed = True
            state.predicted_conversion = self._calculate_fallback_conversion(state)
            state.recommended_approach = self._get_fallback_approach(state)
            
            state.metadata["simulation_results"] = {
                "simulation_id": str(uuid.uuid4()),
                "conversation_summary": f"Fallback simulation for {state.company_name}",
                "key_insights": ["Simulation completed without AgentChat"],
                "objections_identified": ["Budget concerns", "Implementation timeline"],
                "success_factors": ["Company fit", "Pain point alignment"],
                "risk_factors": ["Competition", "Decision timeline"]
            }
            return state
        
        try:
            # Run the simulation with retry logic
            simulation_results = await self._run_simulation_with_retry(state)
            
            # Update state with simulation results
            state.simulation_completed = True
            state.predicted_conversion = simulation_results.get("conversion_probability", 0.0)
            state.recommended_approach = simulation_results.get("recommended_approach", "")
            
            # Store full simulation results including usage stats
            state.metadata["simulation_results"] = {
                "simulation_id": str(uuid.uuid4()),
                "conversation_summary": simulation_results.get("conversation_summary", ""),
                "key_insights": simulation_results.get("insights", []),
                "objections_identified": simulation_results.get("objections", []),
                "success_factors": simulation_results.get("success_factors", []),
                "risk_factors": simulation_results.get("risk_factors", []),
                "model_usage": {
                    "prompt_tokens": self.usage_stats.prompt_tokens,
                    "completion_tokens": self.usage_stats.completion_tokens,
                    "total_tokens": self.usage_stats.total_tokens,
                    "estimated_cost": self.usage_stats.estimated_cost,
                    "response_time": self.usage_stats.response_time,
                    "retry_count": self.usage_stats.retry_count,
                    "model_name": self.model_name,
                    "temperature": self.temperature,
                    "seed": self.seed
                } if self.enable_usage_tracking else None
            }
            
            # Log usage statistics
            if self.enable_usage_tracking:
                self.logger.info(
                    f"Simulation completed for {state.company_name}: "
                    f"{self.usage_stats.total_tokens} tokens, "
                    f"${self.usage_stats.estimated_cost:.4f} cost, "
                    f"{self.usage_stats.response_time:.2f}s, "
                    f"{self.usage_stats.retry_count} retries"
                )
            
        except Exception as e:
            self.logger.error(f"Simulation failed for {state.company_name}: {str(e)}")
            state.metadata["simulation_error"] = str(e)
            
            # Provide fallback recommendation
            state.recommended_approach = "Standard discovery call approach"
            state.predicted_conversion = 0.3  # Default conservative estimate
        
        return state
    
    def _calculate_fallback_conversion(self, state: LeadState) -> float:
        """Calculate fallback conversion probability without AutoGen"""
        base_score = 0.3
        
        # Adjust based on available data
        if state.company_size and state.company_size > 500:
            base_score += 0.2
        if state.engagement_level > 0.6:
            base_score += 0.2
        if state.pain_points and len(state.pain_points) > 0:
            base_score += 0.1
        if state.research_completed:
            base_score += 0.1
            
        return min(base_score, 1.0)
    
    def _get_fallback_approach(self, state: LeadState) -> str:
        """Get fallback approach recommendation"""
        if state.company_size and state.company_size > 1000:
            return "Enterprise discovery call with technical demo"
        elif state.engagement_level > 0.7:
            return "Schedule product demonstration"
        else:
            return "Standard discovery call approach"
    
    def _get_company_size_category(self, state: LeadState) -> CompanySize:
        """Categorize company size for simulation optimization"""
        if not state.company_size:
            return CompanySize.SMB
        
        if state.company_size < 50:
            return CompanySize.STARTUP
        elif state.company_size < 1000:
            return CompanySize.SMB
        else:
            return CompanySize.ENTERPRISE
    
    def _get_optimized_max_tokens(self, state: LeadState) -> int:
        """Get optimized max_tokens based on company size and complexity"""
        company_size = self._get_company_size_category(state)
        
        base_tokens = {
            CompanySize.STARTUP: 2000,
            CompanySize.SMB: 3000,
            CompanySize.ENTERPRISE: 4000
        }
        
        tokens = base_tokens[company_size]
        
        # Adjust based on available data complexity
        if state.pain_points and len(state.pain_points) > 3:
            tokens += 500
        if state.tech_stack and len(state.tech_stack) > 5:
            tokens += 500
        if state.engagement_level > 0.8:
            tokens += 300
            
        return min(tokens, 8000)  # Cap at reasonable limit
    
    def _calculate_estimated_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate estimated cost based on model and token usage"""
        # Pricing as of 2024 (per 1K tokens)
        pricing = {
            "gpt-4o": {"input": 0.0025, "output": 0.01},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
        }
        
        model_pricing = pricing.get(self.model_name, pricing["gpt-4o-mini"])
        
        input_cost = (prompt_tokens / 1000) * model_pricing["input"]
        output_cost = (completion_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    async def _run_simulation_with_retry(self, state: LeadState) -> Dict[str, Any]:
        """Run simulation with exponential backoff retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    # Exponential backoff: 1s, 2s, 4s, 8s...
                    wait_time = 2 ** (attempt - 1)
                    self.logger.info(f"Retrying simulation for {state.company_name} in {wait_time}s (attempt {attempt + 1})")
                    await asyncio.sleep(wait_time)
                    self.usage_stats.retry_count = attempt
                
                start_time = time.time()
                result = await self._run_sales_simulation(state)
                self.usage_stats.response_time = time.time() - start_time
                
                return result
                
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Simulation attempt {attempt + 1} failed: {str(e)}")
                
                if attempt == self.max_retries:
                    break
        
        # All retries failed
        self.logger.error(f"All simulation attempts failed for {state.company_name}: {str(last_exception)}")
        raise last_exception
    
    async def _run_sales_simulation(self, state: LeadState) -> Dict[str, Any]:
        """Run AutoGen simulation of sales conversation"""
        
        if not HAS_AGENTCHAT:
            # This should not be called if AgentChat is not available
            return {
                "conversion_probability": self._calculate_fallback_conversion(state),
                "recommended_approach": self._get_fallback_approach(state),
                "conversation_summary": "Fallback simulation",
                "insights": [],
                "objections": [],
                "success_factors": [],
                "risk_factors": []
            }
        
        # Configure model client with optimized settings for this simulation
        optimized_max_tokens = self._get_optimized_max_tokens(state)
        
        # Create enhanced model client for this simulation
        simulation_model_config = {
            "model": self.model_name,
            "temperature": self._get_conversation_temperature(state),
            "max_tokens": optimized_max_tokens
        }
        
        if self.seed is not None:
            simulation_model_config["seed"] = self.seed
            
        if self.use_json_mode:
            simulation_model_config["response_format"] = {"type": "json_object"}
        
        simulation_model_client = OpenAIChatCompletionClient(**simulation_model_config)
        
        # Create prospect persona agent
        prospect_agent = AssistantAgent(
            name=f"prospect_{state.company_name.replace(' ', '_').lower()}",
            model_client=simulation_model_client,
            system_message=self._create_prospect_persona(state)
        )
        
        # Create sales rep agent  
        sales_agent = AssistantAgent(
            name="sales_rep",
            model_client=simulation_model_client,
            system_message=self._create_sales_rep_persona(state)
        )
        
        # Create sales manager observer with JSON output instruction
        manager_system_message = self._create_sales_manager_persona()
        if self.use_json_mode:
            manager_system_message += "\n\nIMPORTANT: Provide your analysis in valid JSON format."
            
        sales_manager = AssistantAgent(
            name="sales_manager",
            model_client=simulation_model_client,
            system_message=manager_system_message
        )
        
        # Create group chat team with dynamic turn limit based on company size
        company_size = self._get_company_size_category(state)
        max_turns = {
            CompanySize.STARTUP: 6,
            CompanySize.SMB: 8, 
            CompanySize.ENTERPRISE: 12
        }[company_size]
        
        team = RoundRobinGroupChat(
            participants=[sales_agent, prospect_agent, sales_manager],
            max_turns=max_turns
        )
        
        # Start the simulation
        initial_message = f"""
        Let's simulate a discovery call between our sales rep and the prospect from {state.company_name}.
        
        Sales rep: Start with an introduction and discovery questions.
        Prospect: Respond as the contact from {state.company_name} would.
        Sales manager: Observe and provide analysis at the end.
        
        Begin the simulation now.
        """
        
        # Start the conversation with cancellation token for timeout control
        timeout_seconds = 300  # 5 minutes
        cancellation_token = CancellationToken() if HAS_AGENTCHAT else None
        
        try:
            if cancellation_token:
                chat_result = await asyncio.wait_for(
                    team.run(task=initial_message, cancellation_token=cancellation_token),
                    timeout=timeout_seconds
                )
            else:
                chat_result = await team.run(task=initial_message)
        except asyncio.TimeoutError:
            self.logger.warning(f"Simulation timed out for {state.company_name}")
            raise Exception(f"Simulation timeout after {timeout_seconds} seconds")
        
        # Parse the simulation results
        return self._parse_simulation_results(chat_result, state)
    
    def _create_prospect_persona(self, state: LeadState) -> str:
        """Create a realistic prospect persona for simulation"""
        
        persona = f"""
        You are {state.contact_name or 'the decision maker'} at {state.company_name}.
        
        Company Details:
        - Company: {state.company_name}
        - Industry: {state.industry or 'Technology'}
        - Size: {state.company_size or 100} employees
        - Your role: Decision maker for technology purchases
        
        Current Situation:
        """
        
        if state.pain_points:
            persona += f"- Current challenges: {', '.join(state.pain_points)}\n"
        else:
            persona += "- Generally satisfied with current solutions but open to improvements\n"
            
        if state.tech_stack:
            persona += f"- Current technology: {', '.join(state.tech_stack)}\n"
        else:
            persona += "- Using standard industry technology stack\n"
        
        persona += f"""
        Personality:
        - Busy executive with limited time
        - Skeptical of sales pitches but interested in genuine solutions
        - Wants to understand ROI and business impact
        - Asks tough questions about implementation and support
        - Budget-conscious but willing to invest in proven solutions
        
        Conversation Style:
        - Professional but direct
        - Asks specific questions about features, pricing, and implementation
        - Shares relevant challenges when the solution seems promising
        - Raises realistic objections based on past experiences
        - Wants concrete examples and case studies
        
        Respond naturally as this person would in a real sales conversation.
        Be realistic in your responses - not too easy or too difficult.
        """
        
        return persona
    
    def _get_conversation_temperature(self, state: LeadState) -> float:
        """Get optimized temperature based on engagement level and company type"""
        base_temp = self.temperature
        
        # Adjust temperature based on engagement level
        if state.engagement_level > 0.7:
            # High engagement - be more creative/dynamic
            return min(base_temp + 0.2, 1.0)
        elif state.engagement_level < 0.3:
            # Low engagement - be more conservative/structured
            return max(base_temp - 0.2, 0.1)
        
        return base_temp
    
    def _create_sales_manager_persona(self) -> str:
        """Create an analytical sales manager persona for structured feedback"""
        return """
        You are an experienced sales manager observing this conversation.
        Provide a comprehensive analysis with:
        
        1. Conversion probability (0.0-1.0)
        2. Key insights about the prospect
        3. Recommended approach going forward
        4. Objections that were raised
        5. Success factors identified
        6. Risk factors to watch
        7. Next steps recommendations
        8. Conversation quality assessment
        
        Be analytical, objective, and provide actionable feedback.
        Focus on behavioral cues, engagement level, and business fit.
        Consider the prospect's communication style, pain points expressed,
        and readiness to move forward.
        
        Your analysis should be thorough but concise, suitable for
        immediate action by the sales team.
        """
    
    def _create_sales_rep_persona(self, state: LeadState) -> str:
        """Create an effective sales rep persona for simulation"""
        
        return f"""
        You are an experienced B2B sales representative having a discovery call with a prospect from {state.company_name}.
        
        Your Preparation:
        - You've researched {state.company_name} and know they are in {state.industry or 'the technology'} industry
        - Company size: {state.company_size or 'Unknown'} employees
        - You understand their potential pain points: {', '.join(state.pain_points) if state.pain_points else 'Standard industry challenges'}
        - Previous outreach attempts: {state.outreach_attempts}
        
        Your Selling Style:
        - Consultative approach focused on understanding needs
        - Ask thoughtful discovery questions
        - Listen actively and acknowledge pain points
        - Present relevant solutions based on what you learn
        - Use social proof and case studies when appropriate
        - Handle objections professionally
        - Always look for next steps
        
        Your Goals:
        1. Understand their current situation and challenges
        2. Identify if there's a good fit for your solution
        3. Build rapport and trust
        4. Present value proposition if there's alignment
        5. Secure next steps (demo, proposal, etc.)
        
        Conversation Flow:
        - Introduction and agenda setting
        - Discovery questions about current state
        - Understanding pain points and goals
        - Presenting relevant capabilities
        - Handling questions/objections
        - Next steps discussion
        
        Be professional, helpful, and focus on the prospect's needs.
        Don't be pushy - focus on qualifying and providing value.
        """
    
    def _parse_simulation_results(self, chat_result, state: LeadState) -> Dict[str, Any]:
        """Parse the AutoGen simulation results"""
        
        # Extract conversation messages from autogen-agentchat result
        conversation_messages = []
        if hasattr(chat_result, 'messages'):
            conversation_messages = chat_result.messages
        elif hasattr(chat_result, 'task_result') and hasattr(chat_result.task_result, 'messages'):
            conversation_messages = chat_result.task_result.messages
        
        # Default results structure
        results = {
            "conversion_probability": 0.3,
            "recommended_approach": "Standard discovery approach",
            "conversation_summary": "Simulation completed",
            "insights": [],
            "objections": [],
            "success_factors": [],
            "risk_factors": []
        }
        
        # Analyze conversation for insights
        full_conversation = " ".join([
            msg.content if hasattr(msg, 'content') else msg.get("content", "")
            for msg in conversation_messages
        ])
        
        # Simple keyword-based analysis (could be enhanced with more sophisticated NLP)
        if "interested" in full_conversation.lower():
            results["conversion_probability"] += 0.2
        if "budget" in full_conversation.lower():
            results["conversion_probability"] += 0.1
        if "not interested" in full_conversation.lower():
            results["conversion_probability"] -= 0.2
        if "already have" in full_conversation.lower():
            results["conversion_probability"] -= 0.1
            
        # Ensure probability is between 0 and 1
        results["conversion_probability"] = max(0.0, min(1.0, results["conversion_probability"]))
        
        # Extract insights based on conversation content
        if "price" in full_conversation.lower() or "cost" in full_conversation.lower():
            results["objections"].append("Price sensitivity")
            results["recommended_approach"] = "Focus on ROI and value demonstration"
            
        if "implementation" in full_conversation.lower():
            results["risk_factors"].append("Implementation complexity concerns")
            
        if "demo" in full_conversation.lower():
            results["success_factors"].append("Interest in product demonstration")
            results["recommended_approach"] = "Schedule technical demo"
            
        # Generate conversation summary
        results["conversation_summary"] = f"Simulated discovery call with {state.company_name}. "
        if results["conversion_probability"] > 0.6:
            results["conversation_summary"] += "High interest level identified."
        elif results["conversion_probability"] > 0.4:
            results["conversation_summary"] += "Moderate interest with some concerns."
        else:
            results["conversation_summary"] += "Low initial interest, needs nurturing."
            
        # Add simulation insights
        results["insights"] = [
            f"Predicted conversion probability: {results['conversion_probability']:.1%}",
            f"Recommended next step: {results['recommended_approach']}",
            "Simulation identified key conversation patterns"
        ]
        
        # Validate results against schema if structured output was used
        if self.use_json_mode:
            validation_result = validate_simulation_results(results)
            if not validation_result.is_valid:
                self.logger.warning(f"Validation errors for {state.company_name}: {validation_result.errors}")
            if validation_result.warnings:
                self.logger.info(f"Validation warnings for {state.company_name}: {validation_result.warnings}")
        
        return results
    
    def _extract_structured_pydantic_results(self, conversation_messages: List, state: LeadState) -> Optional[SimulationResults]:
        """Extract and validate structured results using Pydantic models"""
        if not self.use_json_mode:
            return None
            
        # Look for sales manager's final analysis
        manager_messages = [
            msg for msg in conversation_messages 
            if hasattr(msg, 'source') and 'manager' in str(msg.source).lower()
        ]
        
        if not manager_messages:
            return None
            
        try:
            # Get the last manager message (should contain the analysis)
            last_manager_msg = manager_messages[-1]
            content = last_manager_msg.content if hasattr(last_manager_msg, 'content') else str(last_manager_msg)
            
            # Try to parse JSON from the content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                parsed_data = json.loads(json_str)
                
                # Enhance with conversation metrics
                if 'conversation_metrics' not in parsed_data:
                    parsed_data['conversation_metrics'] = self._create_conversation_metrics(conversation_messages, state)
                
                # Ensure required fields exist
                if 'conversation_summary' not in parsed_data:
                    parsed_data['conversation_summary'] = f"Simulation completed for {state.company_name}"
                
                # Create Pydantic model
                simulation_results = SimulationResults(**parsed_data)
                return simulation_results
                
        except (json.JSONDecodeError, ValidationError, KeyError, TypeError) as e:
            self.logger.warning(f"Failed to parse Pydantic structured analysis: {str(e)}")
            
        return None
    
    def _create_conversation_metrics(self, conversation_messages: List, state: LeadState) -> Dict[str, Any]:
        """Create conversation metrics from message analysis"""
        total_turns = len(conversation_messages)
        
        # Analyze conversation for engagement signals
        full_conversation = " ".join([
            str(msg.content) if hasattr(msg, 'content') else str(msg)
            for msg in conversation_messages
        ]).lower()
        
        # Calculate engagement score based on keywords
        engagement_keywords = ['interested', 'tell me more', 'sounds good', 'yes', 'exactly', 'perfect']
        disengagement_keywords = ['no', 'not interested', 'busy', 'later', 'maybe']
        
        engagement_count = sum(1 for keyword in engagement_keywords if keyword in full_conversation)
        disengagement_count = sum(1 for keyword in disengagement_keywords if keyword in full_conversation)
        
        engagement_score = max(0.1, min(1.0, 0.5 + (engagement_count * 0.1) - (disengagement_count * 0.15)))
        
        # Determine conversation quality
        if total_turns >= 10 and engagement_score > 0.7:
            quality = "excellent"
        elif total_turns >= 6 and engagement_score > 0.5:
            quality = "good"
        elif total_turns >= 4:
            quality = "fair"
        else:
            quality = "poor"
        
        # Calculate technical depth
        technical_keywords = ['integration', 'api', 'security', 'implementation', 'technical', 'architecture']
        technical_depth = min(5, sum(1 for keyword in technical_keywords if keyword in full_conversation))
        
        return {
            "total_turns": total_turns,
            "prospect_engagement_score": engagement_score,
            "conversation_quality": quality,
            "technical_depth": technical_depth,
            "rapport_score": min(1.0, engagement_score + 0.1),
            "information_gathered": min(1.0, total_turns / 10.0)
        }

from typing import Dict, Any, List
import json
import asyncio
import uuid
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.workflow.states.lead_states import LeadState

# Handle optional autogen-agentchat import
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    HAS_AGENTCHAT = True
except ImportError:
    HAS_AGENTCHAT = False
    AssistantAgent = None
    RoundRobinGroupChat = None
    OpenAIChatCompletionClient = None

class SimulationNode:
    """Node that coordinates sales simulations using AgentChat API"""
    
    def __init__(self):
        # Initialize model client for autogen-agentchat
        self.model_client = None
        if HAS_AGENTCHAT:
            self.model_client = OpenAIChatCompletionClient(
                model="gpt-4o-mini",
                # api_key will be read from environment variable
            )
        
    def execute(self, state: LeadState) -> LeadState:
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
            # Run the simulation
            simulation_results = asyncio.run(self._run_sales_simulation(state))
            
            # Update state with simulation results
            state.simulation_completed = True
            state.predicted_conversion = simulation_results.get("conversion_probability", 0.0)
            state.recommended_approach = simulation_results.get("recommended_approach", "")
            
            # Store full simulation results
            state.metadata["simulation_results"] = {
                "simulation_id": str(uuid.uuid4()),
                "conversation_summary": simulation_results.get("conversation_summary", ""),
                "key_insights": simulation_results.get("insights", []),
                "objections_identified": simulation_results.get("objections", []),
                "success_factors": simulation_results.get("success_factors", []),
                "risk_factors": simulation_results.get("risk_factors", [])
            }
            
        except Exception as e:
            print(f"Simulation failed for {state.company_name}: {str(e)}")
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
        
        # Create prospect persona agent
        prospect_agent = AssistantAgent(
            name=f"prospect_{state.company_name.replace(' ', '_')}",
            model_client=self.model_client,
            system_message=self._create_prospect_persona(state)
        )
        
        # Create sales rep agent  
        sales_agent = AssistantAgent(
            name="sales_rep",
            model_client=self.model_client,
            system_message=self._create_sales_rep_persona(state)
        )
        
        # Create sales manager observer
        sales_manager = AssistantAgent(
            name="sales_manager",
            model_client=self.model_client,
            system_message="""
            You are an experienced sales manager observing this conversation.
            After the conversation, provide:
            1. Conversion probability (0-1)
            2. Key insights about the prospect
            3. Recommended approach going forward
            4. Objections that were raised
            5. Success factors identified
            6. Risk factors to watch
            
            Be analytical and provide actionable feedback.
            """
        )
        
        # Create group chat team
        team = RoundRobinGroupChat(
            participants=[sales_agent, prospect_agent, sales_manager],
            max_turns=8
        )
        
        # Start the simulation
        initial_message = f"""
        Let's simulate a discovery call between our sales rep and the prospect from {state.company_name}.
        
        Sales rep: Start with an introduction and discovery questions.
        Prospect: Respond as the contact from {state.company_name} would.
        Sales manager: Observe and provide analysis at the end.
        
        Begin the simulation now.
        """
        
        # Start the conversation
        chat_result = await team.run(task=initial_message)
        
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
        
        return results

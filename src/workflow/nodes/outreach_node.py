from typing import Dict, Any, List
from datetime import datetime
import uuid
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.workflow.states.lead_states import LeadState
from src.workflow.states.engagement_states import EngagementState, EngagementInteraction, EngagementType

# Handle optional dependencies
try:
    from crewai import Agent, Task, Crew
    HAS_CREWAI = True
except ImportError:
    HAS_CREWAI = False
    Agent = None
    Task = None
    Crew = None

try:
    from langchain_openai import ChatOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    ChatOpenAI = None

class OutreachNode:
    """Node that coordinates outreach campaigns using CrewAI"""
    
    def __init__(self):
        if HAS_OPENAI and ChatOpenAI and os.getenv('OPENAI_API_KEY'):
            self.llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
        else:
            self.llm = None
            
        if HAS_CREWAI and self.llm:
            self.outreach_crew = self._create_outreach_crew()
        else:
            self.outreach_crew = None
        
    def _create_outreach_crew(self) -> Crew:
        """Create the outreach crew with specialized agents"""
        
        # Email Copywriter
        email_writer = Agent(
            role="Email Copywriting Specialist",
            goal="Create compelling, personalized email campaigns that drive responses",
            backstory="You are a master of email copywriting with expertise in B2B sales outreach. You create personalized, value-driven emails that resonate with prospects.",
            llm=self.llm,
            verbose=True
        )
        
        # LinkedIn Outreach Specialist  
        linkedin_specialist = Agent(
            role="LinkedIn Outreach Specialist",
            goal="Develop LinkedIn connection and messaging strategies",
            backstory="You specialize in LinkedIn sales outreach, creating authentic connection requests and follow-up messages that build relationships.",
            llm=self.llm,
            verbose=True
        )
        
        # Multichannel Coordinator
        channel_coordinator = Agent(
            role="Multichannel Campaign Coordinator", 
            goal="Orchestrate cohesive campaigns across multiple channels",
            backstory="You coordinate outreach across email, LinkedIn, and other channels to create unified, sequential campaigns that maximize engagement.",
            llm=self.llm,
            verbose=True
        )
        
        return Crew(
            agents=[email_writer, linkedin_specialist, channel_coordinator],
            verbose=True
        )
    
    def execute(self, state: LeadState) -> LeadState:
        """Execute outreach campaign for the lead"""
        
        if not HAS_CREWAI or not self.outreach_crew:
            # Fallback outreach when CrewAI is not available
            print(f"CrewAI not available, using fallback outreach for {state.company_name}")
            
            # Simple outreach simulation
            state.outreach_attempts += 1
            state.engagement_level = min(state.engagement_level + 0.2, 1.0)
            state.response_rate = 0.3  # Assume 30% response rate
            state.last_contact = datetime.now()
            
            # Add engagement interaction to metadata
            interaction_data = {
                "interaction_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "type": "EMAIL",
                "content": "Fallback email outreach simulation",
                "response_received": True,
                "engagement_score": 0.6
            }
            
            if 'engagement_history' not in state.metadata:
                state.metadata['engagement_history'] = []
            state.metadata['engagement_history'].append(interaction_data)
            
            state.metadata.update({
                "outreach_method": "fallback",
                "outreach_completed": True
            })
            return state
        
        # Create tasks for the outreach crew
        email_task = Task(
            description=f"""
            Create a personalized email outreach sequence for {state.contact_name or 'the contact'} at {state.company_name}.
            
            Use this context:
            - Company: {state.company_name}
            - Industry: {state.industry or 'Unknown'}
            - Pain Points: {', '.join(state.pain_points) if state.pain_points else 'To be discovered'}
            - Company Size: {state.company_size or 'Unknown'}
            
            Create 3 emails:
            1. Initial outreach email (warm introduction)
            2. Value-focused follow-up (address pain points)
            3. Social proof and case study email
            
            Each email should be concise, personalized, and focused on providing value.
            """,
            agent=self.outreach_crew.agents[0],
            expected_output="Three personalized email templates with subject lines"
        )
        
        linkedin_task = Task(
            description=f"""
            Develop a LinkedIn outreach strategy for {state.contact_name or 'the contact'} at {state.company_name}.
            
            Context:
            - Company: {state.company_name} 
            - Industry: {state.industry or 'Unknown'}
            - Insights: {', '.join(state.key_insights) if state.key_insights else 'Standard approach'}
            
            Create:
            1. Connection request message (personalized)
            2. Follow-up message sequence (2-3 messages)
            3. Content engagement strategy
            
            Keep messages authentic and relationship-focused.
            """,
            agent=self.outreach_crew.agents[1],
            expected_output="LinkedIn outreach sequence with connection strategy"
        )
        
        coordination_task = Task(
            description=f"""
            Create a coordinated multichannel outreach campaign for {state.company_name}.
            
            Combine the email and LinkedIn approaches into a unified campaign:
            1. Optimal sequencing across channels
            2. Timing recommendations  
            3. Message coordination to avoid conflicts
            4. Engagement tracking plan
            5. Follow-up decision points
            
            Ensure consistent messaging and value proposition across all channels.
            """,
            agent=self.outreach_crew.agents[2],
            expected_output="Complete multichannel campaign plan with timeline"
        )
        
        # Add tasks to crew
        self.outreach_crew.tasks = [email_task, linkedin_task, coordination_task]
        
        try:
            # Execute outreach planning
            result = self.outreach_crew.kickoff()
            
            # Simulate outreach execution (in practice this would integrate with email/LinkedIn APIs)
            engagement_results = self._simulate_outreach_execution(state, result)
            
            # Update lead state with outreach results
            state.outreach_attempts += 1
            state.last_contact = datetime.now()
            
            # Update engagement metrics based on simulated results
            if engagement_results.get("email_sent"):
                state.engagement_level += 0.1
            if engagement_results.get("linkedin_connected"):
                state.engagement_level += 0.15
            if engagement_results.get("response_received"):
                state.response_rate = (state.response_rate + 0.3) / state.outreach_attempts
                state.engagement_level += 0.2
            
            state.engagement_level = min(state.engagement_level, 1.0)
            
            # Store outreach campaign details in metadata
            state.metadata["last_outreach_campaign"] = {
                "timestamp": datetime.now().isoformat(),
                "channels": ["email", "linkedin"],
                "campaign_id": str(uuid.uuid4()),
                "results": engagement_results
            }
            
        except Exception as e:
            print(f"Outreach failed for {state.company_name}: {str(e)}")
            state.metadata["outreach_error"] = str(e)
        
        return state
    
    def _simulate_outreach_execution(self, state: LeadState, campaign_plan) -> Dict[str, Any]:
        """Simulate the execution of outreach campaign"""
        
        # In a real implementation, this would:
        # 1. Send actual emails via email API
        # 2. Send LinkedIn messages via LinkedIn API  
        # 3. Track opens, clicks, responses
        # 4. Update CRM with interactions
        
        # For simulation, we'll create realistic engagement outcomes
        import random
        
        results = {
            "email_sent": True,
            "linkedin_connected": random.choice([True, False]),
            "email_opened": random.choice([True, False]),
            "email_clicked": random.choice([True, False]),
            "response_received": random.choice([True, False]),
            "engagement_score": random.uniform(0.1, 0.8)
        }
        
        # Higher engagement for companies with identified pain points
        if state.pain_points:
            results["engagement_score"] *= 1.3
            
        # Adjust response likelihood based on company size
        if state.company_size and state.company_size > 100:
            if random.random() < 0.4:  # 40% chance for larger companies
                results["response_received"] = True
        
        return results
    
    def create_engagement_interactions(self, state: LeadState, results: Dict[str, Any]) -> List[EngagementInteraction]:
        """Create engagement interaction records"""
        
        interactions = []
        
        # Email interaction
        if results.get("email_sent"):
            email_interaction = EngagementInteraction(
                interaction_id=str(uuid.uuid4()),
                type=EngagementType.EMAIL,
                success=results.get("email_opened", False),
                response_received=results.get("response_received", False),
                notes="Outreach email sent via campaign",
                metadata={
                    "clicked": str(results.get("email_clicked", False)),
                    "campaign_type": "initial_outreach"
                }
            )
            interactions.append(email_interaction)
        
        # LinkedIn interaction
        if results.get("linkedin_connected"):
            linkedin_interaction = EngagementInteraction(
                interaction_id=str(uuid.uuid4()),
                type=EngagementType.LINKEDIN,
                success=True,
                response_received=results.get("linkedin_response", False),
                notes="LinkedIn connection request sent",
                metadata={
                    "connection_accepted": str(results.get("linkedin_connected", False))
                }
            )
            interactions.append(linkedin_interaction)
            
        return interactions
import asyncio
import sys
import os
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.workflow.states.lead_states import LeadState

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

class ResearchNode:
    """Node that coordinates lead research using CrewAI"""
    
    def __init__(self):
        if HAS_OPENAI and ChatOpenAI and os.getenv('OPENAI_API_KEY'):
            self.llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
        else:
            self.llm = None
        
        if HAS_CREWAI and self.llm:
            self.research_crew = self._create_research_crew()
        else:
            self.research_crew = None
    
    def _create_research_crew(self) -> Crew:
        """Create the research crew with specialized agents"""
        
        # Company Research Agent
        company_researcher = Agent(
            role="Company Research Specialist",
            goal="Research comprehensive information about target companies",
            backstory="You are an expert at gathering detailed company information including size, industry, tech stack, recent news, and key decision makers.",
            llm=self.llm,
            verbose=True
        )
        
        # Pain Point Analyst
        pain_point_analyst = Agent(
            role="Pain Point Analyst", 
            goal="Identify specific pain points and challenges the company might face",
            backstory="You specialize in analyzing companies to identify operational challenges, inefficiencies, and areas where our solution could provide value.",
            llm=self.llm,
            verbose=True
        )
        
        # Competitive Intelligence Agent
        competitive_analyst = Agent(
            role="Competitive Intelligence Specialist",
            goal="Research competitive landscape and current solutions the company uses",
            backstory="You are expert at analyzing what solutions companies currently use, their satisfaction levels, and competitive opportunities.",
            llm=self.llm,
            verbose=True
        )
        
        return Crew(
            agents=[company_researcher, pain_point_analyst, competitive_analyst],
            verbose=True
        )
    
    def execute(self, state: LeadState) -> LeadState:
        """Execute research on the lead"""
        
        if not HAS_CREWAI or not self.research_crew:
            # Fallback research when CrewAI is not available
            print(f"CrewAI not available, using fallback research for {state.company_name}")
            state.research_completed = True
            state.pain_points = self._get_fallback_pain_points(state)
            state.tech_stack = self._get_fallback_tech_stack(state)
            state.key_insights = self._get_fallback_insights(state)
            
            state.metadata.update({
                "research_method": "fallback",
                "research_completed": True
            })
            return state
        
        # Define research tasks
        company_research_task = Task(
            description=f"""
            Research comprehensive information about {state.company_name}:
            - Company size and employee count
            - Industry and business model  
            - Recent news and developments
            - Technology stack and tools used
            - Key decision makers and their roles
            - Financial information (if publicly available)
            
            Focus on gathering factual, actionable intelligence.
            """,
            agent=self.research_crew.agents[0],
            expected_output="Detailed company profile with key facts and insights"
        )
        
        pain_point_task = Task(
            description=f"""
            Analyze {state.company_name} to identify potential pain points:
            - Operational inefficiencies they might face
            - Industry-specific challenges
            - Growth-related problems
            - Technology gaps or limitations
            - Process improvement opportunities
            
            Provide specific, targeted pain points that our solution could address.
            """,
            agent=self.research_crew.agents[1],
            expected_output="List of specific pain points with supporting rationale"
        )
        
        competitive_task = Task(
            description=f"""
            Research competitive landscape for {state.company_name}:
            - Current solutions they likely use
            - Competitive vendors in their space
            - Market positioning opportunities
            - Switching costs and barriers
            - Competitive advantages we could leverage
            
            Identify opportunities to position against current solutions.
            """,
            agent=self.research_crew.agents[2], 
            expected_output="Competitive analysis with positioning recommendations"
        )
        
        # Add tasks to crew
        self.research_crew.tasks = [company_research_task, pain_point_task, competitive_task]
        
        try:
            # Execute research
            result = self.research_crew.kickoff()
            
            # Parse results and update state
            research_results = self._parse_research_results(result)
            
            state.research_completed = True
            state.pain_points = research_results.get("pain_points", [])
            state.tech_stack = research_results.get("tech_stack", [])
            state.key_insights = research_results.get("insights", [])
            
            # Update company information if found
            if research_results.get("company_size"):
                state.company_size = research_results["company_size"]
            if research_results.get("industry"):
                state.industry = research_results["industry"]
            if research_results.get("annual_revenue"):
                state.annual_revenue = research_results["annual_revenue"]
                
            state.metadata.update(research_results.get("metadata", {}))
            
        except Exception as e:
            print(f"Research failed for {state.company_name}: {str(e)}")
            state.metadata["research_error"] = str(e)
        
        return state
    
    def _parse_research_results(self, crew_result) -> Dict[str, Any]:
        """Parse the crew research results into structured data"""
        
        # This is a simplified parser - in practice you'd want more sophisticated parsing
        results = {
            "pain_points": [],
            "tech_stack": [],
            "insights": [],
            "metadata": {}
        }
        
        # Extract information from crew result
        # The crew result contains the output from all agents
        result_text = str(crew_result)
        
        # Basic parsing - could be enhanced with more sophisticated NLP
        if "pain points" in result_text.lower():
            # Extract pain points (simplified)
            pain_points = self._extract_list_items(result_text, "pain points")
            results["pain_points"] = pain_points
        
        if "technology" in result_text.lower() or "tech stack" in result_text.lower():
            tech_stack = self._extract_list_items(result_text, "technology")
            results["tech_stack"] = tech_stack
            
        # Extract other insights
        results["insights"] = [
            "Research completed by AI crew",
            f"Analysis includes company profile, pain points, and competitive positioning"
        ]
        
        return results
    
    def _extract_list_items(self, text: str, category: str) -> List[str]:
        """Extract list items from text for a given category"""
        # Simplified extraction - in practice use more sophisticated parsing
        lines = text.split('\n')
        items = []
        in_section = False
        
        for line in lines:
            if category.lower() in line.lower():
                in_section = True
                continue
            elif in_section and line.strip().startswith('-'):
                items.append(line.strip().lstrip('- '))
            elif in_section and not line.strip():
                break
                
        return items[:5]
    
    def _get_fallback_pain_points(self, state: LeadState) -> List[str]:
        """Generate fallback pain points based on industry"""
        industry_pain_points = {
            "technology": ["Scalability challenges", "Integration complexity", "Technical debt"],
            "software": ["User adoption", "Feature complexity", "Performance optimization"],
            "healthcare": ["Compliance requirements", "Data security", "Operational efficiency"],
            "manufacturing": ["Supply chain optimization", "Quality control", "Automation needs"],
            "fintech": ["Regulatory compliance", "Security requirements", "Market volatility"]
        }
        
        industry_key = state.industry.lower() if state.industry else "technology"
        for key in industry_pain_points:
            if key in industry_key:
                return industry_pain_points[key]
        
        return ["Process optimization", "Cost reduction", "Operational efficiency"]
    
    def _get_fallback_tech_stack(self, state: LeadState) -> List[str]:
        """Generate fallback tech stack based on company size and industry"""
        if state.company_size and state.company_size > 1000:
            return ["Enterprise CRM", "Cloud Infrastructure", "Business Intelligence", "Security Suite"]
        elif state.company_size and state.company_size > 100:
            return ["CRM System", "Cloud Services", "Collaboration Tools", "Analytics Platform"]
        else:
            return ["Basic CRM", "Cloud Storage", "Communication Tools", "Project Management"]
    
    def _get_fallback_insights(self, state: LeadState) -> List[str]:
        """Generate fallback insights"""
        insights = [f"Company operates in {state.industry or 'technology'} sector"]
        
        if state.company_size:
            if state.company_size > 1000:
                insights.append("Large enterprise with complex needs")
            elif state.company_size > 100:
                insights.append("Mid-market company with growth potential")
            else:
                insights.append("Small company with agility advantages")
        
        return insights
from typing import Dict, Any, List
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from src.workflow.states.lead_states import LeadState

# Handle optional dependencies
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

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

class ScoringNode:
    """Node that coordinates lead scoring using CrewAI analytics"""
    
    def __init__(self):
        if HAS_OPENAI and ChatOpenAI and os.getenv('OPENAI_API_KEY'):
            self.llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
        else:
            self.llm = None
            
        if HAS_CREWAI and self.llm:
            self.analytics_crew = self._create_analytics_crew()
        else:
            self.analytics_crew = None
        
    def _create_analytics_crew(self) -> Crew:
        """Create the analytics crew for lead scoring"""
        
        # Lead Scoring Analyst
        scoring_analyst = Agent(
            role="Lead Scoring Analyst",
            goal="Analyze lead characteristics to calculate comprehensive scores",
            backstory="You are an expert at evaluating lead quality using multiple data points including company profile, engagement history, and market indicators.",
            llm=self.llm,
            verbose=True
        )
        
        # Engagement Analyst
        engagement_analyst = Agent(
            role="Engagement Analytics Specialist", 
            goal="Analyze engagement patterns and predict likelihood of conversion",
            backstory="You specialize in analyzing prospect engagement across multiple channels to predict conversion probability and optimal next actions.",
            llm=self.llm,
            verbose=True
        )
        
        # Market Intelligence Analyst
        market_analyst = Agent(
            role="Market Intelligence Analyst",
            goal="Evaluate market conditions and timing factors for sales success",
            backstory="You analyze market trends, competitive landscape, and economic factors to determine optimal sales timing and approach.",
            llm=self.llm,
            verbose=True
        )
        
        return Crew(
            agents=[scoring_analyst, engagement_analyst, market_analyst],
            verbose=True
        )
    
    def execute(self, state: LeadState) -> LeadState:
        """Execute comprehensive lead scoring"""
        
        # Calculate base scores using quantitative methods
        base_scores = self._calculate_base_scores(state)
        
        if not HAS_CREWAI or not self.analytics_crew:
            # Fallback scoring when CrewAI is not available
            print(f"CrewAI not available, using fallback scoring for {state.company_name}")
            state.lead_score = self._calculate_fallback_score(base_scores)
            state.engagement_level = min(state.engagement_level + 0.1, 1.0)
            state.qualification_score = self._calculate_simple_qualification(state)
            
            state.metadata.update({
                "scoring_method": "fallback",
                "base_scores": base_scores
            })
            return state
        
        # Create analytical tasks for the crew
        lead_scoring_task = Task(
            description=f"""
            Analyze the lead quality for {state.company_name} and provide comprehensive scoring.
            
            Lead Data:
            - Company: {state.company_name}
            - Size: {state.company_size or 'Unknown'} employees
            - Industry: {state.industry or 'Unknown'}
            - Annual Revenue: ${state.annual_revenue or 'Unknown'}
            - Pain Points: {', '.join(state.pain_points) if state.pain_points else 'None identified'}
            - Current Stage: {state.stage}
            
            Base Scores:
            - Company Size Score: {base_scores['company_size_score']:.2f}
            - Industry Fit Score: {base_scores['industry_fit_score']:.2f}
            - Research Quality Score: {base_scores['research_score']:.2f}
            
            Provide:
            1. Overall lead quality assessment (1-100)
            2. Key scoring factors and rationale
            3. Risk factors or concerns
            4. Recommendations for next steps
            """,
            agent=self.analytics_crew.agents[0],
            expected_output="Comprehensive lead quality score with detailed analysis"
        )
        
        engagement_analysis_task = Task(
            description=f"""
            Analyze engagement patterns for {state.company_name} to predict conversion likelihood.
            
            Engagement Data:
            - Outreach Attempts: {state.outreach_attempts}
            - Response Rate: {state.response_rate:.2%}
            - Engagement Level: {state.engagement_level:.2f}
            - Last Contact: {state.last_contact or 'Never'}
            - Research Completed: {state.research_completed}
            
            Current Engagement Score: {base_scores['engagement_score']:.2f}
            
            Analyze:
            1. Engagement trajectory and trends
            2. Response quality indicators
            3. Optimal engagement timing
            4. Conversion probability prediction
            5. Recommended engagement strategy
            """,
            agent=self.analytics_crew.agents[1],
            expected_output="Engagement analysis with conversion probability prediction"
        )
        
        market_timing_task = Task(
            description=f"""
            Evaluate market timing and conditions for {state.company_name} in {state.industry or 'their industry'}.
            
            Company Context:
            - Industry: {state.industry or 'Unknown'}
            - Company Size: {state.company_size or 'Unknown'}
            - Location: {state.location or 'Unknown'}
            - Key Insights: {', '.join(state.key_insights) if state.key_insights else 'None'}
            
            Analyze:
            1. Industry trends affecting buying decisions
            2. Seasonal factors and timing considerations  
            3. Economic conditions impact
            4. Competitive landscape timing
            5. Optimal sales approach timing
            """,
            agent=self.analytics_crew.agents[2],
            expected_output="Market timing analysis with strategic recommendations"
        )
        
        # Add tasks to crew
        self.analytics_crew.tasks = [lead_scoring_task, engagement_analysis_task, market_timing_task]
        
        try:
            # Execute analytics
            result = self.analytics_crew.kickoff()
            
            # Parse analytics results
            analytics_results = self._parse_analytics_results(result, base_scores)
            
            # Update lead state with scores
            state.lead_score = analytics_results['final_lead_score']
            state.engagement_level = analytics_results['updated_engagement_level']
            state.qualification_score = analytics_results['qualification_score']
            
            # Store detailed analytics in metadata
            state.metadata.update({
                "scoring_analysis": analytics_results,
                "base_scores": base_scores,
                "scoring_timestamp": state.updated_at.isoformat()
            })
            
        except Exception as e:
            print(f"Scoring failed for {state.company_name}: {str(e)}")
            state.metadata["scoring_error"] = str(e)
            
            # Fallback to base scores only
            state.lead_score = self._calculate_mean(list(base_scores.values()))
        
        return state
    
    def _calculate_base_scores(self, state: LeadState) -> Dict[str, float]:
        """Calculate quantitative base scores"""
        
        scores = {}
        
        # Company size score (larger companies generally score higher)
        if state.company_size:
            if state.company_size >= 1000:
                scores['company_size_score'] = 0.9
            elif state.company_size >= 500:
                scores['company_size_score'] = 0.8
            elif state.company_size >= 100:
                scores['company_size_score'] = 0.7
            elif state.company_size >= 50:
                scores['company_size_score'] = 0.6
            else:
                scores['company_size_score'] = 0.4
        else:
            scores['company_size_score'] = 0.5  # Unknown
        
        # Industry fit score (based on predefined target industries)
        target_industries = ['technology', 'software', 'saas', 'fintech', 'healthcare', 'manufacturing']
        if state.industry and any(industry in state.industry.lower() for industry in target_industries):
            scores['industry_fit_score'] = 0.8
        else:
            scores['industry_fit_score'] = 0.6
        
        # Research quality score
        research_factors = [
            state.research_completed,
            len(state.pain_points) > 0,
            len(state.key_insights) > 0,
            len(state.tech_stack) > 0
        ]
        scores['research_score'] = sum(research_factors) / len(research_factors)
        
        # Engagement score
        engagement_factors = [
            state.response_rate,
            min(state.engagement_level, 1.0),
            1.0 if state.outreach_attempts > 0 else 0.0
        ]
        scores['engagement_score'] = self._calculate_mean(engagement_factors)
        
        # Revenue potential score
        if state.annual_revenue:
            if state.annual_revenue >= 100_000_000:  # $100M+
                scores['revenue_score'] = 0.9
            elif state.annual_revenue >= 50_000_000:  # $50M+
                scores['revenue_score'] = 0.8
            elif state.annual_revenue >= 10_000_000:  # $10M+
                scores['revenue_score'] = 0.7
            else:
                scores['revenue_score'] = 0.5
        else:
            scores['revenue_score'] = 0.6  # Unknown
        
        return scores
    
    def _parse_analytics_results(self, crew_result, base_scores: Dict[str, float]) -> Dict[str, Any]:
        """Parse crew analytics results and combine with base scores"""
        
        # Extract insights from crew analysis
        result_text = str(crew_result)
        
        # Calculate final weighted scores
        base_score = self._calculate_mean(list(base_scores.values()))
        
        # Adjust based on crew insights (simplified - could use more sophisticated NLP)
        adjustment_factor = 1.0
        
        if "high quality" in result_text.lower() or "strong lead" in result_text.lower():
            adjustment_factor += 0.1
        elif "low quality" in result_text.lower() or "weak lead" in result_text.lower():
            adjustment_factor -= 0.1
            
        if "highly engaged" in result_text.lower():
            adjustment_factor += 0.05
        elif "low engagement" in result_text.lower():
            adjustment_factor -= 0.05
        
        final_lead_score = min(base_score * adjustment_factor, 1.0)
        
        # Calculate qualification score
        qualification_factors = [
            base_scores.get('company_size_score', 0.5),
            base_scores.get('engagement_score', 0.0),
            base_scores.get('research_score', 0.0),
            1.0 if "qualified" in result_text.lower() else 0.5
        ]
        qualification_score = self._calculate_mean(qualification_factors)
        
        return {
            "final_lead_score": final_lead_score,
            "updated_engagement_level": min(base_scores.get('engagement_score', 0.0) + 0.1, 1.0),
            "qualification_score": qualification_score,
            "crew_insights": result_text[:500],  # First 500 chars
            "adjustment_factor": adjustment_factor,
            "scoring_components": base_scores
        }
    
    def _calculate_mean(self, values: List[float]) -> float:
        """Calculate mean without numpy"""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    def _calculate_fallback_score(self, base_scores: Dict[str, float]) -> float:
        """Calculate fallback score when CrewAI is not available"""
        return self._calculate_mean(list(base_scores.values()))
    
    def _calculate_simple_qualification(self, state: LeadState) -> float:
        """Simple qualification scoring without AI analysis"""
        factors = []
        
        if state.company_size:
            if state.company_size > 500:
                factors.append(0.8)
            elif state.company_size > 100:
                factors.append(0.6)
            else:
                factors.append(0.4)
        else:
            factors.append(0.5)
        
        if state.engagement_level > 0.6:
            factors.append(0.8)
        elif state.engagement_level > 0.3:
            factors.append(0.6)
        else:
            factors.append(0.3)
            
        if state.research_completed:
            factors.append(0.7)
        else:
            factors.append(0.3)
            
        return self._calculate_mean(factors)
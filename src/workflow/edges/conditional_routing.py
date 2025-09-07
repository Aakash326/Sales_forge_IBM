from typing import Dict, Any, Literal
from ..states.lead_states import LeadState

class ConditionalRouter:
    """Handles conditional routing between workflow nodes"""
    
    def route_after_research(self, state: LeadState) -> Literal["scoring", "end"]:
        """Route after research node completion"""
        
        # If research completed successfully, proceed to scoring
        if state.research_completed:
            return "scoring"
        
        # If research failed, end workflow
        return "end"
    
    def route_after_outreach(self, state: LeadState) -> Literal["qualify", "simulation", "end"]:
        """Route after outreach node completion"""
        
        # If good engagement, proceed to qualification
        if state.engagement_level > 0.6 and state.response_rate > 0.3:
            return "qualify"
        
        # If moderate engagement, run simulation to optimize approach
        elif state.engagement_level > 0.3:
            return "simulation"
        
        # If poor engagement, end for now (could be nurture sequence)
        else:
            return "end"
    
    def route_after_simulation(self, state: LeadState) -> Literal["qualify", "outreach", "end"]:
        """Route after simulation node completion"""
        
        # If simulation predicts high conversion, proceed to qualification
        if state.predicted_conversion > 0.7:
            return "qualify"
        
        # If simulation suggests different approach, try outreach again
        elif state.predicted_conversion > 0.4 and state.outreach_attempts < 3:
            return "outreach"
        
        # Otherwise end workflow
        else:
            return "end"
    
    def route_after_qualification(self, state: LeadState) -> Literal["handoff", "outreach", "end"]:
        """Route after lead qualification"""
        
        # If highly qualified, hand off to sales
        if state.qualification_score > 0.7:
            return "handoff"
        
        # If somewhat qualified but needs more nurturing
        elif state.qualification_score > 0.4 and state.outreach_attempts < 5:
            return "outreach"
        
        # Otherwise end workflow (could move to nurture sequence)
        else:
            return "end"
    
    def should_continue_outreach(self, state: LeadState) -> bool:
        """Determine if outreach should continue"""
        
        # Continue if we haven't hit attempt limits and there's potential
        return (
            state.outreach_attempts < 5 and
            state.engagement_level > 0.2 and
            state.lead_score > 0.4
        )
    
    def requires_simulation(self, state: LeadState) -> bool:
        """Determine if simulation is needed"""
        
        # Run simulation for complex cases or when initial outreach isn't working
        return (
            state.outreach_attempts > 1 and
            state.response_rate < 0.3 and
            state.lead_score > 0.5
        )
    
    def is_ready_for_handoff(self, state: LeadState) -> bool:
        """Determine if lead is ready for sales handoff"""
        
        return (
            state.qualification_score > 0.7 and
            state.engagement_level > 0.6 and
            state.research_completed and
            state.response_rate > 0.3
        )

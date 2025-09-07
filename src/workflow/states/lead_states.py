from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class LeadState(BaseModel):
    """Main state for lead progression through the pipeline"""
    
    # Lead identification
    lead_id: str = Field(..., description="Unique lead identifier")
    company_name: str = Field(..., description="Company name")
    contact_email: str = Field(..., description="Primary contact email")
    contact_name: Optional[str] = Field(None, description="Primary contact name")
    
    # Company information
    company_size: Optional[int] = Field(None, description="Number of employees")
    industry: Optional[str] = Field(None, description="Industry vertical")
    annual_revenue: Optional[float] = Field(None, description="Annual revenue")
    location: Optional[str] = Field(None, description="Company location")
    
    # Pipeline stage tracking
    stage: str = Field("new", description="Current pipeline stage")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Research results
    research_completed: bool = Field(False, description="Whether research has been completed")
    pain_points: List[str] = Field(default_factory=list, description="Identified pain points")
    tech_stack: List[str] = Field(default_factory=list, description="Technology stack")
    key_insights: List[str] = Field(default_factory=list, description="Key research insights")
    
    # Scoring and analytics
    lead_score: float = Field(0.0, description="Overall lead score")
    engagement_level: float = Field(0.0, description="Engagement level (0-1)")
    qualification_score: float = Field(0.0, description="Qualification score")
    
    # Outreach tracking
    outreach_attempts: int = Field(0, description="Number of outreach attempts")
    response_rate: float = Field(0.0, description="Response rate")
    last_contact: Optional[datetime] = Field(None, description="Last contact date")
    
    # Simulation results
    simulation_completed: bool = Field(False, description="Whether simulation has been run")
    predicted_conversion: float = Field(0.0, description="Predicted conversion probability")
    recommended_approach: Optional[str] = Field(None, description="Recommended approach")
    
    # Sales handoff
    assigned_rep: Optional[str] = Field(None, description="Assigned sales representative")
    handoff_notes: Optional[str] = Field(None, description="Notes for sales handoff")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        arbitrary_types_allowed = True
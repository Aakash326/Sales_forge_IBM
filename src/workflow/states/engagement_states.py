from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EngagementType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    LINKEDIN = "linkedin"
    WEBSITE = "website"
    DEMO = "demo"
    MEETING = "meeting"

class EngagementInteraction(BaseModel):
    """Individual engagement interaction"""
    
    interaction_id: str = Field(..., description="Unique interaction ID")
    type: EngagementType = Field(..., description="Type of engagement")
    timestamp: datetime = Field(default_factory=datetime.now)
    success: bool = Field(False, description="Whether interaction was successful")
    response_received: bool = Field(False, description="Whether response was received")
    sentiment: Optional[str] = Field(None, description="Sentiment of interaction")
    notes: Optional[str] = Field(None, description="Interaction notes")
    metadata: Dict[str, str] = Field(default_factory=dict)

class EngagementState(BaseModel):
    """State for tracking lead engagement across all channels"""
    
    lead_id: str = Field(..., description="Associated lead ID")
    interactions: List[EngagementInteraction] = Field(default_factory=list)
    
    # Aggregated metrics
    total_interactions: int = Field(0, description="Total number of interactions")
    successful_interactions: int = Field(0, description="Number of successful interactions")
    response_count: int = Field(0, description="Number of responses received")
    
    # Channel-specific metrics
    email_opens: int = Field(0, description="Email opens")
    email_clicks: int = Field(0, description="Email clicks")
    linkedin_views: int = Field(0, description="LinkedIn profile views")
    website_visits: int = Field(0, description="Website visits")
    
    # Timing metrics
    first_engagement: Optional[datetime] = Field(None, description="First engagement date")
    last_engagement: Optional[datetime] = Field(None, description="Last engagement date")
    avg_response_time: Optional[float] = Field(None, description="Average response time in hours")
    
    # Engagement quality
    engagement_score: float = Field(0.0, description="Overall engagement score")
    interest_level: str = Field("unknown", description="Assessed interest level")
    
    def add_interaction(self, interaction: EngagementInteraction):
        """Add a new engagement interaction"""
        self.interactions.append(interaction)
        self.total_interactions += 1
        
        if interaction.success:
            self.successful_interactions += 1
        
        if interaction.response_received:
            self.response_count += 1
        
        if not self.first_engagement:
            self.first_engagement = interaction.timestamp
        
        self.last_engagement = interaction.timestamp
        self._update_engagement_score()
    
    def _update_engagement_score(self):
        """Update overall engagement score based on interactions"""
        if self.total_interactions == 0:
            self.engagement_score = 0.0
            return
        
        # Calculate score based on success rate, response rate, and recency
        success_rate = self.successful_interactions / self.total_interactions
        response_rate = self.response_count / self.total_interactions
        
        # Recency bonus (interactions in last 7 days get higher weight)
        recency_bonus = 0.0
        if self.last_engagement:
            days_since_last = (datetime.now() - self.last_engagement).days
            recency_bonus = max(0, (7 - days_since_last) / 7) * 0.2
        
        self.engagement_score = min(1.0, success_rate * 0.4 + response_rate * 0.4 + recency_bonus)

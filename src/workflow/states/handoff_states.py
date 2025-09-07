from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class HandoffStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class SalesRep(BaseModel):
    """Sales representative information"""
    rep_id: str
    name: str
    email: str
    territory: Optional[str] = None
    specialization: Optional[str] = None
    capacity: int = 100  # Current capacity percentage

class HandoffState(BaseModel):
    """State for managing sales handoffs"""
    
    lead_id: str = Field(..., description="Associated lead ID")
    handoff_id: str = Field(..., description="Unique handoff ID")
    
    # Handoff details
    status: HandoffStatus = Field(HandoffStatus.PENDING, description="Handoff status")
    assigned_rep: Optional[SalesRep] = Field(None, description="Assigned sales rep")
    created_at: datetime = Field(default_factory=datetime.now)
    accepted_at: Optional[datetime] = Field(None, description="When handoff was accepted")
    
    # Lead summary for sales rep
    lead_summary: Dict[str, str] = Field(default_factory=dict, description="Lead summary")
    qualification_notes: Optional[str] = Field(None, description="Qualification notes")
    recommended_approach: Optional[str] = Field(None, description="Recommended sales approach")
    key_pain_points: List[str] = Field(default_factory=list, description="Key pain points")
    
    # Engagement history summary
    engagement_summary: Dict[str, int] = Field(default_factory=dict, description="Engagement summary")
    best_contact_method: Optional[str] = Field(None, description="Best method to contact lead")
    contact_preferences: Dict[str, str] = Field(default_factory=dict, description="Contact preferences")
    
    # Handoff requirements
    priority_level: str = Field("medium", description="Priority level (low, medium, high)")
    expected_deal_size: Optional[float] = Field(None, description="Expected deal size")
    timeline: Optional[str] = Field(None, description="Expected timeline")
    
    # Tracking
    handoff_notes: List[str] = Field(default_factory=list, description="Handoff notes")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Additional metadata")
    
    def accept_handoff(self, rep: SalesRep, notes: Optional[str] = None):
        """Accept the handoff"""
        self.status = HandoffStatus.ACCEPTED
        self.assigned_rep = rep
        self.accepted_at = datetime.now()
        if notes:
            self.handoff_notes.append(f"Accepted: {notes}")
    
    def reject_handoff(self, reason: str):
        """Reject the handoff"""
        self.status = HandoffStatus.REJECTED
        self.handoff_notes.append(f"Rejected: {reason}")
"""
Pydantic models for structured simulation outputs using AutoGen 0.4.0+ features
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
from datetime import datetime


class ConversationQuality(str, Enum):
    """Quality assessment of the conversation"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class EngagementLevel(str, Enum):
    """Prospect engagement level"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class UrgencyLevel(str, Enum):
    """Timeline urgency assessment"""
    URGENT = "urgent"
    MODERATE = "moderate"
    LOW = "low"


class BuyingStage(str, Enum):
    """Current stage in buying process"""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    POST_PURCHASE = "post_purchase"


class ObjectionCategory(str, Enum):
    """Categories of sales objections"""
    PRICE = "price"
    BUDGET = "budget"
    TIMING = "timing"
    AUTHORITY = "authority"
    NEED = "need"
    TRUST = "trust"
    COMPETITION = "competition"
    IMPLEMENTATION = "implementation"
    SUPPORT = "support"
    FEATURES = "features"


class RiskLevel(str, Enum):
    """Risk assessment levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ConversationMetrics(BaseModel):
    """Metrics about the conversation quality and engagement"""
    
    total_turns: int = Field(..., ge=0, description="Total number of conversation turns")
    prospect_engagement_score: float = Field(..., ge=0.0, le=1.0, description="Engagement level from 0.0 to 1.0")
    conversation_quality: ConversationQuality = Field(..., description="Overall conversation quality assessment")
    technical_depth: int = Field(default=0, ge=0, le=5, description="Technical discussion depth (0-5)")
    rapport_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Rapport building effectiveness")
    information_gathered: float = Field(default=0.5, ge=0.0, le=1.0, description="Amount of useful information gathered")
    
    class Config:
        use_enum_values = True
        
    @field_validator('prospect_engagement_score', 'rapport_score', 'information_gathered')
    def validate_probability_range(cls, v):
        """Ensure probability values are between 0.0 and 1.0"""
        return max(0.0, min(1.0, v))


class ObjectionAnalysis(BaseModel):
    """Analysis of objections raised during the conversation"""
    
    objection_text: str = Field(..., min_length=1, description="The actual objection as stated")
    category: ObjectionCategory = Field(..., description="Category of the objection")
    severity: RiskLevel = Field(..., description="Severity of this objection")
    potential_responses: List[str] = Field(default_factory=list, description="Suggested responses to address this objection")
    is_resolved: bool = Field(default=False, description="Whether the objection was addressed in the conversation")
    underlying_concern: Optional[str] = Field(None, description="The underlying concern behind the objection")
    
    class Config:
        use_enum_values = True
        
    @field_validator('potential_responses')
    def validate_responses(cls, v):
        """Ensure responses are provided for unresolved objections"""
        return v if v else ["Requires follow-up to address this concern"]


class NextStepRecommendations(BaseModel):
    """Recommended next steps and follow-up actions"""
    
    primary_action: str = Field(..., min_length=1, description="The main recommended next step")
    timeline: str = Field(..., description="Suggested timeline for the next step")
    urgency: UrgencyLevel = Field(..., description="Urgency level for follow-up")
    required_resources: List[str] = Field(default_factory=list, description="Resources needed for next steps")
    stakeholders_to_involve: List[str] = Field(default_factory=list, description="Key stakeholders to include")
    success_criteria: List[str] = Field(default_factory=list, description="How to measure success of next steps")
    alternative_actions: List[str] = Field(default_factory=list, description="Alternative approaches if primary action fails")
    
    class Config:
        use_enum_values = True
        
    @field_validator('required_resources', 'stakeholders_to_involve', 'success_criteria')
    def ensure_non_empty_lists(cls, v):
        """Ensure critical lists are not empty"""
        return v if v else ["To be determined"]


class EngagementScoring(BaseModel):
    """Detailed scoring of prospect engagement and buying signals"""
    
    overall_engagement: float = Field(..., ge=0.0, le=1.0, description="Overall engagement score")
    buying_signals_strength: float = Field(..., ge=0.0, le=1.0, description="Strength of buying signals")
    decision_authority: float = Field(..., ge=0.0, le=1.0, description="Prospect's decision-making authority")
    budget_availability: float = Field(..., ge=0.0, le=1.0, description="Likelihood of budget availability")
    timeline_urgency: float = Field(..., ge=0.0, le=1.0, description="Timeline urgency score")
    technical_fit: float = Field(..., ge=0.0, le=1.0, description="Technical solution fit")
    competitive_position: float = Field(..., ge=0.0, le=1.0, description="Our competitive position strength")
    
    # Engagement details
    positive_signals: List[str] = Field(default_factory=list, description="Positive engagement signals observed")
    negative_signals: List[str] = Field(default_factory=list, description="Negative signals or concerns")
    buying_stage: BuyingStage = Field(..., description="Current stage in buying process")
    
    class Config:
        use_enum_values = True
        
    @field_validator('overall_engagement', 'buying_signals_strength', 'decision_authority', 
              'budget_availability', 'timeline_urgency', 'technical_fit', 'competitive_position')
    def validate_score_range(cls, v):
        """Ensure all scores are between 0.0 and 1.0"""
        return max(0.0, min(1.0, v))
    
    @model_validator(mode='before')
    def calculate_overall_engagement(cls, values):
        """Calculate overall engagement from component scores"""
        if isinstance(values, dict):
            component_scores = [
                values.get('buying_signals_strength', 0.5),
                values.get('decision_authority', 0.5),
                values.get('budget_availability', 0.5),
                values.get('timeline_urgency', 0.5),
                values.get('technical_fit', 0.5),
                values.get('competitive_position', 0.5)
            ]
            
            # Override overall_engagement with calculated value if not provided
            if 'overall_engagement' not in values or values.get('overall_engagement', 0.0) == 0.0:
                values['overall_engagement'] = sum(component_scores) / len(component_scores)
                
        return values


class TechnicalRequirements(BaseModel):
    """Technical requirements and considerations identified"""
    
    integration_needs: List[str] = Field(default_factory=list, description="Integration requirements identified")
    security_requirements: List[str] = Field(default_factory=list, description="Security and compliance needs")
    scalability_concerns: List[str] = Field(default_factory=list, description="Scalability requirements")
    performance_requirements: List[str] = Field(default_factory=list, description="Performance expectations")
    implementation_complexity: RiskLevel = Field(default=RiskLevel.MEDIUM, description="Implementation complexity assessment")
    technical_decision_makers: List[str] = Field(default_factory=list, description="Technical stakeholders identified")
    current_tech_stack: List[str] = Field(default_factory=list, description="Current technology stack mentioned")
    
    class Config:
        use_enum_values = True


class CompetitiveIntelligence(BaseModel):
    """Information about competitive landscape and positioning"""
    
    competitors_mentioned: List[str] = Field(default_factory=list, description="Competitors discussed")
    current_solutions: List[str] = Field(default_factory=list, description="Current solutions in use")
    switching_barriers: List[str] = Field(default_factory=list, description="Barriers to switching solutions")
    our_advantages: List[str] = Field(default_factory=list, description="Our competitive advantages highlighted")
    competitive_threats: List[str] = Field(default_factory=list, description="Competitive threats identified")
    differentiation_opportunities: List[str] = Field(default_factory=list, description="Opportunities to differentiate")


class SimulationResults(BaseModel):
    """Complete structured results from sales simulation"""
    
    # Core assessment
    conversion_probability: float = Field(..., ge=0.0, le=1.0, description="Predicted conversion probability")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the prediction")
    
    # Detailed analysis components
    conversation_metrics: ConversationMetrics = Field(..., description="Conversation quality and engagement metrics")
    objection_analysis: List[ObjectionAnalysis] = Field(default_factory=list, description="Analysis of objections raised")
    next_steps: NextStepRecommendations = Field(..., description="Recommended next steps")
    engagement_scoring: EngagementScoring = Field(..., description="Detailed engagement assessment")
    
    # Optional detailed analysis
    technical_requirements: Optional[TechnicalRequirements] = Field(None, description="Technical requirements identified")
    competitive_intelligence: Optional[CompetitiveIntelligence] = Field(None, description="Competitive landscape insights")
    
    # Summary and insights
    conversation_summary: str = Field(..., min_length=1, description="Summary of the conversation")
    key_insights: List[str] = Field(default_factory=list, description="Key insights from the conversation")
    success_factors: List[str] = Field(default_factory=list, description="Factors supporting success")
    risk_factors: List[str] = Field(default_factory=list, description="Risk factors to monitor")
    
    # Metadata
    simulation_metadata: Dict[str, Any] = Field(default_factory=dict, description="Simulation execution metadata")
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "conversion_probability": 0.75,
                "confidence_score": 0.85,
                "conversation_metrics": {
                    "total_turns": 12,
                    "prospect_engagement_score": 0.8,
                    "conversation_quality": "good",
                    "technical_depth": 3,
                    "rapport_score": 0.7,
                    "information_gathered": 0.85
                },
                "objection_analysis": [
                    {
                        "objection_text": "We're concerned about implementation timeline",
                        "category": "timing",
                        "severity": "medium",
                        "potential_responses": ["Provide detailed implementation plan", "Offer phased rollout"],
                        "is_resolved": False,
                        "underlying_concern": "Resource allocation and business disruption"
                    }
                ],
                "next_steps": {
                    "primary_action": "Schedule technical demo with engineering team",
                    "timeline": "Within 1 week",
                    "urgency": "moderate",
                    "required_resources": ["Technical pre-sales engineer", "Demo environment"],
                    "stakeholders_to_involve": ["CTO", "Lead Engineer", "Project Manager"],
                    "success_criteria": ["Technical requirements validated", "Implementation approach agreed"],
                    "alternative_actions": ["Provide detailed technical documentation", "Reference customer call"]
                },
                "engagement_scoring": {
                    "overall_engagement": 0.75,
                    "buying_signals_strength": 0.8,
                    "decision_authority": 0.9,
                    "budget_availability": 0.7,
                    "timeline_urgency": 0.6,
                    "technical_fit": 0.85,
                    "competitive_position": 0.7,
                    "positive_signals": ["Asked about pricing", "Requested technical demo", "Shared current challenges"],
                    "negative_signals": ["Mentioned budget constraints", "Expressed timeline concerns"],
                    "buying_stage": "evaluation"
                },
                "conversation_summary": "Promising discovery call with strong technical interest and clear pain points identified.",
                "key_insights": [
                    "Strong technical fit identified",
                    "Budget approved but timeline concerns exist",
                    "Decision maker engaged and asking detailed questions"
                ],
                "success_factors": [
                    "Technical requirements align well",
                    "Strong rapport established",
                    "Clear business value demonstrated"
                ],
                "risk_factors": [
                    "Implementation timeline concerns",
                    "Budget approval process unclear",
                    "Competitive evaluation ongoing"
                ]
            }
        }
    
    @field_validator('conversion_probability', 'confidence_score')
    def validate_probability_range(cls, v):
        """Ensure probability values are between 0.0 and 1.0"""
        return max(0.0, min(1.0, v))
    
    @field_validator('key_insights', 'success_factors', 'risk_factors')
    def ensure_insights_exist(cls, v, info):
        """Ensure critical insight fields are not empty"""
        if not v:
            field_name = info.field_name.replace('_', ' ') if info else 'insights'
            return [f"No {field_name} identified in simulation"]
        return v
    
    @model_validator(mode='before')
    def validate_consistency(cls, values):
        """Ensure consistency between conversion probability and other metrics"""
        if isinstance(values, dict):
            conversion_prob = values.get('conversion_probability', 0.5)
            engagement = values.get('engagement_scoring')
            
            if engagement and hasattr(engagement, 'overall_engagement'):
                overall_engagement = engagement.overall_engagement
                
                # Check for inconsistencies
                if conversion_prob > 0.8 and overall_engagement < 0.5:
                    values['conversion_probability'] = min(conversion_prob, overall_engagement + 0.3)
                elif conversion_prob < 0.3 and overall_engagement > 0.7:
                    values['conversion_probability'] = max(conversion_prob, overall_engagement - 0.2)
        
        return values


class SimulationRequest(BaseModel):
    """Request structure for running simulations"""
    
    company_name: str = Field(..., min_length=1, description="Company name for simulation")
    industry: Optional[str] = Field(None, description="Industry sector")
    company_size: Optional[int] = Field(None, ge=1, description="Number of employees")
    contact_name: Optional[str] = Field(None, description="Primary contact name")
    pain_points: List[str] = Field(default_factory=list, description="Known pain points")
    tech_stack: List[str] = Field(default_factory=list, description="Current technology stack")
    engagement_level: Optional[float] = Field(None, ge=0.0, le=1.0, description="Current engagement level")
    outreach_attempts: Optional[int] = Field(None, ge=0, description="Previous outreach attempts")
    
    # Simulation configuration
    simulation_type: str = Field(default="standard", description="Type of simulation to run")
    max_turns: Optional[int] = Field(None, ge=4, le=20, description="Maximum conversation turns")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Model temperature")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "TechCorp Solutions",
                "industry": "Software Development",
                "company_size": 250,
                "contact_name": "John Smith",
                "pain_points": ["Manual processes", "Data silos", "Scalability issues"],
                "tech_stack": ["React", "Node.js", "PostgreSQL", "AWS"],
                "engagement_level": 0.6,
                "outreach_attempts": 2,
                "simulation_type": "advanced",
                "max_turns": 10,
                "temperature": 0.7
            }
        }


class SimulationResponse(BaseModel):
    """Response structure for simulation results"""
    
    simulation_id: str = Field(..., description="Unique simulation identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Simulation timestamp")
    status: str = Field(..., description="Simulation status")
    results: Optional[SimulationResults] = Field(None, description="Simulation results if successful")
    error_message: Optional[str] = Field(None, description="Error message if simulation failed")
    execution_time: Optional[float] = Field(None, ge=0.0, description="Execution time in seconds")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ValidationResult(BaseModel):
    """Result of schema validation"""
    
    is_valid: bool = Field(..., description="Whether the data is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors if any")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": True,
                "errors": [],
                "warnings": ["Low confidence score may indicate unreliable prediction"]
            }
        }


def validate_simulation_results(data: Dict[str, Any]) -> ValidationResult:
    """
    Validate simulation results against the schema
    
    Args:
        data: Raw simulation results data
        
    Returns:
        ValidationResult with validation status and any errors
    """
    errors = []
    warnings = []
    
    try:
        # Attempt to parse with Pydantic model
        SimulationResults.parse_obj(data)
        
        # Additional business logic validation
        conversion_prob = data.get('conversion_probability', 0.5)
        confidence = data.get('confidence_score', 0.5)
        
        if conversion_prob > 0.8 and confidence < 0.6:
            warnings.append("High conversion probability with low confidence may indicate unreliable prediction")
        
        if conversion_prob < 0.2 and len(data.get('success_factors', [])) > 3:
            warnings.append("Low conversion probability conflicts with multiple success factors")
        
        return ValidationResult(is_valid=True, errors=errors, warnings=warnings)
        
    except Exception as e:
        errors.append(f"Schema validation failed: {str(e)}")
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)


def create_example_simulation_results() -> SimulationResults:
    """Create example simulation results for testing"""
    
    return SimulationResults(
        conversion_probability=0.75,
        confidence_score=0.85,
        conversation_metrics=ConversationMetrics(
            total_turns=12,
            prospect_engagement_score=0.8,
            conversation_quality=ConversationQuality.GOOD,
            technical_depth=3,
            rapport_score=0.7,
            information_gathered=0.85
        ),
        objection_analysis=[
            ObjectionAnalysis(
                objection_text="We're concerned about implementation timeline",
                category=ObjectionCategory.TIMING,
                severity=RiskLevel.MEDIUM,
                potential_responses=["Provide detailed implementation plan", "Offer phased rollout"],
                is_resolved=False,
                underlying_concern="Resource allocation and business disruption"
            )
        ],
        next_steps=NextStepRecommendations(
            primary_action="Schedule technical demo with engineering team",
            timeline="Within 1 week",
            urgency=UrgencyLevel.MODERATE,
            required_resources=["Technical pre-sales engineer", "Demo environment"],
            stakeholders_to_involve=["CTO", "Lead Engineer", "Project Manager"],
            success_criteria=["Technical requirements validated", "Implementation approach agreed"],
            alternative_actions=["Provide detailed technical documentation", "Reference customer call"]
        ),
        engagement_scoring=EngagementScoring(
            overall_engagement=0.75,
            buying_signals_strength=0.8,
            decision_authority=0.9,
            budget_availability=0.7,
            timeline_urgency=0.6,
            technical_fit=0.85,
            competitive_position=0.7,
            positive_signals=["Asked about pricing", "Requested technical demo", "Shared current challenges"],
            negative_signals=["Mentioned budget constraints", "Expressed timeline concerns"],
            buying_stage=BuyingStage.EVALUATION
        ),
        conversation_summary="Promising discovery call with strong technical interest and clear pain points identified.",
        key_insights=[
            "Strong technical fit identified",
            "Budget approved but timeline concerns exist",
            "Decision maker engaged and asking detailed questions"
        ],
        success_factors=[
            "Technical requirements align well",
            "Strong rapport established", 
            "Clear business value demonstrated"
        ],
        risk_factors=[
            "Implementation timeline concerns",
            "Budget approval process unclear",
            "Competitive evaluation ongoing"
        ]
    )
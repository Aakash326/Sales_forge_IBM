"""
Behavioral Psychology Agent - Advanced Intelligence Layer
Analyzes decision-maker psychology, communication preferences, and behavioral patterns
Optimizes engagement strategies based on personality profiling and behavioral analysis
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import re

class PersonalityType(Enum):
    ANALYTICAL = "analytical"          # Data-driven, methodical
    DRIVER = "driver"                 # Results-focused, decisive  
    EXPRESSIVE = "expressive"         # Relationship-focused, enthusiastic
    AMIABLE = "amiable"              # Steady, supportive, consensus-building

class CommunicationStyle(Enum):
    DIRECT = "direct"                 # Brief, to-the-point
    DETAILED = "detailed"             # Comprehensive, thorough
    VISUAL = "visual"                 # Charts, diagrams, presentations
    COLLABORATIVE = "collaborative"   # Discussion-based, inclusive

class DecisionMakingStyle(Enum):
    INDIVIDUAL = "individual"         # Makes decisions alone
    CONSENSUS = "consensus"           # Seeks group agreement
    CONSULTATIVE = "consultative"    # Gathers input but decides alone
    DELEGATED = "delegated"          # Delegates to experts/team

class RiskTolerance(Enum):
    CONSERVATIVE = "conservative"     # Risk-averse, prefers proven solutions
    MODERATE = "moderate"            # Balanced approach to risk
    AGGRESSIVE = "aggressive"        # Comfortable with innovative solutions

@dataclass
class PersonalityProfile:
    """Comprehensive personality profile"""
    primary_type: PersonalityType = PersonalityType.ANALYTICAL
    secondary_type: Optional[PersonalityType] = None
    traits: List[str] = None
    strengths: List[str] = None
    potential_concerns: List[str] = None
    confidence_score: float = 0.5
    
    def __post_init__(self):
        if self.traits is None:
            self.traits = []
        if self.strengths is None:
            self.strengths = []
        if self.potential_concerns is None:
            self.potential_concerns = []

@dataclass
class CommunicationPreferences:
    """Communication style and preferences"""
    preferred_style: CommunicationStyle = CommunicationStyle.DIRECT
    optimal_frequency: str = ""
    best_contact_times: List[str] = None
    preferred_channels: List[str] = None
    content_preferences: List[str] = None
    meeting_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.best_contact_times is None:
            self.best_contact_times = []
        if self.preferred_channels is None:
            self.preferred_channels = []
        if self.content_preferences is None:
            self.content_preferences = []
        if self.meeting_preferences is None:
            self.meeting_preferences = {}

@dataclass
class DecisionMakingProcess:
    """Decision-making process analysis"""
    style: DecisionMakingStyle = DecisionMakingStyle.CONSULTATIVE
    timeline: str = ""
    key_influencers: List[str] = None
    evaluation_criteria: List[str] = None
    approval_process: List[str] = None
    risk_factors: List[str] = None
    
    def __post_init__(self):
        if self.key_influencers is None:
            self.key_influencers = []
        if self.evaluation_criteria is None:
            self.evaluation_criteria = []
        if self.approval_process is None:
            self.approval_process = []
        if self.risk_factors is None:
            self.risk_factors = []

@dataclass
class PsychologicalTriggers:
    """Key psychological triggers and motivators"""
    primary_motivators: List[str] = None
    decision_triggers: List[str] = None
    credibility_factors: List[str] = None
    influence_strategies: List[str] = None
    avoidance_factors: List[str] = None
    
    def __post_init__(self):
        if self.primary_motivators is None:
            self.primary_motivators = []
        if self.decision_triggers is None:
            self.decision_triggers = []
        if self.credibility_factors is None:
            self.credibility_factors = []
        if self.influence_strategies is None:
            self.influence_strategies = []
        if self.avoidance_factors is None:
            self.avoidance_factors = []

@dataclass
class OptimalEngagement:
    """Optimal engagement strategy"""
    timing_strategy: Dict[str, Any] = None
    content_strategy: Dict[str, Any] = None
    relationship_strategy: Dict[str, Any] = None
    presentation_strategy: Dict[str, Any] = None
    follow_up_strategy: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timing_strategy is None:
            self.timing_strategy = {}
        if self.content_strategy is None:
            self.content_strategy = {}
        if self.relationship_strategy is None:
            self.relationship_strategy = {}
        if self.presentation_strategy is None:
            self.presentation_strategy = {}
        if self.follow_up_strategy is None:
            self.follow_up_strategy = {}

@dataclass
class BehavioralAnalysis:
    """Complete behavioral psychology analysis"""
    personality_profile: Optional[PersonalityProfile] = None
    communication_preferences: Optional[CommunicationPreferences] = None
    decision_making_process: Optional[DecisionMakingProcess] = None
    psychological_triggers: Optional[PsychologicalTriggers] = None
    optimal_engagement: Optional[OptimalEngagement] = None
    
    # Meta information
    analysis_confidence: float = 0.5
    data_sources: List[str] = None
    analysis_date: datetime = None
    behavioral_patterns: List[str] = None
    
    # Risk assessment
    engagement_risks: List[str] = None
    success_probability: float = 0.5
    
    def __post_init__(self):
        if self.analysis_date is None:
            self.analysis_date = datetime.now()
        if self.data_sources is None:
            self.data_sources = []
        if self.behavioral_patterns is None:
            self.behavioral_patterns = []
        if self.engagement_risks is None:
            self.engagement_risks = []

class BehavioralPsychologyAgent:
    """
    Advanced Behavioral Psychology Agent
    
    Analyzes decision-maker psychology and behavioral patterns:
    - DISC-style personality profiling with confidence scoring
    - Communication preference optimization (timing, channels, content)
    - Decision-making process mapping with stakeholder analysis
    - Psychological trigger identification for persuasion strategies
    - Risk tolerance assessment for solution positioning
    - Optimal engagement timing based on behavioral patterns
    - Customized approach recommendations for maximum success
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Behavioral models and personality frameworks
        self.personality_models = self._initialize_personality_models()
        self.behavioral_patterns = self._load_behavioral_patterns()
        
    def _initialize_personality_models(self) -> Dict[str, Any]:
        """Initialize personality assessment models"""
        return {
            "disc_framework": {
                PersonalityType.ANALYTICAL: {
                    "keywords": ["data", "analysis", "research", "technical", "detailed", "systematic"],
                    "traits": ["Detail-oriented", "Methodical", "Quality-focused", "Reserved"],
                    "strengths": ["Thorough analysis", "High quality standards", "Systematic approach"],
                    "concerns": ["Time pressure", "Incomplete information", "Unproven solutions"],
                    "communication": CommunicationStyle.DETAILED,
                    "decision_style": DecisionMakingStyle.CONSULTATIVE,
                    "risk_tolerance": RiskTolerance.CONSERVATIVE
                },
                PersonalityType.DRIVER: {
                    "keywords": ["results", "goals", "efficiency", "bottom-line", "fast", "decisive"],
                    "traits": ["Results-focused", "Decisive", "Efficient", "Direct"],
                    "strengths": ["Quick decisions", "Goal achievement", "Leadership"],
                    "concerns": ["Delays", "Over-analysis", "Consensus building"],
                    "communication": CommunicationStyle.DIRECT,
                    "decision_style": DecisionMakingStyle.INDIVIDUAL,
                    "risk_tolerance": RiskTolerance.AGGRESSIVE
                },
                PersonalityType.EXPRESSIVE: {
                    "keywords": ["team", "vision", "innovation", "creative", "relationships", "inspiring"],
                    "traits": ["Enthusiastic", "Relationship-focused", "Visionary", "Optimistic"],
                    "strengths": ["Team building", "Innovation", "Inspiration"],
                    "concerns": ["Isolation", "Boring details", "Impersonal approaches"],
                    "communication": CommunicationStyle.VISUAL,
                    "decision_style": DecisionMakingStyle.CONSENSUS,
                    "risk_tolerance": RiskTolerance.MODERATE
                },
                PersonalityType.AMIABLE: {
                    "keywords": ["consensus", "stability", "support", "collaboration", "steady", "reliable"],
                    "traits": ["Supportive", "Steady", "Collaborative", "Loyal"],
                    "strengths": ["Team harmony", "Reliability", "Support"],
                    "concerns": ["Conflict", "Pressure", "Rapid change"],
                    "communication": CommunicationStyle.COLLABORATIVE,
                    "decision_style": DecisionMakingStyle.CONSENSUS,
                    "risk_tolerance": RiskTolerance.CONSERVATIVE
                }
            },
            "role_based_patterns": {
                "ceo": {"primary": PersonalityType.DRIVER, "secondary": PersonalityType.EXPRESSIVE},
                "cto": {"primary": PersonalityType.ANALYTICAL, "secondary": PersonalityType.DRIVER},
                "cfo": {"primary": PersonalityType.ANALYTICAL, "secondary": PersonalityType.AMIABLE},
                "vp_sales": {"primary": PersonalityType.DRIVER, "secondary": PersonalityType.EXPRESSIVE},
                "vp_marketing": {"primary": PersonalityType.EXPRESSIVE, "secondary": PersonalityType.ANALYTICAL},
                "director": {"primary": PersonalityType.AMIABLE, "secondary": PersonalityType.ANALYTICAL},
                "manager": {"primary": PersonalityType.AMIABLE, "secondary": PersonalityType.DRIVER}
            }
        }
    
    def _load_behavioral_patterns(self) -> Dict[str, Any]:
        """Load behavioral patterns and communication preferences"""
        return {
            "timing_patterns": {
                PersonalityType.ANALYTICAL: {
                    "best_days": ["Tuesday", "Wednesday", "Thursday"],
                    "best_times": ["9:00 AM", "2:00 PM"],
                    "worst_times": ["Monday morning", "Friday afternoon"],
                    "response_time": "24-48 hours"
                },
                PersonalityType.DRIVER: {
                    "best_days": ["Monday", "Tuesday", "Wednesday"],
                    "best_times": ["8:00 AM", "1:00 PM"],
                    "worst_times": ["Late afternoon", "End of week"],
                    "response_time": "Same day"
                },
                PersonalityType.EXPRESSIVE: {
                    "best_days": ["Tuesday", "Wednesday", "Thursday"],
                    "best_times": ["10:00 AM", "3:00 PM"],
                    "worst_times": ["Early morning", "Late evening"],
                    "response_time": "1-3 days"
                },
                PersonalityType.AMIABLE: {
                    "best_days": ["Wednesday", "Thursday"],
                    "best_times": ["10:00 AM", "2:00 PM"],
                    "worst_times": ["Monday", "Friday"],
                    "response_time": "2-5 days"
                }
            },
            "content_preferences": {
                PersonalityType.ANALYTICAL: ["Technical specifications", "Data sheets", "Case studies", "ROI analysis"],
                PersonalityType.DRIVER: ["Executive summary", "Bottom-line results", "Implementation timeline", "Success metrics"],
                PersonalityType.EXPRESSIVE: ["Vision presentations", "Success stories", "Team impact", "Innovation highlights"],
                PersonalityType.AMIABLE: ["Reference customers", "Support documentation", "Team testimonials", "Gradual adoption plans"]
            },
            "channel_preferences": {
                PersonalityType.ANALYTICAL: ["Email with attachments", "Detailed proposals", "Technical demos"],
                PersonalityType.DRIVER: ["Brief phone calls", "Executive briefings", "Quick meetings"],
                PersonalityType.EXPRESSIVE: ["Video calls", "Presentations", "Group meetings", "Workshops"],
                PersonalityType.AMIABLE: ["Face-to-face meetings", "Team introductions", "Reference calls"]
            }
        }
    
    async def analyze_behavioral_psychology(
        self,
        contact_data: Dict[str, Any],
        company_data: Dict[str, Any],
        interaction_history: Optional[Dict[str, Any]] = None,
        tactical_results: Optional[Dict[str, Any]] = None
    ) -> BehavioralAnalysis:
        """
        Generate comprehensive behavioral psychology analysis
        
        Analyzes decision-maker psychology to optimize engagement:
        - Personality profiling using DISC framework adaptation
        - Communication preference identification
        - Decision-making process mapping
        - Psychological trigger analysis
        - Optimal engagement strategy development
        """
        
        try:
            analysis = BehavioralAnalysis()
            
            self.logger.info(f"Analyzing behavioral psychology for {contact_data.get('contact_name', 'contact')}")
            
            # Run behavioral analysis tasks in parallel
            tasks = [
                self._analyze_personality_profile(contact_data, company_data, interaction_history),
                self._determine_communication_preferences(contact_data, interaction_history),
                self._map_decision_making_process(contact_data, company_data, tactical_results),
                self._identify_psychological_triggers(contact_data, company_data),
                self._optimize_engagement_strategy(contact_data, company_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            analysis.personality_profile = results[0] if not isinstance(results[0], Exception) else PersonalityProfile()
            analysis.communication_preferences = results[1] if not isinstance(results[1], Exception) else CommunicationPreferences()
            analysis.decision_making_process = results[2] if not isinstance(results[2], Exception) else DecisionMakingProcess()
            analysis.psychological_triggers = results[3] if not isinstance(results[3], Exception) else PsychologicalTriggers()
            analysis.optimal_engagement = results[4] if not isinstance(results[4], Exception) else OptimalEngagement()
            
            # Generate behavioral patterns and insights
            analysis.behavioral_patterns = self._identify_behavioral_patterns(analysis)
            analysis.engagement_risks = self._assess_engagement_risks(analysis)
            analysis.success_probability = self._calculate_success_probability(analysis)
            
            # Calculate overall analysis confidence
            analysis.analysis_confidence = self._calculate_analysis_confidence(analysis, contact_data, interaction_history)
            analysis.data_sources = self._identify_data_sources(contact_data, interaction_history, tactical_results)
            
            self.logger.info(f"Behavioral analysis completed with {analysis.analysis_confidence:.1%} confidence")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Behavioral psychology analysis failed: {e}")
            return BehavioralAnalysis()
    
    async def _analyze_personality_profile(
        self,
        contact_data: Dict[str, Any],
        company_data: Dict[str, Any],
        interaction_history: Optional[Dict[str, Any]]
    ) -> PersonalityProfile:
        """Analyze personality profile using DISC framework"""
        
        profile = PersonalityProfile()
        
        try:
            # Extract personality indicators
            personality_indicators = self._extract_personality_indicators(contact_data, interaction_history)
            
            # Use IBM Granite for advanced personality analysis if available
            if self.granite_client and personality_indicators:
                profile = await self._ai_enhanced_personality_analysis(personality_indicators, contact_data)
            else:
                # Fallback rule-based personality analysis
                profile = self._rule_based_personality_analysis(personality_indicators, contact_data)
            
            # Enhance with role-based patterns
            profile = self._apply_role_based_patterns(profile, contact_data)
            
        except Exception as e:
            self.logger.error(f"Personality profile analysis failed: {e}")
            profile.confidence_score = 0.3
        
        return profile
    
    def _extract_personality_indicators(
        self, 
        contact_data: Dict[str, Any], 
        interaction_history: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract personality indicators from available data"""
        indicators = {
            "keywords": [],
            "role_indicators": [],
            "communication_style_clues": [],
            "behavior_patterns": []
        }
        
        # Extract from job title and role
        title = contact_data.get("title", "").lower()
        role = contact_data.get("role", "").lower()
        
        # Role-based indicators
        if any(word in title + role for word in ["ceo", "president", "founder"]):
            indicators["role_indicators"].append("executive_leader")
        if any(word in title + role for word in ["cto", "technical", "engineer"]):
            indicators["role_indicators"].append("technical_leader")
        if any(word in title + role for word in ["cfo", "financial", "finance"]):
            indicators["role_indicators"].append("financial_leader")
        if any(word in title + role for word in ["sales", "revenue", "business_development"]):
            indicators["role_indicators"].append("sales_leader")
        
        # Extract from bio or description
        bio_text = contact_data.get("bio", "") + " " + contact_data.get("description", "")
        bio_words = bio_text.lower().split()
        
        # Keyword analysis for personality types
        for personality_type, model_data in self.personality_models["disc_framework"].items():
            matching_keywords = [kw for kw in model_data["keywords"] if kw in bio_words]
            if matching_keywords:
                indicators["keywords"].extend([(personality_type, kw) for kw in matching_keywords])
        
        # Interaction history analysis
        if interaction_history:
            response_style = interaction_history.get("response_style", "")
            response_time = interaction_history.get("avg_response_time", "")
            
            if "brief" in response_style or "short" in response_style:
                indicators["communication_style_clues"].append("direct_communicator")
            if "detailed" in response_style or "thorough" in response_style:
                indicators["communication_style_clues"].append("detailed_communicator")
            
            if "same_day" in response_time or "immediate" in response_time:
                indicators["behavior_patterns"].append("quick_responder")
            if "several_days" in response_time or "slow" in response_time:
                indicators["behavior_patterns"].append("deliberate_responder")
        
        return indicators
    
    async def _ai_enhanced_personality_analysis(
        self, 
        indicators: Dict[str, Any], 
        contact_data: Dict[str, Any]
    ) -> PersonalityProfile:
        """Use IBM Granite for advanced personality analysis"""
        
        profile = PersonalityProfile()
        
        try:
            # Create personality analysis prompt
            role = contact_data.get("title", "")
            company_size = contact_data.get("company_size", 0)
            industry = contact_data.get("industry", "")
            
            prompt = f"""
            Analyze personality profile for business decision-maker:
            
            Role: {role}
            Company Size: {company_size} employees
            Industry: {industry}
            
            Available Indicators:
            - Role indicators: {indicators.get('role_indicators', [])}
            - Keywords found: {[kw[1] for kw in indicators.get('keywords', [])]}
            - Communication style: {indicators.get('communication_style_clues', [])}
            - Behavior patterns: {indicators.get('behavior_patterns', [])}
            
            Determine primary personality type from: Analytical, Driver, Expressive, Amiable
            
            Provide analysis in JSON format:
            {{
                "primary_type": "analytical|driver|expressive|amiable",
                "confidence": 0.85,
                "key_traits": ["trait1", "trait2", "trait3"],
                "strengths": ["strength1", "strength2"],
                "concerns": ["concern1", "concern2"]
            }}
            """
            
            response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
            
            try:
                analysis_result = json.loads(response.content)
                
                # Map AI response to personality profile
                type_mapping = {
                    "analytical": PersonalityType.ANALYTICAL,
                    "driver": PersonalityType.DRIVER,
                    "expressive": PersonalityType.EXPRESSIVE,
                    "amiable": PersonalityType.AMIABLE
                }
                
                primary_type = type_mapping.get(analysis_result.get("primary_type", "analytical").lower(), PersonalityType.ANALYTICAL)
                
                profile.primary_type = primary_type
                profile.confidence_score = analysis_result.get("confidence", 0.7)
                profile.traits = analysis_result.get("key_traits", [])
                profile.strengths = analysis_result.get("strengths", [])
                profile.potential_concerns = analysis_result.get("concerns", [])
                
                return profile
                
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse AI personality analysis response")
                
        except Exception as e:
            self.logger.error(f"AI personality analysis failed: {e}")
        
        # Fallback to rule-based analysis
        return self._rule_based_personality_analysis(indicators, contact_data)
    
    def _rule_based_personality_analysis(
        self, 
        indicators: Dict[str, Any], 
        contact_data: Dict[str, Any]
    ) -> PersonalityProfile:
        """Rule-based personality analysis fallback"""
        
        profile = PersonalityProfile()
        
        # Score each personality type based on indicators
        type_scores = {ptype: 0 for ptype in PersonalityType}
        
        # Keyword-based scoring
        for personality_type, keyword in indicators.get("keywords", []):
            type_scores[personality_type] += 1
        
        # Role-based scoring
        role_indicators = indicators.get("role_indicators", [])
        if "executive_leader" in role_indicators:
            type_scores[PersonalityType.DRIVER] += 2
            type_scores[PersonalityType.EXPRESSIVE] += 1
        if "technical_leader" in role_indicators:
            type_scores[PersonalityType.ANALYTICAL] += 2
        if "financial_leader" in role_indicators:
            type_scores[PersonalityType.ANALYTICAL] += 2
            type_scores[PersonalityType.AMIABLE] += 1
        if "sales_leader" in role_indicators:
            type_scores[PersonalityType.DRIVER] += 1
            type_scores[PersonalityType.EXPRESSIVE] += 2
        
        # Communication style scoring
        comm_clues = indicators.get("communication_style_clues", [])
        if "direct_communicator" in comm_clues:
            type_scores[PersonalityType.DRIVER] += 1
        if "detailed_communicator" in comm_clues:
            type_scores[PersonalityType.ANALYTICAL] += 1
        
        # Behavior pattern scoring
        behavior_patterns = indicators.get("behavior_patterns", [])
        if "quick_responder" in behavior_patterns:
            type_scores[PersonalityType.DRIVER] += 1
        if "deliberate_responder" in behavior_patterns:
            type_scores[PersonalityType.ANALYTICAL] += 1
            type_scores[PersonalityType.AMIABLE] += 1
        
        # Determine primary and secondary types
        sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
        
        profile.primary_type = sorted_types[0][0]
        if sorted_types[1][1] > 0:
            profile.secondary_type = sorted_types[1][0]
        
        # Set confidence based on indicator strength
        max_score = sorted_types[0][1]
        profile.confidence_score = min(0.9, max(0.3, max_score / 5.0))
        
        # Set traits based on personality type
        if profile.primary_type in self.personality_models["disc_framework"]:
            model_data = self.personality_models["disc_framework"][profile.primary_type]
            profile.traits = model_data["traits"]
            profile.strengths = model_data["strengths"]
            profile.potential_concerns = model_data["concerns"]
        
        return profile
    
    def _apply_role_based_patterns(self, profile: PersonalityProfile, contact_data: Dict[str, Any]) -> PersonalityProfile:
        """Apply role-based personality patterns"""
        
        role = contact_data.get("title", "").lower()
        
        # Check for role-based patterns
        for role_key, pattern in self.personality_models["role_based_patterns"].items():
            if role_key.replace("_", " ") in role or role_key in role:
                # Boost confidence if rule-based analysis matches role pattern
                if profile.primary_type == pattern["primary"]:
                    profile.confidence_score = min(0.95, profile.confidence_score + 0.2)
                
                # Set secondary type if not already determined
                if not profile.secondary_type:
                    profile.secondary_type = pattern["secondary"]
                
                break
        
        return profile
    
    async def _determine_communication_preferences(
        self,
        contact_data: Dict[str, Any],
        interaction_history: Optional[Dict[str, Any]]
    ) -> CommunicationPreferences:
        """Determine optimal communication preferences"""
        
        preferences = CommunicationPreferences()
        
        try:
            # Base preferences on personality type (if we have it)
            personality_type = getattr(contact_data, 'personality_type', PersonalityType.ANALYTICAL)
            
            # Get timing patterns
            if personality_type in self.behavioral_patterns["timing_patterns"]:
                timing_data = self.behavioral_patterns["timing_patterns"][personality_type]
                preferences.best_contact_times = timing_data["best_times"]
                preferences.optimal_frequency = f"Every {timing_data['response_time']}"
            
            # Get content preferences
            if personality_type in self.behavioral_patterns["content_preferences"]:
                preferences.content_preferences = self.behavioral_patterns["content_preferences"][personality_type]
            
            # Get channel preferences
            if personality_type in self.behavioral_patterns["channel_preferences"]:
                preferences.preferred_channels = self.behavioral_patterns["channel_preferences"][personality_type]
            
            # Set communication style
            if personality_type in self.personality_models["disc_framework"]:
                preferences.preferred_style = self.personality_models["disc_framework"][personality_type]["communication"]
            
            # Meeting preferences based on personality
            preferences.meeting_preferences = self._determine_meeting_preferences(personality_type)
            
            # Override with interaction history if available
            if interaction_history:
                preferences = self._apply_interaction_history(preferences, interaction_history)
            
        except Exception as e:
            self.logger.error(f"Communication preferences analysis failed: {e}")
        
        return preferences
    
    def _determine_meeting_preferences(self, personality_type: PersonalityType) -> Dict[str, Any]:
        """Determine meeting preferences based on personality type"""
        
        meeting_prefs = {
            PersonalityType.ANALYTICAL: {
                "duration": "60-90 minutes",
                "format": "Structured presentation with Q&A",
                "materials": "Detailed agenda, technical documentation",
                "attendees": "Technical team, key stakeholders",
                "follow_up": "Comprehensive summary with action items"
            },
            PersonalityType.DRIVER: {
                "duration": "30-45 minutes",
                "format": "Executive briefing with key decisions",
                "materials": "Executive summary, key metrics",
                "attendees": "Decision makers only",
                "follow_up": "Brief action-oriented summary"
            },
            PersonalityType.EXPRESSIVE: {
                "duration": "45-60 minutes",
                "format": "Interactive presentation with discussion",
                "materials": "Visual presentations, success stories",
                "attendees": "Cross-functional team",
                "follow_up": "Visual summary with next steps"
            },
            PersonalityType.AMIABLE: {
                "duration": "45-75 minutes",
                "format": "Collaborative discussion",
                "materials": "Reference materials, testimonials",
                "attendees": "Full stakeholder team",
                "follow_up": "Detailed notes with consensus points"
            }
        }
        
        return meeting_prefs.get(personality_type, meeting_prefs[PersonalityType.ANALYTICAL])
    
    def _apply_interaction_history(
        self, 
        preferences: CommunicationPreferences, 
        interaction_history: Dict[str, Any]
    ) -> CommunicationPreferences:
        """Apply learning from interaction history"""
        
        # Adjust based on successful past interactions
        successful_channels = interaction_history.get("successful_channels", [])
        if successful_channels:
            preferences.preferred_channels = successful_channels
        
        successful_times = interaction_history.get("successful_contact_times", [])
        if successful_times:
            preferences.best_contact_times = successful_times
        
        response_patterns = interaction_history.get("response_patterns", {})
        if response_patterns.get("prefers_brief_communications"):
            preferences.preferred_style = CommunicationStyle.DIRECT
        elif response_patterns.get("requests_detailed_information"):
            preferences.preferred_style = CommunicationStyle.DETAILED
        
        return preferences
    
    async def _map_decision_making_process(
        self,
        contact_data: Dict[str, Any],
        company_data: Dict[str, Any],
        tactical_results: Optional[Dict[str, Any]]
    ) -> DecisionMakingProcess:
        """Map the decision-making process"""
        
        process = DecisionMakingProcess()
        
        try:
            company_size = company_data.get("company_size", 250)
            industry = company_data.get("industry", "").lower()
            role = contact_data.get("title", "").lower()
            
            # Determine decision-making style based on role and company size
            if any(title in role for title in ["ceo", "founder", "president"]) and company_size < 100:
                process.style = DecisionMakingStyle.INDIVIDUAL
                process.timeline = "2-4 weeks"
            elif any(title in role for title in ["cto", "vp"]) and company_size < 500:
                process.style = DecisionMakingStyle.CONSULTATIVE
                process.timeline = "6-8 weeks"
            elif company_size > 1000:
                process.style = DecisionMakingStyle.CONSENSUS
                process.timeline = "12-16 weeks"
            else:
                process.style = DecisionMakingStyle.CONSULTATIVE
                process.timeline = "8-12 weeks"
            
            # Identify key influencers based on company size and industry
            process.key_influencers = self._identify_key_influencers(company_size, industry, role)
            
            # Determine evaluation criteria
            process.evaluation_criteria = self._determine_evaluation_criteria(industry, role, tactical_results)
            
            # Map approval process
            process.approval_process = self._map_approval_process(company_size, role)
            
            # Identify risk factors
            process.risk_factors = self._identify_decision_risk_factors(process.style, company_size)
            
        except Exception as e:
            self.logger.error(f"Decision-making process mapping failed: {e}")
        
        return process
    
    def _identify_key_influencers(self, company_size: int, industry: str, role: str) -> List[str]:
        """Identify key influencers in the decision process"""
        
        influencers = []
        
        # Base influencers by company size
        if company_size < 100:
            influencers = ["CEO/Founder", "Direct manager", "Key user"]
        elif company_size < 500:
            influencers = ["Executive team", "Department head", "IT/Technical team", "Budget owner"]
        elif company_size < 2000:
            influencers = ["C-level executives", "VPs", "Directors", "IT committee", "Procurement"]
        else:
            influencers = ["Board members", "C-suite", "VPs", "Directors", "IT governance", "Procurement", "Legal"]
        
        # Industry-specific influencers
        if "healthcare" in industry:
            influencers.append("Compliance officer")
        if "fintech" in industry or "financial" in industry:
            influencers.extend(["Risk officer", "Compliance team"])
        if "manufacturing" in industry:
            influencers.append("Operations team")
        
        # Role-specific adjustments
        if "cto" in role or "technical" in role:
            influencers.insert(0, "Engineering team")
        if "cfo" in role or "financial" in role:
            influencers.insert(0, "Finance team")
        
        return influencers[:7]  # Limit to top 7 influencers
    
    def _determine_evaluation_criteria(
        self, 
        industry: str, 
        role: str, 
        tactical_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Determine key evaluation criteria"""
        
        criteria = []
        
        # Base criteria by role
        if any(title in role for title in ["ceo", "president", "founder"]):
            criteria = ["ROI and business impact", "Strategic alignment", "Competitive advantage", "Implementation risk"]
        elif "cto" in role or "technical" in role:
            criteria = ["Technical fit", "Scalability", "Security", "Integration complexity", "Team expertise"]
        elif "cfo" in role or "financial" in role:
            criteria = ["Total cost of ownership", "ROI timeline", "Budget impact", "Financial risk", "Compliance costs"]
        else:
            criteria = ["Functionality", "Ease of use", "Support quality", "Implementation timeline", "Cost"]
        
        # Industry-specific criteria
        if "healthcare" in industry:
            criteria.append("HIPAA compliance")
        if "fintech" in industry:
            criteria.extend(["Regulatory compliance", "Security standards"])
        if "manufacturing" in industry:
            criteria.append("Integration with existing systems")
        
        # Add criteria from tactical results
        if tactical_results:
            pain_points = tactical_results.get("pain_points", [])
            for pain_point in pain_points[:2]:  # Top 2 pain points
                criteria.append(f"Solution to {pain_point}")
        
        return criteria[:8]  # Limit to top 8 criteria
    
    def _map_approval_process(self, company_size: int, role: str) -> List[str]:
        """Map the approval process steps"""
        
        if company_size < 50:
            return ["Owner/founder approval", "Budget confirmation", "Implementation planning"]
        elif company_size < 200:
            return ["Department head approval", "Executive sign-off", "Budget allocation", "Implementation approval"]
        elif company_size < 1000:
            return ["Department approval", "Executive committee review", "Budget committee approval", "IT approval", "Contract negotiation"]
        else:
            return ["Department approval", "VP approval", "Executive committee", "Board approval (if >$X)", "Procurement process", "Legal review", "IT security approval"]
    
    def _identify_decision_risk_factors(self, style: DecisionMakingStyle, company_size: int) -> List[str]:
        """Identify risk factors that could derail the decision"""
        
        risk_factors = []
        
        # Style-based risks
        if style == DecisionMakingStyle.INDIVIDUAL:
            risk_factors = ["Decision maker unavailable", "Lack of stakeholder buy-in", "Insufficient information"]
        elif style == DecisionMakingStyle.CONSENSUS:
            risk_factors = ["Stakeholder disagreement", "Decision paralysis", "Extended timeline", "Budget changes"]
        elif style == DecisionMakingStyle.CONSULTATIVE:
            risk_factors = ["Advisor concerns", "Information gaps", "Priority changes"]
        else:  # DELEGATED
            risk_factors = ["Delegated decision maker changes", "Escalation to higher authority", "Scope creep"]
        
        # Company size risks
        if company_size > 1000:
            risk_factors.extend(["Bureaucratic delays", "Policy changes", "Multiple approval layers"])
        elif company_size < 100:
            risk_factors.extend(["Cash flow issues", "Priority shifts", "Resource constraints"])
        
        return risk_factors[:6]  # Limit to top 6 risk factors
    
    async def _identify_psychological_triggers(
        self,
        contact_data: Dict[str, Any],
        company_data: Dict[str, Any]
    ) -> PsychologicalTriggers:
        """Identify key psychological triggers and motivators"""
        
        triggers = PsychologicalTriggers()
        
        try:
            role = contact_data.get("title", "").lower()
            company_size = company_data.get("company_size", 0)
            industry = company_data.get("industry", "").lower()
            
            # Role-based motivators
            triggers.primary_motivators = self._get_role_motivators(role)
            
            # Industry-specific decision triggers
            triggers.decision_triggers = self._get_industry_triggers(industry)
            
            # Credibility factors based on role and company
            triggers.credibility_factors = self._get_credibility_factors(role, company_size)
            
            # Influence strategies based on personality patterns
            triggers.influence_strategies = self._get_influence_strategies(role, company_size)
            
            # Avoidance factors (what NOT to do)
            triggers.avoidance_factors = self._get_avoidance_factors(role)
            
        except Exception as e:
            self.logger.error(f"Psychological triggers identification failed: {e}")
        
        return triggers
    
    def _get_role_motivators(self, role: str) -> List[str]:
        """Get primary motivators based on role"""
        
        if any(title in role for title in ["ceo", "president", "founder"]):
            return ["Business growth", "Competitive advantage", "Strategic vision", "Market leadership", "Shareholder value"]
        elif "cto" in role or "technical" in role:
            return ["Technical excellence", "Innovation", "System reliability", "Team efficiency", "Architecture quality"]
        elif "cfo" in role or "financial" in role:
            return ["Cost optimization", "ROI maximization", "Financial risk management", "Budget control", "Compliance"]
        elif "sales" in role or "revenue" in role:
            return ["Revenue growth", "Sales efficiency", "Team performance", "Market expansion", "Customer satisfaction"]
        elif "marketing" in role:
            return ["Brand growth", "Lead generation", "Customer engagement", "Market positioning", "Campaign effectiveness"]
        else:
            return ["Operational efficiency", "Team productivity", "Problem solving", "Process improvement", "Quality delivery"]
    
    def _get_industry_triggers(self, industry: str) -> List[str]:
        """Get decision triggers specific to industry"""
        
        if "healthcare" in industry:
            return ["Patient safety", "Regulatory compliance", "Cost reduction", "Operational efficiency"]
        elif "fintech" in industry or "financial" in industry:
            return ["Regulatory compliance", "Risk management", "Customer trust", "Market expansion"]
        elif "manufacturing" in industry:
            return ["Operational efficiency", "Quality improvement", "Cost reduction", "Supply chain optimization"]
        elif "retail" in industry:
            return ["Customer experience", "Inventory optimization", "Sales growth", "Omnichannel integration"]
        elif "software" in industry or "tech" in industry:
            return ["Technical innovation", "Scalability", "Development efficiency", "Competitive differentiation"]
        else:
            return ["Efficiency improvement", "Cost reduction", "Growth enablement", "Competitive advantage"]
    
    def _get_credibility_factors(self, role: str, company_size: int) -> List[str]:
        """Get factors that establish credibility"""
        
        base_factors = ["Industry expertise", "Technical competence", "Proven track record", "Customer references"]
        
        # Role-specific credibility factors
        if any(title in role for title in ["ceo", "president", "founder"]):
            base_factors.extend(["Strategic vision", "Business acumen", "Market knowledge"])
        elif "cto" in role or "technical" in role:
            base_factors.extend(["Technical depth", "Architecture expertise", "Security knowledge"])
        elif "cfo" in role:
            base_factors.extend(["Financial modeling", "Risk assessment", "Compliance expertise"])
        
        # Company size factors
        if company_size > 1000:
            base_factors.extend(["Enterprise experience", "Scalability proof", "Compliance track record"])
        elif company_size < 100:
            base_factors.extend(["Startup agility", "Cost-effectiveness", "Growth support"])
        
        return base_factors[:8]  # Top 8 credibility factors
    
    def _get_influence_strategies(self, role: str, company_size: int) -> List[str]:
        """Get effective influence strategies"""
        
        strategies = []
        
        # Role-based strategies
        if any(title in role for title in ["ceo", "president", "founder"]):
            strategies = ["Present strategic vision", "Show competitive advantage", "Demonstrate ROI", "Highlight market opportunity"]
        elif "cto" in role or "technical" in role:
            strategies = ["Technical deep dive", "Architecture discussion", "Security analysis", "Integration planning"]
        elif "cfo" in role:
            strategies = ["Financial modeling", "Cost-benefit analysis", "Risk assessment", "Budget planning"]
        else:
            strategies = ["Problem-solution fit", "Ease of implementation", "Team impact", "Success metrics"]
        
        # Company size strategies
        if company_size > 1000:
            strategies.append("Enterprise case studies")
        elif company_size < 100:
            strategies.append("Quick wins and agile implementation")
        
        return strategies[:6]
    
    def _get_avoidance_factors(self, role: str) -> List[str]:
        """Get factors to avoid (red flags)"""
        
        if any(title in role for title in ["ceo", "president", "founder"]):
            return ["Over-technical details", "Long implementation timelines", "Unclear ROI", "Vendor lock-in concerns"]
        elif "cto" in role or "technical" in role:
            return ["Overselling business benefits", "Ignoring technical concerns", "Security shortcomings", "Integration complexity"]
        elif "cfo" in role:
            return ["Vague financial projections", "Hidden costs", "Unclear contract terms", "Compliance risks"]
        else:
            return ["Overwhelming complexity", "Unclear benefits", "Poor support reputation", "High implementation risk"]
    
    async def _optimize_engagement_strategy(
        self,
        contact_data: Dict[str, Any],
        company_data: Dict[str, Any]
    ) -> OptimalEngagement:
        """Develop optimal engagement strategy"""
        
        engagement = OptimalEngagement()
        
        try:
            # Timing strategy
            engagement.timing_strategy = {
                "optimal_cadence": "Weekly during evaluation phase",
                "best_contact_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_contact_times": ["9:00-11:00 AM", "2:00-4:00 PM"],
                "response_expectations": "24-48 hours",
                "meeting_scheduling": "1-2 weeks advance notice"
            }
            
            # Content strategy
            engagement.content_strategy = {
                "primary_content_type": "Executive briefings with supporting detail",
                "content_sequence": [
                    "Initial value proposition",
                    "Technical deep dive", 
                    "Business case presentation",
                    "Implementation planning",
                    "Reference discussions"
                ],
                "supporting_materials": ["Case studies", "ROI calculator", "Technical specifications"],
                "personalization_focus": "Industry-specific challenges and solutions"
            }
            
            # Relationship strategy
            engagement.relationship_strategy = {
                "primary_contact_approach": "Professional and consultative",
                "stakeholder_mapping": "Identify and engage all decision influencers",
                "trust_building_activities": ["Industry insights sharing", "Peer introductions", "Reference calls"],
                "relationship_timeline": "Build over 8-12 weeks"
            }
            
            # Presentation strategy
            engagement.presentation_strategy = {
                "format_preference": "Structured presentation with interactive Q&A",
                "duration": "45-60 minutes",
                "key_elements": ["Problem validation", "Solution demonstration", "Business case", "Implementation plan"],
                "success_metrics": "Clear next steps defined",
                "follow_up_approach": "Comprehensive summary with action items"
            }
            
            # Follow-up strategy
            engagement.follow_up_strategy = {
                "immediate_follow_up": "Same day summary email",
                "ongoing_cadence": "Weekly progress updates",
                "value_add_touchpoints": "Industry insights and relevant content",
                "milestone_check_ins": "Every 2 weeks during evaluation",
                "nurture_approach": "Educational and consultative"
            }
            
        except Exception as e:
            self.logger.error(f"Engagement strategy optimization failed: {e}")
        
        return engagement
    
    def _identify_behavioral_patterns(self, analysis: BehavioralAnalysis) -> List[str]:
        """Identify key behavioral patterns from the analysis"""
        
        patterns = []
        
        # Personality-based patterns
        if analysis.personality_profile:
            personality_type = analysis.personality_profile.primary_type
            patterns.append(f"Primary personality type: {personality_type.value}")
            
            if analysis.personality_profile.confidence_score > 0.7:
                patterns.append("High confidence in personality assessment")
            elif analysis.personality_profile.confidence_score < 0.5:
                patterns.append("Low confidence - requires more behavioral data")
        
        # Communication patterns
        if analysis.communication_preferences:
            comm_style = analysis.communication_preferences.preferred_style
            patterns.append(f"Prefers {comm_style.value} communication style")
            
            if analysis.communication_preferences.best_contact_times:
                patterns.append(f"Optimal contact timing identified")
        
        # Decision-making patterns
        if analysis.decision_making_process:
            decision_style = analysis.decision_making_process.style
            patterns.append(f"Uses {decision_style.value} decision-making approach")
            
            timeline = analysis.decision_making_process.timeline
            if timeline:
                patterns.append(f"Decision timeline: {timeline}")
        
        return patterns[:6]  # Limit to top 6 patterns
    
    def _assess_engagement_risks(self, analysis: BehavioralAnalysis) -> List[str]:
        """Assess risks in the engagement approach"""
        
        risks = []
        
        # Confidence-based risks
        if analysis.analysis_confidence < 0.5:
            risks.append("Low analysis confidence - may require strategy adjustments")
        
        # Personality-based risks
        if analysis.personality_profile and analysis.personality_profile.potential_concerns:
            risks.extend([f"Potential concern: {concern}" for concern in analysis.personality_profile.potential_concerns[:2]])
        
        # Decision-making risks
        if analysis.decision_making_process and analysis.decision_making_process.risk_factors:
            risks.extend(analysis.decision_making_process.risk_factors[:2])
        
        # Communication risks
        if analysis.communication_preferences:
            if not analysis.communication_preferences.best_contact_times:
                risks.append("Optimal contact timing not established")
        
        return risks[:5]  # Limit to top 5 risks
    
    def _calculate_success_probability(self, analysis: BehavioralAnalysis) -> float:
        """Calculate probability of engagement success"""
        
        success_factors = []
        
        # Analysis confidence factor
        success_factors.append(analysis.analysis_confidence)
        
        # Personality profile confidence
        if analysis.personality_profile:
            success_factors.append(analysis.personality_profile.confidence_score)
        else:
            success_factors.append(0.3)
        
        # Decision-making process clarity
        if analysis.decision_making_process and analysis.decision_making_process.timeline:
            success_factors.append(0.8)  # Clear process = higher success
        else:
            success_factors.append(0.5)
        
        # Communication alignment
        if analysis.communication_preferences and analysis.communication_preferences.preferred_channels:
            success_factors.append(0.7)
        else:
            success_factors.append(0.4)
        
        # Psychological trigger identification
        if analysis.psychological_triggers and analysis.psychological_triggers.primary_motivators:
            success_factors.append(0.8)
        else:
            success_factors.append(0.5)
        
        # Calculate weighted average
        return sum(success_factors) / len(success_factors)
    
    def _calculate_analysis_confidence(
        self,
        analysis: BehavioralAnalysis,
        contact_data: Dict[str, Any],
        interaction_history: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate overall analysis confidence"""
        
        confidence_factors = []
        
        # Data richness factor
        data_fields = len([v for v in contact_data.values() if v])
        data_richness = min(1.0, data_fields / 10.0)  # Normalize to max 1.0
        confidence_factors.append(data_richness)
        
        # Interaction history factor
        if interaction_history:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Individual analysis confidences
        if analysis.personality_profile:
            confidence_factors.append(analysis.personality_profile.confidence_score)
        
        # Method diversity (more analysis methods = higher confidence)
        analysis_methods = sum([
            bool(analysis.personality_profile),
            bool(analysis.communication_preferences),
            bool(analysis.decision_making_process),
            bool(analysis.psychological_triggers),
            bool(analysis.optimal_engagement)
        ])
        
        method_confidence = analysis_methods / 5.0
        confidence_factors.append(method_confidence)
        
        return sum(confidence_factors) / len(confidence_factors)
    
    def _identify_data_sources(
        self,
        contact_data: Dict[str, Any],
        interaction_history: Optional[Dict[str, Any]],
        tactical_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify data sources used in analysis"""
        
        sources = []
        
        if contact_data.get("title"):
            sources.append("Professional title and role")
        if contact_data.get("bio") or contact_data.get("description"):
            sources.append("Professional biography")
        if interaction_history:
            sources.append("Historical interaction patterns")
        if tactical_results:
            sources.append("Tactical research results")
        
        sources.extend([
            "Industry behavioral patterns",
            "Role-based personality models",
            "Communication preference frameworks"
        ])
        
        return sources
    
    # Utility methods for CrewAI integration
    def get_crew_agents(self) -> List[Dict[str, Any]]:
        """Get CrewAI agent definitions for behavioral analysis"""
        return [
            {
                "role": "Personality Analysis Specialist",
                "goal": "Profile decision-maker personality types using behavioral indicators",
                "backstory": "Industrial psychologist with expertise in DISC assessment and executive profiling",
                "tools": ["personality_assessment", "behavioral_analysis", "disc_framework"]
            },
            {
                "role": "Communication Strategy Expert", 
                "goal": "Determine optimal communication approaches and timing strategies",
                "backstory": "Communication specialist focused on B2B executive engagement optimization",
                "tools": ["communication_analysis", "timing_optimization", "channel_selection"]
            },
            {
                "role": "Decision Process Mapper",
                "goal": "Map decision-making workflows and stakeholder influence patterns",
                "backstory": "Organizational psychologist specializing in corporate decision processes",
                "tools": ["process_mapping", "stakeholder_analysis", "decision_modeling"]
            }
        ]
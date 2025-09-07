from typing import Dict, Any, Literal
from ..states.lead_states import LeadState

class ScoringLogic:
    """Handles scoring-based routing decisions"""
    
    def __init__(self):
        self.score_thresholds = {
            "high_value": 0.8,
            "medium_value": 0.6,
            "low_value": 0.4,
            "no_value": 0.2
        }
    
    def evaluate_score(self, state: LeadState) -> Literal["outreach", "simulation", "end"]:
        """Evaluate lead score and route accordingly"""
        
        lead_score = state.lead_score
        
        # High-value leads get immediate outreach
        if lead_score >= self.score_thresholds["high_value"]:
            return "outreach"
        
        # Medium-value leads get simulation to optimize approach
        elif lead_score >= self.score_thresholds["medium_value"]:
            return "simulation"
        
        # Low-value leads might get basic outreach if other factors are positive
        elif lead_score >= self.score_thresholds["low_value"]:
            # Check other positive factors
            if self._has_positive_indicators(state):
                return "outreach"
            else:
                return "simulation"  # Optimize approach first
        
        # Very low value leads end workflow
        else:
            return "end"
    
    def calculate_composite_score(self, state: LeadState) -> float:
        """Calculate composite score from multiple factors"""
        
        factors = {
            "company_size": self._score_company_size(state.company_size),
            "industry_fit": self._score_industry_fit(state.industry),
            "engagement": state.engagement_level,
            "research_quality": self._score_research_quality(state),
            "response_rate": state.response_rate,
            "pain_points": self._score_pain_points(state.pain_points)
        }
        
        # Weighted average
        weights = {
            "company_size": 0.2,
            "industry_fit": 0.15,
            "engagement": 0.25,
            "research_quality": 0.15,
            "response_rate": 0.15,
            "pain_points": 0.1
        }
        
        composite_score = sum(
            factors[factor] * weights[factor] 
            for factor in factors.keys()
        )
        
        return min(composite_score, 1.0)
    
    def _score_company_size(self, company_size: int = None) -> float:
        """Score based on company size"""
        if not company_size:
            return 0.5
        
        if company_size >= 1000:
            return 1.0
        elif company_size >= 500:
            return 0.9
        elif company_size >= 200:
            return 0.8
        elif company_size >= 100:
            return 0.7
        elif company_size >= 50:
            return 0.6
        else:
            return 0.4
    
    def _score_industry_fit(self, industry: str = None) -> float:
        """Score based on industry fit"""
        if not industry:
            return 0.5
        
        high_fit_industries = [
            'technology', 'software', 'saas', 'fintech', 
            'healthcare', 'manufacturing', 'logistics'
        ]
        
        medium_fit_industries = [
            'retail', 'education', 'government', 'non-profit'
        ]
        
        industry_lower = industry.lower()
        
        for high_industry in high_fit_industries:
            if high_industry in industry_lower:
                return 0.9
        
        for medium_industry in medium_fit_industries:
            if medium_industry in industry_lower:
                return 0.7
        
        return 0.6  # Default for unknown industries
    
    def _score_research_quality(self, state: LeadState) -> float:
        """Score based on research completeness and quality"""
        if not state.research_completed:
            return 0.0
        
        quality_factors = [
            len(state.pain_points) > 0,
            len(state.key_insights) > 0,
            len(state.tech_stack) > 0,
            state.company_size is not None,
            state.industry is not None
        ]
        
        return sum(quality_factors) / len(quality_factors)
    
    def _score_pain_points(self, pain_points: list = None) -> float:
        """Score based on identified pain points"""
        if not pain_points:
            return 0.0
        
        # More pain points generally indicate better fit
        if len(pain_points) >= 3:
            return 1.0
        elif len(pain_points) >= 2:
            return 0.8
        elif len(pain_points) >= 1:
            return 0.6
        else:
            return 0.0
    
    def _has_positive_indicators(self, state: LeadState) -> bool:
        """Check if lead has positive indicators despite low score"""
        
        positive_indicators = [
            state.engagement_level > 0.4,
            state.response_rate > 0.2,
            len(state.pain_points) > 0,
            state.company_size and state.company_size > 50,
            state.research_completed
        ]
        
        # Need at least 2 positive indicators
        return sum(positive_indicators) >= 2
    
    def get_score_explanation(self, state: LeadState) -> Dict[str, Any]:
        """Get detailed explanation of scoring"""
        
        composite_score = self.calculate_composite_score(state)
        
        return {
            "overall_score": composite_score,
            "score_category": self._get_score_category(composite_score),
            "component_scores": {
                "company_size": self._score_company_size(state.company_size),
                "industry_fit": self._score_industry_fit(state.industry),
                "engagement": state.engagement_level,
                "research_quality": self._score_research_quality(state),
                "response_rate": state.response_rate,
                "pain_points": self._score_pain_points(state.pain_points)
            },
            "strengths": self._identify_strengths(state),
            "weaknesses": self._identify_weaknesses(state),
            "recommendations": self._get_recommendations(composite_score)
        }
    
    def _get_score_category(self, score: float) -> str:
        """Get category label for score"""
        if score >= self.score_thresholds["high_value"]:
            return "High Value"
        elif score >= self.score_thresholds["medium_value"]:
            return "Medium Value"
        elif score >= self.score_thresholds["low_value"]:
            return "Low Value"
        else:
            return "Poor Fit"
    
    def _identify_strengths(self, state: LeadState) -> list:
        """Identify lead strengths"""
        strengths = []
        
        if state.company_size and state.company_size > 500:
            strengths.append("Large company size")
        if state.engagement_level > 0.6:
            strengths.append("High engagement")
        if state.response_rate > 0.4:
            strengths.append("Good response rate")
        if len(state.pain_points) > 2:
            strengths.append("Multiple pain points identified")
        if state.research_completed:
            strengths.append("Comprehensive research completed")
        
        return strengths
    
    def _identify_weaknesses(self, state: LeadState) -> list:
        """Identify lead weaknesses"""
        weaknesses = []
        
        if state.engagement_level < 0.3:
            weaknesses.append("Low engagement")
        if state.response_rate < 0.2:
            weaknesses.append("Poor response rate")
        if not state.pain_points:
            weaknesses.append("No pain points identified")
        if not state.research_completed:
            weaknesses.append("Research incomplete")
        if state.outreach_attempts > 3 and state.response_rate == 0:
            weaknesses.append("No responses after multiple attempts")
        
        return weaknesses
    
    def _get_recommendations(self, score: float) -> list:
        """Get recommendations based on score"""
        if score >= self.score_thresholds["high_value"]:
            return [
                "Proceed with immediate outreach",
                "Consider expedited sales process",
                "Assign senior sales representative"
            ]
        elif score >= self.score_thresholds["medium_value"]:
            return [
                "Run simulation to optimize approach",
                "Focus on pain point messaging",
                "Schedule discovery call"
            ]
        elif score >= self.score_thresholds["low_value"]:
            return [
                "Conduct additional research",
                "Try different outreach channels",
                "Focus on education and nurturing"
            ]
        else:
            return [
                "Consider removing from active pipeline",
                "Move to long-term nurture sequence",
                "Re-evaluate in 6 months"
            ]

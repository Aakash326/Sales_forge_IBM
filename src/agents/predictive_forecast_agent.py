"""
Predictive Forecast Agent - Advanced Intelligence Layer
Predicts future market trends, customer buying behavior, and competitive movements
Uses advanced pattern recognition and predictive modeling for strategic timing optimization
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import statistics

class PredictionConfidence(Enum):
    LOW = "low"           # <60% confidence
    MEDIUM = "medium"     # 60-80% confidence
    HIGH = "high"         # >80% confidence

class ScenarioType(Enum):
    BEST_CASE = "best_case"
    MOST_LIKELY = "most_likely"
    WORST_CASE = "worst_case"

@dataclass
class BuyingTimelinePrediction:
    """Buying timeline prediction output"""
    predicted_window: str = ""  # e.g., "90 days"
    confidence_level: PredictionConfidence = PredictionConfidence.MEDIUM
    key_milestones: List[Dict[str, Any]] = None
    decision_triggers: List[str] = None
    probability_score: float = 0.5
    
    def __post_init__(self):
        if self.key_milestones is None:
            self.key_milestones = []
        if self.decision_triggers is None:
            self.decision_triggers = []

@dataclass
class MarketTrendForecast:
    """Market trend forecast output"""
    growth_prediction: float = 0.0  # Annual growth rate
    trend_direction: str = "stable"  # up, down, stable, volatile
    market_maturity_shift: str = ""
    technology_disruptions: List[str] = None
    regulatory_impacts: List[str] = None
    forecast_period: str = "12 months"
    
    def __post_init__(self):
        if self.technology_disruptions is None:
            self.technology_disruptions = []
        if self.regulatory_impacts is None:
            self.regulatory_impacts = []

@dataclass
class CompetitiveThreatForecast:
    """Competitive threat timeline prediction"""
    immediate_threats: List[Dict[str, Any]] = None
    emerging_competitors: List[Dict[str, Any]] = None
    market_consolidation_timeline: str = ""
    threat_severity_score: float = 0.5
    recommended_response_timeline: str = ""
    
    def __post_init__(self):
        if self.immediate_threats is None:
            self.immediate_threats = []
        if self.emerging_competitors is None:
            self.emerging_competitors = []

@dataclass
class ScenarioAnalysis:
    """Scenario planning analysis"""
    best_case: Dict[str, Any] = None
    most_likely: Dict[str, Any] = None
    worst_case: Dict[str, Any] = None
    scenario_probabilities: Dict[str, float] = None
    key_variables: List[str] = None
    decision_points: List[str] = None
    
    def __post_init__(self):
        if self.best_case is None:
            self.best_case = {}
        if self.most_likely is None:
            self.most_likely = {}
        if self.worst_case is None:
            self.worst_case = {}
        if self.scenario_probabilities is None:
            self.scenario_probabilities = {
                "best_case": 0.2,
                "most_likely": 0.6,
                "worst_case": 0.2
            }
        if self.key_variables is None:
            self.key_variables = []
        if self.decision_points is None:
            self.decision_points = []

@dataclass
class PredictiveForecast:
    """Complete predictive forecast output"""
    buying_timeline: Optional[BuyingTimelinePrediction] = None
    market_trends: Optional[MarketTrendForecast] = None
    competitive_threats: Optional[CompetitiveThreatForecast] = None
    economic_cycles: Dict[str, Any] = None
    scenario_analysis: Optional[ScenarioAnalysis] = None
    
    # Meta information
    forecast_generated_at: datetime = None
    forecast_confidence: PredictionConfidence = PredictionConfidence.MEDIUM
    data_quality_score: float = 0.5
    prediction_accuracy_history: float = 0.7
    
    # Strategic recommendations
    optimal_engagement_period: str = ""
    key_success_factors: List[str] = None
    risk_mitigation_strategies: List[str] = None
    
    def __post_init__(self):
        if self.forecast_generated_at is None:
            self.forecast_generated_at = datetime.now()
        if self.economic_cycles is None:
            self.economic_cycles = {}
        if self.key_success_factors is None:
            self.key_success_factors = []
        if self.risk_mitigation_strategies is None:
            self.risk_mitigation_strategies = []

class PredictiveForecastAgent:
    """
    Advanced Predictive Forecast Agent
    
    Provides predictive intelligence for strategic sales decision-making:
    - Predicts customer buying timelines with milestone tracking
    - Forecasts market trends and technology disruptions
    - Identifies competitive threats and consolidation patterns  
    - Analyzes economic cycles for optimal timing
    - Generates comprehensive scenario planning
    - Optimizes engagement timing for maximum success probability
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Predictive models and historical patterns
        self.predictive_models = self._initialize_predictive_models()
        self.historical_patterns = self._load_historical_patterns()
        
    def _initialize_predictive_models(self) -> Dict[str, Any]:
        """Initialize predictive models and algorithms"""
        return {
            "buying_timeline_model": {
                "small_company_avg": 45,     # days
                "medium_company_avg": 90,
                "large_company_avg": 180,
                "enterprise_avg": 270,
                "seasonal_factors": {
                    "q1": 1.2,  # 20% longer in Q1
                    "q2": 1.0,  # baseline
                    "q3": 1.1,  # 10% longer in Q3  
                    "q4": 0.8   # 20% faster in Q4
                }
            },
            "market_growth_patterns": {
                "emerging_tech": {"base_growth": 0.35, "volatility": 0.15},
                "established_tech": {"base_growth": 0.12, "volatility": 0.05},
                "mature_markets": {"base_growth": 0.05, "volatility": 0.03},
                "declining_markets": {"base_growth": -0.02, "volatility": 0.08}
            },
            "competitive_threat_indicators": {
                "funding_threat_multiplier": 1.5,
                "product_launch_lead_time": 180,  # days
                "market_consolidation_signals": [
                    "Large funding rounds >$50M",
                    "Strategic acquisitions",
                    "Enterprise partnerships"
                ]
            },
            "economic_cycle_patterns": {
                "expansion": {"duration_avg": 78, "growth_multiplier": 1.2},
                "peak": {"duration_avg": 12, "growth_multiplier": 1.0},
                "recession": {"duration_avg": 18, "growth_multiplier": 0.6},
                "recovery": {"duration_avg": 24, "growth_multiplier": 0.9}
            }
        }
    
    def _load_historical_patterns(self) -> Dict[str, Any]:
        """Load historical patterns for predictive analysis"""
        return {
            "industry_buying_cycles": {
                "software": {"avg_cycle": 120, "decision_makers": 3.2},
                "fintech": {"avg_cycle": 180, "decision_makers": 4.1},
                "healthcare": {"avg_cycle": 240, "decision_makers": 5.3},
                "manufacturing": {"avg_cycle": 300, "decision_makers": 4.8},
                "retail": {"avg_cycle": 90, "decision_makers": 2.7}
            },
            "seasonal_buying_patterns": {
                "q1": {"budget_availability": 0.8, "decision_speed": 0.7},
                "q2": {"budget_availability": 0.9, "decision_speed": 1.0},
                "q3": {"budget_availability": 0.7, "decision_speed": 0.9},
                "q4": {"budget_availability": 1.2, "decision_speed": 1.3}
            },
            "competitive_disruption_history": {
                "avg_disruption_cycle": 36,  # months
                "technology_adoption_curve": 24,  # months
                "market_leader_vulnerability": 0.15  # 15% chance per year
            }
        }
    
    async def generate_predictive_forecast(
        self,
        company_data: Dict[str, Any],
        tactical_results: Optional[Dict[str, Any]] = None,
        strategic_results: Optional[Dict[str, Any]] = None
    ) -> PredictiveForecast:
        """
        Generate comprehensive predictive forecast
        
        Combines multiple predictive models to provide:
        - Buying timeline predictions with milestone tracking
        - Market trend forecasts with disruption analysis
        - Competitive threat assessments with response timelines
        - Economic cycle optimization for timing
        - Scenario planning for strategic decision-making
        """
        
        try:
            forecast = PredictiveForecast()
            
            self.logger.info(f"Generating predictive forecast for {company_data.get('company_name', 'Unknown')}")
            
            # Run predictive analysis tasks in parallel
            tasks = [
                self._predict_buying_timeline(company_data, tactical_results),
                self._forecast_market_trends(company_data, strategic_results),
                self._predict_competitive_threats(company_data, strategic_results),
                self._analyze_economic_cycles(company_data),
                self._generate_scenario_planning(company_data, tactical_results, strategic_results)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            forecast.buying_timeline = results[0] if not isinstance(results[0], Exception) else BuyingTimelinePrediction()
            forecast.market_trends = results[1] if not isinstance(results[1], Exception) else MarketTrendForecast()
            forecast.competitive_threats = results[2] if not isinstance(results[2], Exception) else CompetitiveThreatForecast()
            forecast.economic_cycles = results[3] if not isinstance(results[3], Exception) else {}
            forecast.scenario_analysis = results[4] if not isinstance(results[4], Exception) else ScenarioAnalysis()
            
            # Generate strategic recommendations
            forecast.optimal_engagement_period = self._determine_optimal_timing(forecast)
            forecast.key_success_factors = self._identify_success_factors(forecast)
            forecast.risk_mitigation_strategies = self._generate_risk_strategies(forecast)
            
            # Calculate overall forecast confidence
            forecast.forecast_confidence = self._calculate_forecast_confidence(forecast)
            forecast.data_quality_score = self._assess_data_quality(company_data, tactical_results, strategic_results)
            
            self.logger.info(f"Predictive forecast completed with {forecast.forecast_confidence.value} confidence")
            return forecast
            
        except Exception as e:
            self.logger.error(f"Predictive forecast generation failed: {e}")
            return PredictiveForecast()
    
    async def _predict_buying_timeline(
        self, 
        company_data: Dict[str, Any], 
        tactical_results: Optional[Dict[str, Any]]
    ) -> BuyingTimelinePrediction:
        """Predict when the company is likely to make a buying decision"""
        
        prediction = BuyingTimelinePrediction()
        
        try:
            company_size = company_data.get("company_size", 250)
            industry = company_data.get("industry", "").lower()
            
            # Base timeline prediction based on company size
            if company_size < 100:
                base_timeline = self.predictive_models["buying_timeline_model"]["small_company_avg"]
            elif company_size < 500:
                base_timeline = self.predictive_models["buying_timeline_model"]["medium_company_avg"] 
            elif company_size < 2000:
                base_timeline = self.predictive_models["buying_timeline_model"]["large_company_avg"]
            else:
                base_timeline = self.predictive_models["buying_timeline_model"]["enterprise_avg"]
            
            # Adjust for industry patterns
            if industry in self.historical_patterns["industry_buying_cycles"]:
                industry_factor = self.historical_patterns["industry_buying_cycles"][industry]["avg_cycle"] / 120
                base_timeline = int(base_timeline * industry_factor)
            
            # Seasonal adjustment
            current_quarter = f"q{((datetime.now().month - 1) // 3) + 1}"
            seasonal_factor = self.predictive_models["buying_timeline_model"]["seasonal_factors"].get(current_quarter, 1.0)
            adjusted_timeline = int(base_timeline * seasonal_factor)
            
            # Tactical intelligence adjustments
            if tactical_results:
                engagement_level = tactical_results.get("engagement_level", 0.5)
                pain_urgency = len(tactical_results.get("pain_points", [])) / 5.0  # Normalize to 0-1
                
                # High engagement and urgent pain points accelerate timeline
                urgency_factor = 1.0 - (engagement_level * 0.3 + pain_urgency * 0.2)
                adjusted_timeline = int(adjusted_timeline * max(urgency_factor, 0.5))
            
            prediction.predicted_window = f"{adjusted_timeline} days"
            prediction.probability_score = min(0.9, 0.6 + (0.4 * (1 - seasonal_factor)))
            
            # Generate milestone timeline
            prediction.key_milestones = self._generate_buying_milestones(adjusted_timeline, company_size)
            prediction.decision_triggers = self._identify_decision_triggers(company_data, tactical_results)
            
            # Set confidence based on data quality
            if tactical_results and len(tactical_results.get("pain_points", [])) >= 2:
                prediction.confidence_level = PredictionConfidence.HIGH
            elif tactical_results:
                prediction.confidence_level = PredictionConfidence.MEDIUM
            else:
                prediction.confidence_level = PredictionConfidence.LOW
            
        except Exception as e:
            self.logger.error(f"Buying timeline prediction failed: {e}")
            prediction.predicted_window = "120 days"
            prediction.confidence_level = PredictionConfidence.LOW
        
        return prediction
    
    def _generate_buying_milestones(self, timeline_days: int, company_size: int) -> List[Dict[str, Any]]:
        """Generate key milestones in the buying process"""
        milestones = []
        
        # Milestone percentages based on typical B2B buying process
        milestone_schedule = [
            (0.15, "Initial research and requirements gathering"),
            (0.35, "Vendor identification and initial outreach"),
            (0.55, "Solution evaluation and technical assessment"),
            (0.75, "Proposal review and stakeholder alignment"),
            (0.90, "Final decision and contract negotiation"),
            (1.0, "Purchase decision and implementation start")
        ]
        
        for percentage, milestone_name in milestone_schedule:
            milestone_day = int(timeline_days * percentage)
            milestone_date = (datetime.now() + timedelta(days=milestone_day)).strftime("%Y-%m-%d")
            
            milestones.append({
                "milestone": milestone_name,
                "target_date": milestone_date,
                "days_from_now": milestone_day,
                "completion_probability": max(0.5, 1.0 - percentage * 0.3)  # Earlier milestones more likely
            })
        
        return milestones
    
    def _identify_decision_triggers(
        self, 
        company_data: Dict[str, Any], 
        tactical_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify key triggers that would accelerate decision-making"""
        triggers = []
        
        # Company size based triggers
        company_size = company_data.get("company_size", 0)
        if company_size > 1000:
            triggers.append("Quarterly planning cycles")
            triggers.append("Board-level strategic initiatives")
        elif company_size > 100:
            triggers.append("Department budget approvals")
            triggers.append("Operational efficiency mandates")
        else:
            triggers.append("Immediate operational needs")
            triggers.append("Growth milestone achievements")
        
        # Industry specific triggers
        industry = company_data.get("industry", "").lower()
        if "fintech" in industry:
            triggers.extend(["Regulatory compliance deadlines", "Funding round milestones"])
        elif "healthcare" in industry:
            triggers.extend(["Patient safety improvements", "Regulatory audit preparations"])
        elif "retail" in industry:
            triggers.extend(["Peak season preparations", "Customer experience initiatives"])
        
        # Tactical intelligence based triggers
        if tactical_results:
            pain_points = tactical_results.get("pain_points", [])
            if len(pain_points) >= 3:
                triggers.append("Multiple operational pain point resolution")
            
            engagement_level = tactical_results.get("engagement_level", 0)
            if engagement_level > 0.7:
                triggers.append("High stakeholder engagement momentum")
        
        return triggers[:5]  # Limit to top 5 triggers
    
    async def _forecast_market_trends(
        self, 
        company_data: Dict[str, Any], 
        strategic_results: Optional[Dict[str, Any]]
    ) -> MarketTrendForecast:
        """Forecast market trends and disruption patterns"""
        
        forecast = MarketTrendForecast()
        
        try:
            industry = company_data.get("industry", "").lower()
            
            # Base growth prediction from strategic results or models
            if strategic_results and hasattr(strategic_results, 'market_intelligence'):
                base_growth = getattr(strategic_results.market_intelligence, 'growth_rate', 0.1)
            else:
                # Use predictive models based on industry maturity
                if any(keyword in industry for keyword in ["ai", "blockchain", "quantum"]):
                    growth_pattern = self.predictive_models["market_growth_patterns"]["emerging_tech"]
                elif any(keyword in industry for keyword in ["software", "cloud", "saas"]):
                    growth_pattern = self.predictive_models["market_growth_patterns"]["established_tech"]
                elif any(keyword in industry for keyword in ["manufacturing", "retail"]):
                    growth_pattern = self.predictive_models["market_growth_patterns"]["mature_markets"]
                else:
                    growth_pattern = self.predictive_models["market_growth_patterns"]["established_tech"]
                
                base_growth = growth_pattern["base_growth"]
            
            # Apply economic and trend adjustments using IBM Granite if available
            if self.granite_client:
                adjusted_growth = await self._ai_enhanced_trend_forecast(industry, base_growth)
            else:
                # Fallback trend analysis
                adjusted_growth = self._statistical_trend_forecast(industry, base_growth)
            
            forecast.growth_prediction = adjusted_growth
            forecast.trend_direction = self._determine_trend_direction(adjusted_growth, base_growth)
            forecast.market_maturity_shift = self._assess_market_maturity_shift(industry, adjusted_growth)
            forecast.technology_disruptions = self._predict_tech_disruptions(industry)
            forecast.regulatory_impacts = self._predict_regulatory_impacts(industry)
            
        except Exception as e:
            self.logger.error(f"Market trend forecasting failed: {e}")
            forecast.growth_prediction = 0.08  # Default market growth
            forecast.trend_direction = "stable"
        
        return forecast
    
    async def _ai_enhanced_trend_forecast(self, industry: str, base_growth: float) -> float:
        """Use IBM Granite for advanced trend forecasting"""
        try:
            prompt = f"""
            Analyze market trends for {industry} industry with current growth rate {base_growth*100:.1f}%.
            Consider:
            - Technology disruption patterns
            - Economic indicators and cycles
            - Regulatory environment changes
            - Consumer behavior shifts
            - Competitive landscape evolution
            
            Provide growth rate prediction for next 12 months as decimal (e.g., 0.15 for 15%).
            """
            
            response = self.granite_client.generate(prompt, max_tokens=100, temperature=0.3)
            
            # Extract growth rate from response
            try:
                # Simple parsing - look for decimal number
                import re
                growth_match = re.search(r'(\d+\.?\d*)', response.content)
                if growth_match:
                    predicted_growth = float(growth_match.group(1))
                    # Convert to decimal if it's a percentage
                    if predicted_growth > 1.0:
                        predicted_growth = predicted_growth / 100.0
                    return min(max(predicted_growth, -0.5), 2.0)  # Cap between -50% and 200%
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"AI trend forecasting failed: {e}")
        
        return base_growth  # Fallback to base growth
    
    def _statistical_trend_forecast(self, industry: str, base_growth: float) -> float:
        """Fallback statistical trend forecasting"""
        # Apply industry-specific trend adjustments
        trend_adjustments = {
            "ai": 0.05,      # AI industry +5% adjustment
            "fintech": 0.03,  # Fintech +3%
            "healthcare": 0.02,  # Healthcare +2%
            "manufacturing": -0.01,  # Manufacturing -1%
            "retail": 0.01    # Retail +1%
        }
        
        adjustment = 0
        for keyword, adj in trend_adjustments.items():
            if keyword in industry:
                adjustment = adj
                break
        
        # Apply economic cycle adjustment (simplified)
        current_month = datetime.now().month
        if current_month in [1, 2, 3]:  # Q1 - cautious growth
            cycle_adjustment = -0.01
        elif current_month in [10, 11, 12]:  # Q4 - optimistic growth
            cycle_adjustment = 0.02
        else:
            cycle_adjustment = 0
        
        return base_growth + adjustment + cycle_adjustment
    
    def _determine_trend_direction(self, predicted_growth: float, base_growth: float) -> str:
        """Determine overall trend direction"""
        growth_change = predicted_growth - base_growth
        
        if growth_change > 0.03:
            return "accelerating"
        elif growth_change < -0.03:
            return "declining"
        elif abs(growth_change) > 0.01:
            return "volatile"
        else:
            return "stable"
    
    def _assess_market_maturity_shift(self, industry: str, growth_rate: float) -> str:
        """Assess if market is shifting maturity stages"""
        if growth_rate > 0.25:
            return "Entering high-growth phase"
        elif growth_rate > 0.15:
            return "Sustained growth phase"
        elif growth_rate > 0.05:
            return "Maturation phase"
        elif growth_rate > 0:
            return "Mature market with steady growth"
        else:
            return "Market consolidation phase"
    
    def _predict_tech_disruptions(self, industry: str) -> List[str]:
        """Predict potential technology disruptions"""
        disruption_patterns = {
            "software": ["AI automation", "No-code platforms", "Edge computing"],
            "fintech": ["DeFi integration", "Central bank digital currencies", "AI-powered compliance"],
            "healthcare": ["Telemedicine expansion", "AI diagnostics", "Wearable health monitoring"],
            "manufacturing": ["Industrial IoT", "Predictive maintenance", "Supply chain automation"],
            "retail": ["Virtual commerce", "Personalization AI", "Sustainable supply chains"]
        }
        
        for key, disruptions in disruption_patterns.items():
            if key in industry:
                return disruptions
        
        return ["Digital transformation", "AI integration", "Automation adoption"]
    
    def _predict_regulatory_impacts(self, industry: str) -> List[str]:
        """Predict regulatory impacts on market"""
        regulatory_patterns = {
            "fintech": ["Open banking regulations", "Cryptocurrency oversight", "Data privacy enforcement"],
            "healthcare": ["Interoperability mandates", "AI medical device approval", "Patient data protection"],
            "software": ["Data privacy regulations", "AI governance frameworks", "Cybersecurity mandates"],
            "manufacturing": ["Environmental compliance", "Supply chain transparency", "Worker safety standards"]
        }
        
        for key, impacts in regulatory_patterns.items():
            if key in industry:
                return impacts
        
        return ["Data privacy compliance", "Environmental regulations", "Industry-specific safety standards"]
    
    async def _predict_competitive_threats(
        self, 
        company_data: Dict[str, Any], 
        strategic_results: Optional[Dict[str, Any]]
    ) -> CompetitiveThreatForecast:
        """Predict competitive threats and market consolidation"""
        
        forecast = CompetitiveThreatForecast()
        
        try:
            industry = company_data.get("industry", "").lower()
            company_size = company_data.get("company_size", 0)
            
            # Generate immediate threats based on industry patterns
            forecast.immediate_threats = self._generate_immediate_threats(industry, company_size)
            forecast.emerging_competitors = self._identify_emerging_competitors(industry)
            forecast.market_consolidation_timeline = self._predict_consolidation_timeline(industry)
            forecast.threat_severity_score = self._calculate_threat_severity(forecast.immediate_threats)
            forecast.recommended_response_timeline = self._determine_response_timeline(forecast.threat_severity_score)
            
        except Exception as e:
            self.logger.error(f"Competitive threat prediction failed: {e}")
            forecast.threat_severity_score = 0.5
            forecast.recommended_response_timeline = "6 months"
        
        return forecast
    
    def _generate_immediate_threats(self, industry: str, company_size: int) -> List[Dict[str, Any]]:
        """Generate immediate competitive threats"""
        threats = []
        
        # Industry-specific threat patterns
        industry_threats = {
            "software": [
                {"type": "Big Tech Entry", "probability": 0.3, "timeline": "12 months"},
                {"type": "Open Source Alternative", "probability": 0.5, "timeline": "6 months"},
                {"type": "Startup Disruption", "probability": 0.7, "timeline": "18 months"}
            ],
            "fintech": [
                {"type": "Banking API Integration", "probability": 0.4, "timeline": "9 months"},
                {"type": "Regulatory-backed Competitor", "probability": 0.3, "timeline": "24 months"},
                {"type": "Crypto-native Solution", "probability": 0.6, "timeline": "12 months"}
            ],
            "healthcare": [
                {"type": "Healthcare Giant Partnership", "probability": 0.4, "timeline": "18 months"},
                {"type": "AI-powered Diagnostics", "probability": 0.5, "timeline": "12 months"},
                {"type": "Telehealth Integration", "probability": 0.7, "timeline": "6 months"}
            ]
        }
        
        # Select threats based on industry
        base_threats = []
        for key, threat_list in industry_threats.items():
            if key in industry:
                base_threats = threat_list
                break
        
        if not base_threats:
            base_threats = [
                {"type": "Market Leader Expansion", "probability": 0.4, "timeline": "12 months"},
                {"type": "Technology Disruption", "probability": 0.5, "timeline": "18 months"},
                {"type": "New Entrant Funding", "probability": 0.6, "timeline": "9 months"}
            ]
        
        # Enhance threats with specific details
        for threat in base_threats:
            threats.append({
                "threat_type": threat["type"],
                "probability": threat["probability"],
                "timeline": threat["timeline"],
                "severity": "High" if threat["probability"] > 0.6 else "Medium" if threat["probability"] > 0.3 else "Low",
                "impact_areas": ["Market share", "Pricing pressure", "Feature competition"],
                "early_indicators": [
                    "Industry partnership announcements",
                    "Significant funding rounds",
                    "Product roadmap leaks"
                ]
            })
        
        return threats
    
    def _identify_emerging_competitors(self, industry: str) -> List[Dict[str, Any]]:
        """Identify emerging competitors to watch"""
        emerging = []
        
        # Pattern-based emerging competitor identification
        competitor_patterns = {
            "software": ["Well-funded startups", "Big Tech divisions", "Open source projects"],
            "fintech": ["Neobanks", "DeFi protocols", "Payment processors"],
            "healthcare": ["Healthtech startups", "Pharma tech divisions", "AI diagnostic companies"]
        }
        
        patterns = competitor_patterns.get(industry.split()[0], ["Industry startups", "Technology giants", "Specialized providers"])
        
        for i, pattern in enumerate(patterns):
            emerging.append({
                "competitor_type": pattern,
                "emergence_timeline": f"{(i + 1) * 6} months",
                "threat_level": "Medium" if i == 0 else "Low",
                "key_differentiators": [
                    "Advanced technology integration",
                    "Superior user experience",
                    "Aggressive pricing strategy"
                ],
                "monitoring_priority": "High" if i == 0 else "Medium"
            })
        
        return emerging
    
    def _predict_consolidation_timeline(self, industry: str) -> str:
        """Predict market consolidation timeline"""
        consolidation_patterns = {
            "software": "24-36 months",
            "fintech": "18-30 months", 
            "healthcare": "36-48 months",
            "manufacturing": "48-60 months",
            "retail": "12-24 months"
        }
        
        for key, timeline in consolidation_patterns.items():
            if key in industry:
                return timeline
        
        return "24-36 months"  # Default
    
    def _calculate_threat_severity(self, threats: List[Dict[str, Any]]) -> float:
        """Calculate overall threat severity score"""
        if not threats:
            return 0.3
        
        severity_scores = []
        for threat in threats:
            probability = threat.get("probability", 0.5)
            severity_map = {"High": 0.9, "Medium": 0.6, "Low": 0.3}
            severity = severity_map.get(threat.get("severity", "Medium"), 0.6)
            severity_scores.append(probability * severity)
        
        return min(statistics.mean(severity_scores), 1.0)
    
    def _determine_response_timeline(self, threat_severity: float) -> str:
        """Determine recommended response timeline"""
        if threat_severity > 0.7:
            return "Immediate (30 days)"
        elif threat_severity > 0.5:
            return "Short-term (3 months)"
        elif threat_severity > 0.3:
            return "Medium-term (6 months)"
        else:
            return "Long-term (12+ months)"
    
    async def _analyze_economic_cycles(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze economic cycles for optimal timing"""
        
        analysis = {
            "current_cycle_phase": "expansion",
            "optimal_engagement_window": "next 6 months",
            "economic_indicators": {},
            "sector_health": {},
            "timing_recommendations": []
        }
        
        try:
            industry = company_data.get("industry", "").lower()
            location = company_data.get("location", "").lower()
            
            # Economic cycle analysis
            current_month = datetime.now().month
            
            # Simplified economic cycle detection
            if current_month in [1, 2, 3]:  # Q1
                cycle_phase = "recovery"
                engagement_window = "next 9 months"
                timing_factor = 0.9
            elif current_month in [4, 5, 6]:  # Q2
                cycle_phase = "expansion"
                engagement_window = "next 6 months"
                timing_factor = 1.2
            elif current_month in [7, 8, 9]:  # Q3
                cycle_phase = "peak"
                engagement_window = "next 3 months"
                timing_factor = 1.1
            else:  # Q4
                cycle_phase = "expansion"
                engagement_window = "immediate"
                timing_factor = 1.3
            
            analysis["current_cycle_phase"] = cycle_phase
            analysis["optimal_engagement_window"] = engagement_window
            
            # Industry-specific economic indicators
            analysis["economic_indicators"] = {
                "interest_rates": "Favorable for investments",
                "venture_funding": "Strong activity in tech sectors",
                "market_volatility": "Moderate",
                "inflation_impact": "Minimal for tech services"
            }
            
            # Sector health assessment
            sector_health_map = {
                "software": "Strong",
                "fintech": "Very Strong", 
                "healthcare": "Strong",
                "manufacturing": "Moderate",
                "retail": "Recovering"
            }
            
            for sector, health in sector_health_map.items():
                if sector in industry:
                    analysis["sector_health"] = {
                        "overall_health": health,
                        "growth_outlook": "Positive",
                        "investment_climate": "Favorable"
                    }
                    break
            
            # Timing recommendations
            analysis["timing_recommendations"] = [
                f"Current {cycle_phase} phase favorable for sales activities",
                f"Engage within {engagement_window} for optimal results",
                "Q4 budget cycles create urgency opportunities",
                "Economic stability supports larger investments"
            ]
            
        except Exception as e:
            self.logger.error(f"Economic cycle analysis failed: {e}")
        
        return analysis
    
    async def _generate_scenario_planning(
        self,
        company_data: Dict[str, Any],
        tactical_results: Optional[Dict[str, Any]],
        strategic_results: Optional[Dict[str, Any]]
    ) -> ScenarioAnalysis:
        """Generate comprehensive scenario planning analysis"""
        
        scenario = ScenarioAnalysis()
        
        try:
            base_timeline = 120  # days
            base_revenue = 50000  # $50K ACV estimate
            
            # Best case scenario (20% probability)
            scenario.best_case = {
                "timeline": f"{int(base_timeline * 0.6)} days",  # 40% faster
                "revenue_potential": f"${int(base_revenue * 1.5):,}",  # 50% higher
                "success_probability": 0.9,
                "key_factors": [
                    "Strong stakeholder alignment",
                    "Urgent business need identified", 
                    "Budget pre-approved",
                    "Technical fit confirmed"
                ],
                "competitive_position": "Clear leader",
                "market_conditions": "Highly favorable"
            }
            
            # Most likely scenario (60% probability)
            scenario.most_likely = {
                "timeline": f"{base_timeline} days",
                "revenue_potential": f"${base_revenue:,}",
                "success_probability": 0.6,
                "key_factors": [
                    "Standard evaluation process",
                    "Moderate competition",
                    "Budget requires approval",
                    "Technical evaluation needed"
                ],
                "competitive_position": "Strong contender",
                "market_conditions": "Stable"
            }
            
            # Worst case scenario (20% probability)  
            scenario.worst_case = {
                "timeline": f"{int(base_timeline * 1.8)} days",  # 80% longer
                "revenue_potential": f"${int(base_revenue * 0.7):,}",  # 30% lower
                "success_probability": 0.2,
                "key_factors": [
                    "Budget constraints",
                    "Strong competitive pressure",
                    "Complex approval process",
                    "Technical concerns"
                ],
                "competitive_position": "Challenger",
                "market_conditions": "Challenging"
            }
            
            # Key variables affecting outcomes
            scenario.key_variables = [
                "Economic conditions and market stability",
                "Competitive landscape changes",
                "Client budget and approval timeline",
                "Technical evaluation results",
                "Stakeholder alignment and urgency"
            ]
            
            # Decision points for scenario adaptation
            scenario.decision_points = [
                "30 days: Initial stakeholder feedback",
                "60 days: Technical evaluation results",
                "90 days: Budget and approval status",
                "120 days: Final decision timeline"
            ]
            
        except Exception as e:
            self.logger.error(f"Scenario planning failed: {e}")
        
        return scenario
    
    def _determine_optimal_timing(self, forecast: PredictiveForecast) -> str:
        """Determine optimal engagement timing"""
        factors = []
        
        # Buying timeline factor
        if forecast.buying_timeline and forecast.buying_timeline.predicted_window:
            timeline_days = int(forecast.buying_timeline.predicted_window.split()[0])
            if timeline_days <= 60:
                factors.append("immediate")
            elif timeline_days <= 120:
                factors.append("short-term")
            else:
                factors.append("medium-term")
        
        # Market trends factor
        if forecast.market_trends:
            if forecast.market_trends.trend_direction == "accelerating":
                factors.append("immediate")
            elif forecast.market_trends.trend_direction == "stable":
                factors.append("short-term")
        
        # Economic cycle factor
        if forecast.economic_cycles:
            cycle_phase = forecast.economic_cycles.get("current_cycle_phase", "")
            if cycle_phase in ["expansion", "peak"]:
                factors.append("immediate")
        
        # Determine optimal timing
        if factors.count("immediate") >= 2:
            return "Next 30 days (optimal window)"
        elif "short-term" in factors:
            return "Next 60-90 days"
        else:
            return "Next 3-6 months"
    
    def _identify_success_factors(self, forecast: PredictiveForecast) -> List[str]:
        """Identify key success factors"""
        factors = []
        
        # Timeline-based factors
        if forecast.buying_timeline:
            factors.append("Align with predicted buying timeline")
            if forecast.buying_timeline.decision_triggers:
                factors.append("Leverage identified decision triggers")
        
        # Market-based factors
        if forecast.market_trends and forecast.market_trends.trend_direction == "accelerating":
            factors.append("Capitalize on positive market momentum")
        
        # Competitive factors
        if forecast.competitive_threats and forecast.competitive_threats.threat_severity_score > 0.6:
            factors.append("Establish competitive differentiation early")
        
        # Economic factors
        if forecast.economic_cycles:
            factors.append("Leverage favorable economic conditions")
        
        # Default success factors
        factors.extend([
            "Demonstrate clear ROI and value proposition",
            "Build strong stakeholder relationships",
            "Address technical requirements comprehensively"
        ])
        
        return factors[:5]  # Top 5 factors
    
    def _generate_risk_strategies(self, forecast: PredictiveForecast) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        # Timeline risks
        if forecast.buying_timeline and forecast.buying_timeline.confidence_level == PredictionConfidence.LOW:
            strategies.append("Conduct additional discovery to improve timeline accuracy")
        
        # Market risks
        if forecast.market_trends and forecast.market_trends.trend_direction == "volatile":
            strategies.append("Develop flexible pricing and contract terms")
        
        # Competitive risks  
        if forecast.competitive_threats and forecast.competitive_threats.threat_severity_score > 0.7:
            strategies.append("Accelerate sales process to avoid competitive displacement")
        
        # Scenario risks
        if forecast.scenario_analysis:
            strategies.append("Prepare for multiple outcome scenarios with adaptive strategies")
        
        # Default risk strategies
        strategies.extend([
            "Maintain regular stakeholder communication",
            "Monitor competitive developments closely",
            "Prepare contingency plans for timeline delays"
        ])
        
        return strategies[:5]  # Top 5 strategies
    
    def _calculate_forecast_confidence(self, forecast: PredictiveForecast) -> PredictionConfidence:
        """Calculate overall forecast confidence"""
        confidence_factors = []
        
        # Individual forecast confidences
        if forecast.buying_timeline:
            conf_map = {PredictionConfidence.HIGH: 0.9, PredictionConfidence.MEDIUM: 0.7, PredictionConfidence.LOW: 0.4}
            confidence_factors.append(conf_map.get(forecast.buying_timeline.confidence_level, 0.5))
        
        if forecast.market_trends:
            # Market trends confidence based on data availability
            confidence_factors.append(0.7)  # Moderate confidence in trend analysis
        
        if forecast.competitive_threats:
            # Competitive threat confidence
            confidence_factors.append(0.6)  # Medium confidence in threat prediction
        
        if forecast.economic_cycles:
            # Economic analysis confidence
            confidence_factors.append(0.8)  # High confidence in economic patterns
        
        if forecast.scenario_analysis:
            # Scenario planning confidence
            confidence_factors.append(0.7)  # Good confidence in scenario modeling
        
        # Calculate overall confidence
        if confidence_factors:
            avg_confidence = statistics.mean(confidence_factors)
            if avg_confidence >= 0.8:
                return PredictionConfidence.HIGH
            elif avg_confidence >= 0.6:
                return PredictionConfidence.MEDIUM
            else:
                return PredictionConfidence.LOW
        
        return PredictionConfidence.MEDIUM
    
    def _assess_data_quality(
        self, 
        company_data: Dict[str, Any], 
        tactical_results: Optional[Dict[str, Any]], 
        strategic_results: Optional[Dict[str, Any]]
    ) -> float:
        """Assess quality of input data for prediction accuracy"""
        quality_factors = []
        
        # Company data quality
        required_fields = ["company_name", "company_size", "industry", "annual_revenue"]
        company_completeness = sum(1 for field in required_fields if company_data.get(field)) / len(required_fields)
        quality_factors.append(company_completeness)
        
        # Tactical results quality
        if tactical_results:
            tactical_completeness = min(1.0, len(tactical_results.get("pain_points", [])) / 3.0)
            quality_factors.append(tactical_completeness)
        else:
            quality_factors.append(0.3)
        
        # Strategic results quality
        if strategic_results:
            quality_factors.append(0.8)  # Strategic results boost confidence
        else:
            quality_factors.append(0.5)
        
        return statistics.mean(quality_factors)
    
    # Utility methods for CrewAI integration
    def get_crew_agents(self) -> List[Dict[str, Any]]:
        """Get CrewAI agent definitions for predictive analysis"""
        return [
            {
                "role": "Trend Analysis Specialist",
                "goal": "Analyze historical patterns and predict future market trends",
                "backstory": "Expert in pattern recognition and predictive modeling with deep industry knowledge",
                "tools": ["trend_analysis", "pattern_recognition", "statistical_modeling"]
            },
            {
                "role": "Customer Behavior Predictor", 
                "goal": "Predict when and how customers will make purchasing decisions",
                "backstory": "Behavioral economist specializing in B2B buying psychology and decision timelines",
                "tools": ["behavioral_analysis", "timeline_prediction", "decision_modeling"]
            },
            {
                "role": "Market Timing Optimizer",
                "goal": "Determine optimal timing for sales activities based on multiple factors",
                "backstory": "Strategic advisor with expertise in economic cycles and competitive timing",
                "tools": ["timing_optimization", "economic_analysis", "competitive_intelligence"]
            }
        ]
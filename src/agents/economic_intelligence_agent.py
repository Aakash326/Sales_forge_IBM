"""
Economic Intelligence Agent - Advanced Intelligence Layer
Analyzes economic conditions, investment climate, and optimal timing for sales activities
Provides economic intelligence for strategic decision-making and market timing optimization
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
import calendar

class EconomicPhase(Enum):
    EXPANSION = "expansion"      # Economic growth phase
    PEAK = "peak"               # Economic peak phase
    RECESSION = "recession"     # Economic downturn
    RECOVERY = "recovery"       # Economic recovery phase

class InvestmentClimate(Enum):
    VERY_FAVORABLE = "very_favorable"    # Excellent conditions
    FAVORABLE = "favorable"              # Good conditions
    MODERATE = "moderate"                # Mixed conditions
    CHALLENGING = "challenging"          # Difficult conditions
    POOR = "poor"                       # Very difficult conditions

class SectorHealth(Enum):
    THRIVING = "thriving"        # Exceptional performance
    STRONG = "strong"           # Above-average performance
    STABLE = "stable"           # Average performance
    DECLINING = "declining"     # Below-average performance
    DISTRESSED = "distressed"   # Poor performance

@dataclass
class MacroEconomicIndicators:
    """Macro-economic indicators analysis"""
    gdp_growth_rate: float = 0.0
    inflation_rate: float = 0.0
    interest_rates: Dict[str, float] = field(default_factory=dict)
    unemployment_rate: float = 0.0
    consumer_confidence: float = 0.0
    business_confidence: float = 0.0
    market_volatility_index: float = 0.0
    currency_stability: str = ""
    trade_conditions: str = ""

@dataclass
class SectorAnalysis:
    """Industry sector economic analysis"""
    sector_name: str = ""
    health_status: SectorHealth = SectorHealth.STABLE
    growth_rate: float = 0.0
    investment_flow: float = 0.0
    employment_trends: str = ""
    regulatory_environment: str = ""
    technology_disruption_level: float = 0.5
    competitive_intensity: float = 0.5
    profitability_trends: str = ""

@dataclass
class InvestmentClimateAssessment:
    """Investment climate assessment"""
    overall_climate: InvestmentClimate = InvestmentClimate.MODERATE
    venture_capital_activity: Dict[str, Any] = field(default_factory=dict)
    private_equity_activity: Dict[str, Any] = field(default_factory=dict)
    public_markets_health: Dict[str, Any] = field(default_factory=dict)
    debt_availability: Dict[str, Any] = field(default_factory=dict)
    risk_appetite: str = ""
    funding_trends: List[str] = field(default_factory=list)

@dataclass
class TimingOptimization:
    """Economic timing optimization analysis"""
    optimal_engagement_window: str = ""
    current_cycle_phase: EconomicPhase = EconomicPhase.EXPANSION
    phase_duration_estimate: str = ""
    key_timing_factors: List[str] = field(default_factory=list)
    seasonal_considerations: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    opportunity_windows: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class EconomicScenarios:
    """Economic scenario analysis"""
    base_case: Dict[str, Any] = field(default_factory=dict)
    optimistic_case: Dict[str, Any] = field(default_factory=dict)
    pessimistic_case: Dict[str, Any] = field(default_factory=dict)
    scenario_probabilities: Dict[str, float] = field(default_factory=dict)
    key_variables: List[str] = field(default_factory=list)
    trigger_events: List[str] = field(default_factory=list)

@dataclass
class EconomicIntelligence:
    """Complete economic intelligence analysis"""
    # Core economic analysis
    macro_indicators: Optional[MacroEconomicIndicators] = None
    sector_analysis: Optional[SectorAnalysis] = None
    investment_climate: Optional[InvestmentClimateAssessment] = None
    timing_optimization: Optional[TimingOptimization] = None
    economic_scenarios: Optional[EconomicScenarios] = None
    
    # Regional analysis
    regional_conditions: Dict[str, Any] = field(default_factory=dict)
    global_factors: List[str] = field(default_factory=list)
    
    # Strategic recommendations
    timing_recommendations: List[str] = field(default_factory=list)
    risk_mitigation_strategies: List[str] = field(default_factory=list)
    opportunity_capitalization: List[str] = field(default_factory=list)
    
    # Meta information
    analysis_date: datetime = field(default_factory=datetime.now)
    confidence_level: float = 0.7
    data_recency: str = "current"
    forecast_horizon: str = "12 months"

class EconomicIntelligenceAgent:
    """
    Advanced Economic Intelligence Agent
    
    Provides comprehensive economic intelligence for strategic decision-making:
    - Macro-economic indicator analysis and trend forecasting
    - Industry sector health assessment with growth projections
    - Investment climate evaluation across funding sources
    - Economic cycle timing for optimal sales and investment activities
    - Economic scenario planning with probability assessments
    - Regional economic condition analysis for market expansion
    - Risk assessment and opportunity identification based on economic trends
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Economic models and databases
        self.economic_models = self._initialize_economic_models()
        self.sector_database = self._load_sector_database()
        self.regional_data = self._load_regional_data()
        
    def _initialize_economic_models(self) -> Dict[str, Any]:
        """Initialize economic analysis models"""
        return {
            "economic_cycles": {
                EconomicPhase.EXPANSION: {
                    "avg_duration_months": 78,
                    "characteristics": ["GDP growth", "Low unemployment", "Business investment"],
                    "sales_impact": "positive",
                    "investment_climate": "favorable"
                },
                EconomicPhase.PEAK: {
                    "avg_duration_months": 12,
                    "characteristics": ["Maximum growth", "Tight labor market", "Inflation pressure"],
                    "sales_impact": "mixed",
                    "investment_climate": "cautious"
                },
                EconomicPhase.RECESSION: {
                    "avg_duration_months": 18,
                    "characteristics": ["GDP contraction", "Rising unemployment", "Reduced spending"],
                    "sales_impact": "negative",
                    "investment_climate": "poor"
                },
                EconomicPhase.RECOVERY: {
                    "avg_duration_months": 24,
                    "characteristics": ["Gradual growth", "Stabilizing markets", "Cautious spending"],
                    "sales_impact": "improving",
                    "investment_climate": "moderate"
                }
            },
            "sector_indicators": {
                "technology": {
                    "cyclical_sensitivity": 0.7,  # High sensitivity to economic cycles
                    "growth_correlation": 0.8,    # Strong correlation with GDP growth
                    "investment_sensitivity": 0.9  # Very sensitive to investment climate
                },
                "healthcare": {
                    "cyclical_sensitivity": 0.3,  # Low sensitivity (defensive sector)
                    "growth_correlation": 0.4,    # Moderate correlation
                    "investment_sensitivity": 0.5  # Moderate sensitivity
                },
                "financial_services": {
                    "cyclical_sensitivity": 0.8,  # High sensitivity
                    "growth_correlation": 0.7,    # Strong correlation
                    "investment_sensitivity": 0.6  # Moderate sensitivity
                },
                "consumer_discretionary": {
                    "cyclical_sensitivity": 0.9,  # Very high sensitivity
                    "growth_correlation": 0.8,    # Strong correlation
                    "investment_sensitivity": 0.7  # High sensitivity
                }
            },
            "investment_patterns": {
                "venture_capital": {
                    "cycle_sensitivity": 0.8,
                    "typical_deal_size_range": [1_000_000, 50_000_000],
                    "activity_indicators": ["Deal count", "Average deal size", "New fund formation"]
                },
                "private_equity": {
                    "cycle_sensitivity": 0.6,
                    "typical_deal_size_range": [25_000_000, 500_000_000],
                    "activity_indicators": ["Buyout activity", "Dry powder levels", "Exit activity"]
                },
                "public_markets": {
                    "cycle_sensitivity": 1.0,
                    "key_metrics": ["Market capitalization", "IPO activity", "Valuation multiples"]
                }
            }
        }
    
    def _load_sector_database(self) -> Dict[str, Any]:
        """Load sector-specific economic data"""
        return {
            "software": {
                "base_growth_rate": 0.12,
                "economic_multiplier": 1.2,  # Amplifies economic effects
                "funding_dependency": 0.7,
                "recession_resilience": 0.6,
                "key_indicators": ["Cloud spending", "Digital transformation", "SaaS adoption"]
            },
            "fintech": {
                "base_growth_rate": 0.25,
                "economic_multiplier": 1.5,
                "funding_dependency": 0.8,
                "recession_resilience": 0.4,
                "key_indicators": ["Financial regulation", "Digital payments", "Interest rates"]
            },
            "healthcare": {
                "base_growth_rate": 0.08,
                "economic_multiplier": 0.8,  # Less sensitive to cycles
                "funding_dependency": 0.5,
                "recession_resilience": 0.9,  # Highly resilient
                "key_indicators": ["Healthcare spending", "Aging population", "Regulatory changes"]
            },
            "manufacturing": {
                "base_growth_rate": 0.06,
                "economic_multiplier": 1.4,
                "funding_dependency": 0.6,
                "recession_resilience": 0.5,
                "key_indicators": ["Industrial production", "Supply chain", "Trade policies"]
            },
            "retail": {
                "base_growth_rate": 0.04,
                "economic_multiplier": 1.6,  # Highly cyclical
                "funding_dependency": 0.5,
                "recession_resilience": 0.3,
                "key_indicators": ["Consumer spending", "E-commerce", "Employment levels"]
            }
        }
    
    def _load_regional_data(self) -> Dict[str, Any]:
        """Load regional economic data"""
        return {
            "north_america": {
                "economic_phase": EconomicPhase.EXPANSION,
                "gdp_growth": 0.025,
                "key_factors": ["Federal Reserve policy", "Tech sector strength", "Infrastructure investment"],
                "investment_climate": InvestmentClimate.FAVORABLE
            },
            "europe": {
                "economic_phase": EconomicPhase.RECOVERY,
                "gdp_growth": 0.018,
                "key_factors": ["ECB monetary policy", "Energy transition", "Regulatory environment"],
                "investment_climate": InvestmentClimate.MODERATE
            },
            "asia_pacific": {
                "economic_phase": EconomicPhase.EXPANSION,
                "gdp_growth": 0.045,
                "key_factors": ["Digital transformation", "Manufacturing recovery", "Trade relationships"],
                "investment_climate": InvestmentClimate.FAVORABLE
            }
        }
    
    async def analyze_economic_intelligence(
        self,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]] = None,
        regional_focus: Optional[str] = None
    ) -> EconomicIntelligence:
        """
        Generate comprehensive economic intelligence analysis
        
        Provides strategic economic intelligence including:
        - Macro-economic indicators and trend analysis
        - Industry sector health and growth projections
        - Investment climate assessment across funding sources
        - Economic cycle timing for optimal business activities
        - Economic scenario planning with risk/opportunity analysis
        """
        
        try:
            intelligence = EconomicIntelligence()
            
            industry = company_data.get("industry", "").lower()
            location = company_data.get("location", "").lower()
            company_size = company_data.get("company_size", 0)
            
            self.logger.info(f"Analyzing economic intelligence for {industry} industry")
            
            # Execute economic analysis tasks in parallel
            tasks = [
                self._analyze_macro_indicators(),
                self._analyze_sector_health(industry, market_intelligence),
                self._assess_investment_climate(industry, company_size),
                self._optimize_economic_timing(industry, location),
                self._generate_economic_scenarios(industry, company_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results safely
            intelligence.macro_indicators = results[0] if not isinstance(results[0], Exception) else MacroEconomicIndicators()
            intelligence.sector_analysis = results[1] if not isinstance(results[1], Exception) else SectorAnalysis()
            intelligence.investment_climate = results[2] if not isinstance(results[2], Exception) else InvestmentClimateAssessment()
            intelligence.timing_optimization = results[3] if not isinstance(results[3], Exception) else TimingOptimization()
            intelligence.economic_scenarios = results[4] if not isinstance(results[4], Exception) else EconomicScenarios()
            
            # Regional analysis
            intelligence.regional_conditions = self._analyze_regional_conditions(location, regional_focus)
            intelligence.global_factors = self._identify_global_factors()
            
            # Generate strategic recommendations
            intelligence.timing_recommendations = self._generate_timing_recommendations(intelligence)
            intelligence.risk_mitigation_strategies = self._generate_risk_strategies(intelligence)
            intelligence.opportunity_capitalization = self._identify_opportunities(intelligence)
            
            # Calculate confidence and quality metrics
            intelligence.confidence_level = self._calculate_confidence_level(intelligence)
            intelligence.data_recency = self._assess_data_recency()
            
            self.logger.info(f"Economic intelligence analysis completed with {intelligence.confidence_level:.1%} confidence")
            return intelligence
            
        except Exception as e:
            self.logger.error(f"Economic intelligence analysis failed: {e}")
            return EconomicIntelligence()
    
    async def _analyze_macro_indicators(self) -> MacroEconomicIndicators:
        """Analyze macro-economic indicators"""
        
        indicators = MacroEconomicIndicators()
        
        try:
            # Current economic indicators (simulated data - in production would connect to real APIs)
            current_quarter = (datetime.now().month - 1) // 3 + 1
            
            # Simulate realistic economic indicators
            indicators.gdp_growth_rate = self._simulate_gdp_growth(current_quarter)
            indicators.inflation_rate = self._simulate_inflation_rate(current_quarter)
            indicators.interest_rates = {
                "federal_funds_rate": 5.25,
                "10_year_treasury": 4.5,
                "corporate_bond_yield": 5.8
            }
            indicators.unemployment_rate = 3.8
            indicators.consumer_confidence = 102.3
            indicators.business_confidence = 98.7
            indicators.market_volatility_index = 18.5
            indicators.currency_stability = "Stable with moderate volatility"
            indicators.trade_conditions = "Generally favorable with some regional tensions"
            
            # Use AI for enhanced analysis if available
            if self.granite_client:
                indicators = await self._ai_enhanced_macro_analysis(indicators)
            
        except Exception as e:
            self.logger.error(f"Macro indicators analysis failed: {e}")
        
        return indicators
    
    def _simulate_gdp_growth(self, quarter: int) -> float:
        """Simulate realistic GDP growth rate"""
        # Simulate seasonal patterns in GDP growth
        seasonal_factors = {1: -0.002, 2: 0.001, 3: 0.000, 4: 0.003}  # Q4 typically strongest
        base_growth = 0.025  # 2.5% base annual growth
        return base_growth + seasonal_factors.get(quarter, 0)
    
    def _simulate_inflation_rate(self, quarter: int) -> float:
        """Simulate realistic inflation rate"""
        # Simulate current inflation environment
        base_inflation = 0.032  # 3.2% base inflation
        seasonal_variation = 0.002 if quarter in [2, 3] else -0.001  # Higher in summer
        return base_inflation + seasonal_variation
    
    async def _ai_enhanced_macro_analysis(self, indicators: MacroEconomicIndicators) -> MacroEconomicIndicators:
        """Use IBM Granite for enhanced macro-economic analysis"""
        
        try:
            prompt = f"""
            Analyze current macro-economic conditions:
            
            Current indicators:
            - GDP Growth: {indicators.gdp_growth_rate*100:.1f}%
            - Inflation: {indicators.inflation_rate*100:.1f}%
            - Fed Funds Rate: {indicators.interest_rates.get('federal_funds_rate', 5.25)}%
            - Unemployment: {indicators.unemployment_rate}%
            - Consumer Confidence: {indicators.consumer_confidence}
            
            Provide economic outlook assessment:
            - Overall economic health (strong/moderate/weak)
            - Business environment favorability
            - Investment climate implications
            - Key risk factors
            
            Format as brief analysis focusing on business implications.
            """
            
            response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
            
            # Enhanced interpretation (simplified - would be more sophisticated in production)
            if "strong" in response.content.lower():
                indicators.business_confidence = min(110.0, indicators.business_confidence + 5)
            elif "weak" in response.content.lower():
                indicators.business_confidence = max(85.0, indicators.business_confidence - 5)
            
        except Exception as e:
            self.logger.error(f"AI macro analysis failed: {e}")
        
        return indicators
    
    async def _analyze_sector_health(
        self,
        industry: str,
        market_intelligence: Optional[Dict[str, Any]]
    ) -> SectorAnalysis:
        """Analyze industry sector health"""
        
        analysis = SectorAnalysis()
        
        try:
            # Determine sector category
            sector_key = self._map_industry_to_sector(industry)
            analysis.sector_name = industry.title()
            
            # Get sector data
            if sector_key in self.sector_database:
                sector_data = self.sector_database[sector_key]
                
                # Calculate adjusted growth rate based on economic conditions
                base_growth = sector_data["base_growth_rate"]
                economic_multiplier = sector_data["economic_multiplier"]
                
                # Apply economic cycle adjustment
                current_phase = self._determine_current_economic_phase()
                cycle_adjustment = self._get_cycle_adjustment(current_phase)
                
                analysis.growth_rate = base_growth * (1 + cycle_adjustment * economic_multiplier)
                
                # Determine health status
                analysis.health_status = self._determine_sector_health(analysis.growth_rate, sector_data)
                
                # Investment flow estimation
                analysis.investment_flow = self._estimate_investment_flow(sector_key, analysis.growth_rate)
                
                # Additional sector insights
                analysis.employment_trends = self._analyze_employment_trends(sector_key)
                analysis.regulatory_environment = self._assess_regulatory_environment(industry)
                analysis.technology_disruption_level = self._assess_tech_disruption(sector_key)
                analysis.competitive_intensity = self._assess_competitive_intensity(sector_key)
                analysis.profitability_trends = self._analyze_profitability_trends(sector_key, analysis.growth_rate)
            
            # Integrate market intelligence if available
            if market_intelligence:
                analysis = self._integrate_market_intelligence(analysis, market_intelligence)
            
        except Exception as e:
            self.logger.error(f"Sector health analysis failed: {e}")
        
        return analysis
    
    def _map_industry_to_sector(self, industry: str) -> str:
        """Map industry to sector category"""
        industry_mapping = {
            "software": "software",
            "saas": "software",
            "technology": "software",
            "fintech": "fintech",
            "financial": "fintech",
            "healthcare": "healthcare",
            "health": "healthcare",
            "manufacturing": "manufacturing",
            "industrial": "manufacturing",
            "retail": "retail",
            "e-commerce": "retail"
        }
        
        for key, sector in industry_mapping.items():
            if key in industry:
                return sector
        
        return "software"  # Default sector
    
    def _determine_current_economic_phase(self) -> EconomicPhase:
        """Determine current economic phase"""
        # Simplified phase determination (in production would use real economic indicators)
        current_month = datetime.now().month
        
        # Simulate economic cycle based on time of year (simplified model)
        if current_month in [1, 2, 3]:  # Q1 - typically recovery
            return EconomicPhase.RECOVERY
        elif current_month in [4, 5, 6]:  # Q2 - expansion
            return EconomicPhase.EXPANSION
        elif current_month in [7, 8, 9]:  # Q3 - peak
            return EconomicPhase.PEAK
        else:  # Q4 - continued expansion
            return EconomicPhase.EXPANSION
    
    def _get_cycle_adjustment(self, phase: EconomicPhase) -> float:
        """Get economic cycle adjustment factor"""
        adjustments = {
            EconomicPhase.EXPANSION: 0.15,   # +15% growth boost
            EconomicPhase.PEAK: 0.05,        # +5% modest boost
            EconomicPhase.RECESSION: -0.25,  # -25% growth penalty
            EconomicPhase.RECOVERY: -0.05    # -5% modest penalty
        }
        return adjustments.get(phase, 0.0)
    
    def _determine_sector_health(self, growth_rate: float, sector_data: Dict[str, Any]) -> SectorHealth:
        """Determine sector health status"""
        base_growth = sector_data["base_growth_rate"]
        
        if growth_rate > base_growth * 1.5:
            return SectorHealth.THRIVING
        elif growth_rate > base_growth * 1.1:
            return SectorHealth.STRONG
        elif growth_rate > base_growth * 0.8:
            return SectorHealth.STABLE
        elif growth_rate > 0:
            return SectorHealth.DECLINING
        else:
            return SectorHealth.DISTRESSED
    
    def _estimate_investment_flow(self, sector_key: str, growth_rate: float) -> float:
        """Estimate investment flow into sector"""
        # Base investment levels by sector (billions)
        base_investments = {
            "software": 150_000_000_000,
            "fintech": 50_000_000_000,
            "healthcare": 200_000_000_000,
            "manufacturing": 300_000_000_000,
            "retail": 75_000_000_000
        }
        
        base_investment = base_investments.get(sector_key, 100_000_000_000)
        
        # Adjust based on growth rate
        growth_multiplier = max(0.5, min(2.0, 1 + growth_rate * 2))  # Cap between 0.5x and 2x
        
        return base_investment * growth_multiplier
    
    def _analyze_employment_trends(self, sector_key: str) -> str:
        """Analyze employment trends in sector"""
        employment_trends = {
            "software": "Strong hiring in AI/ML, cloud, and cybersecurity roles",
            "fintech": "Growing demand for compliance and risk management professionals",
            "healthcare": "Steady growth with focus on digital health and telemedicine",
            "manufacturing": "Mixed trends with automation offsetting some job growth",
            "retail": "Shift toward e-commerce and omnichannel capabilities"
        }
        return employment_trends.get(sector_key, "Moderate employment growth")
    
    def _assess_regulatory_environment(self, industry: str) -> str:
        """Assess regulatory environment for industry"""
        if "fintech" in industry or "financial" in industry:
            return "Increasing regulation with focus on consumer protection and systemic risk"
        elif "healthcare" in industry:
            return "Complex regulatory landscape with emphasis on data privacy and patient safety"
        elif "software" in industry or "tech" in industry:
            return "Growing regulatory scrutiny on data privacy, AI governance, and market competition"
        else:
            return "Standard regulatory environment with gradual evolution"
    
    def _assess_tech_disruption(self, sector_key: str) -> float:
        """Assess technology disruption level"""
        disruption_levels = {
            "software": 0.8,     # High disruption
            "fintech": 0.7,      # High disruption
            "retail": 0.6,       # Moderate-high disruption
            "healthcare": 0.5,   # Moderate disruption
            "manufacturing": 0.4  # Moderate disruption
        }
        return disruption_levels.get(sector_key, 0.5)
    
    def _assess_competitive_intensity(self, sector_key: str) -> float:
        """Assess competitive intensity in sector"""
        intensity_levels = {
            "software": 0.9,     # Very high intensity
            "fintech": 0.8,      # High intensity
            "retail": 0.7,       # High intensity
            "healthcare": 0.4,   # Moderate intensity (regulated)
            "manufacturing": 0.5  # Moderate intensity
        }
        return intensity_levels.get(sector_key, 0.6)
    
    def _analyze_profitability_trends(self, sector_key: str, growth_rate: float) -> str:
        """Analyze profitability trends"""
        if growth_rate > 0.15:
            return "Strong profitability with expanding margins"
        elif growth_rate > 0.08:
            return "Healthy profitability with stable margins"
        elif growth_rate > 0.03:
            return "Moderate profitability under pressure"
        else:
            return "Profitability challenges with margin compression"
    
    def _integrate_market_intelligence(
        self,
        analysis: SectorAnalysis,
        market_intelligence: Dict[str, Any]
    ) -> SectorAnalysis:
        """Integrate market intelligence data"""
        
        # Adjust growth rate if market intelligence provides different data
        if hasattr(market_intelligence, 'growth_rate') and market_intelligence.growth_rate:
            # Average with our calculation for more accuracy
            mi_growth = getattr(market_intelligence, 'growth_rate', analysis.growth_rate)
            analysis.growth_rate = (analysis.growth_rate + mi_growth) / 2
        
        return analysis
    
    async def _assess_investment_climate(
        self,
        industry: str,
        company_size: int
    ) -> InvestmentClimateAssessment:
        """Assess investment climate conditions"""
        
        assessment = InvestmentClimateAssessment()
        
        try:
            # Assess overall investment climate
            assessment.overall_climate = self._determine_overall_climate()
            
            # Venture capital activity
            assessment.venture_capital_activity = {
                "activity_level": "High" if assessment.overall_climate in [InvestmentClimate.FAVORABLE, InvestmentClimate.VERY_FAVORABLE] else "Moderate",
                "average_deal_size": self._estimate_vc_deal_size(industry),
                "deals_per_quarter": self._estimate_vc_deal_count(industry),
                "key_focus_areas": self._get_vc_focus_areas(industry),
                "geographic_concentration": "Silicon Valley, NYC, Boston remain top markets"
            }
            
            # Private equity activity
            assessment.private_equity_activity = {
                "activity_level": "Moderate" if assessment.overall_climate != InvestmentClimate.POOR else "Low",
                "average_deal_size": self._estimate_pe_deal_size(company_size),
                "buyout_activity": "Selective with focus on profitable companies",
                "dry_powder_levels": "High levels available for quality deals",
                "exit_environment": "Mixed with strong performing companies finding good exits"
            }
            
            # Public markets health
            assessment.public_markets_health = {
                "ipo_activity": "Moderate with quality companies accessing markets",
                "valuation_multiples": self._get_valuation_multiples(industry),
                "market_sentiment": "Cautiously optimistic",
                "volatility_level": "Elevated but manageable"
            }
            
            # Debt availability
            assessment.debt_availability = {
                "bank_lending": "Selective with tighter underwriting standards",
                "corporate_bonds": "Available for investment grade companies",
                "alternative_lending": "Growing market with competitive rates",
                "cost_of_capital": "Moderately elevated due to interest rate environment"
            }
            
            # Risk appetite and funding trends
            assessment.risk_appetite = self._assess_risk_appetite(assessment.overall_climate)
            assessment.funding_trends = self._identify_funding_trends(industry, assessment.overall_climate)
            
        except Exception as e:
            self.logger.error(f"Investment climate assessment failed: {e}")
        
        return assessment
    
    def _determine_overall_climate(self) -> InvestmentClimate:
        """Determine overall investment climate"""
        # Simplified determination based on current economic conditions
        current_phase = self._determine_current_economic_phase()
        
        climate_mapping = {
            EconomicPhase.EXPANSION: InvestmentClimate.FAVORABLE,
            EconomicPhase.PEAK: InvestmentClimate.MODERATE,
            EconomicPhase.RECESSION: InvestmentClimate.CHALLENGING,
            EconomicPhase.RECOVERY: InvestmentClimate.MODERATE
        }
        
        return climate_mapping.get(current_phase, InvestmentClimate.MODERATE)
    
    def _estimate_vc_deal_size(self, industry: str) -> str:
        """Estimate average VC deal size for industry"""
        deal_sizes = {
            "software": "$8-15M Series A, $25-40M Series B",
            "fintech": "$10-20M Series A, $30-50M Series B", 
            "healthcare": "$15-25M Series A, $35-60M Series B",
            "manufacturing": "$12-20M Series A, $25-45M Series B"
        }
        
        for key, size in deal_sizes.items():
            if key in industry:
                return size
        
        return "$10-15M Series A, $25-40M Series B"  # Default
    
    def _estimate_vc_deal_count(self, industry: str) -> str:
        """Estimate VC deal count for industry"""
        deal_counts = {
            "software": "800-1000 deals per quarter",
            "fintech": "200-300 deals per quarter",
            "healthcare": "400-500 deals per quarter",
            "manufacturing": "100-150 deals per quarter"
        }
        
        for key, count in deal_counts.items():
            if key in industry:
                return count
        
        return "500-600 deals per quarter"  # Default
    
    def _get_vc_focus_areas(self, industry: str) -> List[str]:
        """Get current VC focus areas"""
        focus_areas = {
            "software": ["AI/ML", "Developer tools", "Cybersecurity", "No-code/Low-code"],
            "fintech": ["Embedded finance", "RegTech", "Digital banking", "Crypto infrastructure"],
            "healthcare": ["Digital therapeutics", "Telemedicine", "Health data analytics", "Medical devices"],
            "manufacturing": ["Industrial IoT", "Supply chain tech", "Sustainability", "Automation"]
        }
        
        for key, areas in focus_areas.items():
            if key in industry:
                return areas
        
        return ["Enterprise SaaS", "AI/ML", "Developer tools", "Cybersecurity"]  # Default
    
    def _estimate_pe_deal_size(self, company_size: int) -> str:
        """Estimate PE deal size based on company size"""
        if company_size > 2000:
            return "$500M-2B+ (Large buyouts)"
        elif company_size > 500:
            return "$100M-500M (Mid-market)"
        elif company_size > 100:
            return "$25M-100M (Lower mid-market)"
        else:
            return "$10M-50M (Small market)"
    
    def _get_valuation_multiples(self, industry: str) -> Dict[str, str]:
        """Get current valuation multiples by industry"""
        multiples = {
            "software": {"revenue": "6-12x", "ebitda": "20-40x"},
            "fintech": {"revenue": "4-8x", "ebitda": "15-25x"},
            "healthcare": {"revenue": "3-6x", "ebitda": "12-20x"},
            "manufacturing": {"revenue": "1-3x", "ebitda": "8-15x"}
        }
        
        for key, multiple in multiples.items():
            if key in industry:
                return multiple
        
        return {"revenue": "4-8x", "ebitda": "15-25x"}  # Default
    
    def _assess_risk_appetite(self, climate: InvestmentClimate) -> str:
        """Assess current risk appetite"""
        risk_mapping = {
            InvestmentClimate.VERY_FAVORABLE: "High risk appetite with growth focus",
            InvestmentClimate.FAVORABLE: "Moderate-high risk appetite",
            InvestmentClimate.MODERATE: "Balanced risk approach with selectivity",
            InvestmentClimate.CHALLENGING: "Conservative risk approach",
            InvestmentClimate.POOR: "Risk-averse with focus on defensible businesses"
        }
        return risk_mapping[climate]
    
    def _identify_funding_trends(self, industry: str, climate: InvestmentClimate) -> List[str]:
        """Identify current funding trends"""
        base_trends = [
            "Focus on profitability and unit economics",
            "Longer due diligence processes",
            "Emphasis on AI and automation capabilities",
            "ESG considerations in investment decisions"
        ]
        
        if climate in [InvestmentClimate.FAVORABLE, InvestmentClimate.VERY_FAVORABLE]:
            base_trends.extend([
                "Increased competition for quality deals",
                "Rising valuations for top performers"
            ])
        else:
            base_trends.extend([
                "Flight to quality with proven business models",
                "Down rounds for overvalued companies"
            ])
        
        return base_trends
    
    async def _optimize_economic_timing(
        self,
        industry: str,
        location: str
    ) -> TimingOptimization:
        """Optimize timing based on economic conditions"""
        
        optimization = TimingOptimization()
        
        try:
            # Determine current economic cycle phase
            optimization.current_cycle_phase = self._determine_current_economic_phase()
            
            # Get phase characteristics
            phase_data = self.economic_models["economic_cycles"][optimization.current_cycle_phase]
            optimization.phase_duration_estimate = f"~{phase_data['avg_duration_months']} months typical duration"
            
            # Determine optimal engagement window
            optimization.optimal_engagement_window = self._determine_optimal_window(
                optimization.current_cycle_phase,
                industry
            )
            
            # Key timing factors
            optimization.key_timing_factors = self._identify_timing_factors(
                optimization.current_cycle_phase,
                industry
            )
            
            # Seasonal considerations
            optimization.seasonal_considerations = self._analyze_seasonal_factors()
            
            # Risk factors for timing
            optimization.risk_factors = self._identify_timing_risks(optimization.current_cycle_phase)
            
            # Opportunity windows
            optimization.opportunity_windows = self._identify_opportunity_windows(
                optimization.current_cycle_phase,
                industry
            )
            
        except Exception as e:
            self.logger.error(f"Economic timing optimization failed: {e}")
        
        return optimization
    
    def _determine_optimal_window(self, phase: EconomicPhase, industry: str) -> str:
        """Determine optimal engagement window"""
        
        phase_windows = {
            EconomicPhase.EXPANSION: "Immediate to 6 months - favorable conditions",
            EconomicPhase.PEAK: "Immediate to 3 months - act before downturn",
            EconomicPhase.RECESSION: "6-12 months - prepare for recovery",
            EconomicPhase.RECOVERY: "3-9 months - position for expansion"
        }
        
        base_window = phase_windows[phase]
        
        # Adjust for industry sensitivity
        sector_key = self._map_industry_to_sector(industry)
        if sector_key in self.sector_database:
            cyclical_sensitivity = self.sector_database[sector_key].get("cyclical_sensitivity", 0.5)
            
            if cyclical_sensitivity > 0.7:  # Highly cyclical
                if phase == EconomicPhase.EXPANSION:
                    return "Immediate - capitalize on strong conditions"
                elif phase == EconomicPhase.RECESSION:
                    return "12-18 months - wait for clear recovery signals"
        
        return base_window
    
    def _identify_timing_factors(self, phase: EconomicPhase, industry: str) -> List[str]:
        """Identify key timing factors"""
        
        base_factors = {
            EconomicPhase.EXPANSION: [
                "Business confidence is high",
                "Investment budgets are growing",
                "Competition for talent is increasing",
                "Valuation multiples are elevated"
            ],
            EconomicPhase.PEAK: [
                "Maximum business activity levels",
                "Tight labor markets affecting costs",
                "Potential for interest rate increases",
                "Market volatility may increase"
            ],
            EconomicPhase.RECESSION: [
                "Reduced business spending",
                "Focus shifts to cost savings",
                "Talent becomes more available",
                "Valuation multiples compress"
            ],
            EconomicPhase.RECOVERY: [
                "Cautious optimism returning",
                "Selective investment in growth",
                "Gradual improvement in conditions",
                "Opportunity for market share gains"
            ]
        }
        
        factors = base_factors[phase].copy()
        
        # Add industry-specific factors
        if "software" in industry:
            factors.append("Digital transformation priorities remain strong")
        elif "fintech" in industry:
            factors.append("Financial services seeking efficiency gains")
        
        return factors
    
    def _analyze_seasonal_factors(self) -> List[str]:
        """Analyze seasonal economic factors"""
        current_month = datetime.now().month
        current_quarter = (current_month - 1) // 3 + 1
        
        seasonal_factors = {
            1: ["Q1 budget planning and allocation", "Post-holiday business resumption", "Tax planning considerations"],
            2: ["Q2 implementation activities", "Mid-year planning cycles", "Strong business activity levels"],
            3: ["Q3 summer slowdown potential", "Preparation for year-end push", "Budget use-or-lose dynamics"],
            4: ["Q4 budget urgency", "Year-end decision-making", "Holiday seasonal effects"]
        }
        
        return seasonal_factors.get(current_quarter, [])
    
    def _identify_timing_risks(self, phase: EconomicPhase) -> List[str]:
        """Identify timing-related risks"""
        
        risk_map = {
            EconomicPhase.EXPANSION: [
                "Potential economic overheating",
                "Asset price bubbles developing",
                "Inflation pressure building"
            ],
            EconomicPhase.PEAK: [
                "Imminent economic downturn",
                "Market volatility increasing",
                "Policy tightening risks"
            ],
            EconomicPhase.RECESSION: [
                "Extended downturn duration",
                "Credit availability constraints",
                "Demand destruction risks"
            ],
            EconomicPhase.RECOVERY: [
                "False recovery signals",
                "Uneven sectoral recovery",
                "Policy support withdrawal"
            ]
        }
        
        return risk_map.get(phase, [])
    
    def _identify_opportunity_windows(self, phase: EconomicPhase, industry: str) -> List[Dict[str, Any]]:
        """Identify specific opportunity windows"""
        
        opportunities = []
        
        if phase == EconomicPhase.EXPANSION:
            opportunities.extend([
                {
                    "window": "Immediate - 3 months",
                    "opportunity": "High-growth customer acquisition",
                    "rationale": "Strong business confidence and spending"
                },
                {
                    "window": "3-6 months", 
                    "opportunity": "Premium pricing opportunities",
                    "rationale": "Customers willing to pay for value in good times"
                }
            ])
        elif phase == EconomicPhase.RECOVERY:
            opportunities.extend([
                {
                    "window": "6-12 months",
                    "opportunity": "Market share expansion",
                    "rationale": "Competitors may still be cautious"
                },
                {
                    "window": "3-9 months",
                    "opportunity": "Talent acquisition advantage",
                    "rationale": "Quality talent available before full recovery"
                }
            ])
        
        return opportunities
    
    async def _generate_economic_scenarios(
        self,
        industry: str,
        company_data: Dict[str, Any]
    ) -> EconomicScenarios:
        """Generate economic scenario analysis"""
        
        scenarios = EconomicScenarios()
        
        try:
            company_size = company_data.get("company_size", 0)
            annual_revenue = company_data.get("annual_revenue", 0)
            
            # Base case scenario (most likely)
            scenarios.base_case = {
                "description": "Continued moderate economic growth",
                "gdp_growth": "2.0-2.5%",
                "business_impact": "Stable demand with gradual improvement",
                "investment_climate": "Moderate with selective funding",
                "timeline": "12-18 months",
                "revenue_impact": "5-10% growth",
                "key_assumptions": ["No major economic shocks", "Gradual policy normalization", "Stable geopolitical environment"]
            }
            
            # Optimistic case
            scenarios.optimistic_case = {
                "description": "Strong economic acceleration",
                "gdp_growth": "3.5-4.0%",
                "business_impact": "Strong demand growth and expansion opportunities",
                "investment_climate": "Very favorable with abundant funding",
                "timeline": "6-12 months",
                "revenue_impact": "15-25% growth",
                "key_assumptions": ["Productivity gains from AI", "Resolution of supply chain issues", "Strong consumer confidence"]
            }
            
            # Pessimistic case
            scenarios.pessimistic_case = {
                "description": "Economic slowdown or mild recession",
                "gdp_growth": "0.5-1.0% (or negative)",
                "business_impact": "Reduced demand and cost-cutting focus",
                "investment_climate": "Challenging with limited funding",
                "timeline": "12-24 months",
                "revenue_impact": "5-15% decline",
                "key_assumptions": ["Persistent inflation", "Financial market stress", "Geopolitical tensions"]
            }
            
            # Scenario probabilities
            scenarios.scenario_probabilities = {
                "base_case": 0.6,
                "optimistic_case": 0.2,
                "pessimistic_case": 0.2
            }
            
            # Key variables affecting scenarios
            scenarios.key_variables = [
                "Federal Reserve monetary policy",
                "Inflation trajectory and persistence",
                "Geopolitical stability and trade relations",
                "Technology adoption and productivity gains",
                "Labor market dynamics and wage growth"
            ]
            
            # Trigger events that could change scenarios
            scenarios.trigger_events = [
                "Major policy announcements or changes",
                "Significant geopolitical developments",
                "Financial market disruptions",
                "Unexpected inflation readings",
                "Major corporate earnings surprises"
            ]
            
        except Exception as e:
            self.logger.error(f"Economic scenarios generation failed: {e}")
        
        return scenarios
    
    def _analyze_regional_conditions(self, location: str, regional_focus: Optional[str]) -> Dict[str, Any]:
        """Analyze regional economic conditions"""
        
        # Determine region from location
        region = self._map_location_to_region(location, regional_focus)
        
        if region in self.regional_data:
            regional_data = self.regional_data[region].copy()
            
            # Add specific regional insights
            regional_data["specific_factors"] = self._get_regional_specific_factors(region)
            regional_data["business_environment"] = self._assess_regional_business_environment(region)
            
            return regional_data
        
        # Default global conditions
        return {
            "economic_phase": EconomicPhase.EXPANSION,
            "gdp_growth": 0.025,
            "key_factors": ["Global economic integration", "Technology adoption", "Trade relationships"],
            "investment_climate": InvestmentClimate.MODERATE,
            "business_environment": "Mixed conditions with regional variations"
        }
    
    def _map_location_to_region(self, location: str, regional_focus: Optional[str]) -> str:
        """Map location to economic region"""
        if regional_focus:
            return regional_focus.lower().replace(" ", "_")
        
        location_lower = location.lower()
        
        if any(place in location_lower for place in ["us", "usa", "united states", "california", "new york", "texas"]):
            return "north_america"
        elif any(place in location_lower for place in ["europe", "uk", "germany", "france", "london", "berlin"]):
            return "europe"
        elif any(place in location_lower for place in ["asia", "china", "japan", "singapore", "india", "tokyo"]):
            return "asia_pacific"
        else:
            return "north_america"  # Default
    
    def _get_regional_specific_factors(self, region: str) -> List[str]:
        """Get region-specific economic factors"""
        factors = {
            "north_america": [
                "Federal Reserve policy normalization",
                "Strong tech sector performance",
                "Infrastructure investment initiatives",
                "Labor market tightness in key sectors"
            ],
            "europe": [
                "ECB monetary policy coordination",
                "Energy transition investments",
                "Brexit ongoing effects",
                "EU regulatory harmonization"
            ],
            "asia_pacific": [
                "Supply chain regionalization",
                "Digital economy growth",
                "Trade relationship dynamics",
                "Infrastructure development programs"
            ]
        }
        return factors.get(region, [])
    
    def _assess_regional_business_environment(self, region: str) -> str:
        """Assess regional business environment"""
        assessments = {
            "north_america": "Generally favorable with strong innovation ecosystem",
            "europe": "Moderate conditions with regulatory complexity but stable institutions",
            "asia_pacific": "Dynamic growth environment with significant opportunities"
        }
        return assessments.get(region, "Mixed business environment")
    
    def _identify_global_factors(self) -> List[str]:
        """Identify global economic factors"""
        return [
            "Central bank policy coordination and divergence",
            "Supply chain resilience and regionalization trends", 
            "Climate change and energy transition investments",
            "Technological disruption and AI adoption",
            "Geopolitical tensions and trade relationships",
            "Demographic trends and labor market changes"
        ]
    
    def _generate_timing_recommendations(self, intelligence: EconomicIntelligence) -> List[str]:
        """Generate timing recommendations based on economic intelligence"""
        
        recommendations = []
        
        # Phase-based recommendations
        if intelligence.timing_optimization:
            current_phase = intelligence.timing_optimization.current_cycle_phase
            
            if current_phase == EconomicPhase.EXPANSION:
                recommendations.extend([
                    "Accelerate growth initiatives while conditions remain favorable",
                    "Consider premium positioning strategies",
                    "Invest in market expansion and customer acquisition"
                ])
            elif current_phase == EconomicPhase.RECOVERY:
                recommendations.extend([
                    "Position for market share gains as conditions improve",
                    "Focus on operational efficiency and competitive positioning",
                    "Prepare for increased investment as recovery strengthens"
                ])
        
        # Investment climate recommendations
        if intelligence.investment_climate:
            climate = intelligence.investment_climate.overall_climate
            
            if climate in [InvestmentClimate.FAVORABLE, InvestmentClimate.VERY_FAVORABLE]:
                recommendations.append("Optimal timing for funding activities and strategic partnerships")
            elif climate == InvestmentClimate.CHALLENGING:
                recommendations.append("Focus on profitability and cash flow management")
        
        # Sector-specific recommendations
        if intelligence.sector_analysis:
            if intelligence.sector_analysis.health_status in [SectorHealth.STRONG, SectorHealth.THRIVING]:
                recommendations.append("Capitalize on strong sector momentum")
        
        return recommendations[:6]  # Top 6 recommendations
    
    def _generate_risk_strategies(self, intelligence: EconomicIntelligence) -> List[str]:
        """Generate risk mitigation strategies"""
        
        strategies = []
        
        # Economic cycle risks
        if intelligence.timing_optimization:
            phase = intelligence.timing_optimization.current_cycle_phase
            
            if phase == EconomicPhase.PEAK:
                strategies.extend([
                    "Build cash reserves for potential downturn",
                    "Diversify customer base and revenue streams",
                    "Prepare contingency plans for economic slowdown"
                ])
            elif phase == EconomicPhase.RECESSION:
                strategies.extend([
                    "Focus on customer retention over acquisition",
                    "Optimize cost structure for efficiency",
                    "Maintain investment in core capabilities"
                ])
        
        # Investment climate risks
        if intelligence.investment_climate:
            if intelligence.investment_climate.overall_climate == InvestmentClimate.CHALLENGING:
                strategies.append("Extend runway and reduce burn rate")
        
        # General economic risks
        strategies.extend([
            "Monitor economic indicators for early warning signals",
            "Maintain operational flexibility for rapid adaptation",
            "Build strong balance sheet for economic volatility"
        ])
        
        return strategies[:6]  # Top 6 strategies
    
    def _identify_opportunities(self, intelligence: EconomicIntelligence) -> List[str]:
        """Identify economic opportunity capitalization strategies"""
        
        opportunities = []
        
        # Sector opportunities
        if intelligence.sector_analysis:
            if intelligence.sector_analysis.health_status == SectorHealth.THRIVING:
                opportunities.append("Accelerate sector-specific product development")
            
            if intelligence.sector_analysis.investment_flow > 100_000_000_000:  # High investment flow
                opportunities.append("Position for partnership with well-funded sector players")
        
        # Investment climate opportunities
        if intelligence.investment_climate:
            climate = intelligence.investment_climate.overall_climate
            
            if climate == InvestmentClimate.VERY_FAVORABLE:
                opportunities.extend([
                    "Consider strategic acquisitions while valuations are reasonable",
                    "Launch new products or enter new markets with available capital"
                ])
        
        # Economic scenario opportunities
        if intelligence.economic_scenarios:
            optimistic_prob = intelligence.economic_scenarios.scenario_probabilities.get("optimistic_case", 0)
            if optimistic_prob > 0.3:  # High probability of optimistic scenario
                opportunities.append("Prepare for accelerated growth scenario")
        
        # Default opportunities
        opportunities.extend([
            "Leverage economic intelligence for competitive positioning",
            "Align strategy with economic cycle timing",
            "Build capabilities for multiple economic scenarios"
        ])
        
        return opportunities[:6]  # Top 6 opportunities
    
    def _calculate_confidence_level(self, intelligence: EconomicIntelligence) -> float:
        """Calculate confidence level in economic analysis"""
        
        confidence_factors = []
        
        # Macro indicators confidence
        if intelligence.macro_indicators and intelligence.macro_indicators.gdp_growth_rate != 0.0:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Sector analysis confidence
        if intelligence.sector_analysis and intelligence.sector_analysis.sector_name:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.3)
        
        # Investment climate confidence
        if intelligence.investment_climate:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)
        
        # Timing optimization confidence
        if intelligence.timing_optimization and intelligence.timing_optimization.optimal_engagement_window:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.5)
        
        # Scenario analysis confidence
        if intelligence.economic_scenarios and intelligence.economic_scenarios.scenario_probabilities:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        return statistics.mean(confidence_factors)
    
    def _assess_data_recency(self) -> str:
        """Assess data recency for analysis"""
        # In production, this would check actual data timestamps
        return "Current - data from last 24-48 hours"
    
    # Utility methods for CrewAI integration
    def get_crew_agents(self) -> List[Dict[str, Any]]:
        """Get CrewAI agent definitions for economic intelligence"""
        return [
            {
                "role": "Macro Economic Analyst",
                "goal": "Analyze broad economic indicators and trends for strategic planning",
                "backstory": "Senior economist with expertise in macroeconomic analysis and business cycle forecasting",
                "tools": ["economic_indicators", "trend_analysis", "cycle_modeling"]
            },
            {
                "role": "Industry Intelligence Specialist",
                "goal": "Focus on sector-specific economic conditions and industry health metrics",
                "backstory": "Industry analyst specializing in sector economic performance and investment flows",
                "tools": ["sector_analysis", "industry_metrics", "competitive_dynamics"]
            },
            {
                "role": "Investment Climate Assessor",
                "goal": "Evaluate funding availability and market conditions for strategic decisions",
                "backstory": "Investment professional with deep knowledge of capital markets and funding trends",
                "tools": ["investment_tracking", "funding_analysis", "market_sentiment"]
            }
        ]
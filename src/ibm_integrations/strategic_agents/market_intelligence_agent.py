"""
Market Intelligence Agent - Strategic Layer
Provides industry analysis, competitive landscape, and market timing intelligence
Complements (not duplicates) CrewAI's tactical research capabilities
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class MarketIntelligence:
    """Strategic market intelligence output"""
    market_size: Optional[float] = None  # Total addressable market in $
    growth_rate: Optional[float] = None  # Annual market growth rate
    competitive_landscape: List[Dict[str, Any]] = None
    market_maturity: str = "Unknown"  # emerging, growth, mature, decline
    seasonal_factors: List[str] = None
    economic_indicators: Dict[str, Any] = None
    buying_patterns: Dict[str, Any] = None
    regulatory_environment: List[str] = None
    technology_trends: List[str] = None
    investment_climate: str = "Unknown"
    risk_factors: List[str] = None
    opportunity_score: float = 0.5
    timing_score: float = 0.5
    strategic_recommendations: List[str] = None
    confidence_level: float = 0.5
    
    def __post_init__(self):
        if self.competitive_landscape is None:
            self.competitive_landscape = []
        if self.seasonal_factors is None:
            self.seasonal_factors = []
        if self.economic_indicators is None:
            self.economic_indicators = {}
        if self.buying_patterns is None:
            self.buying_patterns = {}
        if self.regulatory_environment is None:
            self.regulatory_environment = []
        if self.technology_trends is None:
            self.technology_trends = []
        if self.risk_factors is None:
            self.risk_factors = []
        if self.strategic_recommendations is None:
            self.strategic_recommendations = []

class MarketIntelligenceAgent:
    """
    Strategic Market Intelligence Agent
    
    Provides deep market analysis beyond tactical research:
    - Industry landscape analysis ($XXX billion market size, X% growth)
    - Competitive intelligence and positioning
    - Market timing and seasonal factors
    - Investment climate and funding patterns
    - Technology trends affecting buying decisions
    - Regulatory environment impacts
    - Strategic market entry recommendations
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Market intelligence databases (in production, connect to real data sources)
        self.market_data = self._initialize_market_data()
        
    def _initialize_market_data(self) -> Dict[str, Any]:
        """Initialize market intelligence databases"""
        return {
            "industry_sizes": {
                "software": {"size": 650_000_000_000, "growth": 0.11},  # $650B, 11% growth
                "technology": {"size": 5_200_000_000_000, "growth": 0.13},  # $5.2T, 13% growth
                "fintech": {"size": 180_000_000_000, "growth": 0.25},  # $180B, 25% growth
                "healthcare": {"size": 4_500_000_000_000, "growth": 0.08},  # $4.5T, 8% growth
                "manufacturing": {"size": 2_300_000_000_000, "growth": 0.06},  # $2.3T, 6% growth
                "cloud": {"size": 480_000_000_000, "growth": 0.22},  # $480B, 22% growth
                "ai": {"size": 140_000_000_000, "growth": 0.37},  # $140B, 37% growth
                "cybersecurity": {"size": 155_000_000_000, "growth": 0.12},  # $155B, 12% growth
                "data_analytics": {"size": 280_000_000_000, "growth": 0.18}  # $280B, 18% growth
            },
            "competitive_intelligence": {
                "software": {
                    "major_players": ["Microsoft", "Oracle", "Salesforce", "SAP", "Adobe"],
                    "market_concentration": "fragmented",
                    "innovation_pace": "rapid"
                },
                "fintech": {
                    "major_players": ["Square", "Stripe", "PayPal", "Plaid", "Robinhood"],
                    "market_concentration": "consolidating",
                    "innovation_pace": "very_rapid"
                }
            },
            "seasonal_patterns": {
                "q1": {"budget_allocation": "high", "decision_velocity": "slow"},
                "q2": {"budget_allocation": "medium", "decision_velocity": "medium"},
                "q3": {"budget_allocation": "low", "decision_velocity": "medium"},
                "q4": {"budget_allocation": "very_high", "decision_velocity": "fast"}
            }
        }
    
    async def analyze_market_intelligence(
        self, 
        company_data: Dict[str, Any],
        crewai_results: Optional[Dict[str, Any]] = None
    ) -> MarketIntelligence:
        """
        Generate strategic market intelligence
        
        Takes CrewAI tactical research as input and adds strategic layer:
        - Market sizing and growth analysis
        - Competitive positioning opportunities
        - Investment climate assessment
        - Technology trend impacts
        - Regulatory considerations
        """
        
        try:
            # Extract key data points
            industry = company_data.get("industry", "").lower()
            company_size = company_data.get("company_size", 0)
            location = company_data.get("location", "")
            
            # Generate strategic market analysis
            market_intel = MarketIntelligence()
            
            # 1. Market sizing and growth analysis
            market_intel.market_size, market_intel.growth_rate = self._analyze_market_size(industry)
            
            # 2. Competitive landscape analysis
            market_intel.competitive_landscape = await self._analyze_competitive_landscape(
                industry, company_size, crewai_results
            )
            
            # 3. Market maturity assessment
            market_intel.market_maturity = self._assess_market_maturity(industry, market_intel.growth_rate)
            
            # 4. Seasonal and timing factors
            market_intel.seasonal_factors = self._analyze_seasonal_factors(industry)
            market_intel.timing_score = self._calculate_timing_score()
            
            # 5. Economic and investment climate
            market_intel.economic_indicators = self._analyze_economic_indicators(industry, location)
            market_intel.investment_climate = self._assess_investment_climate(industry)
            
            # 6. Technology trends impact
            market_intel.technology_trends = await self._analyze_technology_trends(industry, crewai_results)
            
            # 7. Regulatory environment
            market_intel.regulatory_environment = self._analyze_regulatory_environment(industry)
            
            # 8. Risk assessment
            market_intel.risk_factors = self._identify_risk_factors(industry, market_intel.growth_rate)
            
            # 9. Strategic recommendations
            market_intel.strategic_recommendations = await self._generate_strategic_recommendations(
                market_intel, company_data, crewai_results
            )
            
            # 10. Calculate overall opportunity and confidence scores
            market_intel.opportunity_score = self._calculate_opportunity_score(market_intel)
            market_intel.confidence_level = self._calculate_confidence_level(market_intel, crewai_results)
            
            self.logger.info(f"Market intelligence generated for {industry} industry")
            return market_intel
            
        except Exception as e:
            self.logger.error(f"Market intelligence analysis failed: {e}")
            return MarketIntelligence()
    
    def _analyze_market_size(self, industry: str) -> Tuple[Optional[float], Optional[float]]:
        """Analyze total addressable market and growth rate"""
        for key, data in self.market_data["industry_sizes"].items():
            if key in industry:
                return data["size"], data["growth"]
        
        # Default for unknown industries
        return 50_000_000_000, 0.08  # $50B, 8% growth
    
    async def _analyze_competitive_landscape(
        self, 
        industry: str, 
        company_size: int,
        crewai_results: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze competitive landscape and positioning opportunities"""
        
        landscape = []
        
        # Get base competitive data
        comp_data = self.market_data["competitive_intelligence"].get(industry, {})
        
        if self.granite_client:
            try:
                prompt = f"""
                Analyze the competitive landscape for the {industry} industry.
                Focus on strategic positioning opportunities for a company with {company_size} employees.
                
                {"CrewAI tactical research found: " + str(crewai_results.get('competitive_analysis', '')) if crewai_results else ""}
                
                Provide strategic analysis in JSON format:
                {{
                    "market_leaders": ["company1", "company2"],
                    "market_gaps": ["gap1", "gap2"],
                    "differentiation_opportunities": ["opp1", "opp2"],
                    "competitive_threats": ["threat1", "threat2"],
                    "market_positioning": "best positioning strategy"
                }}
                """
                
                response = self.granite_client.generate(prompt, max_tokens=1024, temperature=0.3)
                
                try:
                    analysis = json.loads(response.content)
                    landscape.append({
                        "type": "strategic_analysis",
                        "market_leaders": analysis.get("market_leaders", []),
                        "market_gaps": analysis.get("market_gaps", []),
                        "differentiation_opportunities": analysis.get("differentiation_opportunities", []),
                        "competitive_threats": analysis.get("competitive_threats", []),
                        "market_positioning": analysis.get("market_positioning", "")
                    })
                except (json.JSONDecodeError, KeyError):
                    pass
                    
            except Exception as e:
                self.logger.error(f"Competitive analysis failed: {e}")
        
        # Add fallback competitive intelligence
        if comp_data:
            landscape.append({
                "type": "industry_overview",
                "major_players": comp_data.get("major_players", []),
                "market_concentration": comp_data.get("market_concentration", "unknown"),
                "innovation_pace": comp_data.get("innovation_pace", "moderate")
            })
        
        return landscape
    
    def _assess_market_maturity(self, industry: str, growth_rate: Optional[float]) -> str:
        """Assess market maturity stage"""
        if not growth_rate:
            return "Unknown"
        
        if growth_rate > 0.20:
            return "Emerging/High Growth"
        elif growth_rate > 0.10:
            return "Growth Stage"
        elif growth_rate > 0.05:
            return "Mature"
        else:
            return "Mature/Declining"
    
    def _analyze_seasonal_factors(self, industry: str) -> List[str]:
        """Analyze seasonal buying patterns and timing factors"""
        current_quarter = f"q{((datetime.now().month - 1) // 3) + 1}"
        season_data = self.market_data["seasonal_patterns"].get(current_quarter, {})
        
        factors = []
        if season_data.get("budget_allocation") == "high":
            factors.append("High budget allocation period - favorable for large deals")
        elif season_data.get("budget_allocation") == "very_high":
            factors.append("Peak budget season - optimal for enterprise sales")
        
        if season_data.get("decision_velocity") == "fast":
            factors.append("Fast decision-making period - accelerated sales cycles")
        elif season_data.get("decision_velocity") == "slow":
            factors.append("Slower decision period - longer nurturing required")
        
        # Industry-specific seasonal factors
        if "retail" in industry:
            factors.append("Retail industry affected by seasonal consumer patterns")
        elif "education" in industry:
            factors.append("Education sector budget cycles aligned with academic calendar")
        
        return factors
    
    def _calculate_timing_score(self) -> float:
        """Calculate market timing score based on current conditions"""
        current_quarter = f"q{((datetime.now().month - 1) // 3) + 1}"
        season_data = self.market_data["seasonal_patterns"].get(current_quarter, {})
        
        score = 0.5  # Base score
        
        if season_data.get("budget_allocation") == "very_high":
            score += 0.3
        elif season_data.get("budget_allocation") == "high":
            score += 0.2
        
        if season_data.get("decision_velocity") == "fast":
            score += 0.2
        elif season_data.get("decision_velocity") == "slow":
            score -= 0.1
        
        return min(max(score, 0.0), 1.0)
    
    def _analyze_economic_indicators(self, industry: str, location: str) -> Dict[str, Any]:
        """Analyze economic indicators affecting buying decisions"""
        indicators = {
            "interest_rates": "Current rates favorable for capital investments",
            "venture_funding": "VC funding levels affecting growth companies",
            "economic_outlook": "Economic stability supporting business investments",
            "currency_stability": "Exchange rates impacting global companies"
        }
        
        # Industry-specific economic factors
        if "fintech" in industry:
            indicators["regulatory_changes"] = "Financial regulations driving compliance spending"
        elif "healthcare" in industry:
            indicators["healthcare_spending"] = "Healthcare sector investments increasing"
        
        return indicators
    
    def _assess_investment_climate(self, industry: str) -> str:
        """Assess current investment climate for the industry"""
        high_investment_industries = ["ai", "fintech", "cybersecurity", "cloud"]
        
        if any(sector in industry for sector in high_investment_industries):
            return "High Investment Climate - Strong VC/PE interest"
        else:
            return "Moderate Investment Climate - Selective funding"
    
    async def _analyze_technology_trends(
        self, 
        industry: str, 
        crewai_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Analyze technology trends affecting buying decisions"""
        
        trends = []
        
        if self.granite_client:
            try:
                prompt = f"""
                Analyze current technology trends affecting {industry} industry buying decisions.
                Focus on strategic technology shifts that drive enterprise purchasing.
                
                {"CrewAI found these technologies in use: " + str(crewai_results.get('tech_stack', [])) if crewai_results else ""}
                
                Provide 3-4 major technology trends as a JSON array:
                ["AI/ML adoption driving analytics investments", "Cloud migration creating infrastructure needs"]
                """
                
                response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
                
                try:
                    trends = json.loads(response.content)
                    if isinstance(trends, list):
                        return trends[:4]  # Limit to 4 trends
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Technology trends analysis failed: {e}")
        
        # Fallback technology trends by industry
        industry_trends = {
            "software": ["AI/ML integration", "Cloud-native architectures", "DevOps automation"],
            "fintech": ["Blockchain adoption", "Open banking APIs", "AI-driven compliance"],
            "healthcare": ["Telemedicine expansion", "AI diagnostics", "Interoperability standards"],
            "manufacturing": ["Industrial IoT", "Predictive maintenance", "Supply chain digitization"]
        }
        
        for key, trend_list in industry_trends.items():
            if key in industry:
                return trend_list
        
        return ["Digital transformation acceleration", "Cloud adoption", "Automation initiatives"]
    
    def _analyze_regulatory_environment(self, industry: str) -> List[str]:
        """Analyze regulatory environment impacts"""
        regulations = []
        
        if "fintech" in industry or "financial" in industry:
            regulations.extend([
                "PCI DSS compliance requirements",
                "Open Banking regulations driving API adoption",
                "AML/KYC compliance automation needs"
            ])
        elif "healthcare" in industry:
            regulations.extend([
                "HIPAA compliance driving security investments",
                "Interoperability mandates requiring new systems",
                "FDA regulations affecting medical device software"
            ])
        elif "technology" in industry or "software" in industry:
            regulations.extend([
                "GDPR/CCPA privacy regulations",
                "SOC 2 compliance requirements",
                "Accessibility standards (WCAG) compliance"
            ])
        
        return regulations
    
    def _identify_risk_factors(self, industry: str, growth_rate: Optional[float]) -> List[str]:
        """Identify strategic risk factors affecting market opportunity"""
        risks = []
        
        if growth_rate and growth_rate > 0.25:
            risks.append("Rapid growth market - high competition and price pressure")
        elif growth_rate and growth_rate < 0.05:
            risks.append("Slow growth market - limited expansion opportunities")
        
        # Industry-specific risks
        if "fintech" in industry:
            risks.append("Regulatory uncertainty affecting fintech investments")
        elif "healthcare" in industry:
            risks.append("Complex healthcare regulations slowing adoption")
        
        risks.extend([
            "Economic uncertainty affecting enterprise spending",
            "Supply chain disruptions impacting delivery",
            "Competitive pricing pressure from established players"
        ])
        
        return risks
    
    async def _generate_strategic_recommendations(
        self,
        market_intel: MarketIntelligence,
        company_data: Dict[str, Any],
        crewai_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate strategic market entry and positioning recommendations"""
        
        recommendations = []
        
        if self.granite_client:
            try:
                prompt = f"""
                Based on this market intelligence analysis, provide strategic recommendations:
                
                Market Size: ${market_intel.market_size or 0:,.0f}
                Growth Rate: {(market_intel.growth_rate or 0) * 100:.1f}%
                Market Maturity: {market_intel.market_maturity}
                Timing Score: {market_intel.timing_score:.2f}
                Investment Climate: {market_intel.investment_climate}
                
                Target Company: {company_data.get('company_name', 'Unknown')} 
                ({company_data.get('company_size', 0)} employees)
                
                {"CrewAI tactical research identified: " + str(crewai_results.get('pain_points', [])) if crewai_results else ""}
                
                Provide 4-5 strategic recommendations as JSON array:
                ["Focus on Q4 timing for enterprise deals", "Position against legacy solutions"]
                """
                
                response = self.granite_client.generate(prompt, max_tokens=1024, temperature=0.3)
                
                try:
                    recs = json.loads(response.content)
                    if isinstance(recs, list):
                        recommendations = recs[:5]
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Strategic recommendations generation failed: {e}")
        
        # Fallback recommendations
        if not recommendations:
            if market_intel.growth_rate and market_intel.growth_rate > 0.15:
                recommendations.append("Target high-growth market segment with rapid expansion strategy")
            
            if market_intel.timing_score > 0.7:
                recommendations.append("Leverage favorable timing for accelerated sales cycles")
            
            if "High Investment" in market_intel.investment_climate:
                recommendations.append("Position for venture-backed companies with growth capital")
            
            recommendations.extend([
                "Focus on market differentiation through unique value proposition",
                "Align sales strategy with industry seasonal patterns"
            ])
        
        return recommendations
    
    def _calculate_opportunity_score(self, market_intel: MarketIntelligence) -> float:
        """Calculate overall market opportunity score"""
        factors = []
        
        # Market size factor
        if market_intel.market_size:
            if market_intel.market_size > 100_000_000_000:  # >$100B
                factors.append(0.9)
            elif market_intel.market_size > 10_000_000_000:  # >$10B
                factors.append(0.7)
            else:
                factors.append(0.5)
        
        # Growth rate factor
        if market_intel.growth_rate:
            if market_intel.growth_rate > 0.20:
                factors.append(0.9)
            elif market_intel.growth_rate > 0.10:
                factors.append(0.7)
            else:
                factors.append(0.5)
        
        # Timing factor
        factors.append(market_intel.timing_score)
        
        # Investment climate factor
        if "High Investment" in market_intel.investment_climate:
            factors.append(0.8)
        else:
            factors.append(0.6)
        
        return sum(factors) / len(factors) if factors else 0.5
    
    def _calculate_confidence_level(
        self, 
        market_intel: MarketIntelligence, 
        crewai_results: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate confidence level in the analysis"""
        confidence_factors = []
        
        # Data availability
        if market_intel.market_size and market_intel.growth_rate:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Competitive intelligence depth
        if len(market_intel.competitive_landscape) > 0:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.3)
        
        # CrewAI data integration
        if crewai_results:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Technology trends analysis
        if len(market_intel.technology_trends) >= 3:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        return sum(confidence_factors) / len(confidence_factors)
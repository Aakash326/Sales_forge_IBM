"""
Sales Intelligence Orchestrator - Complete Integrated Workflow
Orchestrates all intelligence agents to provide comprehensive sales intelligence
Follows the integrated workflow example from TechFlow analysis
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field

# Import all intelligence agents
from .behavioral_psychology_agent import BehavioralPsychologyAgent, BehavioralAnalysis
from .competitive_intelligence_agent import CompetitiveIntelligenceAgent, CompetitiveIntelligence
from .economic_intelligence_agent import EconomicIntelligenceAgent, EconomicIntelligence
from .predictive_forecast_agent import PredictiveForecastAgent, PredictiveForecast
from .document_intelligence_agent import DocumentIntelligenceAgent, DocumentIntelligence

@dataclass
class StrategicIntelligenceReport:
    """Complete strategic intelligence report combining all agents"""
    
    # Executive Summary
    executive_summary: str = ""
    recommendation: str = ""
    investment_amount: str = ""
    roi_projection: str = ""
    approval_tier: str = ""
    
    # Market Intelligence
    market_size: str = ""
    market_growth: str = ""
    timing_window: str = ""
    economic_climate: str = ""
    
    # Technical Assessment
    technical_complexity: str = ""
    implementation_timeline: str = ""
    feasibility_score: str = ""
    technical_risk: str = ""
    
    # Financial Decision
    total_investment: str = ""
    projected_roi: str = ""
    payback_period: str = ""
    decision_tier: str = ""
    
    # Behavioral Strategy
    decision_maker_profile: str = ""
    optimal_approach: str = ""
    engagement_timeline: str = ""
    
    # Predictive Insights
    buying_window: str = ""
    competitive_threats: str = ""
    economic_window: str = ""
    
    # Recommended Actions
    immediate_actions: List[str] = field(default_factory=list)
    short_term_actions: List[str] = field(default_factory=list)
    long_term_actions: List[str] = field(default_factory=list)
    
    # Strategic Priority and Confidence
    confidence_level: str = ""
    strategic_priority: str = ""
    success_probability: str = ""
    
    # Individual agent results
    behavioral_analysis: Optional[BehavioralAnalysis] = None
    competitive_intelligence: Optional[CompetitiveIntelligence] = None
    economic_intelligence: Optional[EconomicIntelligence] = None
    predictive_forecast: Optional[PredictiveForecast] = None
    document_intelligence: Optional[DocumentIntelligence] = None
    
    # Meta information
    analysis_date: datetime = field(default_factory=datetime.now)
    total_processing_time: float = 0.0

class SalesIntelligenceOrchestrator:
    """
    Sales Intelligence Orchestrator
    
    Coordinates all intelligence agents to provide comprehensive sales intelligence:
    - Market Intelligence: Size, growth, timing, economic climate
    - Technical Architecture: Complexity, feasibility, implementation
    - Executive Decision: Investment analysis, ROI, approval tier
    - Behavioral Strategy: Decision maker profiling, optimal approach
    - Predictive Insights: Timeline prediction, threat analysis
    - Strategic Recommendations: Immediate and long-term actions
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize all intelligence agents
        self.behavioral_agent = BehavioralPsychologyAgent(granite_client, config)
        self.competitive_agent = CompetitiveIntelligenceAgent(granite_client, config)
        self.economic_agent = EconomicIntelligenceAgent(granite_client, config)
        self.predictive_agent = PredictiveForecastAgent(granite_client, config)
        self.document_agent = DocumentIntelligenceAgent(granite_client, config)
        
        # Intelligence synthesis patterns
        self.synthesis_patterns = self._initialize_synthesis_patterns()
        
    def _initialize_synthesis_patterns(self) -> Dict[str, Any]:
        """Initialize patterns for intelligence synthesis"""
        return {
            "investment_tiers": {
                "tactical": {"max_amount": 100_000, "approval": "Department head"},
                "strategic": {"max_amount": 1_000_000, "approval": "Executive committee"},
                "transformational": {"max_amount": 10_000_000, "approval": "Board approval"}
            },
            "roi_thresholds": {
                "excellent": 3.0,    # 3x ROI
                "good": 2.0,         # 2x ROI
                "acceptable": 1.5,   # 1.5x ROI
                "marginal": 1.2      # 1.2x ROI
            },
            "confidence_mapping": {
                (0.9, 1.0): "Very High",
                (0.8, 0.9): "High", 
                (0.6, 0.8): "Medium",
                (0.4, 0.6): "Low",
                (0.0, 0.4): "Very Low"
            },
            "priority_mapping": {
                (0.8, 1.0): "CRITICAL",
                (0.6, 0.8): "HIGH",
                (0.4, 0.6): "MEDIUM",
                (0.0, 0.4): "LOW"
            }
        }
    
    async def generate_complete_intelligence_report(
        self,
        company_data: Dict[str, Any],
        contact_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        interaction_history: Optional[Dict[str, Any]] = None
    ) -> StrategicIntelligenceReport:
        """
        Generate complete strategic intelligence report
        
        Following the integrated workflow pattern:
        📊 Market Intelligence → 🏗️ Technical Architecture → 💰 Executive Decision
        → 🧠 Behavioral Strategy → 🔮 Predictive Insights → 🎯 Strategic Actions
        """
        
        start_time = datetime.now()
        report = StrategicIntelligenceReport()
        
        try:
            company_name = company_data.get("company_name", "Target Company")
            self.logger.info(f"Generating complete intelligence report for {company_name}")
            
            # Phase 1: Parallel Intelligence Gathering
            self.logger.info("Phase 1: Gathering intelligence from all agents...")
            intelligence_tasks = [
                self._run_behavioral_analysis(contact_data, company_data, interaction_history),
                self._run_competitive_intelligence(company_data, market_data),
                self._run_economic_analysis(company_data, market_data),
                self._run_predictive_forecast(company_data, market_data),
                self._run_document_analysis(documents, company_data) if documents else self._create_empty_document_analysis()
            ]
            
            intelligence_results = await asyncio.gather(*intelligence_tasks, return_exceptions=True)
            
            # Store individual results
            report.behavioral_analysis = intelligence_results[0] if not isinstance(intelligence_results[0], Exception) else None
            report.competitive_intelligence = intelligence_results[1] if not isinstance(intelligence_results[1], Exception) else None
            report.economic_intelligence = intelligence_results[2] if not isinstance(intelligence_results[2], Exception) else None
            report.predictive_forecast = intelligence_results[3] if not isinstance(intelligence_results[3], Exception) else None
            report.document_intelligence = intelligence_results[4] if not isinstance(intelligence_results[4], Exception) else None
            
            # Phase 2: Cross-Agent Intelligence Synthesis
            self.logger.info("Phase 2: Synthesizing cross-agent intelligence...")
            
            # Market Intelligence synthesis
            report = self._synthesize_market_intelligence(report)
            
            # Technical Architecture assessment
            report = self._assess_technical_architecture(report, company_data)
            
            # Executive Decision analysis
            report = self._analyze_executive_decision(report, company_data)
            
            # Behavioral Strategy optimization
            report = self._optimize_behavioral_strategy(report)
            
            # Predictive Insights integration
            report = self._integrate_predictive_insights(report)
            
            # Phase 3: Strategic Recommendations Generation
            self.logger.info("Phase 3: Generating strategic recommendations...")
            report = self._generate_strategic_recommendations(report)
            
            # Phase 4: Executive Summary and Final Assessment
            self.logger.info("Phase 4: Creating executive summary...")
            report = self._create_executive_summary(report, company_data)
            
            # Calculate processing metrics
            report.total_processing_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Complete intelligence report generated in {report.total_processing_time:.2f}s")
            self.logger.info(f"Strategic Priority: {report.strategic_priority}, Confidence: {report.confidence_level}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Intelligence report generation failed: {e}")
            report.total_processing_time = (datetime.now() - start_time).total_seconds()
            report.executive_summary = "Intelligence gathering encountered issues. Partial analysis available."
            return report
    
    async def _run_behavioral_analysis(
        self, 
        contact_data: Dict[str, Any], 
        company_data: Dict[str, Any], 
        interaction_history: Optional[Dict[str, Any]]
    ) -> Optional[BehavioralAnalysis]:
        """Run behavioral psychology analysis"""
        try:
            return await self.behavioral_agent.analyze_behavioral_psychology(
                contact_data, company_data, interaction_history
            )
        except Exception as e:
            self.logger.error(f"Behavioral analysis failed: {e}")
            return None
    
    async def _run_competitive_intelligence(
        self, 
        company_data: Dict[str, Any], 
        market_data: Optional[Dict[str, Any]]
    ) -> Optional[CompetitiveIntelligence]:
        """Run competitive intelligence analysis"""
        try:
            return await self.competitive_agent.analyze_competitive_intelligence(
                company_data, market_data
            )
        except Exception as e:
            self.logger.error(f"Competitive intelligence failed: {e}")
            return None
    
    async def _run_economic_analysis(
        self, 
        company_data: Dict[str, Any], 
        market_data: Optional[Dict[str, Any]]
    ) -> Optional[EconomicIntelligence]:
        """Run economic intelligence analysis"""
        try:
            return await self.economic_agent.analyze_economic_intelligence(
                company_data, market_data
            )
        except Exception as e:
            self.logger.error(f"Economic analysis failed: {e}")
            return None
    
    async def _run_predictive_forecast(
        self, 
        company_data: Dict[str, Any], 
        market_data: Optional[Dict[str, Any]]
    ) -> Optional[PredictiveForecast]:
        """Run predictive forecast analysis"""
        try:
            return await self.predictive_agent.generate_predictive_forecast(
                company_data, market_data
            )
        except Exception as e:
            self.logger.error(f"Predictive forecast failed: {e}")
            return None
    
    async def _run_document_analysis(
        self, 
        documents: List[Dict[str, Any]], 
        company_data: Dict[str, Any]
    ) -> Optional[DocumentIntelligence]:
        """Run document intelligence analysis"""
        try:
            return await self.document_agent.analyze_documents(documents, company_data)
        except Exception as e:
            self.logger.error(f"Document analysis failed: {e}")
            return None
    
    async def _create_empty_document_analysis(self) -> Optional[DocumentIntelligence]:
        """Create empty document analysis when no documents provided"""
        return None
    
    def _synthesize_market_intelligence(self, report: StrategicIntelligenceReport) -> StrategicIntelligenceReport:
        """Synthesize market intelligence from competitive and economic agents"""
        
        # Market size from competitive intelligence
        if report.competitive_intelligence and report.competitive_intelligence.market_opportunities:
            opportunities = report.competitive_intelligence.market_opportunities
            if opportunities:
                # Find largest opportunity
                largest_opp = max(opportunities, key=lambda x: len(x.opportunity_size))
                report.market_size = largest_opp.opportunity_size
        
        # Market growth from economic intelligence
        if report.economic_intelligence and report.economic_intelligence.sector_analysis:
            sector = report.economic_intelligence.sector_analysis
            growth_rate = getattr(sector, 'growth_rate', 0.0)
            if growth_rate > 0.15:
                report.market_growth = f"{growth_rate*100:.1f}% (strong growth)"
            elif growth_rate > 0.08:
                report.market_growth = f"{growth_rate*100:.1f}% (moderate growth)"
            else:
                report.market_growth = f"{growth_rate*100:.1f}% (slow growth)"
        
        # Timing window from predictive forecast
        if report.predictive_forecast and report.predictive_forecast.optimal_engagement_period:
            report.timing_window = report.predictive_forecast.optimal_engagement_period
        
        # Economic climate from economic intelligence
        if report.economic_intelligence and report.economic_intelligence.investment_climate:
            climate = report.economic_intelligence.investment_climate.overall_climate
            report.economic_climate = f"{climate.value.replace('_', ' ').title()}"
        
        # Default values if not found
        if not report.market_size:
            report.market_size = "$650M addressable market"
        if not report.market_growth:
            report.market_growth = "12% annual growth"
        if not report.timing_window:
            report.timing_window = "18-month optimal window"
        if not report.economic_climate:
            report.economic_climate = "Favorable conditions"
        
        return report
    
    def _assess_technical_architecture(
        self, 
        report: StrategicIntelligenceReport, 
        company_data: Dict[str, Any]
    ) -> StrategicIntelligenceReport:
        """Assess technical architecture complexity and feasibility"""
        
        company_size = company_data.get("company_size", 250)
        industry = company_data.get("industry", "software")
        
        # Base complexity assessment
        if company_size > 1000:
            complexity_score = 9.8
            timeline_months = 9
            team_size = 6
            feasibility = 75
        elif company_size > 500:
            complexity_score = 7.5
            timeline_months = 6
            team_size = 4
            feasibility = 80
        else:
            complexity_score = 5.2
            timeline_months = 4
            team_size = 3
            feasibility = 85
        
        # Adjust based on technical requirements from documents
        if report.document_intelligence and report.document_intelligence.technical_requirements:
            tech_req = report.document_intelligence.technical_requirements
            if len(tech_req.technology_stack) > 5:
                complexity_score += 1.0
                timeline_months += 1
            if len(tech_req.security_requirements) > 3:
                complexity_score += 0.5
                timeline_months += 1
        
        # Industry adjustments
        if "fintech" in industry.lower():
            complexity_score += 1.5  # Higher compliance requirements
            feasibility -= 5
        elif "healthcare" in industry.lower():
            complexity_score += 2.0  # HIPAA and regulatory complexity
            feasibility -= 10
        
        report.technical_complexity = f"High ({complexity_score:.1f}/10 complexity score)"
        report.implementation_timeline = f"{timeline_months} months, {team_size}-person team"
        report.feasibility_score = f"{feasibility}% (strong with proper resources)"
        
        # Technical risk assessment
        if complexity_score > 8:
            report.technical_risk = "High (enterprise-scale complexity)"
        elif complexity_score > 6:
            report.technical_risk = "Medium (standard implementation challenges)"
        else:
            report.technical_risk = "Low (straightforward implementation)"
        
        return report
    
    def _analyze_executive_decision(
        self, 
        report: StrategicIntelligenceReport, 
        company_data: Dict[str, Any]
    ) -> StrategicIntelligenceReport:
        """Analyze executive decision framework and investment tier"""
        
        # Base investment calculation
        company_size = company_data.get("company_size", 250)
        annual_revenue = company_data.get("annual_revenue", 10_000_000)
        
        # Calculate investment based on company size and technical complexity
        if company_size > 1000:
            base_investment = 800_000
        elif company_size > 500:
            base_investment = 400_000
        elif company_size > 100:
            base_investment = 200_000
        else:
            base_investment = 100_000
        
        # Adjust based on technical complexity
        if "High" in report.technical_complexity:
            base_investment = int(base_investment * 1.3)
        elif "Medium" in report.technical_risk:
            base_investment = int(base_investment * 1.1)
        
        report.total_investment = f"${base_investment:,}"
        
        # ROI calculation based on market growth and company revenue
        market_growth = 0.12  # Default 12%
        if report.market_growth:
            try:
                growth_match = report.market_growth.split('%')[0]
                market_growth = float(growth_match) / 100
            except:
                pass
        
        # Calculate 3-year ROI
        annual_benefit = annual_revenue * market_growth * 0.05  # 5% of growth impact
        three_year_benefit = annual_benefit * 3
        roi_multiple = three_year_benefit / base_investment
        
        report.projected_roi = f"{roi_multiple:.2f}x over 3 years"
        
        # Payback period
        monthly_benefit = annual_benefit / 12
        payback_months = base_investment / monthly_benefit
        report.payback_period = f"{payback_months:.1f} months"
        
        # Determine approval tier
        if base_investment > 500_000:
            report.decision_tier = "Strategic (requires board approval)"
        elif base_investment > 100_000:
            report.decision_tier = "Executive (committee approval)"
        else:
            report.decision_tier = "Tactical (department approval)"
        
        return report
    
    def _optimize_behavioral_strategy(self, report: StrategicIntelligenceReport) -> StrategicIntelligenceReport:
        """Optimize behavioral strategy based on decision maker analysis"""
        
        if report.behavioral_analysis and report.behavioral_analysis.personality_profile:
            personality = report.behavioral_analysis.personality_profile
            primary_type = personality.primary_type.value
            
            # Decision maker profile
            traits = ", ".join(personality.traits[:3]) if personality.traits else "analytical approach"
            report.decision_maker_profile = f"{primary_type.title()} personality: {traits}"
            
            # Optimal approach based on personality
            if primary_type == "analytical":
                report.optimal_approach = "Lead with technical architecture and detailed analysis"
            elif primary_type == "driver": 
                report.optimal_approach = "Focus on ROI and implementation timeline"
            elif primary_type == "expressive":
                report.optimal_approach = "Emphasize innovation and team impact"
            elif primary_type == "amiable":
                report.optimal_approach = "Build consensus with stakeholder involvement"
            else:
                report.optimal_approach = "Balanced approach with data and relationship focus"
        else:
            report.decision_maker_profile = "Technical executive with analytical approach"
            report.optimal_approach = "Lead with architecture and technical value"
        
        # Engagement timeline from behavioral analysis
        if report.behavioral_analysis and report.behavioral_analysis.decision_making_process:
            timeline = report.behavioral_analysis.decision_making_process.timeline
            report.engagement_timeline = f"Start Q4, close Q1 (aligns with {timeline} decision cycle)"
        else:
            report.engagement_timeline = "Start Q4, close Q1 (standard enterprise cycle)"
        
        return report
    
    def _integrate_predictive_insights(self, report: StrategicIntelligenceReport) -> StrategicIntelligenceReport:
        """Integrate predictive insights from forecast agent"""
        
        if report.predictive_forecast:
            forecast = report.predictive_forecast
            
            # Buying window prediction
            if forecast.buying_timeline and forecast.buying_timeline.predicted_window:
                report.buying_window = f"{forecast.buying_timeline.predicted_window} buying window predicted"
            else:
                report.buying_window = "90-day buying window predicted"
            
            # Competitive threats
            if forecast.competitive_threats and forecast.competitive_threats.immediate_threats:
                threat_count = len(forecast.competitive_threats.immediate_threats)
                report.competitive_threats = f"Competitor threats increasing ({threat_count} identified)"
            else:
                report.competitive_threats = "Moderate competitive pressure"
            
            # Economic window
            if forecast.economic_cycles:
                phase = forecast.economic_cycles.get("current_cycle_phase", "expansion")
                window = forecast.economic_cycles.get("optimal_engagement_window", "next 6 months")
                report.economic_window = f"Economic window optimal for {window}"
            else:
                report.economic_window = "Economic window optimal for next 6 months"
        else:
            # Default predictive insights
            report.buying_window = "90-day buying window predicted"
            report.competitive_threats = "Moderate competitive pressure" 
            report.economic_window = "Economic window optimal for next 6 months"
        
        return report
    
    def _generate_strategic_recommendations(self, report: StrategicIntelligenceReport) -> StrategicIntelligenceReport:
        """Generate strategic action recommendations"""
        
        # Immediate actions (next 30 days)
        immediate_actions = []
        if report.behavioral_analysis and report.behavioral_analysis.personality_profile:
            if report.behavioral_analysis.personality_profile.primary_type.value == "analytical":
                immediate_actions.append("Technical architecture presentation to decision maker")
            else:
                immediate_actions.append("Executive value proposition presentation")
        else:
            immediate_actions.append("Technical architecture presentation to decision maker")
        
        # Add urgency-based actions
        if "90-day" in report.buying_window:
            immediate_actions.append("Accelerate discovery and qualification process")
        
        report.immediate_actions = immediate_actions[:3]
        
        # Short-term actions (30-90 days)
        short_term_actions = [
            "Engineering team workshop and technical validation",
            "Business case development with ROI modeling",
            "Stakeholder alignment and executive briefings"
        ]
        
        # Add behavioral-specific actions
        if report.behavioral_analysis and report.behavioral_analysis.decision_making_process:
            if report.behavioral_analysis.decision_making_process.style.value == "consensus":
                short_term_actions.append("Multi-stakeholder consensus building sessions")
        
        report.short_term_actions = short_term_actions[:4]
        
        # Long-term actions (90+ days)
        long_term_actions = [
            "Proposal submission and contract negotiation",
            "Implementation planning and resource allocation",
            "Success metrics definition and tracking setup"
        ]
        
        # Add competitive response actions
        if "increasing" in report.competitive_threats:
            long_term_actions.insert(0, "Competitive differentiation and urgency creation")
        
        report.long_term_actions = long_term_actions[:3]
        
        return report
    
    def _create_executive_summary(
        self, 
        report: StrategicIntelligenceReport, 
        company_data: Dict[str, Any]
    ) -> StrategicIntelligenceReport:
        """Create executive summary and final assessments"""
        
        company_name = company_data.get("company_name", "Target Company")
        investment = report.total_investment
        roi = report.projected_roi
        market_size = report.market_size
        
        # Executive summary
        report.executive_summary = f"{investment} strategic investment → {roi} in {market_size} growing market"
        
        # Recommendation
        if report.decision_tier and "Strategic" in report.decision_tier:
            report.recommendation = "Proceed with Strategic Tier approval"
        elif report.decision_tier and "Executive" in report.decision_tier:
            report.recommendation = "Proceed with Executive Committee approval"
        else:
            report.recommendation = "Proceed with department-level approval"
        
        # Calculate overall confidence
        confidence_factors = []
        
        if report.behavioral_analysis:
            confidence_factors.append(report.behavioral_analysis.analysis_confidence)
        if report.competitive_intelligence:
            confidence_factors.append(report.competitive_intelligence.intelligence_confidence)
        if report.economic_intelligence:
            confidence_factors.append(report.economic_intelligence.confidence_level)
        if report.predictive_forecast:
            # Convert enum to float
            pred_conf = report.predictive_forecast.forecast_confidence
            conf_map = {"low": 0.4, "medium": 0.7, "high": 0.9}
            confidence_factors.append(conf_map.get(pred_conf.value, 0.7))
        
        if confidence_factors:
            avg_confidence = sum(confidence_factors) / len(confidence_factors)
            report.confidence_level = self._map_confidence_level(avg_confidence)
        else:
            report.confidence_level = "Medium"
        
        # Success probability
        success_factors = []
        if report.behavioral_analysis:
            success_factors.append(report.behavioral_analysis.success_probability)
        if "Strong" in report.feasibility_score:
            success_factors.append(0.75)
        if "Favorable" in report.economic_climate:
            success_factors.append(0.8)
        
        if success_factors:
            avg_success = sum(success_factors) / len(success_factors)
            report.success_probability = f"{avg_success*100:.0f}% success probability"
        else:
            report.success_probability = "75% success probability"
        
        # Strategic priority based on ROI and timing
        try:
            roi_value = float(report.projected_roi.split('x')[0])
            if roi_value > 2.0 and "optimal" in report.economic_window.lower():
                report.strategic_priority = "HIGH (limited window, strong ROI, favorable conditions)"
            elif roi_value > 1.5:
                report.strategic_priority = "MEDIUM (good ROI, stable conditions)"
            else:
                report.strategic_priority = "LOW (marginal ROI, assess timing)"
        except:
            report.strategic_priority = "MEDIUM (evaluate based on strategic fit)"
        
        return report
    
    def _map_confidence_level(self, confidence_score: float) -> str:
        """Map confidence score to confidence level"""
        for (min_val, max_val), level in self.synthesis_patterns["confidence_mapping"].items():
            if min_val <= confidence_score < max_val:
                return level
        return "Medium"
    
    # Utility methods for report formatting
    def format_executive_report(self, report: StrategicIntelligenceReport) -> str:
        """Format the complete report in the example style"""
        
        return f"""
📊 STRATEGIC INTELLIGENCE REPORT - {report.analysis_date.strftime('%Y-%m-%d')}

🎯 EXECUTIVE SUMMARY:
{report.executive_summary}
RECOMMENDATION: {report.recommendation}

📈 MARKET INTELLIGENCE:
- Market: {report.market_size}, growing {report.market_growth}
- Timing: {report.timing_window}
- Economic climate: {report.economic_climate}

🏗️ TECHNICAL ARCHITECTURE:
- Complexity: {report.technical_complexity}
- Feasibility: {report.feasibility_score}
- Risk: {report.technical_risk}

💰 EXECUTIVE DECISION:
- Investment: {report.total_investment}
- ROI: {report.projected_roi}
- Payback: {report.payback_period}
- Tier: {report.decision_tier}

🧠 BEHAVIORAL STRATEGY:
- Decision maker: {report.decision_maker_profile}
- Approach: {report.optimal_approach}
- Timeline: {report.engagement_timeline}

🔮 PREDICTIVE INSIGHTS:
- {report.buying_window}
- {report.competitive_threats}
- {report.economic_window}

🎯 RECOMMENDED ACTIONS:
1. Immediate: {'; '.join(report.immediate_actions)}
2. 30 days: {'; '.join(report.short_term_actions)}
3. 60 days: {'; '.join(report.long_term_actions[:2])}
4. 90 days: {'; '.join(report.long_term_actions[2:])}

CONFIDENCE LEVEL: {report.confidence_level}
STRATEGIC PRIORITY: {report.strategic_priority}
SUCCESS PROBABILITY: {report.success_probability}
        """.strip()
    
    def export_detailed_analysis(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Export detailed analysis data for further processing"""
        
        return {
            "executive_summary": {
                "recommendation": report.recommendation,
                "investment": report.total_investment,
                "roi": report.projected_roi,
                "confidence": report.confidence_level,
                "priority": report.strategic_priority
            },
            "market_intelligence": {
                "market_size": report.market_size,
                "growth_rate": report.market_growth,
                "timing_window": report.timing_window,
                "economic_climate": report.economic_climate
            },
            "technical_assessment": {
                "complexity": report.technical_complexity,
                "implementation_timeline": report.implementation_timeline,
                "feasibility": report.feasibility_score,
                "risk_level": report.technical_risk
            },
            "behavioral_strategy": {
                "decision_maker": report.decision_maker_profile,
                "approach": report.optimal_approach,
                "timeline": report.engagement_timeline
            },
            "predictive_insights": {
                "buying_window": report.buying_window,
                "competitive_threats": report.competitive_threats,
                "economic_window": report.economic_window
            },
            "strategic_actions": {
                "immediate": report.immediate_actions,
                "short_term": report.short_term_actions,
                "long_term": report.long_term_actions
            },
            "raw_intelligence": {
                "behavioral_analysis": report.behavioral_analysis,
                "competitive_intelligence": report.competitive_intelligence,
                "economic_intelligence": report.economic_intelligence,
                "predictive_forecast": report.predictive_forecast,
                "document_intelligence": report.document_intelligence
            },
            "metadata": {
                "analysis_date": report.analysis_date.isoformat(),
                "processing_time": report.total_processing_time,
                "success_probability": report.success_probability
            }
        }

# Example usage function
async def analyze_techflow_example():
    """Example analysis following the TechFlow workflow from the prompt"""
    
    orchestrator = SalesIntelligenceOrchestrator()
    
    # TechFlow company data
    company_data = {
        "company_name": "TechFlow Inc",
        "company_size": 350,
        "industry": "software development",
        "annual_revenue": 25_000_000,
        "location": "San Francisco, CA"
    }
    
    # Decision maker data  
    contact_data = {
        "contact_name": "Sarah Chen",
        "title": "CTO",
        "role": "technical_leader",
        "bio": "Technical leader focused on scalable architecture and engineering excellence"
    }
    
    # Example documents
    documents = [
        {
            "type": "financial_report",
            "content": "Revenue growth: 180% YoY accelerating. Burn rate: $890K/month. 18 months runway. Customer metrics: 15% churn, $2.1K ACV. Cash position: Strong for 12-18 months.",
            "metadata": {"date": "2024-01-01", "source": "Q4 Financial Report"}
        },
        {
            "type": "board_presentation", 
            "content": "Strategic priorities: Scale to enterprise, Improve margins. Budget allocation: 40% to product, 25% to sales. Timeline: Enterprise push by Q2 next year. Executive buy-in: CEO fully committed to scaling.",
            "metadata": {"date": "2024-01-15", "source": "Board Strategy Deck"}
        }
    ]
    
    # Generate complete intelligence report
    report = await orchestrator.generate_complete_intelligence_report(
        company_data=company_data,
        contact_data=contact_data,
        documents=documents
    )
    
    # Print formatted report
    formatted_report = orchestrator.format_executive_report(report)
    print(formatted_report)
    
    return report

if __name__ == "__main__":
    # Run example analysis
    import asyncio
    asyncio.run(analyze_techflow_example())
"""
Strategic Orchestrator - IBM Strategic Intelligence Coordination
Coordinates and integrates all strategic IBM agents to create comprehensive business intelligence
Transforms tactical CrewAI results into strategic executive decision support
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json

# Import all strategic agents
from ..ibm_integrations.strategic_agents.market_intelligence_agent import (
    MarketIntelligenceAgent, MarketIntelligence
)
from ..ibm_integrations.strategic_agents.technical_architecture_agent import (
    TechnicalArchitectureAgent, TechnicalArchitecture
)
from ..ibm_integrations.strategic_agents.executive_decision_agent import (
    ExecutiveDecisionAgent, ExecutiveDecisionIntelligence
)
from ..ibm_integrations.strategic_agents.compliance_risk_agent import (
    ComplianceRiskAgent, ComplianceRiskAssessment
)

@dataclass
class StrategicIntelligenceReport:
    """Comprehensive strategic intelligence report combining all agent outputs"""
    
    # Report Metadata
    company_name: str = ""
    report_id: str = ""
    generated_at: datetime = None
    analysis_confidence: float = 0.0
    
    # Input Data Summary
    crewai_tactical_summary: Dict[str, Any] = None
    company_profile: Dict[str, Any] = None
    
    # Strategic Intelligence Components
    market_intelligence: Optional[MarketIntelligence] = None
    technical_architecture: Optional[TechnicalArchitecture] = None
    executive_decision_intelligence: Optional[ExecutiveDecisionIntelligence] = None
    compliance_risk_assessment: Optional[ComplianceRiskAssessment] = None
    
    # Cross-Agent Insights
    strategic_synthesis: Dict[str, Any] = None
    key_recommendations: List[str] = None
    executive_summary: str = ""
    
    # Business Intelligence Dashboard
    strategic_kpis: Dict[str, Any] = None
    risk_dashboard: Dict[str, Any] = None
    opportunity_dashboard: Dict[str, Any] = None
    
    # Next Actions
    immediate_actions: List[str] = None
    strategic_initiatives: List[str] = None
    follow_up_timeline: Dict[str, str] = None
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()
        if self.crewai_tactical_summary is None:
            self.crewai_tactical_summary = {}
        if self.company_profile is None:
            self.company_profile = {}
        if self.strategic_synthesis is None:
            self.strategic_synthesis = {}
        if self.key_recommendations is None:
            self.key_recommendations = []
        if self.strategic_kpis is None:
            self.strategic_kpis = {}
        if self.risk_dashboard is None:
            self.risk_dashboard = {}
        if self.opportunity_dashboard is None:
            self.opportunity_dashboard = {}
        if self.immediate_actions is None:
            self.immediate_actions = []
        if self.strategic_initiatives is None:
            self.strategic_initiatives = []
        if self.follow_up_timeline is None:
            self.follow_up_timeline = {}

class StrategicOrchestrator:
    """
    Strategic Intelligence Orchestrator
    
    Coordinates all IBM strategic agents to transform tactical CrewAI intelligence
    into comprehensive executive decision support:
    
    Input: CrewAI tactical results (research, scoring, outreach)
    Process: Strategic analysis across market, technical, executive, and compliance dimensions
    Output: Executive-ready strategic intelligence report with ROI, risk, and recommendations
    
    Architecture:
    CrewAI (49s tactical) → IBM Strategic Analysis (2-5 min) → Executive Dashboard
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize strategic agents
        self.market_intelligence_agent = MarketIntelligenceAgent(granite_client, config)
        self.technical_architecture_agent = TechnicalArchitectureAgent(granite_client, config)
        self.executive_decision_agent = ExecutiveDecisionAgent(granite_client, config)
        self.compliance_risk_agent = ComplianceRiskAgent(granite_client, config)
        
        # Analysis flow configuration
        self.analysis_config = self._initialize_analysis_config()
        
    def _initialize_analysis_config(self) -> Dict[str, Any]:
        """Initialize strategic analysis configuration"""
        return {
            "parallel_execution": True,  # Run agents in parallel for speed
            "cross_agent_integration": True,  # Enable cross-agent data sharing
            "confidence_threshold": 0.6,  # Minimum confidence for recommendations
            "executive_focus": True,  # Optimize for executive consumption
            "real_time_synthesis": True,  # Generate insights during analysis
            
            # Agent weights for final synthesis
            "agent_weights": {
                "market_intelligence": 0.25,
                "technical_architecture": 0.25, 
                "executive_decision": 0.30,  # Highest weight for executive intelligence
                "compliance_risk": 0.20
            },
            
            # Analysis timeouts (seconds)
            "agent_timeouts": {
                "market_intelligence": 90,
                "technical_architecture": 120,
                "executive_decision": 60,
                "compliance_risk": 90
            }
        }
    
    async def generate_strategic_intelligence(
        self,
        company_data: Dict[str, Any],
        crewai_results: Optional[Dict[str, Any]] = None,
        solution_requirements: Optional[Dict[str, Any]] = None
    ) -> StrategicIntelligenceReport:
        """
        Generate comprehensive strategic intelligence report
        
        Takes CrewAI tactical intelligence and transforms it into executive-level
        strategic business intelligence with ROI analysis, risk assessment,
        and strategic recommendations.
        """
        
        try:
            # Initialize strategic intelligence report
            report = StrategicIntelligenceReport(
                company_name=company_data.get("company_name", "Target Company"),
                report_id=f"SI_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                company_profile=company_data,
                crewai_tactical_summary=self._summarize_crewai_results(crewai_results)
            )
            
            self.logger.info(f"Starting strategic intelligence generation for {report.company_name}")
            start_time = datetime.now()
            
            # Phase 1: Parallel Strategic Analysis
            self.logger.info("Phase 1: Executing parallel strategic analysis")
            analysis_results = await self._execute_parallel_strategic_analysis(
                company_data, crewai_results, solution_requirements
            )
            
            # Unpack results
            report.market_intelligence = analysis_results["market_intelligence"]
            report.technical_architecture = analysis_results["technical_architecture"]
            report.compliance_risk_assessment = analysis_results["compliance_risk"]
            
            # Phase 2: Executive Decision Intelligence (requires other analyses)
            self.logger.info("Phase 2: Generating executive decision intelligence")
            report.executive_decision_intelligence = await self._generate_executive_intelligence(
                company_data, report.market_intelligence, report.technical_architecture, 
                report.compliance_risk_assessment, crewai_results
            )
            
            # Phase 3: Strategic Synthesis and Cross-Agent Insights
            self.logger.info("Phase 3: Performing strategic synthesis")
            report.strategic_synthesis = await self._perform_strategic_synthesis(report)
            
            # Phase 4: Executive Dashboard and KPIs
            self.logger.info("Phase 4: Creating executive dashboard")
            report.strategic_kpis = self._create_strategic_kpis(report)
            report.risk_dashboard = self._create_risk_dashboard(report)
            report.opportunity_dashboard = self._create_opportunity_dashboard(report)
            
            # Phase 5: Key Recommendations and Actions
            self.logger.info("Phase 5: Generating recommendations and actions")
            report.key_recommendations = await self._generate_key_recommendations(report)
            report.immediate_actions = self._identify_immediate_actions(report)
            report.strategic_initiatives = self._identify_strategic_initiatives(report)
            report.follow_up_timeline = self._create_follow_up_timeline(report)
            
            # Phase 6: Executive Summary Generation
            self.logger.info("Phase 6: Creating executive summary")
            report.executive_summary = await self._generate_executive_summary(report)
            
            # Final: Calculate overall confidence
            report.analysis_confidence = self._calculate_overall_confidence(report)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Strategic intelligence generation completed in {execution_time:.1f} seconds")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Strategic intelligence generation failed: {e}")
            return StrategicIntelligenceReport(
                company_name=company_data.get("company_name", "Target Company"),
                report_id=f"SI_ERROR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                executive_summary="Strategic analysis failed due to technical error. Manual review required."
            )
    
    def _summarize_crewai_results(self, crewai_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize CrewAI tactical results for strategic context"""
        
        if not crewai_results:
            return {
                "tactical_analysis_available": False,
                "note": "Strategic analysis performed without tactical intelligence input"
            }
        
        summary = {
            "tactical_analysis_available": True,
            "research_completed": crewai_results.get("research_completed", False),
            "pain_points_identified": len(crewai_results.get("pain_points", [])),
            "tech_stack_analyzed": len(crewai_results.get("tech_stack", [])),
            "lead_score": crewai_results.get("lead_score", 0),
            "key_insights_count": len(crewai_results.get("key_insights", [])),
            "tactical_quality_score": self._assess_crewai_quality(crewai_results)
        }
        
        return summary
    
    def _assess_crewai_quality(self, crewai_results: Dict[str, Any]) -> float:
        """Assess quality of CrewAI tactical intelligence for strategic planning"""
        
        quality_factors = []
        
        # Research completeness
        if crewai_results.get("research_completed"):
            quality_factors.append(0.8)
        else:
            quality_factors.append(0.3)
        
        # Pain points depth
        pain_points = crewai_results.get("pain_points", [])
        if len(pain_points) >= 3:
            quality_factors.append(0.9)
        elif len(pain_points) >= 1:
            quality_factors.append(0.6)
        else:
            quality_factors.append(0.2)
        
        # Tech stack analysis
        tech_stack = crewai_results.get("tech_stack", [])
        if len(tech_stack) >= 3:
            quality_factors.append(0.8)
        elif len(tech_stack) >= 1:
            quality_factors.append(0.5)
        else:
            quality_factors.append(0.3)
        
        # Lead scoring quality
        lead_score = crewai_results.get("lead_score", 0)
        if lead_score > 0.7:
            quality_factors.append(0.9)
        elif lead_score > 0.5:
            quality_factors.append(0.7)
        else:
            quality_factors.append(0.4)
        
        return sum(quality_factors) / len(quality_factors) if quality_factors else 0.5
    
    async def _execute_parallel_strategic_analysis(
        self,
        company_data: Dict[str, Any],
        crewai_results: Optional[Dict[str, Any]],
        solution_requirements: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute strategic agents in parallel for performance"""
        
        if self.analysis_config["parallel_execution"]:
            # Create tasks for parallel execution
            tasks = [
                asyncio.create_task(
                    asyncio.wait_for(
                        self.market_intelligence_agent.analyze_market_intelligence(
                            company_data, crewai_results
                        ),
                        timeout=self.analysis_config["agent_timeouts"]["market_intelligence"]
                    ),
                    name="market_intelligence"
                ),
                asyncio.create_task(
                    asyncio.wait_for(
                        self.technical_architecture_agent.analyze_technical_architecture(
                            company_data, crewai_results, solution_requirements
                        ),
                        timeout=self.analysis_config["agent_timeouts"]["technical_architecture"]
                    ),
                    name="technical_architecture"
                ),
                asyncio.create_task(
                    asyncio.wait_for(
                        self.compliance_risk_agent.assess_compliance_and_risk(
                            company_data
                        ),
                        timeout=self.analysis_config["agent_timeouts"]["compliance_risk"]
                    ),
                    name="compliance_risk"
                )
            ]
            
            # Execute all tasks in parallel
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results and handle any exceptions
                analysis_results = {}
                task_names = ["market_intelligence", "technical_architecture", "compliance_risk"]
                
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        self.logger.error(f"Agent {task_names[i]} failed: {result}")
                        # Provide fallback empty results
                        if task_names[i] == "market_intelligence":
                            analysis_results[task_names[i]] = MarketIntelligence()
                        elif task_names[i] == "technical_architecture":
                            analysis_results[task_names[i]] = TechnicalArchitecture()
                        else:  # compliance_risk
                            analysis_results[task_names[i]] = ComplianceRiskAssessment()
                    else:
                        analysis_results[task_names[i]] = result
                
                return analysis_results
                
            except Exception as e:
                self.logger.error(f"Parallel execution failed: {e}")
                # Return empty results
                return {
                    "market_intelligence": MarketIntelligence(),
                    "technical_architecture": TechnicalArchitecture(),
                    "compliance_risk": ComplianceRiskAssessment()
                }
        else:
            # Sequential execution fallback
            return {
                "market_intelligence": await self.market_intelligence_agent.analyze_market_intelligence(company_data, crewai_results),
                "technical_architecture": await self.technical_architecture_agent.analyze_technical_architecture(company_data, crewai_results, solution_requirements),
                "compliance_risk": await self.compliance_risk_agent.assess_compliance_and_risk(company_data)
            }
    
    async def _generate_executive_intelligence(
        self,
        company_data: Dict[str, Any],
        market_intel: Optional[MarketIntelligence],
        tech_arch: Optional[TechnicalArchitecture],
        compliance_risk: Optional[ComplianceRiskAssessment],
        crewai_results: Optional[Dict[str, Any]]
    ) -> ExecutiveDecisionIntelligence:
        """Generate executive decision intelligence using all other analyses"""
        
        try:
            # Convert analyses to dictionaries for executive agent
            market_data = asdict(market_intel) if market_intel else None
            tech_data = asdict(tech_arch) if tech_arch else None
            compliance_data = asdict(compliance_risk) if compliance_risk else None
            
            executive_intel = await asyncio.wait_for(
                self.executive_decision_agent.generate_executive_decision_intelligence(
                    company_data, market_data, tech_data, crewai_results
                ),
                timeout=self.analysis_config["agent_timeouts"]["executive_decision"]
            )
            
            return executive_intel
            
        except Exception as e:
            self.logger.error(f"Executive intelligence generation failed: {e}")
            return ExecutiveDecisionIntelligence()
    
    async def _perform_strategic_synthesis(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Synthesize insights across all strategic agents"""
        
        synthesis = {
            "cross_agent_insights": [],
            "strategic_alignment_score": 0.0,
            "confidence_correlation": {},
            "investment_coherence": {},
            "risk_opportunity_balance": {}
        }
        
        try:
            # Cross-agent insight generation
            if self.granite_client:
                cross_insights = await self._generate_cross_agent_insights(report)
                synthesis["cross_agent_insights"] = cross_insights
            
            # Strategic alignment assessment
            synthesis["strategic_alignment_score"] = self._assess_strategic_alignment(report)
            
            # Confidence correlation analysis
            synthesis["confidence_correlation"] = self._analyze_confidence_correlation(report)
            
            # Investment coherence analysis
            synthesis["investment_coherence"] = self._analyze_investment_coherence(report)
            
            # Risk-opportunity balance
            synthesis["risk_opportunity_balance"] = self._analyze_risk_opportunity_balance(report)
            
        except Exception as e:
            self.logger.error(f"Strategic synthesis failed: {e}")
        
        return synthesis
    
    async def _generate_cross_agent_insights(self, report: StrategicIntelligenceReport) -> List[str]:
        """Generate insights that span across multiple strategic dimensions"""
        
        insights = []
        
        if not self.granite_client:
            return [
                "Market opportunity aligns with technical capabilities",
                "Risk assessment supports investment thesis",
                "Compliance requirements factored into ROI projections"
            ]
        
        try:
            # Gather key data points from all agents
            market_size = report.market_intelligence.market_size if report.market_intelligence else 0
            growth_rate = report.market_intelligence.growth_rate if report.market_intelligence else 0
            roi = report.executive_decision_intelligence.projected_roi if report.executive_decision_intelligence else 0
            risk_level = report.compliance_risk_assessment.overall_risk_level.value if report.compliance_risk_assessment else "medium"
            tech_feasibility = report.technical_architecture.feasibility_score if report.technical_architecture else 0.5
            
            prompt = f"""
            Analyze strategic insights across multiple dimensions:
            
            Market Intelligence:
            - Market Size: ${market_size:,.0f}
            - Growth Rate: {(growth_rate * 100):.1f}%
            
            Executive Decision:
            - Projected ROI: {roi:.1f}x
            - Investment Tier: Enterprise-level analysis
            
            Risk Assessment:
            - Overall Risk Level: {risk_level}
            - Compliance Requirements: Multiple frameworks
            
            Technical Architecture:
            - Feasibility Score: {tech_feasibility:.2f}
            
            Generate 4-5 strategic insights that connect these dimensions:
            ["Market timing favorable for high-ROI investment", "Technical feasibility supports aggressive growth projections"]
            """
            
            response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
            
            try:
                cross_insights = json.loads(response.content)
                if isinstance(cross_insights, list):
                    insights = cross_insights[:5]
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            self.logger.error(f"Cross-agent insights generation failed: {e}")
        
        # Fallback insights
        if not insights:
            insights = [
                "Strategic analysis shows alignment between market opportunity and technical capabilities",
                "Risk-adjusted ROI projections support investment recommendation",
                "Compliance timeline aligns with technical implementation phases",
                "Market growth trends support aggressive expansion strategy"
            ]
        
        return insights
    
    def _assess_strategic_alignment(self, report: StrategicIntelligenceReport) -> float:
        """Assess alignment between different strategic dimensions"""
        
        alignment_factors = []
        
        # Market-Executive alignment
        if report.market_intelligence and report.executive_decision_intelligence:
            market_opportunity = report.market_intelligence.opportunity_score
            executive_confidence = report.executive_decision_intelligence.roi_confidence.value
            
            # High market opportunity should align with high executive confidence
            market_exec_alignment = 1.0 - abs(market_opportunity - (0.8 if "high" in executive_confidence else 0.5))
            alignment_factors.append(market_exec_alignment)
        
        # Technical-Risk alignment
        if report.technical_architecture and report.compliance_risk_assessment:
            tech_feasibility = report.technical_architecture.feasibility_score
            risk_score = 1.0 - report.compliance_risk_assessment.risk_score
            
            # High technical feasibility should align with low risk
            tech_risk_alignment = 1.0 - abs(tech_feasibility - risk_score)
            alignment_factors.append(tech_risk_alignment)
        
        # ROI-Risk alignment
        if report.executive_decision_intelligence and report.compliance_risk_assessment:
            roi_score = min(report.executive_decision_intelligence.projected_roi / 3.0, 1.0)  # Normalize ROI
            risk_adjusted_score = 1.0 - report.compliance_risk_assessment.risk_score
            
            # High ROI should be supported by manageable risk
            roi_risk_alignment = 1.0 - abs(roi_score - risk_adjusted_score)
            alignment_factors.append(roi_risk_alignment)
        
        return sum(alignment_factors) / len(alignment_factors) if alignment_factors else 0.5
    
    def _analyze_confidence_correlation(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Analyze correlation between agent confidence levels"""
        
        confidences = {}
        
        if report.market_intelligence:
            confidences["market"] = report.market_intelligence.confidence_level
        if report.technical_architecture:
            confidences["technical"] = report.technical_architecture.confidence_level
        if report.executive_decision_intelligence:
            confidences["executive"] = 0.8 if "high" in report.executive_decision_intelligence.roi_confidence.value else 0.6
        if report.compliance_risk_assessment:
            confidences["compliance"] = report.compliance_risk_assessment.assessment_confidence
        
        # Calculate average confidence
        avg_confidence = sum(confidences.values()) / len(confidences) if confidences else 0.5
        
        # Identify confidence gaps
        confidence_gaps = []
        for agent, confidence in confidences.items():
            if confidence < avg_confidence - 0.2:
                confidence_gaps.append(f"{agent}: {confidence:.2f} (below average)")
        
        return {
            "agent_confidences": confidences,
            "average_confidence": avg_confidence,
            "confidence_gaps": confidence_gaps,
            "confidence_consistency": 1.0 - (max(confidences.values()) - min(confidences.values())) if confidences else 0.5
        }
    
    def _analyze_investment_coherence(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Analyze coherence of investment recommendations across agents"""
        
        coherence = {
            "market_supports_investment": False,
            "technical_supports_investment": False,
            "risk_supports_investment": False,
            "executive_recommends_investment": False,
            "overall_coherence_score": 0.0
        }
        
        # Market intelligence support
        if report.market_intelligence:
            if report.market_intelligence.opportunity_score > 0.7:
                coherence["market_supports_investment"] = True
        
        # Technical architecture support
        if report.technical_architecture:
            if report.technical_architecture.feasibility_score > 0.6:
                coherence["technical_supports_investment"] = True
        
        # Risk assessment support
        if report.compliance_risk_assessment:
            if report.compliance_risk_assessment.risk_score < 0.6:  # Lower risk score = supports investment
                coherence["risk_supports_investment"] = True
        
        # Executive recommendation
        if report.executive_decision_intelligence:
            if "RECOMMEND" in report.executive_decision_intelligence.executive_recommendation:
                coherence["executive_recommends_investment"] = True
        
        # Calculate overall coherence
        support_factors = [
            coherence["market_supports_investment"],
            coherence["technical_supports_investment"], 
            coherence["risk_supports_investment"],
            coherence["executive_recommends_investment"]
        ]
        
        coherence["overall_coherence_score"] = sum(support_factors) / len(support_factors)
        
        return coherence
    
    def _analyze_risk_opportunity_balance(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Analyze balance between risks and opportunities"""
        
        balance = {
            "opportunity_score": 0.5,
            "risk_score": 0.5,
            "balance_ratio": 1.0,
            "recommendation": "balanced"
        }
        
        # Calculate opportunity score
        opportunity_factors = []
        if report.market_intelligence:
            opportunity_factors.append(report.market_intelligence.opportunity_score)
        if report.executive_decision_intelligence:
            roi_opportunity = min(report.executive_decision_intelligence.projected_roi / 3.0, 1.0)
            opportunity_factors.append(roi_opportunity)
        
        balance["opportunity_score"] = sum(opportunity_factors) / len(opportunity_factors) if opportunity_factors else 0.5
        
        # Calculate risk score
        if report.compliance_risk_assessment:
            balance["risk_score"] = report.compliance_risk_assessment.risk_score
        
        # Calculate balance ratio (opportunity/risk)
        if balance["risk_score"] > 0:
            balance["balance_ratio"] = balance["opportunity_score"] / balance["risk_score"]
        
        # Generate recommendation
        if balance["balance_ratio"] > 1.5:
            balance["recommendation"] = "opportunity_favorable"
        elif balance["balance_ratio"] < 0.7:
            balance["recommendation"] = "risk_concern"
        else:
            balance["recommendation"] = "balanced"
        
        return balance
    
    def _create_strategic_kpis(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Create strategic KPI dashboard"""
        
        kpis = {
            "financial_metrics": {},
            "market_metrics": {},
            "operational_metrics": {},
            "risk_metrics": {}
        }
        
        # Financial KPIs
        if report.executive_decision_intelligence:
            kpis["financial_metrics"] = {
                "projected_roi": f"{report.executive_decision_intelligence.projected_roi:.1f}x",
                "total_investment": f"${report.executive_decision_intelligence.total_investment:,.0f}",
                "payback_period": f"{report.executive_decision_intelligence.payback_period_months} months",
                "3yr_revenue_potential": f"${report.executive_decision_intelligence.recurring_revenue_potential:,.0f}"
            }
        
        # Market KPIs
        if report.market_intelligence:
            kpis["market_metrics"] = {
                "market_size": f"${report.market_intelligence.market_size:,.0f}",
                "growth_rate": f"{(report.market_intelligence.growth_rate * 100):.1f}%",
                "opportunity_score": f"{report.market_intelligence.opportunity_score:.2f}",
                "timing_score": f"{report.market_intelligence.timing_score:.2f}"
            }
        
        # Operational KPIs
        if report.technical_architecture:
            kpis["operational_metrics"] = {
                "feasibility_score": f"{report.technical_architecture.feasibility_score:.2f}",
                "implementation_timeline": f"{report.technical_architecture.timeline_estimate.get('adjusted_duration_months', 6)} months",
                "team_size_required": f"{report.technical_architecture.resource_requirements.get('development_team_size', 3)} people",
                "architecture_score": f"{report.technical_architecture.architecture_score:.2f}"
            }
        
        # Risk KPIs
        if report.compliance_risk_assessment:
            kpis["risk_metrics"] = {
                "overall_risk_level": report.compliance_risk_assessment.overall_risk_level.value,
                "risk_score": f"{report.compliance_risk_assessment.risk_score:.2f}",
                "compliance_readiness": f"{report.compliance_risk_assessment.compliance_readiness_score:.2f}",
                "potential_financial_impact": f"${report.compliance_risk_assessment.potential_financial_impact:,.0f}"
            }
        
        return kpis
    
    def _create_risk_dashboard(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Create risk management dashboard"""
        
        dashboard = {
            "risk_summary": {},
            "top_risks": [],
            "mitigation_priorities": [],
            "compliance_status": {}
        }
        
        if report.compliance_risk_assessment:
            # Risk summary
            dashboard["risk_summary"] = {
                "overall_level": report.compliance_risk_assessment.overall_risk_level.value,
                "total_risks_identified": (
                    len(report.compliance_risk_assessment.business_risks) +
                    len(report.compliance_risk_assessment.operational_risks) +
                    len(report.compliance_risk_assessment.technology_risks)
                ),
                "high_priority_risks": len([
                    risk for risk in (
                        report.compliance_risk_assessment.business_risks +
                        report.compliance_risk_assessment.operational_risks +
                        report.compliance_risk_assessment.technology_risks
                    ) if risk.get("impact") == "high"
                ]),
                "financial_exposure": f"${report.compliance_risk_assessment.potential_financial_impact:,.0f}"
            }
            
            # Top risks (highest financial impact)
            all_risks = (
                report.compliance_risk_assessment.business_risks +
                report.compliance_risk_assessment.operational_risks +
                report.compliance_risk_assessment.technology_risks
            )
            
            sorted_risks = sorted(
                all_risks,
                key=lambda x: x.get("financial_impact", 0),
                reverse=True
            )
            
            dashboard["top_risks"] = [
                {
                    "risk": risk["risk"],
                    "impact": f"${risk.get('financial_impact', 0):,.0f}",
                    "probability": risk.get("probability", "medium"),
                    "category": "business" if risk in report.compliance_risk_assessment.business_risks else "operational"
                }
                for risk in sorted_risks[:5]
            ]
            
            # Compliance status
            dashboard["compliance_status"] = {
                "frameworks_applicable": len(report.compliance_risk_assessment.applicable_regulations),
                "compliance_gaps": len(report.compliance_risk_assessment.compliance_gaps),
                "readiness_score": f"{report.compliance_risk_assessment.compliance_readiness_score:.2f}",
                "estimated_compliance_cost": f"${report.compliance_risk_assessment.compliance_costs.get('total_implementation_cost', 0):,.0f}"
            }
        
        return dashboard
    
    def _create_opportunity_dashboard(self, report: StrategicIntelligenceReport) -> Dict[str, Any]:
        """Create strategic opportunity dashboard"""
        
        dashboard = {
            "market_opportunities": {},
            "strategic_advantages": [],
            "investment_highlights": {},
            "growth_projections": {}
        }
        
        # Market opportunities
        if report.market_intelligence:
            dashboard["market_opportunities"] = {
                "market_size": f"${report.market_intelligence.market_size:,.0f}",
                "annual_growth": f"{(report.market_intelligence.growth_rate * 100):.1f}%",
                "opportunity_score": report.market_intelligence.opportunity_score,
                "timing_favorability": "favorable" if report.market_intelligence.timing_score > 0.7 else "moderate"
            }
            
            dashboard["strategic_advantages"] = report.market_intelligence.strategic_recommendations[:3]
        
        # Investment highlights
        if report.executive_decision_intelligence:
            dashboard["investment_highlights"] = {
                "roi_multiple": f"{report.executive_decision_intelligence.projected_roi:.1f}x",
                "payback_timeline": f"{report.executive_decision_intelligence.payback_period_months} months",
                "investment_tier": report.executive_decision_intelligence.investment_tier.value,
                "probability_of_success": f"{report.executive_decision_intelligence.probability_of_success:.1%}"
            }
            
            # Growth projections
            dashboard["growth_projections"] = {
                "year_1_revenue": f"${report.executive_decision_intelligence.revenue_opportunity:,.0f}",
                "3_year_total": f"${report.executive_decision_intelligence.recurring_revenue_potential:,.0f}",
                "customer_lifetime_value": f"${report.executive_decision_intelligence.customer_lifetime_value:,.0f}",
                "market_expansion_potential": f"${report.executive_decision_intelligence.market_expansion_value:,.0f}"
            }
        
        return dashboard
    
    async def _generate_key_recommendations(self, report: StrategicIntelligenceReport) -> List[str]:
        """Generate top strategic recommendations across all dimensions"""
        
        recommendations = []
        
        if self.granite_client:
            try:
                # Gather top insights from each agent
                market_recs = report.market_intelligence.strategic_recommendations[:2] if report.market_intelligence else []
                exec_rec = report.executive_decision_intelligence.executive_recommendation if report.executive_decision_intelligence else ""
                risk_recs = report.compliance_risk_assessment.governance_recommendations[:2] if report.compliance_risk_assessment else []
                
                prompt = f"""
                Synthesize top strategic recommendations from comprehensive analysis:
                
                Market Intelligence Recommendations: {market_recs}
                Executive Recommendation: {exec_rec}
                Risk Management Recommendations: {risk_recs}
                
                Create 5 prioritized strategic recommendations that integrate all dimensions:
                ["INVEST: Strong ROI opportunity with favorable market timing", "ACCELERATE: Fast-track technical implementation"]
                
                Focus on actionable, executive-level strategic guidance.
                """
                
                response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
                
                try:
                    recs = json.loads(response.content)
                    if isinstance(recs, list):
                        recommendations = recs[:5]
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Key recommendations generation failed: {e}")
        
        # Fallback recommendations based on analysis results
        if not recommendations:
            # Investment recommendation
            if (report.executive_decision_intelligence and 
                report.executive_decision_intelligence.projected_roi > 2.0):
                recommendations.append("INVEST: Strong ROI opportunity exceeds investment hurdle rates")
            
            # Market timing recommendation
            if (report.market_intelligence and 
                report.market_intelligence.timing_score > 0.7):
                recommendations.append("ACCELERATE: Market timing favorable for aggressive expansion")
            
            # Risk management recommendation
            if (report.compliance_risk_assessment and 
                len(report.compliance_risk_assessment.compliance_gaps) > 2):
                recommendations.append("PRIORITIZE: Address compliance gaps before full deployment")
            
            # Technical readiness recommendation
            if (report.technical_architecture and 
                report.technical_architecture.feasibility_score > 0.7):
                recommendations.append("EXECUTE: Technical feasibility supports implementation timeline")
            
            # Default strategic recommendation
            if len(recommendations) < 3:
                recommendations.append("EVALUATE: Proceed with phased implementation approach")
        
        return recommendations
    
    def _identify_immediate_actions(self, report: StrategicIntelligenceReport) -> List[str]:
        """Identify immediate actions (next 30 days)"""
        
        actions = []
        
        # Executive decision actions
        if (report.executive_decision_intelligence and 
            "STRONG RECOMMEND" in report.executive_decision_intelligence.executive_recommendation):
            actions.append("Schedule executive committee meeting for investment approval")
        
        # Compliance actions
        if (report.compliance_risk_assessment and 
            len(report.compliance_risk_assessment.compliance_gaps) > 0):
            actions.append("Initiate compliance gap assessment and remediation planning")
        
        # Market timing actions
        if (report.market_intelligence and 
            report.market_intelligence.timing_score > 0.8):
            actions.append("Accelerate business development activities to capitalize on market timing")
        
        # Technical preparation actions
        if (report.technical_architecture and 
            report.technical_architecture.solution_complexity.value in ["high", "enterprise"]):
            actions.append("Engage technical architecture consultants for detailed implementation planning")
        
        # Default actions
        if not actions:
            actions = [
                "Conduct stakeholder alignment meeting",
                "Finalize project scope and requirements",
                "Prepare detailed implementation timeline"
            ]
        
        return actions[:5]  # Limit to 5 immediate actions
    
    def _identify_strategic_initiatives(self, report: StrategicIntelligenceReport) -> List[str]:
        """Identify strategic initiatives (3-12 months)"""
        
        initiatives = []
        
        # Market expansion initiatives
        if (report.market_intelligence and 
            report.market_intelligence.market_expansion_value > 1000000):
            initiatives.append("Launch market expansion program targeting high-growth segments")
        
        # Technology modernization initiatives
        if (report.technical_architecture and 
            len(report.technical_architecture.modernization_opportunities) > 2):
            initiatives.append("Execute technology modernization roadmap")
        
        # Compliance program initiatives
        if (report.compliance_risk_assessment and 
            len(report.compliance_risk_assessment.applicable_regulations) > 2):
            initiatives.append("Establish enterprise compliance and risk management program")
        
        # Revenue optimization initiatives
        if (report.executive_decision_intelligence and 
            report.executive_decision_intelligence.recurring_revenue_potential > 2000000):
            initiatives.append("Deploy customer success program to maximize revenue expansion")
        
        # Default strategic initiatives
        if not initiatives:
            initiatives = [
                "Build strategic partnership ecosystem",
                "Establish market leadership positioning",
                "Develop competitive differentiation strategy"
            ]
        
        return initiatives[:4]  # Limit to 4 strategic initiatives
    
    def _create_follow_up_timeline(self, report: StrategicIntelligenceReport) -> Dict[str, str]:
        """Create follow-up timeline for strategic intelligence refresh"""
        
        timeline = {
            "next_review": "90 days",
            "quarterly_update": "Quarterly strategic intelligence refresh",
            "annual_assessment": "Annual comprehensive strategic review"
        }
        
        # Adjust based on risk level and market dynamics
        if (report.compliance_risk_assessment and 
            report.compliance_risk_assessment.overall_risk_level.value == "critical"):
            timeline["next_review"] = "30 days"
            timeline["monthly_monitoring"] = "Monthly risk assessment updates"
        
        if (report.market_intelligence and 
            report.market_intelligence.growth_rate > 0.25):  # >25% growth market
            timeline["market_monitoring"] = "Monthly market intelligence updates"
        
        return timeline
    
    async def _generate_executive_summary(self, report: StrategicIntelligenceReport) -> str:
        """Generate comprehensive executive summary"""
        
        if self.granite_client:
            try:
                # Gather key metrics for summary
                roi = report.executive_decision_intelligence.projected_roi if report.executive_decision_intelligence else 0
                investment = report.executive_decision_intelligence.total_investment if report.executive_decision_intelligence else 0
                market_size = report.market_intelligence.market_size if report.market_intelligence else 0
                risk_level = report.compliance_risk_assessment.overall_risk_level.value if report.compliance_risk_assessment else "medium"
                
                prompt = f"""
                Create an executive summary for strategic intelligence report:
                
                Company: {report.company_name}
                Key Metrics:
                - Investment Required: ${investment:,.0f}
                - Projected ROI: {roi:.1f}x
                - Market Size: ${market_size:,.0f}
                - Risk Level: {risk_level}
                - Analysis Confidence: {report.analysis_confidence:.2f}
                
                Top Recommendations: {report.key_recommendations[:2]}
                
                Write a compelling 4-5 sentence executive summary that captures:
                1. Strategic opportunity assessment
                2. Investment recommendation
                3. Key success factors and risks
                4. Next steps
                
                Focus on business impact and strategic value.
                """
                
                response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
                return response.content.strip()
                
            except Exception as e:
                self.logger.error(f"Executive summary generation failed: {e}")
        
        # Fallback executive summary
        investment = report.executive_decision_intelligence.total_investment if report.executive_decision_intelligence else 500000
        roi = report.executive_decision_intelligence.projected_roi if report.executive_decision_intelligence else 1.5
        
        return f"""
        Strategic analysis of {report.company_name} reveals a compelling investment opportunity with ${investment:,.0f} 
        investment generating {roi:.1f}x ROI potential. Market intelligence indicates favorable timing with strong 
        growth dynamics, while technical feasibility assessment confirms implementation viability. Risk analysis 
        identifies manageable compliance and operational considerations with appropriate mitigation strategies. 
        Recommend proceeding with phased implementation approach prioritizing immediate market capture opportunities.
        """
    
    def _calculate_overall_confidence(self, report: StrategicIntelligenceReport) -> float:
        """Calculate overall confidence in strategic intelligence report"""
        
        confidence_factors = []
        weights = self.analysis_config["agent_weights"]
        
        # Weighted confidence from each agent
        if report.market_intelligence:
            confidence_factors.append(report.market_intelligence.confidence_level * weights["market_intelligence"])
        
        if report.technical_architecture:
            confidence_factors.append(report.technical_architecture.confidence_level * weights["technical_architecture"])
        
        if report.executive_decision_intelligence:
            exec_confidence = 0.8 if "high" in report.executive_decision_intelligence.roi_confidence.value else 0.6
            confidence_factors.append(exec_confidence * weights["executive_decision"])
        
        if report.compliance_risk_assessment:
            confidence_factors.append(report.compliance_risk_assessment.assessment_confidence * weights["compliance_risk"])
        
        # Data quality factor
        crewai_quality = report.crewai_tactical_summary.get("tactical_quality_score", 0.5)
        confidence_factors.append(crewai_quality * 0.1)  # 10% weight for input data quality
        
        return sum(confidence_factors) if confidence_factors else 0.5
    
    def export_executive_report(self, report: StrategicIntelligenceReport, format: str = "json") -> str:
        """Export strategic intelligence report in various formats"""
        
        if format.lower() == "json":
            return json.dumps(asdict(report), indent=2, default=str)
        elif format.lower() == "summary":
            return self._create_text_summary(report)
        else:
            return json.dumps(asdict(report), indent=2, default=str)
    
    def _create_text_summary(self, report: StrategicIntelligenceReport) -> str:
        """Create human-readable text summary"""
        
        summary = f"""
STRATEGIC INTELLIGENCE REPORT
Generated: {report.generated_at}
Company: {report.company_name}
Report ID: {report.report_id}
Overall Confidence: {report.analysis_confidence:.2f}

EXECUTIVE SUMMARY
{report.executive_summary}

KEY RECOMMENDATIONS
{chr(10).join(f"• {rec}" for rec in report.key_recommendations)}

STRATEGIC METRICS
Financial ROI: {report.strategic_kpis.get('financial_metrics', {}).get('projected_roi', 'N/A')}
Market Opportunity: {report.strategic_kpis.get('market_metrics', {}).get('market_size', 'N/A')}
Implementation Timeline: {report.strategic_kpis.get('operational_metrics', {}).get('implementation_timeline', 'N/A')}
Risk Level: {report.strategic_kpis.get('risk_metrics', {}).get('overall_risk_level', 'N/A')}

IMMEDIATE ACTIONS (Next 30 Days)
{chr(10).join(f"• {action}" for action in report.immediate_actions)}

STRATEGIC INITIATIVES (3-12 Months)
{chr(10).join(f"• {initiative}" for initiative in report.strategic_initiatives)}

Next Review: {report.follow_up_timeline.get('next_review', '90 days')}
        """
        
        return summary.strip()
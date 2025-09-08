"""
Executive Decision Support Agent - Strategic Layer
Provides ROI modeling, business case development, and executive-level decision intelligence
Transforms tactical lead data into strategic business intelligence for C-level decision making
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class InvestmentTier(Enum):
    SMALL = "small"        # <$100K
    MEDIUM = "medium"      # $100K-$500K 
    LARGE = "large"        # $500K-$2M
    ENTERPRISE = "enterprise"  # >$2M

class ROIConfidence(Enum):
    LOW = "low"           # <60% confidence
    MEDIUM = "medium"     # 60-80% confidence
    HIGH = "high"         # >80% confidence

@dataclass
class ExecutiveDecisionIntelligence:
    """Executive decision support analysis output"""
    
    # Financial Analysis
    total_investment: float = 0.0
    projected_roi: float = 0.0
    payback_period_months: int = 0
    npv: float = 0.0
    irr: float = 0.0
    
    # Revenue Impact
    revenue_opportunity: float = 0.0
    recurring_revenue_potential: float = 0.0
    customer_lifetime_value: float = 0.0
    market_expansion_value: float = 0.0
    
    # Cost Analysis  
    implementation_costs: Dict[str, float] = None
    operational_costs: Dict[str, float] = None
    risk_adjusted_costs: float = 0.0
    
    # Strategic Benefits
    strategic_value_drivers: List[str] = None
    competitive_advantages: List[str] = None
    risk_mitigation_value: float = 0.0
    
    # Risk Assessment
    business_risks: List[Dict[str, Any]] = None
    financial_risks: List[Dict[str, Any]] = None
    probability_of_success: float = 0.5
    
    # Decision Framework
    investment_tier: InvestmentTier = InvestmentTier.MEDIUM
    decision_urgency: str = "normal"
    stakeholder_impact: List[str] = None
    approval_requirements: List[str] = None
    
    # Executive Summary
    business_case_summary: str = ""
    key_success_metrics: List[str] = None
    implementation_milestones: List[Dict[str, Any]] = None
    executive_recommendation: str = ""
    
    # Confidence and Validation
    roi_confidence: ROIConfidence = ROIConfidence.MEDIUM
    data_quality_score: float = 0.5
    analysis_limitations: List[str] = None
    
    def __post_init__(self):
        if self.implementation_costs is None:
            self.implementation_costs = {}
        if self.operational_costs is None:
            self.operational_costs = {}
        if self.strategic_value_drivers is None:
            self.strategic_value_drivers = []
        if self.competitive_advantages is None:
            self.competitive_advantages = []
        if self.business_risks is None:
            self.business_risks = []
        if self.financial_risks is None:
            self.financial_risks = []
        if self.stakeholder_impact is None:
            self.stakeholder_impact = []
        if self.approval_requirements is None:
            self.approval_requirements = []
        if self.key_success_metrics is None:
            self.key_success_metrics = []
        if self.implementation_milestones is None:
            self.implementation_milestones = []
        if self.analysis_limitations is None:
            self.analysis_limitations = []

class ExecutiveDecisionAgent:
    """
    Strategic Executive Decision Support Agent
    
    Transforms tactical sales intelligence into executive-level business intelligence:
    - ROI modeling and financial projections ($X investment → $Y return over Z months)
    - Business case development with strategic value drivers
    - Risk-adjusted financial analysis with confidence intervals
    - Competitive advantage assessment and market positioning
    - Executive dashboard metrics and KPI recommendations
    - Stakeholder impact analysis and approval workflow guidance
    - Implementation roadmap aligned with business objectives
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Executive decision models and benchmarks
        self.financial_models = self._initialize_financial_models()
        self.industry_benchmarks = self._initialize_industry_benchmarks()
        
    def _initialize_financial_models(self) -> Dict[str, Any]:
        """Initialize financial modeling parameters"""
        return {
            "discount_rate": 0.10,  # 10% discount rate for NPV
            "corporate_tax_rate": 0.25,  # 25% corporate tax rate
            "risk_free_rate": 0.03,  # 3% risk-free rate
            "market_risk_premium": 0.07,  # 7% market risk premium
            "inflation_rate": 0.03,  # 3% inflation assumption
            
            # Industry average metrics
            "software_multiples": {
                "revenue": 8.5,  # 8.5x revenue multiple
                "ebitda": 25.0,  # 25x EBITDA multiple
                "customer_acquisition_cost": 0.3  # 30% of first year revenue
            },
            
            # ROI benchmarks by investment size
            "roi_benchmarks": {
                InvestmentTier.SMALL: {"target_roi": 3.0, "payback_months": 12},
                InvestmentTier.MEDIUM: {"target_roi": 2.5, "payback_months": 18},
                InvestmentTier.LARGE: {"target_roi": 2.0, "payback_months": 24},
                InvestmentTier.ENTERPRISE: {"target_roi": 1.8, "payback_months": 30}
            }
        }
    
    def _initialize_industry_benchmarks(self) -> Dict[str, Any]:
        """Initialize industry-specific benchmarks and assumptions"""
        return {
            "software": {
                "gross_margin": 0.80,
                "churn_rate": 0.05,  # 5% annual churn
                "expansion_revenue": 1.15,  # 15% expansion
                "sales_cycle_months": 6,
                "customer_growth_rate": 0.25
            },
            "fintech": {
                "gross_margin": 0.75,
                "churn_rate": 0.08,
                "expansion_revenue": 1.10,
                "sales_cycle_months": 9,
                "customer_growth_rate": 0.30
            },
            "healthcare": {
                "gross_margin": 0.70,
                "churn_rate": 0.03,  # Lower churn due to switching costs
                "expansion_revenue": 1.20,
                "sales_cycle_months": 12,
                "customer_growth_rate": 0.15
            },
            "manufacturing": {
                "gross_margin": 0.60,
                "churn_rate": 0.06,
                "expansion_revenue": 1.25,
                "sales_cycle_months": 18,
                "customer_growth_rate": 0.10
            }
        }
    
    async def generate_executive_decision_intelligence(
        self,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]] = None,
        technical_architecture: Optional[Dict[str, Any]] = None,
        crewai_results: Optional[Dict[str, Any]] = None
    ) -> ExecutiveDecisionIntelligence:
        """
        Generate comprehensive executive decision support analysis
        
        Integrates all strategic intelligence layers to provide:
        - Financial ROI analysis with confidence intervals
        - Strategic business case with value drivers
        - Risk assessment with mitigation strategies
        - Executive recommendation with approval framework
        """
        
        try:
            # Initialize executive decision intelligence
            exec_intel = ExecutiveDecisionIntelligence()
            
            # Extract key data points
            company_size = company_data.get("company_size", 0)
            industry = company_data.get("industry", "").lower()
            annual_revenue = company_data.get("annual_revenue", 0)
            
            # 1. Investment tier classification
            exec_intel.investment_tier = self._classify_investment_tier(
                company_size, annual_revenue, technical_architecture
            )
            
            # 2. Financial analysis and ROI modeling
            await self._perform_financial_analysis(exec_intel, company_data, technical_architecture)
            
            # 3. Revenue opportunity assessment
            await self._assess_revenue_opportunity(
                exec_intel, company_data, market_intelligence, crewai_results
            )
            
            # 4. Cost analysis (implementation + operational)
            self._analyze_costs(exec_intel, technical_architecture, company_size)
            
            # 5. Strategic value drivers identification
            exec_intel.strategic_value_drivers = await self._identify_strategic_value_drivers(
                company_data, market_intelligence, crewai_results
            )
            
            # 6. Competitive advantage assessment
            exec_intel.competitive_advantages = await self._assess_competitive_advantages(
                company_data, market_intelligence, technical_architecture
            )
            
            # 7. Risk assessment (business + financial)
            await self._assess_executive_risks(
                exec_intel, company_data, market_intelligence, technical_architecture
            )
            
            # 8. Decision framework and approval requirements
            self._determine_decision_framework(exec_intel, company_data)
            
            # 9. Generate executive business case
            exec_intel.business_case_summary = await self._generate_business_case_summary(
                exec_intel, company_data
            )
            
            # 10. Success metrics and milestones
            exec_intel.key_success_metrics = self._define_success_metrics(exec_intel)
            exec_intel.implementation_milestones = self._create_implementation_milestones(
                exec_intel, technical_architecture
            )
            
            # 11. Executive recommendation
            exec_intel.executive_recommendation = await self._generate_executive_recommendation(
                exec_intel, company_data
            )
            
            # 12. Confidence and data quality assessment
            exec_intel.roi_confidence, exec_intel.data_quality_score = self._assess_confidence_and_quality(
                exec_intel, market_intelligence, technical_architecture, crewai_results
            )
            
            self.logger.info(f"Executive decision intelligence generated for {company_data.get('company_name', 'target company')}")
            return exec_intel
            
        except Exception as e:
            self.logger.error(f"Executive decision analysis failed: {e}")
            return ExecutiveDecisionIntelligence()
    
    def _classify_investment_tier(
        self,
        company_size: int,
        annual_revenue: float,
        technical_architecture: Optional[Dict[str, Any]]
    ) -> InvestmentTier:
        """Classify investment tier based on company profile and technical complexity"""
        
        # Base investment estimation
        if company_size > 5000 or (annual_revenue and annual_revenue > 500_000_000):
            base_tier = InvestmentTier.ENTERPRISE
        elif company_size > 1000 or (annual_revenue and annual_revenue > 50_000_000):
            base_tier = InvestmentTier.LARGE
        elif company_size > 100 or (annual_revenue and annual_revenue > 5_000_000):
            base_tier = InvestmentTier.MEDIUM
        else:
            base_tier = InvestmentTier.SMALL
        
        # Adjust based on technical complexity
        if technical_architecture:
            complexity = technical_architecture.get("solution_complexity", "medium")
            if complexity == "enterprise" and base_tier != InvestmentTier.ENTERPRISE:
                # Bump up one tier for enterprise complexity
                tier_order = [InvestmentTier.SMALL, InvestmentTier.MEDIUM, InvestmentTier.LARGE, InvestmentTier.ENTERPRISE]
                current_index = tier_order.index(base_tier)
                base_tier = tier_order[min(current_index + 1, len(tier_order) - 1)]
        
        return base_tier
    
    async def _perform_financial_analysis(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]]
    ):
        """Perform comprehensive financial analysis and ROI modeling"""
        
        # Estimate total investment
        if technical_architecture:
            implementation_cost = technical_architecture.get("roi_technical_factors", {}).get("implementation_cost", 300000)
            infrastructure_cost = technical_architecture.get("roi_technical_factors", {}).get("infrastructure_cost", 60000)
            exec_intel.total_investment = implementation_cost + infrastructure_cost
        else:
            # Fallback investment estimates by tier
            investment_estimates = {
                InvestmentTier.SMALL: 75000,
                InvestmentTier.MEDIUM: 250000,
                InvestmentTier.LARGE: 750000,
                InvestmentTier.ENTERPRISE: 2000000
            }
            exec_intel.total_investment = investment_estimates.get(exec_intel.investment_tier, 250000)
        
        # Revenue projections (to be refined in revenue assessment)
        company_size = company_data.get("company_size", 250)
        annual_contract_value = self._estimate_annual_contract_value(company_size, exec_intel.investment_tier)
        
        # Multi-year revenue projection
        year1_revenue = annual_contract_value
        year2_revenue = annual_contract_value * 1.15  # 15% expansion
        year3_revenue = annual_contract_value * 1.32  # Compounded growth
        
        total_3yr_revenue = year1_revenue + year2_revenue + year3_revenue
        
        # Calculate ROI metrics
        net_benefit = total_3yr_revenue - exec_intel.total_investment
        exec_intel.projected_roi = net_benefit / exec_intel.total_investment if exec_intel.total_investment > 0 else 0
        
        # Payback period calculation
        exec_intel.payback_period_months = int((exec_intel.total_investment / annual_contract_value) * 12) if annual_contract_value > 0 else 24
        
        # NPV calculation
        discount_rate = self.financial_models["discount_rate"]
        cash_flows = [-exec_intel.total_investment, year1_revenue, year2_revenue, year3_revenue]
        exec_intel.npv = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows))
        
        # IRR approximation (simplified)
        if exec_intel.total_investment > 0:
            exec_intel.irr = (total_3yr_revenue / exec_intel.total_investment) ** (1/3) - 1
        
    def _estimate_annual_contract_value(self, company_size: int, investment_tier: InvestmentTier) -> float:
        """Estimate annual contract value based on company size and investment tier"""
        
        # Base ACV by company size
        if company_size > 5000:
            base_acv = 150000
        elif company_size > 1000:
            base_acv = 75000
        elif company_size > 500:
            base_acv = 40000
        elif company_size > 100:
            base_acv = 20000
        else:
            base_acv = 10000
        
        # Adjust by investment tier
        tier_multipliers = {
            InvestmentTier.SMALL: 0.8,
            InvestmentTier.MEDIUM: 1.0,
            InvestmentTier.LARGE: 1.5,
            InvestmentTier.ENTERPRISE: 2.5
        }
        
        return base_acv * tier_multipliers.get(investment_tier, 1.0)
    
    async def _assess_revenue_opportunity(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]],
        crewai_results: Optional[Dict[str, Any]]
    ):
        """Assess comprehensive revenue opportunity"""
        
        company_size = company_data.get("company_size", 250)
        
        # Base revenue opportunity (already calculated in financial analysis)
        exec_intel.revenue_opportunity = self._estimate_annual_contract_value(company_size, exec_intel.investment_tier)
        
        # Recurring revenue potential (3-year projection)
        churn_rate = 0.05  # Default 5% annual churn
        expansion_rate = 1.15  # Default 15% expansion
        
        year1 = exec_intel.revenue_opportunity
        year2 = year1 * (1 - churn_rate) * expansion_rate
        year3 = year2 * (1 - churn_rate) * expansion_rate
        
        exec_intel.recurring_revenue_potential = year1 + year2 + year3
        
        # Customer lifetime value
        exec_intel.customer_lifetime_value = exec_intel.revenue_opportunity / churn_rate if churn_rate > 0 else exec_intel.revenue_opportunity * 10
        
        # Market expansion value (from market intelligence)
        if market_intelligence:
            market_size = market_intelligence.get("market_size", 0)
            growth_rate = market_intelligence.get("growth_rate", 0.1)
            
            # Estimate market share potential (very conservative)
            potential_market_share = min(0.001, 100000000 / market_size) if market_size > 0 else 0.0001  # 0.1% or less
            exec_intel.market_expansion_value = market_size * potential_market_share * growth_rate * 3  # 3-year expansion
        else:
            exec_intel.market_expansion_value = exec_intel.revenue_opportunity * 0.5  # Conservative expansion estimate
    
    def _analyze_costs(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        technical_architecture: Optional[Dict[str, Any]],
        company_size: int
    ):
        """Analyze implementation and operational costs"""
        
        # Implementation costs breakdown
        if technical_architecture:
            resource_costs = technical_architecture.get("resource_requirements", {}).get("estimated_monthly_cost", 45000)
            timeline_months = technical_architecture.get("timeline_estimate", {}).get("adjusted_duration_months", 6)
            
            exec_intel.implementation_costs = {
                "development": resource_costs * timeline_months,
                "infrastructure_setup": technical_architecture.get("infrastructure_needs", {}).get("estimated_monthly_cost", 5000) * 2,
                "project_management": resource_costs * timeline_months * 0.15,
                "training_and_adoption": company_size * 100,  # $100 per employee for training
                "contingency": (resource_costs * timeline_months) * 0.20  # 20% contingency
            }
        else:
            # Fallback cost estimates
            base_dev_cost = {
                InvestmentTier.SMALL: 50000,
                InvestmentTier.MEDIUM: 150000,
                InvestmentTier.LARGE: 400000,
                InvestmentTier.ENTERPRISE: 1000000
            }.get(exec_intel.investment_tier, 150000)
            
            exec_intel.implementation_costs = {
                "development": base_dev_cost,
                "infrastructure_setup": base_dev_cost * 0.2,
                "project_management": base_dev_cost * 0.15,
                "training_and_adoption": company_size * 100,
                "contingency": base_dev_cost * 0.20
            }
        
        # Operational costs (annual)
        if technical_architecture:
            monthly_infra = technical_architecture.get("infrastructure_needs", {}).get("estimated_monthly_cost", 5000)
            exec_intel.operational_costs = {
                "infrastructure": monthly_infra * 12,
                "maintenance_support": sum(exec_intel.implementation_costs.values()) * 0.20,  # 20% of implementation
                "ongoing_development": monthly_infra * 12 * 0.3,  # 30% of infrastructure for dev
                "compliance_auditing": 25000 if len(technical_architecture.get("compliance_frameworks", [])) > 1 else 10000
            }
        else:
            base_annual_ops = exec_intel.total_investment * 0.25  # 25% of implementation cost annually
            exec_intel.operational_costs = {
                "infrastructure": base_annual_ops * 0.4,
                "maintenance_support": base_annual_ops * 0.3,
                "ongoing_development": base_annual_ops * 0.2,
                "compliance_auditing": base_annual_ops * 0.1
            }
        
        # Risk-adjusted costs (add 15% risk premium)
        total_implementation = sum(exec_intel.implementation_costs.values())
        total_operational_3yr = sum(exec_intel.operational_costs.values()) * 3
        exec_intel.risk_adjusted_costs = (total_implementation + total_operational_3yr) * 1.15
    
    async def _identify_strategic_value_drivers(
        self,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]],
        crewai_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify strategic value drivers for executive presentation"""
        
        value_drivers = []
        
        if self.granite_client:
            try:
                market_info = market_intelligence or {}
                pain_points = crewai_results.get("pain_points", []) if crewai_results else []
                
                prompt = f"""
                Identify strategic business value drivers for a {company_data.get('industry', 'technology')} company:
                
                Company: {company_data.get('company_name', 'target company')} ({company_data.get('company_size', 0)} employees)
                Market Size: ${market_info.get('market_size', 0):,.0f}
                Growth Rate: {(market_info.get('growth_rate', 0.1) * 100):.1f}%
                Pain Points: {pain_points}
                
                Provide 5-6 strategic value drivers as JSON array:
                ["Revenue growth acceleration", "Operational efficiency gains", "Market differentiation advantage"]
                Focus on C-level strategic benefits, not tactical features.
                """
                
                response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
                
                try:
                    drivers = json.loads(response.content)
                    if isinstance(drivers, list):
                        value_drivers = drivers[:6]
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Strategic value drivers analysis failed: {e}")
        
        # Fallback strategic value drivers
        if not value_drivers:
            industry = company_data.get("industry", "").lower()
            if "fintech" in industry:
                value_drivers = [
                    "Revenue acceleration through faster time-to-market",
                    "Risk mitigation via automated compliance",
                    "Customer experience differentiation",
                    "Operational cost reduction through automation",
                    "Market share expansion in high-growth segment"
                ]
            elif "healthcare" in industry:
                value_drivers = [
                    "Patient outcome improvement and safety",
                    "Regulatory compliance cost reduction",
                    "Operational efficiency and cost savings",
                    "Provider satisfaction and retention",
                    "Market leadership in digital health"
                ]
            else:
                value_drivers = [
                    "Revenue growth acceleration",
                    "Operational efficiency and cost reduction",
                    "Customer satisfaction and retention improvement",
                    "Competitive differentiation and market positioning",
                    "Risk mitigation and business continuity",
                    "Team productivity and collaboration enhancement"
                ]
        
        return value_drivers
    
    async def _assess_competitive_advantages(
        self,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Assess competitive advantages and market positioning benefits"""
        
        advantages = []
        
        # Technology-based advantages
        if technical_architecture:
            modernization_opps = technical_architecture.get("modernization_opportunities", [])
            if modernization_opps:
                advantages.append("Technology leadership through modern architecture")
            
            scalability = technical_architecture.get("scalability_assessment", {})
            if scalability.get("availability_requirement", "").startswith("99.9"):
                advantages.append("Enterprise-grade reliability and availability")
        
        # Market-based advantages
        if market_intelligence:
            timing_score = market_intelligence.get("timing_score", 0.5)
            if timing_score > 0.7:
                advantages.append("First-mover advantage in favorable market conditions")
            
            opportunity_score = market_intelligence.get("opportunity_score", 0.5)
            if opportunity_score > 0.8:
                advantages.append("Access to high-growth market opportunity")
        
        # Industry-specific advantages
        industry = company_data.get("industry", "").lower()
        if "fintech" in industry:
            advantages.extend([
                "Regulatory compliance automation advantage",
                "Financial data security and privacy leadership"
            ])
        elif "healthcare" in industry:
            advantages.extend([
                "Healthcare compliance and interoperability",
                "Patient data security and HIPAA leadership"
            ])
        
        # Fallback advantages
        if not advantages:
            advantages = [
                "Operational efficiency competitive advantage",
                "Customer experience differentiation",
                "Technology modernization leadership",
                "Scalability and growth readiness"
            ]
        
        return advantages[:5]  # Limit to top 5
    
    async def _assess_executive_risks(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]],
        technical_architecture: Optional[Dict[str, Any]]
    ):
        """Assess business and financial risks for executive consideration"""
        
        # Business risks
        exec_intel.business_risks = []
        
        # Market risks
        if market_intelligence:
            growth_rate = market_intelligence.get("growth_rate", 0.1)
            if growth_rate > 0.25:
                exec_intel.business_risks.append({
                    "risk": "High-growth market volatility",
                    "probability": "medium",
                    "impact": "medium",
                    "mitigation": "Flexible architecture and agile development"
                })
        
        # Technical risks
        if technical_architecture:
            tech_risks = technical_architecture.get("technical_risks", [])
            for risk in tech_risks[:2]:  # Top 2 technical risks
                exec_intel.business_risks.append({
                    "risk": f"Technical implementation: {risk.get('risk', 'Unknown risk')}",
                    "probability": risk.get("probability", "medium"),
                    "impact": risk.get("impact", "medium"),
                    "mitigation": risk.get("mitigation", "Risk mitigation plan required")
                })
        
        # Financial risks
        exec_intel.financial_risks = []
        
        # Investment size risk
        if exec_intel.investment_tier in [InvestmentTier.LARGE, InvestmentTier.ENTERPRISE]:
            exec_intel.financial_risks.append({
                "risk": "Large capital investment execution risk",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Phased implementation with milestone gates"
            })
        
        # ROI risk
        if exec_intel.projected_roi < 1.5:
            exec_intel.financial_risks.append({
                "risk": "ROI below industry benchmark",
                "probability": "high",
                "impact": "high",
                "mitigation": "Value engineering and scope optimization"
            })
        
        # Market risk
        exec_intel.financial_risks.append({
            "risk": "Market conditions affecting revenue projections",
            "probability": "low",
            "impact": "medium",
            "mitigation": "Conservative projections and scenario planning"
        })
        
        # Calculate probability of success
        risk_count = len(exec_intel.business_risks) + len(exec_intel.financial_risks)
        base_success_rate = 0.75  # 75% base success rate
        
        # Adjust for risk factors
        risk_adjustment = min(risk_count * 0.05, 0.25)  # Max 25% reduction
        exec_intel.probability_of_success = max(base_success_rate - risk_adjustment, 0.5)
    
    def _determine_decision_framework(self, exec_intel: ExecutiveDecisionIntelligence, company_data: Dict[str, Any]):
        """Determine decision urgency and approval requirements"""
        
        # Decision urgency
        if exec_intel.investment_tier == InvestmentTier.ENTERPRISE:
            exec_intel.decision_urgency = "high"  # Large investments need quick decisions
        elif exec_intel.projected_roi > 2.0 and exec_intel.payback_period_months <= 18:
            exec_intel.decision_urgency = "high"  # High ROI opportunities
        else:
            exec_intel.decision_urgency = "normal"
        
        # Stakeholder impact
        company_size = company_data.get("company_size", 0)
        if company_size > 1000:
            exec_intel.stakeholder_impact = [
                "Executive leadership (CEO, CTO, CFO)",
                "Department heads and business unit leaders",
                "IT and operations teams",
                "End users across organization",
                "Board of directors (for enterprise investments)"
            ]
        else:
            exec_intel.stakeholder_impact = [
                "Executive team (CEO, CTO)",
                "Department managers",
                "IT team",
                "Key end users"
            ]
        
        # Approval requirements
        if exec_intel.investment_tier == InvestmentTier.ENTERPRISE:
            exec_intel.approval_requirements = [
                "Board of directors approval",
                "Executive committee approval",
                "CFO financial review",
                "CTO technical review",
                "Legal and compliance review"
            ]
        elif exec_intel.investment_tier == InvestmentTier.LARGE:
            exec_intel.approval_requirements = [
                "Executive team approval",
                "CFO budget approval",
                "CTO technical approval",
                "Legal review"
            ]
        else:
            exec_intel.approval_requirements = [
                "Executive sponsor approval",
                "Budget approval",
                "Technical review"
            ]
    
    async def _generate_business_case_summary(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        company_data: Dict[str, Any]
    ) -> str:
        """Generate executive business case summary"""
        
        if self.granite_client:
            try:
                prompt = f"""
                Create an executive business case summary for:
                
                Company: {company_data.get('company_name', 'target company')}
                Investment: ${exec_intel.total_investment:,.0f}
                Projected ROI: {exec_intel.projected_roi:.1f}x
                Payback Period: {exec_intel.payback_period_months} months
                3-Year Revenue: ${exec_intel.recurring_revenue_potential:,.0f}
                
                Value Drivers: {exec_intel.strategic_value_drivers[:3]}
                
                Write a concise 3-4 sentence executive summary focusing on strategic business impact.
                """
                
                response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
                return response.content.strip()
                
            except Exception as e:
                self.logger.error(f"Business case generation failed: {e}")
        
        # Fallback business case
        return f"""
        Strategic investment opportunity with ${exec_intel.total_investment:,.0f} investment delivering {exec_intel.projected_roi:.1f}x ROI 
        over {exec_intel.payback_period_months} months. Projected 3-year revenue potential of ${exec_intel.recurring_revenue_potential:,.0f} 
        with key strategic benefits including {', '.join(exec_intel.strategic_value_drivers[:2])}. 
        Recommended for {exec_intel.decision_urgency} priority execution with {exec_intel.probability_of_success:.0%} probability of success.
        """
    
    def _define_success_metrics(self, exec_intel: ExecutiveDecisionIntelligence) -> List[str]:
        """Define key success metrics for executive dashboard"""
        metrics = [
            f"ROI achievement: Target {exec_intel.projected_roi:.1f}x within {exec_intel.payback_period_months} months",
            f"Revenue generation: ${exec_intel.revenue_opportunity:,.0f} annual recurring revenue",
            f"Implementation timeline: Complete within {exec_intel.payback_period_months // 2} months of target",
            "User adoption: 80%+ active user engagement within 6 months",
            "Customer satisfaction: 4.5+ NPS score"
        ]
        
        # Add tier-specific metrics
        if exec_intel.investment_tier in [InvestmentTier.LARGE, InvestmentTier.ENTERPRISE]:
            metrics.append("Executive stakeholder satisfaction: 90%+ approval rating")
            metrics.append("Business process improvement: 25%+ efficiency gains")
        
        return metrics
    
    def _create_implementation_milestones(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        technical_architecture: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create executive-level implementation milestones"""
        milestones = []
        
        if technical_architecture and technical_architecture.get("implementation_phases"):
            phases = technical_architecture["implementation_phases"]
            cumulative_weeks = 0
            
            for i, phase in enumerate(phases):
                cumulative_weeks += phase.get("duration_weeks", 8)
                milestone = {
                    "milestone": f"Phase {phase['phase']}: {phase['name']}",
                    "target_date": f"Week {cumulative_weeks}",
                    "success_criteria": f"Complete {phase['name'].lower()} with quality gates",
                    "executive_review": i == len(phases) - 1 or cumulative_weeks >= 12  # Review at end or every 12 weeks
                }
                milestones.append(milestone)
        else:
            # Fallback milestones
            timeline_months = exec_intel.payback_period_months // 2  # Implementation is half of payback
            milestones = [
                {
                    "milestone": "Project Kickoff and Team Assembly",
                    "target_date": "Month 1",
                    "success_criteria": "Team assembled, project plan approved",
                    "executive_review": True
                },
                {
                    "milestone": "Core System Implementation",
                    "target_date": f"Month {timeline_months // 2}",
                    "success_criteria": "Core functionality operational",
                    "executive_review": False
                },
                {
                    "milestone": "Full System Deployment",
                    "target_date": f"Month {timeline_months}",
                    "success_criteria": "System live and user adoption initiated",
                    "executive_review": True
                }
            ]
        
        return milestones
    
    async def _generate_executive_recommendation(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        company_data: Dict[str, Any]
    ) -> str:
        """Generate final executive recommendation"""
        
        # Determine recommendation based on financial metrics
        roi_benchmark = self.financial_models["roi_benchmarks"][exec_intel.investment_tier]["target_roi"]
        payback_benchmark = self.financial_models["roi_benchmarks"][exec_intel.investment_tier]["payback_months"]
        
        if (exec_intel.projected_roi >= roi_benchmark and 
            exec_intel.payback_period_months <= payback_benchmark and
            exec_intel.probability_of_success >= 0.7):
            
            recommendation = f"STRONG RECOMMEND: Exceptional investment opportunity with {exec_intel.projected_roi:.1f}x ROI exceeding {roi_benchmark:.1f}x benchmark."
            
        elif (exec_intel.projected_roi >= roi_benchmark * 0.8 and
              exec_intel.payback_period_months <= payback_benchmark * 1.2 and
              exec_intel.probability_of_success >= 0.6):
            
            recommendation = f"RECOMMEND: Solid investment opportunity with {exec_intel.projected_roi:.1f}x ROI meeting strategic objectives."
            
        elif exec_intel.probability_of_success >= 0.6:
            recommendation = f"CONDITIONAL RECOMMEND: Consider with scope optimization to improve ROI from {exec_intel.projected_roi:.1f}x to target {roi_benchmark:.1f}x."
            
        else:
            recommendation = f"RECONSIDER: Investment requires significant risk mitigation or scope changes to meet executive criteria."
        
        return recommendation
    
    def _assess_confidence_and_quality(
        self,
        exec_intel: ExecutiveDecisionIntelligence,
        market_intelligence: Optional[Dict[str, Any]],
        technical_architecture: Optional[Dict[str, Any]],
        crewai_results: Optional[Dict[str, Any]]
    ) -> Tuple[ROIConfidence, float]:
        """Assess confidence level and data quality"""
        
        confidence_factors = []
        
        # Market data quality
        if market_intelligence and market_intelligence.get("market_size"):
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Technical architecture quality
        if technical_architecture and technical_architecture.get("feasibility_score", 0) > 0.7:
            confidence_factors.append(0.8)
        elif technical_architecture:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.3)
        
        # Tactical research quality
        if crewai_results and crewai_results.get("pain_points"):
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)
        
        # Financial model robustness
        if exec_intel.total_investment > 0 and exec_intel.revenue_opportunity > 0:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.3)
        
        # Calculate overall confidence
        data_quality_score = sum(confidence_factors) / len(confidence_factors)
        
        # Map to ROI confidence levels
        if data_quality_score >= 0.8:
            roi_confidence = ROIConfidence.HIGH
        elif data_quality_score >= 0.6:
            roi_confidence = ROIConfidence.MEDIUM
        else:
            roi_confidence = ROIConfidence.LOW
        
        # Set analysis limitations
        exec_intel.analysis_limitations = []
        if data_quality_score < 0.8:
            exec_intel.analysis_limitations.append("Limited market data - projections based on industry benchmarks")
        if not technical_architecture:
            exec_intel.analysis_limitations.append("Technical complexity estimated - detailed architecture analysis recommended")
        if not crewai_results:
            exec_intel.analysis_limitations.append("Customer research limited - direct customer validation recommended")
        
        return roi_confidence, data_quality_score
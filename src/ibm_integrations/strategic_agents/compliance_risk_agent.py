"""
Compliance & Risk Agent - Strategic Layer
Provides regulatory compliance assessment, enterprise risk analysis, and governance frameworks
Complements tactical implementation with strategic risk management and compliance intelligence
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"           # Minimal risk, standard mitigation
    MEDIUM = "medium"     # Moderate risk, enhanced controls needed
    HIGH = "high"         # Significant risk, executive attention required
    CRITICAL = "critical" # Severe risk, immediate action required

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"         # Meets all requirements
    PARTIALLY_COMPLIANT = "partial" # Some gaps, plan required
    NON_COMPLIANT = "non_compliant" # Significant gaps, major effort
    NOT_APPLICABLE = "n/a"          # Framework not applicable

@dataclass 
class ComplianceRiskAssessment:
    """Comprehensive compliance and risk assessment output"""
    
    # Regulatory Compliance Analysis
    applicable_regulations: List[Dict[str, Any]] = None
    compliance_gaps: List[Dict[str, Any]] = None
    compliance_readiness_score: float = 0.5
    regulatory_timeline: Dict[str, Any] = None
    compliance_costs: Dict[str, float] = None
    
    # Enterprise Risk Assessment
    business_risks: List[Dict[str, Any]] = None
    operational_risks: List[Dict[str, Any]] = None
    technology_risks: List[Dict[str, Any]] = None
    financial_risks: List[Dict[str, Any]] = None
    reputational_risks: List[Dict[str, Any]] = None
    
    # Risk Metrics
    overall_risk_level: RiskLevel = RiskLevel.MEDIUM
    risk_score: float = 0.5  # 0-1 scale
    probability_risk_materialization: float = 0.3
    potential_financial_impact: float = 0.0
    
    # Governance and Controls
    required_governance_frameworks: List[str] = None
    security_controls: List[Dict[str, Any]] = None
    audit_requirements: List[str] = None
    monitoring_controls: List[str] = None
    
    # Mitigation Strategies
    risk_mitigation_plan: List[Dict[str, Any]] = None
    compliance_roadmap: List[Dict[str, Any]] = None
    governance_recommendations: List[str] = None
    
    # Executive Risk Intelligence
    board_reporting_requirements: List[str] = None
    insurance_considerations: List[str] = None
    legal_review_requirements: List[str] = None
    third_party_risk_factors: List[str] = None
    
    # Assessment Metadata
    assessment_confidence: float = 0.5
    last_updated: datetime = None
    next_review_date: datetime = None
    assessment_limitations: List[str] = None
    
    def __post_init__(self):
        if self.applicable_regulations is None:
            self.applicable_regulations = []
        if self.compliance_gaps is None:
            self.compliance_gaps = []
        if self.regulatory_timeline is None:
            self.regulatory_timeline = {}
        if self.compliance_costs is None:
            self.compliance_costs = {}
        if self.business_risks is None:
            self.business_risks = []
        if self.operational_risks is None:
            self.operational_risks = []
        if self.technology_risks is None:
            self.technology_risks = []
        if self.financial_risks is None:
            self.financial_risks = []
        if self.reputational_risks is None:
            self.reputational_risks = []
        if self.required_governance_frameworks is None:
            self.required_governance_frameworks = []
        if self.security_controls is None:
            self.security_controls = []
        if self.audit_requirements is None:
            self.audit_requirements = []
        if self.monitoring_controls is None:
            self.monitoring_controls = []
        if self.risk_mitigation_plan is None:
            self.risk_mitigation_plan = []
        if self.compliance_roadmap is None:
            self.compliance_roadmap = []
        if self.governance_recommendations is None:
            self.governance_recommendations = []
        if self.board_reporting_requirements is None:
            self.board_reporting_requirements = []
        if self.insurance_considerations is None:
            self.insurance_considerations = []
        if self.legal_review_requirements is None:
            self.legal_review_requirements = []
        if self.third_party_risk_factors is None:
            self.third_party_risk_factors = []
        if self.assessment_limitations is None:
            self.assessment_limitations = []
        if self.last_updated is None:
            self.last_updated = datetime.now()
        if self.next_review_date is None:
            self.next_review_date = datetime.now() + timedelta(days=90)

class ComplianceRiskAgent:
    """
    Strategic Compliance & Risk Assessment Agent
    
    Provides enterprise-grade compliance and risk intelligence:
    - Regulatory compliance gap analysis and roadmaps
    - Multi-dimensional enterprise risk assessment
    - Governance framework recommendations
    - Risk mitigation strategies and controls
    - Board-level risk reporting and oversight requirements
    - Legal and insurance considerations
    - Third-party and vendor risk assessment
    - Audit and monitoring framework design
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Compliance and risk knowledge bases
        self.regulatory_frameworks = self._initialize_regulatory_frameworks()
        self.risk_assessment_models = self._initialize_risk_models()
        self.governance_frameworks = self._initialize_governance_frameworks()
        
    def _initialize_regulatory_frameworks(self) -> Dict[str, Any]:
        """Initialize regulatory compliance frameworks database"""
        return {
            "GDPR": {
                "full_name": "General Data Protection Regulation",
                "jurisdiction": ["EU", "Global"],
                "applicability": "Companies processing EU personal data",
                "key_requirements": [
                    "Consent management", "Data portability", "Right to erasure",
                    "Privacy by design", "Data protection impact assessments"
                ],
                "penalties": "Up to 4% of annual revenue or €20M",
                "implementation_timeline": "6-12 months",
                "compliance_cost_range": [50000, 500000],
                "risk_level": RiskLevel.HIGH
            },
            "SOC2": {
                "full_name": "Service Organization Control 2",
                "jurisdiction": ["US", "Global"],
                "applicability": "Service providers handling customer data",
                "key_requirements": [
                    "Security controls", "Availability controls", "Processing integrity",
                    "Confidentiality", "Privacy controls"
                ],
                "penalties": "Customer contract violations, reputational damage",
                "implementation_timeline": "6-12 months",
                "compliance_cost_range": [75000, 300000],
                "risk_level": RiskLevel.MEDIUM
            },
            "HIPAA": {
                "full_name": "Health Insurance Portability and Accountability Act",
                "jurisdiction": ["US"],
                "applicability": "Healthcare and healthcare technology companies",
                "key_requirements": [
                    "Administrative safeguards", "Physical safeguards", "Technical safeguards",
                    "Business associate agreements", "Breach notification"
                ],
                "penalties": "$100-$50,000 per violation, up to $1.5M per incident",
                "implementation_timeline": "9-18 months",
                "compliance_cost_range": [100000, 750000],
                "risk_level": RiskLevel.HIGH
            },
            "PCI_DSS": {
                "full_name": "Payment Card Industry Data Security Standard",
                "jurisdiction": ["Global"],
                "applicability": "Companies handling credit card data",
                "key_requirements": [
                    "Network security", "Cardholder data protection", "Vulnerability management",
                    "Access controls", "Monitoring and testing"
                ],
                "penalties": "Fines from $5,000-$100,000 per month",
                "implementation_timeline": "6-15 months",
                "compliance_cost_range": [80000, 400000],
                "risk_level": RiskLevel.HIGH
            },
            "ISO27001": {
                "full_name": "Information Security Management System",
                "jurisdiction": ["Global"],
                "applicability": "Organizations seeking security certification",
                "key_requirements": [
                    "Information security policy", "Risk assessment", "Security controls",
                    "Management review", "Continuous improvement"
                ],
                "penalties": "Certification loss, customer contract issues",
                "implementation_timeline": "12-18 months", 
                "compliance_cost_range": [150000, 500000],
                "risk_level": RiskLevel.MEDIUM
            },
            "CCPA": {
                "full_name": "California Consumer Privacy Act",
                "jurisdiction": ["California", "US"],
                "applicability": "Companies with California consumers",
                "key_requirements": [
                    "Consumer rights notices", "Opt-out mechanisms", "Data inventory",
                    "Third-party disclosure", "Non-discrimination"
                ],
                "penalties": "$2,500-$7,500 per violation",
                "implementation_timeline": "4-8 months",
                "compliance_cost_range": [30000, 200000],
                "risk_level": RiskLevel.MEDIUM
            }
        }
    
    def _initialize_risk_models(self) -> Dict[str, Any]:
        """Initialize enterprise risk assessment models"""
        return {
            "business_risk_factors": [
                {"factor": "Market volatility", "weight": 0.15},
                {"factor": "Competitive displacement", "weight": 0.20},
                {"factor": "Customer concentration", "weight": 0.10},
                {"factor": "Regulatory changes", "weight": 0.25},
                {"factor": "Economic downturn", "weight": 0.15},
                {"factor": "Supply chain disruption", "weight": 0.15}
            ],
            "operational_risk_factors": [
                {"factor": "System downtime", "weight": 0.25},
                {"factor": "Data breach", "weight": 0.30},
                {"factor": "Key person dependency", "weight": 0.15},
                {"factor": "Process failures", "weight": 0.15},
                {"factor": "Vendor dependencies", "weight": 0.15}
            ],
            "financial_risk_thresholds": {
                "low": 100000,      # <$100K potential loss
                "medium": 1000000,  # $100K-$1M potential loss
                "high": 10000000,   # $1M-$10M potential loss
                "critical": 10000000 # >$10M potential loss
            }
        }
    
    def _initialize_governance_frameworks(self) -> Dict[str, Any]:
        """Initialize governance framework templates"""
        return {
            "COSO": {
                "name": "Committee of Sponsoring Organizations",
                "focus": "Internal controls and enterprise risk management",
                "components": ["Control environment", "Risk assessment", "Control activities", "Information & communication", "Monitoring"]
            },
            "COBIT": {
                "name": "Control Objectives for Information and Related Technologies",
                "focus": "IT governance and management",
                "components": ["Governance framework", "Management framework", "Process model", "Capability assessment"]
            },
            "NIST": {
                "name": "National Institute of Standards and Technology",
                "focus": "Cybersecurity framework",
                "components": ["Identify", "Protect", "Detect", "Respond", "Recover"]
            }
        }
    
    async def assess_compliance_and_risk(
        self,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]] = None,
        market_intelligence: Optional[Dict[str, Any]] = None,
        executive_intelligence: Optional[Dict[str, Any]] = None
    ) -> ComplianceRiskAssessment:
        """
        Perform comprehensive compliance and risk assessment
        
        Integrates with other strategic intelligence to provide:
        - Regulatory compliance gap analysis
        - Enterprise risk assessment across all dimensions
        - Governance framework recommendations
        - Risk mitigation and compliance roadmap
        """
        
        try:
            # Initialize assessment
            assessment = ComplianceRiskAssessment()
            
            # Extract key data points
            industry = company_data.get("industry", "").lower()
            company_size = company_data.get("company_size", 0)
            location = company_data.get("location", "")
            annual_revenue = company_data.get("annual_revenue", 0)
            
            # 1. Identify applicable regulations
            assessment.applicable_regulations = self._identify_applicable_regulations(
                industry, location, company_size, annual_revenue
            )
            
            # 2. Assess compliance readiness and gaps
            assessment.compliance_gaps, assessment.compliance_readiness_score = await self._assess_compliance_readiness(
                assessment.applicable_regulations, company_data, technical_architecture
            )
            
            # 3. Develop regulatory timeline and costs
            assessment.regulatory_timeline = self._develop_regulatory_timeline(assessment.applicable_regulations)
            assessment.compliance_costs = self._estimate_compliance_costs(
                assessment.applicable_regulations, company_size
            )
            
            # 4. Comprehensive risk assessment
            await self._perform_risk_assessment(
                assessment, company_data, technical_architecture, market_intelligence, executive_intelligence
            )
            
            # 5. Governance framework recommendations
            assessment.required_governance_frameworks = self._recommend_governance_frameworks(
                company_size, industry, assessment.applicable_regulations
            )
            
            # 6. Security controls and audit requirements
            assessment.security_controls = await self._define_security_controls(
                assessment.applicable_regulations, technical_architecture
            )
            assessment.audit_requirements = self._determine_audit_requirements(assessment.applicable_regulations)
            assessment.monitoring_controls = self._design_monitoring_controls(assessment)
            
            # 7. Risk mitigation planning
            assessment.risk_mitigation_plan = await self._develop_risk_mitigation_plan(assessment)
            assessment.compliance_roadmap = self._create_compliance_roadmap(assessment)
            
            # 8. Executive and board intelligence
            assessment.board_reporting_requirements = self._determine_board_reporting(
                assessment, company_size
            )
            assessment.insurance_considerations = self._assess_insurance_needs(assessment)
            assessment.legal_review_requirements = self._determine_legal_reviews(assessment)
            assessment.third_party_risk_factors = await self._assess_third_party_risks(
                company_data, technical_architecture
            )
            
            # 9. Final risk scoring and recommendations
            assessment.overall_risk_level, assessment.risk_score = self._calculate_overall_risk(assessment)
            assessment.governance_recommendations = await self._generate_governance_recommendations(assessment)
            
            # 10. Assessment confidence and limitations
            assessment.assessment_confidence = self._calculate_assessment_confidence(
                assessment, technical_architecture, market_intelligence
            )
            assessment.assessment_limitations = self._identify_assessment_limitations(
                company_data, technical_architecture
            )
            
            self.logger.info(f"Compliance and risk assessment completed for {industry} industry")
            return assessment
            
        except Exception as e:
            self.logger.error(f"Compliance and risk assessment failed: {e}")
            return ComplianceRiskAssessment()
    
    def _identify_applicable_regulations(
        self,
        industry: str,
        location: str,
        company_size: int,
        annual_revenue: float
    ) -> List[Dict[str, Any]]:
        """Identify applicable regulatory frameworks based on company profile"""
        
        applicable = []
        
        for framework_id, framework in self.regulatory_frameworks.items():
            is_applicable = False
            applicability_reason = []
            
            # Geographic applicability
            if "Global" in framework["jurisdiction"]:
                is_applicable = True
                applicability_reason.append("Global framework")
            elif "US" in framework["jurisdiction"] and ("us" in location.lower() or "usa" in location.lower() or "united states" in location.lower()):
                is_applicable = True
                applicability_reason.append("US jurisdiction")
            elif "EU" in framework["jurisdiction"] and any(country in location.lower() for country in ["eu", "europe", "germany", "france", "uk", "spain", "italy"]):
                is_applicable = True
                applicability_reason.append("EU jurisdiction")
            elif "California" in framework["jurisdiction"] and "california" in location.lower():
                is_applicable = True
                applicability_reason.append("California jurisdiction")
            
            # Industry-specific applicability
            if framework_id == "HIPAA" and any(term in industry for term in ["health", "medical", "healthcare"]):
                is_applicable = True
                applicability_reason.append("Healthcare industry")
            elif framework_id == "PCI_DSS" and any(term in industry for term in ["fintech", "payment", "ecommerce", "retail"]):
                is_applicable = True
                applicability_reason.append("Handles payment data")
            elif framework_id in ["SOC2", "ISO27001"] and any(term in industry for term in ["software", "saas", "technology", "cloud"]):
                is_applicable = True
                applicability_reason.append("Technology service provider")
            
            # Company size thresholds
            if framework_id == "GDPR" and (company_size > 250 or annual_revenue > 20000000):
                is_applicable = True
                applicability_reason.append("Size threshold for GDPR")
            elif framework_id == "SOC2" and company_size > 50:
                is_applicable = True
                applicability_reason.append("Service organization size")
            
            if is_applicable:
                applicable_reg = framework.copy()
                applicable_reg["framework_id"] = framework_id
                applicable_reg["applicability_reasons"] = applicability_reason
                applicable_reg["priority"] = self._determine_compliance_priority(framework_id, industry)
                applicable.append(applicable_reg)
        
        return sorted(applicable, key=lambda x: x["priority"], reverse=True)
    
    def _determine_compliance_priority(self, framework_id: str, industry: str) -> int:
        """Determine compliance priority (1-10 scale)"""
        # Critical frameworks
        if framework_id in ["HIPAA", "PCI_DSS"] and any(term in industry for term in ["health", "fintech", "payment"]):
            return 10
        elif framework_id == "GDPR":
            return 9
        elif framework_id == "SOC2" and "software" in industry:
            return 8
        elif framework_id in ["ISO27001", "CCPA"]:
            return 6
        else:
            return 5
    
    async def _assess_compliance_readiness(
        self,
        applicable_regulations: List[Dict[str, Any]],
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], float]:
        """Assess current compliance readiness and identify gaps"""
        
        compliance_gaps = []
        readiness_scores = []
        
        for regulation in applicable_regulations:
            framework_id = regulation["framework_id"]
            
            # Assess current state vs requirements
            gaps = []
            current_controls = self._assess_current_controls(company_data, technical_architecture)
            
            for requirement in regulation["key_requirements"]:
                gap_assessment = await self._assess_requirement_gap(
                    framework_id, requirement, current_controls, company_data
                )
                if gap_assessment["has_gap"]:
                    gaps.append(gap_assessment)
            
            # Calculate framework readiness score
            if gaps:
                framework_readiness = max(0, 1.0 - (len(gaps) / len(regulation["key_requirements"])))
            else:
                framework_readiness = 0.8  # Conservative estimate when no gaps identified
            
            readiness_scores.append(framework_readiness)
            
            if gaps:
                compliance_gaps.append({
                    "framework": framework_id,
                    "framework_name": regulation["full_name"],
                    "gaps": gaps,
                    "readiness_score": framework_readiness,
                    "estimated_effort": self._estimate_gap_remediation_effort(gaps),
                    "risk_level": regulation["risk_level"].value
                })
        
        # Overall readiness score (weighted by framework priority)
        if readiness_scores and applicable_regulations:
            weights = [reg["priority"] for reg in applicable_regulations]
            overall_readiness = sum(score * weight for score, weight in zip(readiness_scores, weights)) / sum(weights)
        else:
            overall_readiness = 0.5  # Default when no applicable regulations
        
        return compliance_gaps, overall_readiness
    
    def _assess_current_controls(
        self,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> Dict[str, bool]:
        """Assess current security and compliance controls"""
        
        controls = {
            "data_encryption": False,
            "access_controls": False,
            "audit_logging": False,
            "backup_systems": False,
            "incident_response": False,
            "vulnerability_management": False,
            "employee_training": False,
            "third_party_agreements": False,
            "privacy_policy": False,
            "data_classification": False
        }
        
        # Infer controls from technical architecture
        if technical_architecture:
            security_reqs = technical_architecture.get("security_requirements", [])
            
            if any("encryption" in req.lower() for req in security_reqs):
                controls["data_encryption"] = True
            if any("access control" in req.lower() or "authentication" in req.lower() for req in security_reqs):
                controls["access_controls"] = True
            if any("monitoring" in req.lower() or "logging" in req.lower() for req in security_reqs):
                controls["audit_logging"] = True
        
        # Company size assumptions
        company_size = company_data.get("company_size", 0)
        if company_size > 500:
            controls["employee_training"] = True
            controls["incident_response"] = True
        if company_size > 100:
            controls["backup_systems"] = True
            controls["privacy_policy"] = True
        
        return controls
    
    async def _assess_requirement_gap(
        self,
        framework_id: str,
        requirement: str,
        current_controls: Dict[str, bool],
        company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess specific compliance requirement gap"""
        
        # Map requirements to controls
        requirement_mappings = {
            "data encryption": ["data_encryption"],
            "access controls": ["access_controls"],
            "audit logging": ["audit_logging"],
            "monitoring": ["audit_logging"],
            "backup": ["backup_systems"],
            "privacy": ["privacy_policy", "data_classification"],
            "training": ["employee_training"],
            "incident": ["incident_response"]
        }
        
        has_gap = True
        gap_severity = "medium"
        
        # Check if requirement is covered by current controls
        for req_key, control_keys in requirement_mappings.items():
            if req_key.lower() in requirement.lower():
                if any(current_controls.get(control_key, False) for control_key in control_keys):
                    has_gap = False
                break
        
        # Determine gap severity
        critical_requirements = ["data encryption", "access controls", "audit logging"]
        if any(crit_req in requirement.lower() for crit_req in critical_requirements):
            gap_severity = "high"
        
        return {
            "requirement": requirement,
            "has_gap": has_gap,
            "gap_severity": gap_severity,
            "remediation_effort": "high" if gap_severity == "high" else "medium",
            "estimated_cost": self._estimate_requirement_cost(requirement, company_data.get("company_size", 0))
        }
    
    def _estimate_requirement_cost(self, requirement: str, company_size: int) -> float:
        """Estimate cost to implement specific requirement"""
        
        base_costs = {
            "data encryption": 25000,
            "access controls": 40000,
            "audit logging": 30000,
            "backup systems": 20000,
            "incident response": 50000,
            "employee training": 15000,
            "privacy policy": 10000
        }
        
        # Find matching base cost
        base_cost = 20000  # Default
        for cost_key, cost_val in base_costs.items():
            if cost_key.lower() in requirement.lower():
                base_cost = cost_val
                break
        
        # Scale by company size
        if company_size > 1000:
            return base_cost * 2.0
        elif company_size > 500:
            return base_cost * 1.5
        elif company_size > 100:
            return base_cost * 1.2
        else:
            return base_cost
    
    def _estimate_gap_remediation_effort(self, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate effort to remediate compliance gaps"""
        
        total_cost = sum(gap["estimated_cost"] for gap in gaps)
        high_severity_gaps = sum(1 for gap in gaps if gap["gap_severity"] == "high")
        
        # Timeline estimation
        if high_severity_gaps > 3:
            timeline_months = 12
        elif high_severity_gaps > 1:
            timeline_months = 8
        elif len(gaps) > 5:
            timeline_months = 6
        else:
            timeline_months = 4
        
        return {
            "total_estimated_cost": total_cost,
            "timeline_months": timeline_months,
            "high_priority_gaps": high_severity_gaps,
            "total_gaps": len(gaps),
            "effort_level": "high" if high_severity_gaps > 2 else "medium"
        }
    
    def _develop_regulatory_timeline(self, applicable_regulations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Develop implementation timeline for regulatory compliance"""
        
        if not applicable_regulations:
            return {}
        
        # Sort by priority and find most critical timeline
        sorted_regs = sorted(applicable_regulations, key=lambda x: x["priority"], reverse=True)
        critical_timeline = sorted_regs[0]["implementation_timeline"]
        
        # Parse timeline (e.g., "6-12 months")
        if "-" in critical_timeline:
            min_months, max_months = critical_timeline.replace(" months", "").split("-")
            target_months = int(max_months)  # Use conservative estimate
        else:
            target_months = 12  # Default
        
        return {
            "critical_compliance_deadline": f"{target_months} months",
            "phased_approach_recommended": len(applicable_regulations) > 2,
            "regulatory_priorities": [
                {
                    "framework": reg["framework_id"],
                    "priority": reg["priority"],
                    "timeline": reg["implementation_timeline"]
                }
                for reg in sorted_regs[:3]  # Top 3 priorities
            ]
        }
    
    def _estimate_compliance_costs(
        self,
        applicable_regulations: List[Dict[str, Any]],
        company_size: int
    ) -> Dict[str, float]:
        """Estimate compliance implementation and ongoing costs"""
        
        total_implementation = 0
        total_annual_ongoing = 0
        
        size_multiplier = 1.0
        if company_size > 1000:
            size_multiplier = 2.0
        elif company_size > 500:
            size_multiplier = 1.5
        elif company_size > 100:
            size_multiplier = 1.2
        
        for regulation in applicable_regulations:
            cost_range = regulation["compliance_cost_range"]
            # Use 75th percentile of cost range
            implementation_cost = (cost_range[0] + (cost_range[1] - cost_range[0]) * 0.75) * size_multiplier
            
            total_implementation += implementation_cost
            total_annual_ongoing += implementation_cost * 0.25  # 25% ongoing annually
        
        return {
            "total_implementation_cost": total_implementation,
            "annual_ongoing_cost": total_annual_ongoing,
            "3_year_total_cost": total_implementation + (total_annual_ongoing * 3),
            "cost_per_employee": total_implementation / max(company_size, 1) if company_size > 0 else 0
        }
    
    async def _perform_risk_assessment(
        self,
        assessment: ComplianceRiskAssessment,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]],
        market_intelligence: Optional[Dict[str, Any]],
        executive_intelligence: Optional[Dict[str, Any]]
    ):
        """Perform comprehensive multi-dimensional risk assessment"""
        
        # Business risks
        assessment.business_risks = await self._assess_business_risks(
            company_data, market_intelligence, executive_intelligence
        )
        
        # Operational risks
        assessment.operational_risks = await self._assess_operational_risks(
            company_data, technical_architecture
        )
        
        # Technology risks
        assessment.technology_risks = self._assess_technology_risks(technical_architecture)
        
        # Financial risks
        assessment.financial_risks = self._assess_financial_risks(
            company_data, executive_intelligence
        )
        
        # Reputational risks
        assessment.reputational_risks = await self._assess_reputational_risks(
            company_data, assessment.applicable_regulations
        )
        
        # Calculate financial impact
        assessment.potential_financial_impact = self._calculate_potential_financial_impact(
            assessment, company_data
        )
        
        # Risk materialization probability
        assessment.probability_risk_materialization = self._calculate_risk_probability(assessment)
    
    async def _assess_business_risks(
        self,
        company_data: Dict[str, Any],
        market_intelligence: Optional[Dict[str, Any]],
        executive_intelligence: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Assess strategic business risks"""
        
        risks = []
        
        # Market volatility risk
        if market_intelligence:
            growth_rate = market_intelligence.get("growth_rate", 0.1)
            if growth_rate > 0.25:
                risks.append({
                    "risk": "High market volatility in rapid-growth sector",
                    "probability": "medium",
                    "impact": "medium",
                    "financial_impact": 500000,
                    "mitigation": "Diversification strategy and agile planning"
                })
        
        # Competitive displacement
        company_size = company_data.get("company_size", 0)
        if company_size < 500:
            risks.append({
                "risk": "Competitive displacement by larger players",
                "probability": "medium", 
                "impact": "high",
                "financial_impact": 1000000,
                "mitigation": "Niche specialization and customer intimacy"
            })
        
        # Regulatory compliance risk
        if len(assessment.applicable_regulations) > 2:
            risks.append({
                "risk": "Regulatory non-compliance penalties and restrictions",
                "probability": "high",
                "impact": "high",
                "financial_impact": 2000000,
                "mitigation": "Proactive compliance program and legal counsel"
            })
        
        return risks
    
    async def _assess_operational_risks(
        self,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Assess operational and process risks"""
        
        risks = []
        
        # System availability risk
        if technical_architecture:
            availability = technical_architecture.get("scalability_assessment", {}).get("availability_requirement", "99%")
            if "99.9" not in availability:
                risks.append({
                    "risk": "System downtime affecting business operations",
                    "probability": "medium",
                    "impact": "high",
                    "financial_impact": 100000,  # Per incident
                    "mitigation": "High availability architecture and disaster recovery"
                })
        
        # Data breach risk
        risks.append({
            "risk": "Data breach exposing customer information",
            "probability": "low",
            "impact": "critical",
            "financial_impact": 5000000,  # Average breach cost
            "mitigation": "Comprehensive security controls and incident response"
        })
        
        # Key person dependency
        company_size = company_data.get("company_size", 0)
        if company_size < 200:
            risks.append({
                "risk": "Key person dependency affecting operations",
                "probability": "medium",
                "impact": "medium",
                "financial_impact": 200000,
                "mitigation": "Knowledge documentation and succession planning"
            })
        
        return risks
    
    def _assess_technology_risks(self, technical_architecture: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assess technology and infrastructure risks"""
        
        risks = []
        
        if technical_architecture:
            # Extract technical risks from architecture analysis
            tech_risks = technical_architecture.get("technical_risks", [])
            for risk in tech_risks:
                risks.append({
                    "risk": risk.get("risk", "Technical implementation risk"),
                    "probability": risk.get("probability", "medium"),
                    "impact": risk.get("impact", "medium"),
                    "financial_impact": 300000,  # Default technical risk cost
                    "mitigation": risk.get("mitigation", "Technical risk mitigation required")
                })
        
        # Default technology risks
        if not risks:
            risks = [
                {
                    "risk": "Technology obsolescence and maintenance challenges",
                    "probability": "medium",
                    "impact": "medium",
                    "financial_impact": 250000,
                    "mitigation": "Regular technology refresh and modernization planning"
                },
                {
                    "risk": "Integration failures affecting system reliability",
                    "probability": "low",
                    "impact": "high",
                    "financial_impact": 400000,
                    "mitigation": "Comprehensive testing and rollback procedures"
                }
            ]
        
        return risks
    
    def _assess_financial_risks(
        self,
        company_data: Dict[str, Any],
        executive_intelligence: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Assess financial and investment risks"""
        
        risks = []
        
        # Budget overrun risk
        if executive_intelligence:
            total_investment = executive_intelligence.get("total_investment", 0)
            if total_investment > 500000:
                risks.append({
                    "risk": "Project budget overrun affecting ROI",
                    "probability": "medium",
                    "impact": "high", 
                    "financial_impact": total_investment * 0.3,  # 30% overrun
                    "mitigation": "Phased implementation with milestone gates"
                })
        
        # Revenue shortfall risk
        risks.append({
            "risk": "Revenue projections not materializing as expected",
            "probability": "medium",
            "impact": "high",
            "financial_impact": 1000000,
            "mitigation": "Conservative projections and contingency planning"
        })
        
        return risks
    
    async def _assess_reputational_risks(
        self,
        company_data: Dict[str, Any],
        applicable_regulations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Assess reputational and brand risks"""
        
        risks = []
        
        # Compliance violation reputational risk
        high_profile_regulations = ["GDPR", "HIPAA", "PCI_DSS"]
        if any(reg["framework_id"] in high_profile_regulations for reg in applicable_regulations):
            risks.append({
                "risk": "Public compliance violations affecting brand reputation",
                "probability": "low",
                "impact": "critical",
                "financial_impact": 2000000,
                "mitigation": "Proactive compliance and public relations strategy"
            })
        
        # Customer trust risk
        industry = company_data.get("industry", "").lower()
        if any(term in industry for term in ["fintech", "healthcare", "financial"]):
            risks.append({
                "risk": "Loss of customer trust affecting retention and acquisition",
                "probability": "medium",
                "impact": "high",
                "financial_impact": 1500000,
                "mitigation": "Transparency, security leadership, and customer communication"
            })
        
        return risks
    
    def _calculate_potential_financial_impact(
        self,
        assessment: ComplianceRiskAssessment,
        company_data: Dict[str, Any]
    ) -> float:
        """Calculate total potential financial impact of identified risks"""
        
        all_risks = (
            assessment.business_risks +
            assessment.operational_risks +
            assessment.technology_risks +
            assessment.financial_risks +
            assessment.reputational_risks
        )
        
        # Calculate probability-weighted impact
        total_impact = 0
        for risk in all_risks:
            probability = {"low": 0.2, "medium": 0.5, "high": 0.8}.get(risk.get("probability", "medium"), 0.5)
            impact = risk.get("financial_impact", 0)
            total_impact += probability * impact
        
        return total_impact
    
    def _calculate_risk_probability(self, assessment: ComplianceRiskAssessment) -> float:
        """Calculate overall probability of material risk event"""
        
        all_risks = (
            assessment.business_risks +
            assessment.operational_risks + 
            assessment.technology_risks +
            assessment.financial_risks +
            assessment.reputational_risks
        )
        
        if not all_risks:
            return 0.3  # Default 30% probability
        
        # Calculate composite probability (not cumulative)
        high_prob_risks = sum(1 for risk in all_risks if risk.get("probability") == "high")
        medium_prob_risks = sum(1 for risk in all_risks if risk.get("probability") == "medium")
        
        # Weighted probability calculation
        risk_score = (high_prob_risks * 0.8 + medium_prob_risks * 0.5) / len(all_risks)
        return min(risk_score, 0.9)  # Cap at 90%
    
    def _recommend_governance_frameworks(
        self,
        company_size: int,
        industry: str,
        applicable_regulations: List[Dict[str, Any]]
    ) -> List[str]:
        """Recommend governance frameworks based on company profile"""
        
        frameworks = []
        
        # Size-based recommendations
        if company_size > 1000:
            frameworks.extend(["COSO Enterprise Risk Management", "COBIT IT Governance"])
        elif company_size > 500:
            frameworks.append("COSO Internal Controls")
        
        # Industry-specific frameworks
        if any(term in industry for term in ["technology", "software", "cyber"]):
            frameworks.append("NIST Cybersecurity Framework")
        
        # Regulation-driven frameworks
        framework_ids = [reg["framework_id"] for reg in applicable_regulations]
        if "ISO27001" in framework_ids:
            frameworks.append("ISO 27001 ISMS")
        if any(fid in ["HIPAA", "PCI_DSS", "GDPR"] for fid in framework_ids):
            frameworks.append("Privacy and Data Protection Governance")
        
        return list(set(frameworks))  # Remove duplicates
    
    async def _define_security_controls(
        self,
        applicable_regulations: List[Dict[str, Any]],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Define required security controls"""
        
        controls = []
        
        # Base security controls
        base_controls = [
            {"control": "Multi-factor Authentication", "category": "access", "priority": "high"},
            {"control": "Data Encryption at Rest", "category": "data_protection", "priority": "high"},
            {"control": "Data Encryption in Transit", "category": "data_protection", "priority": "high"},
            {"control": "Audit Logging and Monitoring", "category": "monitoring", "priority": "medium"},
            {"control": "Vulnerability Management", "category": "security", "priority": "medium"},
            {"control": "Incident Response Plan", "category": "response", "priority": "high"}
        ]
        
        controls.extend(base_controls)
        
        # Regulation-specific controls
        framework_ids = [reg["framework_id"] for reg in applicable_regulations]
        
        if "GDPR" in framework_ids:
            controls.extend([
                {"control": "Data Subject Rights Management", "category": "privacy", "priority": "high"},
                {"control": "Privacy Impact Assessments", "category": "privacy", "priority": "medium"}
            ])
        
        if "HIPAA" in framework_ids:
            controls.extend([
                {"control": "PHI Access Controls", "category": "access", "priority": "critical"},
                {"control": "Business Associate Agreements", "category": "legal", "priority": "high"}
            ])
        
        if "PCI_DSS" in framework_ids:
            controls.extend([
                {"control": "Cardholder Data Environment Segmentation", "category": "network", "priority": "critical"},
                {"control": "Payment Data Tokenization", "category": "data_protection", "priority": "high"}
            ])
        
        return controls
    
    def _determine_audit_requirements(self, applicable_regulations: List[Dict[str, Any]]) -> List[str]:
        """Determine audit and assessment requirements"""
        
        requirements = []
        
        framework_ids = [reg["framework_id"] for reg in applicable_regulations]
        
        # Standard audit requirements
        requirements.append("Annual compliance assessment")
        requirements.append("Quarterly security reviews")
        
        # Regulation-specific audits
        if "SOC2" in framework_ids:
            requirements.extend(["SOC 2 Type II audit", "Continuous monitoring program"])
        
        if "ISO27001" in framework_ids:
            requirements.extend(["ISO 27001 certification audit", "Annual surveillance audits"])
        
        if "PCI_DSS" in framework_ids:
            requirements.extend(["PCI DSS assessment", "Quarterly network scans"])
        
        if any(fid in ["HIPAA", "GDPR"] for fid in framework_ids):
            requirements.append("Privacy compliance audit")
        
        return requirements
    
    def _design_monitoring_controls(self, assessment: ComplianceRiskAssessment) -> List[str]:
        """Design monitoring and alerting controls"""
        
        controls = [
            "Real-time security event monitoring",
            "Compliance dashboard and reporting",
            "Risk metric tracking and alerting",
            "Audit trail integrity monitoring"
        ]
        
        # Add risk-specific monitoring
        if assessment.overall_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            controls.extend([
                "Executive risk reporting dashboard",
                "Automated compliance violation alerts",
                "Third-party risk monitoring"
            ])
        
        return controls
    
    async def _develop_risk_mitigation_plan(self, assessment: ComplianceRiskAssessment) -> List[Dict[str, Any]]:
        """Develop comprehensive risk mitigation plan"""
        
        mitigation_plan = []
        
        # Process all risk categories
        all_risks = (
            assessment.business_risks +
            assessment.operational_risks +
            assessment.technology_risks +
            assessment.financial_risks +
            assessment.reputational_risks
        )
        
        # Sort by impact and probability
        high_priority_risks = [
            risk for risk in all_risks 
            if risk.get("impact") in ["high", "critical"] and risk.get("probability") in ["medium", "high"]
        ]
        
        for risk in high_priority_risks[:5]:  # Top 5 risks
            mitigation_plan.append({
                "risk": risk["risk"],
                "mitigation_strategy": risk.get("mitigation", "Mitigation strategy required"),
                "priority": "high" if risk.get("impact") == "critical" else "medium",
                "timeline": "immediate" if risk.get("impact") == "critical" else "30 days",
                "responsible_party": "Risk Management Team",
                "estimated_cost": risk.get("financial_impact", 0) * 0.1  # 10% of impact for mitigation
            })
        
        return mitigation_plan
    
    def _create_compliance_roadmap(self, assessment: ComplianceRiskAssessment) -> List[Dict[str, Any]]:
        """Create compliance implementation roadmap"""
        
        roadmap = []
        
        # Sort compliance gaps by priority
        sorted_gaps = sorted(
            assessment.compliance_gaps,
            key=lambda x: (x["risk_level"] == "critical", x["readiness_score"]),
            reverse=True
        )
        
        cumulative_months = 0
        for i, gap in enumerate(sorted_gaps[:3]):  # Top 3 compliance priorities
            effort = gap["estimated_effort"]
            timeline_months = effort.get("timeline_months", 6)
            
            roadmap.append({
                "phase": i + 1,
                "framework": gap["framework"],
                "timeline": f"Months {cumulative_months + 1}-{cumulative_months + timeline_months}",
                "key_activities": [f"Address {len(gap['gaps'])} compliance gaps", "Implement controls", "Validate compliance"],
                "success_criteria": f"Achieve {gap['framework']} compliance readiness",
                "estimated_cost": effort.get("total_estimated_cost", 100000)
            })
            
            cumulative_months += timeline_months
        
        return roadmap
    
    def _determine_board_reporting(
        self,
        assessment: ComplianceRiskAssessment,
        company_size: int
    ) -> List[str]:
        """Determine board-level reporting requirements"""
        
        requirements = []
        
        if company_size > 1000 or assessment.overall_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            requirements.extend([
                "Quarterly risk assessment summary",
                "Annual compliance status report",
                "Critical incident notifications within 24 hours"
            ])
        
        if assessment.potential_financial_impact > 1000000:
            requirements.append("Material risk exposure reporting")
        
        if len(assessment.applicable_regulations) > 2:
            requirements.append("Regulatory compliance dashboard")
        
        return requirements
    
    def _assess_insurance_needs(self, assessment: ComplianceRiskAssessment) -> List[str]:
        """Assess insurance coverage needs"""
        
        insurance_needs = []
        
        # Base insurance recommendations
        if assessment.potential_financial_impact > 500000:
            insurance_needs.append("Cyber liability insurance")
            insurance_needs.append("Professional liability insurance")
        
        # Regulation-specific insurance
        framework_ids = [reg["framework_id"] for reg in assessment.applicable_regulations]
        
        if any(fid in ["GDPR", "CCPA", "HIPAA"] for fid in framework_ids):
            insurance_needs.append("Privacy liability insurance")
        
        if "PCI_DSS" in framework_ids:
            insurance_needs.append("Payment card industry liability coverage")
        
        # High-risk scenarios
        if assessment.overall_risk_level == RiskLevel.CRITICAL:
            insurance_needs.extend([
                "Directors and officers liability",
                "Business interruption insurance"
            ])
        
        return insurance_needs
    
    def _determine_legal_reviews(self, assessment: ComplianceRiskAssessment) -> List[str]:
        """Determine legal review requirements"""
        
        reviews = []
        
        # Base legal reviews
        if len(assessment.applicable_regulations) > 0:
            reviews.append("Compliance legal review")
        
        # Regulation-specific reviews
        framework_ids = [reg["framework_id"] for reg in assessment.applicable_regulations]
        
        if any(fid in ["GDPR", "CCPA"] for fid in framework_ids):
            reviews.extend([
                "Privacy policy review",
                "Data processing agreement review"
            ])
        
        if "HIPAA" in framework_ids:
            reviews.append("Business associate agreement review")
        
        if assessment.overall_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            reviews.append("Risk management legal counsel")
        
        return reviews
    
    async def _assess_third_party_risks(
        self,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Assess third-party and vendor risk factors"""
        
        risk_factors = []
        
        # Technical vendor risks
        if technical_architecture:
            integration_count = len(technical_architecture.get("integration_requirements", []))
            if integration_count > 3:
                risk_factors.append("Multiple vendor integrations increase supply chain risk")
            
            if technical_architecture.get("infrastructure_needs", {}).get("hosting_recommendation") == "cloud":
                risk_factors.append("Cloud vendor dependency and data sovereignty considerations")
        
        # Industry-specific third-party risks
        industry = company_data.get("industry", "").lower()
        if any(term in industry for term in ["fintech", "financial"]):
            risk_factors.extend([
                "Financial service partner compliance requirements",
                "Payment processor vendor risk assessment"
            ])
        
        if any(term in industry for term in ["healthcare", "medical"]):
            risk_factors.append("Healthcare vendor BAA and HIPAA compliance requirements")
        
        # Default third-party risks
        if not risk_factors:
            risk_factors = [
                "Vendor security assessment and ongoing monitoring",
                "Service level agreement and business continuity planning",
                "Data processing and privacy agreement requirements"
            ]
        
        return risk_factors
    
    def _calculate_overall_risk(self, assessment: ComplianceRiskAssessment) -> Tuple[RiskLevel, float]:
        """Calculate overall risk level and score"""
        
        risk_factors = []
        
        # Compliance risk factor
        compliance_risk = 1.0 - assessment.compliance_readiness_score
        risk_factors.append(compliance_risk * 0.3)  # 30% weight
        
        # Financial impact factor
        if assessment.potential_financial_impact > 5000000:
            risk_factors.append(0.8 * 0.25)  # High financial risk, 25% weight
        elif assessment.potential_financial_impact > 1000000:
            risk_factors.append(0.6 * 0.25)
        else:
            risk_factors.append(0.3 * 0.25)
        
        # Probability factor
        risk_factors.append(assessment.probability_risk_materialization * 0.25)  # 25% weight
        
        # Regulatory complexity factor
        reg_complexity = min(len(assessment.applicable_regulations) / 5.0, 1.0)
        risk_factors.append(reg_complexity * 0.2)  # 20% weight
        
        # Calculate overall risk score
        overall_risk_score = sum(risk_factors)
        
        # Map to risk level
        if overall_risk_score >= 0.75:
            risk_level = RiskLevel.CRITICAL
        elif overall_risk_score >= 0.6:
            risk_level = RiskLevel.HIGH
        elif overall_risk_score >= 0.4:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return risk_level, overall_risk_score
    
    async def _generate_governance_recommendations(self, assessment: ComplianceRiskAssessment) -> List[str]:
        """Generate governance and oversight recommendations"""
        
        recommendations = []
        
        # Risk-based recommendations
        if assessment.overall_risk_level == RiskLevel.CRITICAL:
            recommendations.extend([
                "Establish executive-level risk committee with monthly meetings",
                "Implement continuous risk monitoring with real-time alerting",
                "Engage external risk management consultants for specialized expertise"
            ])
        elif assessment.overall_risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Create cross-functional risk management team",
                "Implement quarterly risk assessment and reporting cycle",
                "Consider external audit of risk management processes"
            ])
        else:
            recommendations.extend([
                "Assign dedicated compliance officer or risk manager",
                "Establish semi-annual risk review process",
                "Implement basic risk management policies and procedures"
            ])
        
        # Compliance-based recommendations
        if len(assessment.compliance_gaps) > 2:
            recommendations.append("Prioritize compliance gap remediation with phased approach")
        
        if len(assessment.applicable_regulations) > 3:
            recommendations.append("Consider compliance management platform for regulatory coordination")
        
        return recommendations
    
    def _calculate_assessment_confidence(
        self,
        assessment: ComplianceRiskAssessment,
        technical_architecture: Optional[Dict[str, Any]],
        market_intelligence: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate confidence level in the risk assessment"""
        
        confidence_factors = []
        
        # Data availability
        if len(assessment.applicable_regulations) > 0:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Technical architecture integration
        if technical_architecture and technical_architecture.get("confidence_level", 0) > 0.7:
            confidence_factors.append(0.8)
        elif technical_architecture:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Market intelligence integration
        if market_intelligence:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Assessment completeness
        if len(assessment.business_risks) > 0 and len(assessment.operational_risks) > 0:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        return sum(confidence_factors) / len(confidence_factors)
    
    def _identify_assessment_limitations(
        self,
        company_data: Dict[str, Any],
        technical_architecture: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify limitations in the risk assessment"""
        
        limitations = []
        
        if not technical_architecture:
            limitations.append("Limited technical architecture data - security controls assessment may be incomplete")
        
        if not company_data.get("annual_revenue"):
            limitations.append("Financial data limited - cost-benefit analysis estimates may vary significantly")
        
        if not company_data.get("location"):
            limitations.append("Geographic location unknown - regulatory applicability may be incomplete")
        
        limitations.append("Assessment based on standard industry frameworks - organization-specific risks may exist")
        limitations.append("Risk probability estimates based on industry averages - actual probability may vary")
        
        return limitations
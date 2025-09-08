"""
Technical Architecture Agent - Strategic Layer
Provides solution design, technical feasibility, and architecture recommendations
Complements CrewAI's tactical tech stack research with strategic technical analysis
"""

import logging
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class ComplexityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ENTERPRISE = "enterprise"

class IntegrationRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class TechnicalArchitecture:
    """Strategic technical architecture assessment"""
    solution_complexity: ComplexityLevel = ComplexityLevel.MEDIUM
    integration_requirements: List[Dict[str, Any]] = None
    scalability_assessment: Dict[str, Any] = None
    security_requirements: List[str] = None
    compliance_frameworks: List[str] = None
    infrastructure_needs: Dict[str, Any] = None
    implementation_phases: List[Dict[str, Any]] = None
    resource_requirements: Dict[str, Any] = None
    timeline_estimate: Dict[str, Any] = None
    technical_risks: List[Dict[str, Any]] = None
    integration_risks: IntegrationRisk = IntegrationRisk.MEDIUM
    modernization_opportunities: List[str] = None
    technology_roadmap: List[Dict[str, Any]] = None
    roi_technical_factors: Dict[str, float] = None
    architecture_score: float = 0.5
    feasibility_score: float = 0.5
    confidence_level: float = 0.5
    
    def __post_init__(self):
        if self.integration_requirements is None:
            self.integration_requirements = []
        if self.scalability_assessment is None:
            self.scalability_assessment = {}
        if self.security_requirements is None:
            self.security_requirements = []
        if self.compliance_frameworks is None:
            self.compliance_frameworks = []
        if self.infrastructure_needs is None:
            self.infrastructure_needs = {}
        if self.implementation_phases is None:
            self.implementation_phases = []
        if self.resource_requirements is None:
            self.resource_requirements = {}
        if self.timeline_estimate is None:
            self.timeline_estimate = {}
        if self.technical_risks is None:
            self.technical_risks = []
        if self.modernization_opportunities is None:
            self.modernization_opportunities = []
        if self.technology_roadmap is None:
            self.technology_roadmap = []
        if self.roi_technical_factors is None:
            self.roi_technical_factors = {}

class TechnicalArchitectureAgent:
    """
    Strategic Technical Architecture Agent
    
    Provides enterprise-grade technical solution design:
    - Solution architecture complexity assessment
    - Integration requirements and feasibility analysis  
    - Scalability and performance projections
    - Security and compliance framework alignment
    - Implementation roadmap and phasing strategy
    - Resource and timeline estimation
    - Technical risk assessment and mitigation
    - Technology modernization opportunities
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Technical knowledge bases
        self.architecture_patterns = self._initialize_architecture_patterns()
        self.compliance_frameworks = self._initialize_compliance_frameworks()
        
    def _initialize_architecture_patterns(self) -> Dict[str, Any]:
        """Initialize common architecture patterns and complexity assessments"""
        return {
            "microservices": {
                "complexity": ComplexityLevel.HIGH,
                "benefits": ["scalability", "flexibility", "fault_isolation"],
                "challenges": ["distributed_complexity", "network_latency", "data_consistency"],
                "timeline_factor": 1.4
            },
            "monolithic": {
                "complexity": ComplexityLevel.LOW,
                "benefits": ["simplicity", "easier_deployment", "performance"],
                "challenges": ["scalability_limits", "technology_lock_in", "maintenance"],
                "timeline_factor": 1.0
            },
            "serverless": {
                "complexity": ComplexityLevel.MEDIUM,
                "benefits": ["cost_efficiency", "auto_scaling", "reduced_ops"],
                "challenges": ["vendor_lock_in", "cold_starts", "debugging"],
                "timeline_factor": 1.2
            },
            "hybrid_cloud": {
                "complexity": ComplexityLevel.ENTERPRISE,
                "benefits": ["flexibility", "compliance", "cost_optimization"],
                "challenges": ["complexity", "security", "governance"],
                "timeline_factor": 1.8
            }
        }
    
    def _initialize_compliance_frameworks(self) -> Dict[str, Any]:
        """Initialize compliance framework requirements"""
        return {
            "SOC2": {
                "industries": ["software", "saas", "technology"],
                "requirements": ["access_controls", "encryption", "monitoring", "backup"],
                "implementation_time": "6-12 months",
                "complexity": ComplexityLevel.MEDIUM
            },
            "HIPAA": {
                "industries": ["healthcare", "medical"],
                "requirements": ["data_encryption", "access_logs", "audit_trails", "breach_notification"],
                "implementation_time": "9-18 months",
                "complexity": ComplexityLevel.HIGH
            },
            "PCI_DSS": {
                "industries": ["fintech", "payment", "ecommerce"],
                "requirements": ["network_security", "data_protection", "vulnerability_management"],
                "implementation_time": "6-15 months",
                "complexity": ComplexityLevel.HIGH
            },
            "GDPR": {
                "industries": ["all"],
                "requirements": ["consent_management", "data_portability", "right_to_erasure"],
                "implementation_time": "4-8 months",
                "complexity": ComplexityLevel.MEDIUM
            }
        }
    
    async def analyze_technical_architecture(
        self,
        company_data: Dict[str, Any],
        crewai_results: Optional[Dict[str, Any]] = None,
        solution_requirements: Optional[Dict[str, Any]] = None
    ) -> TechnicalArchitecture:
        """
        Generate strategic technical architecture assessment
        
        Takes CrewAI tactical tech stack research and solution requirements,
        adds strategic technical analysis:
        - Architecture complexity and pattern recommendations
        - Integration feasibility and requirements
        - Scalability projections and infrastructure needs
        - Compliance and security framework alignment
        - Implementation roadmap with phases and timelines
        - Resource requirements and technical ROI factors
        """
        
        try:
            # Extract key data points
            company_size = company_data.get("company_size", 0)
            industry = company_data.get("industry", "").lower()
            existing_tech = crewai_results.get("tech_stack", []) if crewai_results else []
            
            # Initialize technical architecture assessment
            tech_arch = TechnicalArchitecture()
            
            # 1. Solution complexity assessment
            tech_arch.solution_complexity = self._assess_solution_complexity(
                company_size, industry, existing_tech, solution_requirements
            )
            
            # 2. Integration requirements analysis
            tech_arch.integration_requirements = await self._analyze_integration_requirements(
                existing_tech, company_data, solution_requirements
            )
            
            # 3. Scalability assessment
            tech_arch.scalability_assessment = self._assess_scalability_requirements(
                company_size, tech_arch.solution_complexity
            )
            
            # 4. Security and compliance requirements
            tech_arch.security_requirements = self._determine_security_requirements(industry, company_size)
            tech_arch.compliance_frameworks = self._identify_compliance_frameworks(industry)
            
            # 5. Infrastructure needs analysis
            tech_arch.infrastructure_needs = await self._analyze_infrastructure_needs(
                company_size, tech_arch.solution_complexity, existing_tech
            )
            
            # 6. Implementation phases and timeline
            tech_arch.implementation_phases = self._plan_implementation_phases(tech_arch)
            tech_arch.timeline_estimate = self._estimate_implementation_timeline(tech_arch)
            
            # 7. Resource requirements
            tech_arch.resource_requirements = self._calculate_resource_requirements(
                tech_arch, company_size
            )
            
            # 8. Risk assessment
            tech_arch.technical_risks = self._assess_technical_risks(tech_arch, existing_tech)
            tech_arch.integration_risks = self._assess_integration_risks(
                len(tech_arch.integration_requirements), tech_arch.solution_complexity
            )
            
            # 9. Modernization opportunities
            tech_arch.modernization_opportunities = await self._identify_modernization_opportunities(
                existing_tech, industry, crewai_results
            )
            
            # 10. Technology roadmap
            tech_arch.technology_roadmap = await self._create_technology_roadmap(
                tech_arch, company_data
            )
            
            # 11. ROI technical factors
            tech_arch.roi_technical_factors = self._calculate_roi_technical_factors(tech_arch)
            
            # 12. Calculate scores
            tech_arch.architecture_score = self._calculate_architecture_score(tech_arch)
            tech_arch.feasibility_score = self._calculate_feasibility_score(tech_arch)
            tech_arch.confidence_level = self._calculate_confidence_level(
                tech_arch, crewai_results, solution_requirements
            )
            
            self.logger.info(f"Technical architecture analysis completed for {industry} industry")
            return tech_arch
            
        except Exception as e:
            self.logger.error(f"Technical architecture analysis failed: {e}")
            return TechnicalArchitecture()
    
    def _assess_solution_complexity(
        self,
        company_size: int,
        industry: str,
        existing_tech: List[str],
        solution_requirements: Optional[Dict[str, Any]]
    ) -> ComplexityLevel:
        """Assess overall solution complexity level"""
        
        complexity_score = 0
        
        # Company size factor
        if company_size > 1000:
            complexity_score += 3  # Enterprise
        elif company_size > 500:
            complexity_score += 2  # High
        elif company_size > 100:
            complexity_score += 1  # Medium
        # else: Low (0 points)
        
        # Industry complexity factor
        high_complexity_industries = ["fintech", "healthcare", "aerospace", "defense"]
        medium_complexity_industries = ["manufacturing", "retail", "education"]
        
        if any(ind in industry for ind in high_complexity_industries):
            complexity_score += 2
        elif any(ind in industry for ind in medium_complexity_industries):
            complexity_score += 1
        
        # Existing tech stack complexity
        enterprise_tech_indicators = ["kubernetes", "microservices", "enterprise", "oracle", "sap"]
        if any(tech.lower() for tech in existing_tech if any(indicator in tech.lower() for indicator in enterprise_tech_indicators)):
            complexity_score += 1
        
        # Solution requirements complexity
        if solution_requirements:
            if solution_requirements.get("multi_tenant", False):
                complexity_score += 1
            if solution_requirements.get("real_time_processing", False):
                complexity_score += 1
            if solution_requirements.get("global_deployment", False):
                complexity_score += 1
        
        # Map score to complexity level
        if complexity_score >= 6:
            return ComplexityLevel.ENTERPRISE
        elif complexity_score >= 4:
            return ComplexityLevel.HIGH
        elif complexity_score >= 2:
            return ComplexityLevel.MEDIUM
        else:
            return ComplexityLevel.LOW
    
    async def _analyze_integration_requirements(
        self,
        existing_tech: List[str],
        company_data: Dict[str, Any],
        solution_requirements: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze integration requirements with existing systems"""
        
        integrations = []
        
        if self.granite_client:
            try:
                prompt = f"""
                Analyze integration requirements for a company with these systems:
                Existing Technology: {existing_tech}
                Company Size: {company_data.get('company_size', 0)} employees
                Industry: {company_data.get('industry', 'Unknown')}
                
                Identify key integration points and provide technical analysis in JSON:
                {{
                    "critical_integrations": [
                        {{
                            "system": "CRM",
                            "complexity": "medium",
                            "method": "REST API",
                            "data_volume": "high",
                            "sync_frequency": "real-time"
                        }}
                    ],
                    "data_migration_needs": ["customer_data", "transaction_history"],
                    "api_requirements": ["authentication", "rate_limiting", "versioning"]
                }}
                """
                
                response = self.granite_client.generate(prompt, max_tokens=1024, temperature=0.3)
                
                try:
                    analysis = json.loads(response.content)
                    integrations.extend(analysis.get("critical_integrations", []))
                    
                    # Add additional integration metadata
                    if analysis.get("data_migration_needs"):
                        integrations.append({
                            "type": "data_migration",
                            "requirements": analysis["data_migration_needs"],
                            "complexity": "high"
                        })
                    
                    if analysis.get("api_requirements"):
                        integrations.append({
                            "type": "api_infrastructure", 
                            "requirements": analysis["api_requirements"],
                            "complexity": "medium"
                        })
                        
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Integration analysis failed: {e}")
        
        # Fallback integration analysis
        if not integrations and existing_tech:
            for tech in existing_tech[:3]:  # Limit to top 3 for simplicity
                integrations.append({
                    "system": tech,
                    "complexity": "medium",
                    "method": "API",
                    "estimated_effort": "2-4 weeks"
                })
        
        return integrations
    
    def _assess_scalability_requirements(self, company_size: int, complexity: ComplexityLevel) -> Dict[str, Any]:
        """Assess scalability requirements and projections"""
        
        # Base user projections
        current_users = max(company_size, 50)
        projected_growth = 1.5 if company_size < 500 else 1.2  # Smaller companies grow faster
        
        scalability = {
            "current_user_base": current_users,
            "projected_users_1yr": int(current_users * projected_growth),
            "projected_users_3yr": int(current_users * (projected_growth ** 2)),
            "concurrent_users": int(current_users * 0.2),  # 20% concurrent usage
            "peak_load_factor": 3.0,  # Peak is 3x normal load
            "data_growth_rate": 0.25,  # 25% annual data growth
        }
        
        # Adjust based on complexity
        if complexity == ComplexityLevel.ENTERPRISE:
            scalability["availability_requirement"] = "99.9%"
            scalability["performance_requirement"] = "<200ms response time"
            scalability["disaster_recovery"] = "4 hour RTO, 1 hour RPO"
        elif complexity == ComplexityLevel.HIGH:
            scalability["availability_requirement"] = "99.5%"
            scalability["performance_requirement"] = "<500ms response time"
            scalability["disaster_recovery"] = "24 hour RTO, 4 hour RPO"
        else:
            scalability["availability_requirement"] = "99.0%"
            scalability["performance_requirement"] = "<1s response time"
            scalability["disaster_recovery"] = "Basic backup and recovery"
        
        return scalability
    
    def _determine_security_requirements(self, industry: str, company_size: int) -> List[str]:
        """Determine security requirements based on industry and company size"""
        requirements = []
        
        # Base security requirements
        requirements.extend([
            "Multi-factor authentication",
            "Role-based access control",
            "Data encryption at rest and in transit",
            "Security monitoring and logging"
        ])
        
        # Industry-specific requirements
        if "fintech" in industry or "financial" in industry:
            requirements.extend([
                "PCI DSS compliance",
                "Fraud detection systems", 
                "Real-time transaction monitoring"
            ])
        elif "healthcare" in industry:
            requirements.extend([
                "HIPAA compliance",
                "PHI data protection",
                "Audit trail requirements"
            ])
        elif "government" in industry:
            requirements.extend([
                "FedRAMP compliance",
                "Authority to Operate (ATO)",
                "FISMA requirements"
            ])
        
        # Enterprise requirements
        if company_size > 500:
            requirements.extend([
                "Enterprise SSO integration",
                "Advanced threat protection",
                "Security incident response plan"
            ])
        
        return requirements
    
    def _identify_compliance_frameworks(self, industry: str) -> List[str]:
        """Identify applicable compliance frameworks"""
        frameworks = []
        
        # Universal frameworks
        frameworks.append("GDPR")  # Most companies need GDPR compliance
        
        # Industry-specific frameworks
        for framework, data in self.compliance_frameworks.items():
            if industry in data.get("industries", []) or "all" in data.get("industries", []):
                frameworks.append(framework)
        
        return frameworks
    
    async def _analyze_infrastructure_needs(
        self,
        company_size: int,
        complexity: ComplexityLevel,
        existing_tech: List[str]
    ) -> Dict[str, Any]:
        """Analyze infrastructure requirements and recommendations"""
        
        infrastructure = {}
        
        if self.granite_client:
            try:
                prompt = f"""
                Recommend infrastructure architecture for:
                Company Size: {company_size} employees
                Solution Complexity: {complexity.value}
                Existing Technology: {existing_tech}
                
                Provide infrastructure recommendations as JSON:
                {{
                    "hosting_recommendation": "cloud/hybrid/on-premise",
                    "cloud_services": ["compute", "database", "storage"],
                    "estimated_monthly_cost": 5000,
                    "scalability_approach": "auto-scaling",
                    "backup_strategy": "automated daily backups"
                }}
                """
                
                response = self.granite_client.generate(prompt, max_tokens=1024, temperature=0.3)
                
                try:
                    infra_rec = json.loads(response.content)
                    infrastructure.update(infra_rec)
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Infrastructure analysis failed: {e}")
        
        # Fallback infrastructure recommendations
        if not infrastructure:
            if company_size > 1000:
                infrastructure = {
                    "hosting_recommendation": "hybrid_cloud",
                    "estimated_monthly_cost": 15000,
                    "scalability_approach": "enterprise_auto_scaling",
                    "high_availability": True
                }
            elif company_size > 100:
                infrastructure = {
                    "hosting_recommendation": "cloud",
                    "estimated_monthly_cost": 5000,
                    "scalability_approach": "auto_scaling",
                    "high_availability": True
                }
            else:
                infrastructure = {
                    "hosting_recommendation": "cloud",
                    "estimated_monthly_cost": 1500,
                    "scalability_approach": "manual_scaling",
                    "high_availability": False
                }
        
        return infrastructure
    
    def _plan_implementation_phases(self, tech_arch: TechnicalArchitecture) -> List[Dict[str, Any]]:
        """Plan implementation phases based on complexity and requirements"""
        phases = []
        
        # Phase 1: Foundation and Core Systems
        phase1 = {
            "phase": 1,
            "name": "Foundation & Core Systems",
            "duration_weeks": 8 if tech_arch.solution_complexity == ComplexityLevel.LOW else 12,
            "activities": [
                "Infrastructure setup",
                "Core system implementation",
                "Basic security implementation",
                "Initial integrations"
            ]
        }
        phases.append(phase1)
        
        # Phase 2: Integrations and Advanced Features
        if tech_arch.solution_complexity != ComplexityLevel.LOW:
            phase2 = {
                "phase": 2,
                "name": "Integrations & Advanced Features",
                "duration_weeks": 6 if tech_arch.solution_complexity == ComplexityLevel.MEDIUM else 10,
                "activities": [
                    "System integrations",
                    "Advanced feature development",
                    "Performance optimization",
                    "Security hardening"
                ]
            }
            phases.append(phase2)
        
        # Phase 3: Enterprise Features and Compliance
        if tech_arch.solution_complexity in [ComplexityLevel.HIGH, ComplexityLevel.ENTERPRISE]:
            phase3 = {
                "phase": 3,
                "name": "Enterprise & Compliance",
                "duration_weeks": 8 if tech_arch.solution_complexity == ComplexityLevel.HIGH else 12,
                "activities": [
                    "Compliance framework implementation",
                    "Enterprise feature rollout",
                    "Advanced monitoring",
                    "User training and adoption"
                ]
            }
            phases.append(phase3)
        
        return phases
    
    def _estimate_implementation_timeline(self, tech_arch: TechnicalArchitecture) -> Dict[str, Any]:
        """Estimate implementation timeline"""
        total_weeks = sum(phase["duration_weeks"] for phase in tech_arch.implementation_phases)
        
        timeline = {
            "total_duration_weeks": total_weeks,
            "total_duration_months": round(total_weeks / 4.3, 1),
            "estimated_start_delay": 2,  # weeks to start
            "risk_buffer": round(total_weeks * 0.2),  # 20% risk buffer
            "milestone_count": len(tech_arch.implementation_phases)
        }
        
        # Add complexity-based adjustments
        complexity_multipliers = {
            ComplexityLevel.LOW: 1.0,
            ComplexityLevel.MEDIUM: 1.2,
            ComplexityLevel.HIGH: 1.4,
            ComplexityLevel.ENTERPRISE: 1.6
        }
        
        multiplier = complexity_multipliers.get(tech_arch.solution_complexity, 1.2)
        timeline["adjusted_duration_months"] = round(timeline["total_duration_months"] * multiplier, 1)
        
        return timeline
    
    def _calculate_resource_requirements(
        self,
        tech_arch: TechnicalArchitecture,
        company_size: int
    ) -> Dict[str, Any]:
        """Calculate technical resource requirements"""
        
        base_team_size = 3  # Minimum team
        
        # Adjust team size based on complexity
        complexity_multipliers = {
            ComplexityLevel.LOW: 1.0,
            ComplexityLevel.MEDIUM: 1.5,
            ComplexityLevel.HIGH: 2.0,
            ComplexityLevel.ENTERPRISE: 3.0
        }
        
        multiplier = complexity_multipliers.get(tech_arch.solution_complexity, 1.5)
        team_size = int(base_team_size * multiplier)
        
        resources = {
            "development_team_size": team_size,
            "technical_lead_required": True,
            "architect_required": tech_arch.solution_complexity in [ComplexityLevel.HIGH, ComplexityLevel.ENTERPRISE],
            "devops_specialist": team_size > 4,
            "security_specialist": len(tech_arch.compliance_frameworks) > 1,
            "estimated_monthly_cost": team_size * 15000,  # $15k per dev per month
            "external_consultants": tech_arch.solution_complexity == ComplexityLevel.ENTERPRISE
        }
        
        return resources
    
    def _assess_technical_risks(
        self,
        tech_arch: TechnicalArchitecture,
        existing_tech: List[str]
    ) -> List[Dict[str, Any]]:
        """Assess technical implementation risks"""
        risks = []
        
        # Complexity-based risks
        if tech_arch.solution_complexity in [ComplexityLevel.HIGH, ComplexityLevel.ENTERPRISE]:
            risks.append({
                "risk": "High complexity implementation challenges",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Experienced technical lead and phased approach"
            })
        
        # Integration risks
        if len(tech_arch.integration_requirements) > 3:
            risks.append({
                "risk": "Multiple integration points increase failure risk",
                "probability": "high",
                "impact": "medium",
                "mitigation": "Thorough API testing and fallback mechanisms"
            })
        
        # Legacy system risks
        legacy_indicators = ["mainframe", "cobol", "legacy", "deprecated"]
        if any(tech.lower() for tech in existing_tech if any(indicator in tech.lower() for indicator in legacy_indicators)):
            risks.append({
                "risk": "Legacy system integration challenges",
                "probability": "high",
                "impact": "high",
                "mitigation": "API gateway and data transformation layer"
            })
        
        # Scalability risks
        if tech_arch.scalability_assessment.get("projected_users_3yr", 0) > 10000:
            risks.append({
                "risk": "Scalability requirements may exceed initial architecture",
                "probability": "medium",
                "impact": "high",
                "mitigation": "Design for scalability from start, use microservices"
            })
        
        return risks
    
    def _assess_integration_risks(self, integration_count: int, complexity: ComplexityLevel) -> IntegrationRisk:
        """Assess overall integration risk level"""
        if integration_count == 0:
            return IntegrationRisk.LOW
        elif integration_count <= 2 and complexity == ComplexityLevel.LOW:
            return IntegrationRisk.LOW
        elif integration_count <= 3 and complexity != ComplexityLevel.ENTERPRISE:
            return IntegrationRisk.MEDIUM
        elif integration_count > 5 or complexity == ComplexityLevel.ENTERPRISE:
            return IntegrationRisk.CRITICAL
        else:
            return IntegrationRisk.HIGH
    
    async def _identify_modernization_opportunities(
        self,
        existing_tech: List[str],
        industry: str,
        crewai_results: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify technology modernization opportunities"""
        opportunities = []
        
        if self.granite_client:
            try:
                pain_points = crewai_results.get("pain_points", []) if crewai_results else []
                
                prompt = f"""
                Identify technology modernization opportunities for:
                Current Technology: {existing_tech}
                Industry: {industry}
                Business Challenges: {pain_points}
                
                Provide modernization opportunities as JSON array:
                ["Cloud migration for improved scalability", "API-first architecture for better integrations"]
                """
                
                response = self.granite_client.generate(prompt, max_tokens=512, temperature=0.3)
                
                try:
                    opps = json.loads(response.content)
                    if isinstance(opps, list):
                        opportunities = opps[:5]
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                self.logger.error(f"Modernization analysis failed: {e}")
        
        # Fallback modernization opportunities
        if not opportunities:
            opportunities = [
                "Cloud-native architecture for improved scalability",
                "API-first design for better system integration", 
                "Microservices architecture for team autonomy",
                "DevOps automation for faster deployment cycles",
                "Modern security frameworks for enhanced protection"
            ]
        
        return opportunities
    
    async def _create_technology_roadmap(
        self,
        tech_arch: TechnicalArchitecture,
        company_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create strategic technology roadmap"""
        roadmap = []
        
        # Immediate (0-6 months)
        immediate = {
            "timeframe": "0-6 months",
            "priority": "critical",
            "initiatives": [
                "Core system implementation",
                "Essential integrations",
                "Basic security measures"
            ]
        }
        roadmap.append(immediate)
        
        # Short-term (6-12 months)
        short_term = {
            "timeframe": "6-12 months", 
            "priority": "high",
            "initiatives": [
                "Advanced features rollout",
                "Performance optimization",
                "User training and adoption"
            ]
        }
        roadmap.append(short_term)
        
        # Medium-term (1-2 years)
        if tech_arch.solution_complexity in [ComplexityLevel.HIGH, ComplexityLevel.ENTERPRISE]:
            medium_term = {
                "timeframe": "1-2 years",
                "priority": "medium",
                "initiatives": [
                    "Scalability enhancements",
                    "Advanced analytics integration",
                    "Enterprise feature expansion"
                ]
            }
            roadmap.append(medium_term)
        
        return roadmap
    
    def _calculate_roi_technical_factors(self, tech_arch: TechnicalArchitecture) -> Dict[str, float]:
        """Calculate technical factors affecting ROI"""
        factors = {}
        
        # Implementation cost factor
        total_cost = tech_arch.resource_requirements.get("estimated_monthly_cost", 45000) * \
                    tech_arch.timeline_estimate.get("adjusted_duration_months", 6)
        
        factors["implementation_cost"] = total_cost
        factors["infrastructure_cost"] = tech_arch.infrastructure_needs.get("estimated_monthly_cost", 5000) * 12
        
        # Efficiency gains
        complexity_efficiency = {
            ComplexityLevel.LOW: 1.1,
            ComplexityLevel.MEDIUM: 1.3,
            ComplexityLevel.HIGH: 1.5,
            ComplexityLevel.ENTERPRISE: 1.8
        }
        factors["efficiency_multiplier"] = complexity_efficiency.get(tech_arch.solution_complexity, 1.3)
        
        # Risk adjustment
        risk_factors = {
            IntegrationRisk.LOW: 0.05,
            IntegrationRisk.MEDIUM: 0.15,
            IntegrationRisk.HIGH: 0.25,
            IntegrationRisk.CRITICAL: 0.40
        }
        factors["risk_adjustment"] = risk_factors.get(tech_arch.integration_risks, 0.15)
        
        return factors
    
    def _calculate_architecture_score(self, tech_arch: TechnicalArchitecture) -> float:
        """Calculate overall architecture quality score"""
        score_factors = []
        
        # Scalability score
        scalability = tech_arch.scalability_assessment
        if scalability.get("availability_requirement", "").startswith("99.9"):
            score_factors.append(0.9)
        elif scalability.get("availability_requirement", "").startswith("99."):
            score_factors.append(0.7)
        else:
            score_factors.append(0.5)
        
        # Security score
        security_score = min(len(tech_arch.security_requirements) / 10.0, 1.0)
        score_factors.append(security_score)
        
        # Integration score
        if tech_arch.integration_risks == IntegrationRisk.LOW:
            score_factors.append(0.9)
        elif tech_arch.integration_risks == IntegrationRisk.MEDIUM:
            score_factors.append(0.7)
        else:
            score_factors.append(0.5)
        
        # Modernization score
        modernization_score = min(len(tech_arch.modernization_opportunities) / 5.0, 1.0)
        score_factors.append(modernization_score)
        
        return sum(score_factors) / len(score_factors)
    
    def _calculate_feasibility_score(self, tech_arch: TechnicalArchitecture) -> float:
        """Calculate implementation feasibility score"""
        feasibility_factors = []
        
        # Timeline feasibility
        timeline_months = tech_arch.timeline_estimate.get("adjusted_duration_months", 6)
        if timeline_months <= 6:
            feasibility_factors.append(0.9)
        elif timeline_months <= 12:
            feasibility_factors.append(0.7)
        else:
            feasibility_factors.append(0.5)
        
        # Resource feasibility
        team_size = tech_arch.resource_requirements.get("development_team_size", 3)
        if team_size <= 5:
            feasibility_factors.append(0.8)
        elif team_size <= 8:
            feasibility_factors.append(0.6)
        else:
            feasibility_factors.append(0.4)
        
        # Risk feasibility
        risk_count = len(tech_arch.technical_risks)
        if risk_count <= 2:
            feasibility_factors.append(0.8)
        elif risk_count <= 4:
            feasibility_factors.append(0.6)
        else:
            feasibility_factors.append(0.4)
        
        return sum(feasibility_factors) / len(feasibility_factors)
    
    def _calculate_confidence_level(
        self,
        tech_arch: TechnicalArchitecture,
        crewai_results: Optional[Dict[str, Any]],
        solution_requirements: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate confidence level in the technical analysis"""
        confidence_factors = []
        
        # Data availability
        if crewai_results and crewai_results.get("tech_stack"):
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        # Requirements clarity
        if solution_requirements:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        # Analysis depth
        if len(tech_arch.integration_requirements) > 0:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)
        
        # Risk assessment completeness
        if len(tech_arch.technical_risks) >= 2:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        return sum(confidence_factors) / len(confidence_factors)
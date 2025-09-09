"""
Document Intelligence Agent - Advanced Intelligence Layer
Analyzes financial documents, contracts, and presentations for strategic insights
Extracts key intelligence from company documents to inform sales strategies
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import re

class DocumentType(Enum):
    FINANCIAL_REPORT = "financial_report"
    BOARD_PRESENTATION = "board_presentation"
    CONTRACT = "contract"
    PROPOSAL = "proposal"
    TECHNICAL_SPEC = "technical_specification"
    MEETING_MINUTES = "meeting_minutes"
    STRATEGIC_PLAN = "strategic_plan"

class ConfidenceLevel(Enum):
    LOW = "low"           # <60% confidence
    MEDIUM = "medium"     # 60-80% confidence
    HIGH = "high"         # >80% confidence
    VERY_HIGH = "very_high"  # >90% confidence

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FinancialAnalysis:
    """Financial document analysis results"""
    revenue_growth: str = ""
    burn_rate: str = ""
    runway_months: str = ""
    cash_position: str = ""
    customer_metrics: Dict[str, Any] = field(default_factory=dict)
    profitability_trends: str = ""
    funding_status: str = ""
    financial_health_score: float = 0.5
    key_financial_insights: List[str] = field(default_factory=list)

@dataclass
class ContractAnalysis:
    """Contract analysis results"""
    contract_type: str = ""
    remaining_duration: str = ""
    termination_clauses: List[str] = field(default_factory=list)
    renewal_terms: str = ""
    integration_requirements: List[str] = field(default_factory=list)
    switching_costs: str = ""
    risk_level: RiskLevel = RiskLevel.MEDIUM
    contract_insights: List[str] = field(default_factory=list)

@dataclass
class PresentationAnalysis:
    """Board/presentation analysis results"""
    strategic_priorities: List[str] = field(default_factory=list)
    budget_allocation: Dict[str, str] = field(default_factory=dict)
    timeline_commitments: List[str] = field(default_factory=list)
    executive_sentiment: str = ""
    growth_targets: Dict[str, Any] = field(default_factory=dict)
    pain_points_mentioned: List[str] = field(default_factory=list)
    opportunity_indicators: List[str] = field(default_factory=list)

@dataclass
class TechnicalRequirements:
    """Technical specification analysis"""
    technology_stack: List[str] = field(default_factory=list)
    integration_points: List[str] = field(default_factory=list)
    security_requirements: List[str] = field(default_factory=list)
    compliance_needs: List[str] = field(default_factory=list)
    scalability_requirements: str = ""
    performance_criteria: List[str] = field(default_factory=list)
    technical_constraints: List[str] = field(default_factory=list)

@dataclass
class StrategicIntelligence:
    """Strategic insights from documents"""
    business_objectives: List[str] = field(default_factory=list)
    growth_strategy: str = ""
    competitive_concerns: List[str] = field(default_factory=list)
    market_expansion_plans: List[str] = field(default_factory=list)
    technology_priorities: List[str] = field(default_factory=list)
    investment_focus: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)

@dataclass
class DocumentIntelligence:
    """Complete document intelligence analysis"""
    # Core analysis components
    financial_analysis: Optional[FinancialAnalysis] = None
    contract_analysis: Optional[ContractAnalysis] = None
    presentation_analysis: Optional[PresentationAnalysis] = None
    technical_requirements: Optional[TechnicalRequirements] = None
    strategic_intelligence: Optional[StrategicIntelligence] = None
    
    # Meta information
    documents_analyzed: List[str] = field(default_factory=list)
    analysis_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    data_extraction_score: float = 0.7
    intelligence_quality: float = 0.6
    
    # Key findings summary
    executive_summary: str = ""
    priority_insights: List[str] = field(default_factory=list)
    actionable_intelligence: List[str] = field(default_factory=list)
    sales_opportunities: List[str] = field(default_factory=list)
    
    # Analysis metadata
    analysis_date: datetime = field(default_factory=datetime.now)
    processing_time: float = 0.0

class DocumentIntelligenceAgent:
    """
    Advanced Document Intelligence Agent
    
    Provides comprehensive document analysis for strategic sales intelligence:
    - Financial document analysis for health assessment and opportunity sizing
    - Contract analysis for competitive positioning and switching cost evaluation
    - Board presentation analysis for strategic priority identification
    - Technical specification parsing for solution alignment
    - Strategic document mining for business intelligence
    - Cross-document pattern recognition for comprehensive insights
    """
    
    def __init__(self, granite_client=None, config: Optional[Dict[str, Any]] = None):
        self.granite_client = granite_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Document analysis models and patterns
        self.financial_patterns = self._initialize_financial_patterns()
        self.contract_patterns = self._initialize_contract_patterns()
        self.strategic_keywords = self._load_strategic_keywords()
        self.technical_frameworks = self._load_technical_frameworks()
        
    def _initialize_financial_patterns(self) -> Dict[str, Any]:
        """Initialize financial analysis patterns"""
        return {
            "revenue_indicators": [
                r"revenue.*(\$[\d,]+\.?\d*[MBK]?)",
                r"sales.*(\$[\d,]+\.?\d*[MBK]?)",
                r"(\d+)%.*growth",
                r"ARR.*(\$[\d,]+\.?\d*[MBK]?)",
                r"MRR.*(\$[\d,]+\.?\d*[MBK]?)"
            ],
            "burn_rate_indicators": [
                r"burn.*rate.*(\$[\d,]+\.?\d*[MBK]?)",
                r"monthly.*burn.*(\$[\d,]+\.?\d*[MBK]?)",
                r"cash.*burn.*(\$[\d,]+\.?\d*[MBK]?)"
            ],
            "runway_indicators": [
                r"(\d+).*months.*runway",
                r"runway.*(\d+).*months",
                r"cash.*runway.*(\d+)"
            ],
            "customer_metrics": [
                r"(\d+)%.*churn",
                r"churn.*(\d+)%",
                r"ACV.*(\$[\d,]+\.?\d*[K]?)",
                r"LTV.*(\$[\d,]+\.?\d*[K]?)",
                r"CAC.*(\$[\d,]+\.?\d*[K]?)"
            ],
            "health_indicators": {
                "positive": ["profitable", "growing", "strong", "healthy", "positive", "increasing", "up"],
                "negative": ["loss", "declining", "weak", "concerning", "negative", "decreasing", "down"],
                "neutral": ["stable", "flat", "maintaining", "steady"]
            }
        }
    
    def _initialize_contract_patterns(self) -> Dict[str, Any]:
        """Initialize contract analysis patterns"""
        return {
            "termination_clauses": [
                r"(\d+).*days.*notice",
                r"terminate.*(\d+).*days",
                r"cancellation.*(\d+).*days",
                r"early.*termination",
                r"for.*cause.*termination"
            ],
            "renewal_terms": [
                r"auto.*renew",
                r"automatic.*renewal",
                r"(\d+).*year.*term",
                r"month.*to.*month",
                r"annual.*renewal"
            ],
            "integration_requirements": [
                r"API.*access",
                r"integration.*required",
                r"data.*migration",
                r"SSO.*integration",
                r"webhook.*support"
            ],
            "switching_costs": {
                "high": ["migration", "training", "integration", "customization", "data transfer"],
                "medium": ["setup", "configuration", "onboarding"],
                "low": ["minimal", "easy", "simple", "quick"]
            }
        }
    
    def _load_strategic_keywords(self) -> Dict[str, List[str]]:
        """Load strategic keyword patterns"""
        return {
            "growth_priorities": [
                "scale", "expansion", "growth", "increase market share", "customer acquisition",
                "geographic expansion", "product development", "innovation", "digital transformation"
            ],
            "cost_concerns": [
                "cost reduction", "efficiency", "optimize", "streamline", "automation",
                "reduce overhead", "improve margins", "cost savings"
            ],
            "technology_focus": [
                "AI", "machine learning", "cloud", "digital", "automation", "analytics",
                "modernization", "infrastructure", "platform", "integration"
            ],
            "competitive_threats": [
                "competitive pressure", "market share", "differentiation", "competitive advantage",
                "threat", "disruption", "new entrants"
            ],
            "urgency_indicators": [
                "immediate", "urgent", "critical", "priority", "must have", "deadline",
                "time-sensitive", "Q1", "Q2", "Q3", "Q4", "by end of year"
            ]
        }
    
    def _load_technical_frameworks(self) -> Dict[str, List[str]]:
        """Load technical framework patterns"""
        return {
            "cloud_platforms": ["AWS", "Azure", "GCP", "Google Cloud", "IBM Cloud"],
            "programming_languages": ["Python", "Java", "JavaScript", "C#", "Go", "Ruby"],
            "databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch"],
            "frameworks": ["React", "Angular", "Node.js", "Django", "Spring", "Rails"],
            "security_standards": ["SOC2", "ISO 27001", "HIPAA", "GDPR", "PCI DSS"],
            "integration_protocols": ["REST", "GraphQL", "gRPC", "Webhook", "API Gateway"]
        }
    
    async def analyze_documents(
        self,
        documents: List[Dict[str, Any]],
        company_data: Dict[str, Any],
        analysis_scope: Optional[List[str]] = None
    ) -> DocumentIntelligence:
        """
        Analyze multiple documents for comprehensive intelligence
        
        Documents should be provided as:
        [
            {
                "type": "financial_report",
                "content": "document text content",
                "metadata": {"date": "2024-01-01", "source": "Q4 Board Deck"}
            }
        ]
        """
        
        start_time = datetime.now()
        intelligence = DocumentIntelligence()
        
        try:
            self.logger.info(f"Analyzing {len(documents)} documents for {company_data.get('company_name', 'Unknown')}")
            
            # Categorize documents by type
            doc_categories = self._categorize_documents(documents)
            
            # Run analysis tasks in parallel
            tasks = []
            
            if doc_categories.get("financial"):
                tasks.append(self._analyze_financial_documents(doc_categories["financial"], company_data))
            
            if doc_categories.get("contracts"):
                tasks.append(self._analyze_contract_documents(doc_categories["contracts"]))
            
            if doc_categories.get("presentations"):
                tasks.append(self._analyze_presentation_documents(doc_categories["presentations"]))
            
            if doc_categories.get("technical"):
                tasks.append(self._analyze_technical_documents(doc_categories["technical"]))
            
            # Always run strategic analysis on all documents
            tasks.append(self._extract_strategic_intelligence(documents))
            
            # Execute analysis tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results based on what was analyzed
            result_index = 0
            
            if doc_categories.get("financial"):
                result = results[result_index]
                if isinstance(result, FinancialAnalysis):
                    intelligence.financial_analysis = result
                elif not isinstance(result, Exception):
                    intelligence.financial_analysis = result
                else:
                    intelligence.financial_analysis = FinancialAnalysis()
                result_index += 1
            
            if doc_categories.get("contracts"):
                result = results[result_index]
                if isinstance(result, ContractAnalysis):
                    intelligence.contract_analysis = result
                elif not isinstance(result, Exception):
                    intelligence.contract_analysis = result
                else:
                    intelligence.contract_analysis = ContractAnalysis()
                result_index += 1
            
            if doc_categories.get("presentations"):
                result = results[result_index]
                if isinstance(result, PresentationAnalysis):
                    intelligence.presentation_analysis = result
                elif not isinstance(result, Exception):
                    intelligence.presentation_analysis = result
                else:
                    intelligence.presentation_analysis = PresentationAnalysis()
                result_index += 1
            
            if doc_categories.get("technical"):
                result = results[result_index]
                if isinstance(result, TechnicalRequirements):
                    intelligence.technical_requirements = result
                elif not isinstance(result, Exception):
                    intelligence.technical_requirements = result
                else:
                    intelligence.technical_requirements = TechnicalRequirements()
                result_index += 1
            
            # Strategic intelligence is always last
            strategic_result = results[-1]
            if isinstance(strategic_result, StrategicIntelligence):
                intelligence.strategic_intelligence = strategic_result
            elif not isinstance(strategic_result, Exception):
                intelligence.strategic_intelligence = strategic_result
            else:
                intelligence.strategic_intelligence = StrategicIntelligence()
            
            # Generate comprehensive analysis
            intelligence.executive_summary = self._generate_executive_summary(intelligence)
            intelligence.priority_insights = self._extract_priority_insights(intelligence)
            intelligence.actionable_intelligence = self._generate_actionable_intelligence(intelligence)
            intelligence.sales_opportunities = self._identify_sales_opportunities(intelligence, company_data)
            
            # Calculate quality metrics
            intelligence.analysis_confidence = self._calculate_analysis_confidence(intelligence, documents)
            intelligence.data_extraction_score = self._assess_extraction_quality(documents)
            intelligence.intelligence_quality = self._assess_intelligence_quality(intelligence)
            
            # Set metadata
            intelligence.documents_analyzed = [doc.get("metadata", {}).get("source", f"Document {i+1}") for i, doc in enumerate(documents)]
            intelligence.processing_time = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"Document analysis completed in {intelligence.processing_time:.2f}s with {intelligence.analysis_confidence.value} confidence")
            return intelligence
            
        except Exception as e:
            self.logger.error(f"Document analysis failed: {e}")
            intelligence.processing_time = (datetime.now() - start_time).total_seconds()
            return intelligence
    
    def _categorize_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize documents by type for targeted analysis"""
        categories = {
            "financial": [],
            "contracts": [],
            "presentations": [],
            "technical": [],
            "strategic": []
        }
        
        for doc in documents:
            doc_type = doc.get("type", "").lower()
            content = doc.get("content", "").lower()
            
            # Categorize by explicit type
            if doc_type in ["financial_report", "financial"]:
                categories["financial"].append(doc)
            elif doc_type in ["contract", "agreement"]:
                categories["contracts"].append(doc)
            elif doc_type in ["board_presentation", "presentation", "deck"]:
                categories["presentations"].append(doc)
            elif doc_type in ["technical_spec", "technical", "requirements"]:
                categories["technical"].append(doc)
            elif doc_type in ["strategic_plan", "strategy"]:
                categories["strategic"].append(doc)
            else:
                # Auto-categorize based on content
                if any(keyword in content for keyword in ["revenue", "financial", "earnings", "cash flow"]):
                    categories["financial"].append(doc)
                elif any(keyword in content for keyword in ["contract", "agreement", "terms", "sla"]):
                    categories["contracts"].append(doc)
                elif any(keyword in content for keyword in ["board", "executive", "presentation", "strategic"]):
                    categories["presentations"].append(doc)
                elif any(keyword in content for keyword in ["api", "technical", "architecture", "requirements"]):
                    categories["technical"].append(doc)
                else:
                    categories["strategic"].append(doc)
        
        return categories
    
    async def _analyze_financial_documents(
        self, 
        financial_docs: List[Dict[str, Any]], 
        company_data: Dict[str, Any]
    ) -> FinancialAnalysis:
        """Analyze financial documents for business health insights"""
        
        analysis = FinancialAnalysis()
        
        try:
            # Combine all financial document content
            combined_content = " ".join([doc.get("content", "") for doc in financial_docs])
            
            # Use AI for enhanced analysis if available
            if self.granite_client and combined_content:
                analysis = await self._ai_enhanced_financial_analysis(combined_content, company_data)
            else:
                # Rule-based financial analysis
                analysis = self._rule_based_financial_analysis(combined_content)
            
            # Extract specific metrics using pattern matching
            analysis = self._extract_financial_metrics(analysis, combined_content)
            
        except Exception as e:
            self.logger.error(f"Financial document analysis failed: {e}")
        
        return analysis
    
    async def _ai_enhanced_financial_analysis(
        self, 
        content: str, 
        company_data: Dict[str, Any]
    ) -> FinancialAnalysis:
        """Use IBM Granite for advanced financial analysis"""
        
        analysis = FinancialAnalysis()
        
        try:
            company_size = company_data.get("company_size", 0)
            industry = company_data.get("industry", "")
            
            prompt = f"""
            Analyze financial health from this document content for a {company_size}-person {industry} company:
            
            Content: {content[:2000]}...
            
            Extract and analyze:
            1. Revenue growth rate and trends
            2. Monthly burn rate and cash runway
            3. Customer metrics (churn, ACV, etc.)
            4. Overall financial health assessment
            5. Key financial insights and concerns
            
            Provide analysis in this JSON format:
            {{
                "revenue_growth": "X% YoY growth trend",
                "burn_rate": "$X/month burn rate", 
                "runway_months": "X months runway",
                "cash_position": "Strong/Moderate/Weak for X months",
                "customer_metrics": {{"churn": "X%", "ACV": "$X"}},
                "financial_health_score": 0.8,
                "key_insights": ["insight1", "insight2"]
            }}
            """
            
            if self.granite_client:
                response = self.granite_client.generate(prompt, max_tokens=1024, temperature=0.3)
            else:
                # Fallback when no client available
                return self._rule_based_financial_analysis(content)
            
            try:
                financial_data = json.loads(response.content)
                
                analysis.revenue_growth = financial_data.get("revenue_growth", "")
                analysis.burn_rate = financial_data.get("burn_rate", "")
                analysis.runway_months = financial_data.get("runway_months", "")
                analysis.cash_position = financial_data.get("cash_position", "")
                analysis.customer_metrics = financial_data.get("customer_metrics", {})
                analysis.financial_health_score = financial_data.get("financial_health_score", 0.5)
                analysis.key_financial_insights = financial_data.get("key_insights", [])
                
                return analysis
                
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse AI financial analysis response")
                
        except Exception as e:
            self.logger.error(f"AI financial analysis failed: {e}")
        
        # Fallback to rule-based analysis
        return self._rule_based_financial_analysis(content)
    
    def _rule_based_financial_analysis(self, content: str) -> FinancialAnalysis:
        """Rule-based financial analysis fallback"""
        
        analysis = FinancialAnalysis()
        content_lower = content.lower()
        
        # Extract revenue information
        for pattern in self.financial_patterns["revenue_indicators"]:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            if matches:
                analysis.revenue_growth = f"Found revenue indicators: {matches[0]}"
                break
        
        # Extract burn rate
        for pattern in self.financial_patterns["burn_rate_indicators"]:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            if matches:
                analysis.burn_rate = f"{matches[0]} monthly burn rate"
                break
        
        # Extract runway
        for pattern in self.financial_patterns["runway_indicators"]:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            if matches:
                analysis.runway_months = f"{matches[0]} months runway"
                break
        
        # Assess financial health based on keywords
        positive_count = sum(1 for word in self.financial_patterns["health_indicators"]["positive"] if word in content_lower)
        negative_count = sum(1 for word in self.financial_patterns["health_indicators"]["negative"] if word in content_lower)
        
        if positive_count > negative_count:
            analysis.financial_health_score = 0.7
            analysis.cash_position = "Strong financial position indicated"
        elif negative_count > positive_count:
            analysis.financial_health_score = 0.3
            analysis.cash_position = "Financial concerns indicated"
        else:
            analysis.financial_health_score = 0.5
            analysis.cash_position = "Moderate financial position"
        
        return analysis
    
    def _extract_financial_metrics(self, analysis: FinancialAnalysis, content: str) -> FinancialAnalysis:
        """Extract specific financial metrics using pattern matching"""
        
        # Extract customer metrics
        customer_metrics = {}
        for pattern in self.financial_patterns["customer_metrics"]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                if "churn" in pattern.lower():
                    customer_metrics["churn_rate"] = matches[0]
                elif "acv" in pattern.lower():
                    customer_metrics["ACV"] = matches[0]
                elif "ltv" in pattern.lower():
                    customer_metrics["LTV"] = matches[0]
                elif "cac" in pattern.lower():
                    customer_metrics["CAC"] = matches[0]
        
        if customer_metrics:
            analysis.customer_metrics.update(customer_metrics)
        
        return analysis
    
    async def _analyze_contract_documents(self, contract_docs: List[Dict[str, Any]]) -> ContractAnalysis:
        """Analyze contract documents for switching cost assessment"""
        
        analysis = ContractAnalysis()
        
        try:
            # Combine contract content
            combined_content = " ".join([doc.get("content", "") for doc in contract_docs])
            
            # Extract termination clauses
            for pattern in self.contract_patterns["termination_clauses"]:
                matches = re.findall(pattern, combined_content, re.IGNORECASE)
                if matches:
                    analysis.termination_clauses.append(f"{matches[0]} days notice required")
            
            # Extract renewal terms
            for pattern in self.contract_patterns["renewal_terms"]:
                matches = re.findall(pattern, combined_content, re.IGNORECASE)
                if matches:
                    analysis.renewal_terms = f"Found renewal terms: {matches[0]}"
                    break
            
            # Assess switching costs
            content_lower = combined_content.lower()
            high_cost_indicators = sum(1 for indicator in self.contract_patterns["switching_costs"]["high"] if indicator in content_lower)
            medium_cost_indicators = sum(1 for indicator in self.contract_patterns["switching_costs"]["medium"] if indicator in content_lower)
            low_cost_indicators = sum(1 for indicator in self.contract_patterns["switching_costs"]["low"] if indicator in content_lower)
            
            if high_cost_indicators > medium_cost_indicators and high_cost_indicators > low_cost_indicators:
                analysis.switching_costs = "High switching costs - complex migration required"
                analysis.risk_level = RiskLevel.HIGH
            elif low_cost_indicators > high_cost_indicators:
                analysis.switching_costs = "Low switching costs - minimal barriers"
                analysis.risk_level = RiskLevel.LOW
            else:
                analysis.switching_costs = "Moderate switching costs"
                analysis.risk_level = RiskLevel.MEDIUM
            
        except Exception as e:
            self.logger.error(f"Contract analysis failed: {e}")
        
        return analysis
    
    async def _analyze_presentation_documents(self, presentation_docs: List[Dict[str, Any]]) -> PresentationAnalysis:
        """Analyze board presentations for strategic insights"""
        
        analysis = PresentationAnalysis()
        
        try:
            combined_content = " ".join([doc.get("content", "") for doc in presentation_docs])
            
            # Extract strategic priorities
            for priority in self.strategic_keywords["growth_priorities"]:
                if priority.lower() in combined_content.lower():
                    analysis.strategic_priorities.append(priority)
            
            # Extract budget information
            budget_patterns = [
                r"(\d+)%.*to\s+(\w+)",
                r"budget.*(\d+)%.*(\w+)",
                r"allocate.*(\d+)%.*(\w+)"
            ]
            
            for pattern in budget_patterns:
                matches = re.findall(pattern, combined_content, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        analysis.budget_allocation[match[1]] = f"{match[0]}%"
            
            # Identify pain points mentioned
            pain_indicators = ["challenge", "problem", "issue", "concern", "bottleneck", "inefficiency"]
            for indicator in pain_indicators:
                if indicator in combined_content.lower():
                    analysis.pain_points_mentioned.append(f"Mentioned {indicator}s in strategy")
            
            # Extract timeline commitments
            timeline_patterns = [
                r"by\s+(Q[1-4])",
                r"(Q[1-4])\s+\d{4}",
                r"end\s+of\s+(\d{4})",
                r"next\s+(\d+)\s+months"
            ]
            
            for pattern in timeline_patterns:
                matches = re.findall(pattern, combined_content, re.IGNORECASE)
                analysis.timeline_commitments.extend([f"Commitment by {match}" for match in matches])
            
        except Exception as e:
            self.logger.error(f"Presentation analysis failed: {e}")
        
        return analysis
    
    async def _analyze_technical_documents(self, technical_docs: List[Dict[str, Any]]) -> TechnicalRequirements:
        """Analyze technical documents for requirements and constraints"""
        
        requirements = TechnicalRequirements()
        
        try:
            combined_content = " ".join([doc.get("content", "") for doc in technical_docs])
            content_lower = combined_content.lower()
            
            # Identify technology stack
            for category, technologies in self.technical_frameworks.items():
                for tech in technologies:
                    if tech.lower() in content_lower:
                        requirements.technology_stack.append(tech)
            
            # Extract security requirements
            for standard in self.technical_frameworks["security_standards"]:
                if standard.lower() in content_lower:
                    requirements.security_requirements.append(f"{standard} compliance required")
            
            # Identify integration requirements
            integration_keywords = ["integration", "api", "webhook", "sso", "saml", "oauth"]
            for keyword in integration_keywords:
                if keyword in content_lower:
                    requirements.integration_points.append(f"{keyword.upper()} integration")
            
            # Extract scalability requirements
            scalability_patterns = [
                r"support.*(\d+).*users",
                r"handle.*(\d+).*requests",
                r"scale.*to.*(\d+)",
                r"(\d+).*concurrent"
            ]
            
            for pattern in scalability_patterns:
                matches = re.findall(pattern, content_lower)
                if matches:
                    requirements.scalability_requirements = f"Must support {matches[0]} scale"
                    break
            
        except Exception as e:
            self.logger.error(f"Technical analysis failed: {e}")
        
        return requirements
    
    async def _extract_strategic_intelligence(self, all_docs: List[Dict[str, Any]]) -> StrategicIntelligence:
        """Extract strategic intelligence from all documents"""
        
        intelligence = StrategicIntelligence()
        
        try:
            combined_content = " ".join([doc.get("content", "") for doc in all_docs])
            content_lower = combined_content.lower()
            
            # Extract business objectives
            objective_patterns = ["goal", "objective", "target", "initiative", "strategy", "priority"]
            for pattern in objective_patterns:
                # Look for sentences containing these patterns
                sentences = re.findall(rf'[^.]*{pattern}[^.]*\.', content_lower)
                intelligence.business_objectives.extend(sentences[:3])  # Top 3
            
            # Identify growth strategy
            growth_indicators = self.strategic_keywords["growth_priorities"]
            mentioned_growth = [indicator for indicator in growth_indicators if indicator in content_lower]
            if mentioned_growth:
                intelligence.growth_strategy = f"Focus on: {', '.join(mentioned_growth[:3])}"
            
            # Extract competitive concerns
            for concern in self.strategic_keywords["competitive_threats"]:
                if concern in content_lower:
                    intelligence.competitive_concerns.append(concern)
            
            # Identify technology priorities
            tech_priorities = self.strategic_keywords["technology_focus"]
            mentioned_tech = [tech for tech in tech_priorities if tech in content_lower]
            intelligence.technology_priorities = mentioned_tech[:5]
            
            # Extract urgency indicators
            urgency_found = [indicator for indicator in self.strategic_keywords["urgency_indicators"] if indicator in content_lower]
            if urgency_found:
                intelligence.risk_factors.append(f"Time-sensitive priorities: {', '.join(urgency_found[:3])}")
            
        except Exception as e:
            self.logger.error(f"Strategic intelligence extraction failed: {e}")
        
        return intelligence
    
    def _generate_executive_summary(self, intelligence: DocumentIntelligence) -> str:
        """Generate executive summary of key findings"""
        
        summary_parts = []
        
        # Financial summary
        if intelligence.financial_analysis and intelligence.financial_analysis.revenue_growth:
            summary_parts.append(f"Financial Health: {intelligence.financial_analysis.cash_position}")
        
        # Strategic summary
        if intelligence.strategic_intelligence and intelligence.strategic_intelligence.growth_strategy:
            summary_parts.append(f"Growth Strategy: {intelligence.strategic_intelligence.growth_strategy}")
        
        # Contract summary
        if intelligence.contract_analysis and intelligence.contract_analysis.switching_costs:
            summary_parts.append(f"Switching Costs: {intelligence.contract_analysis.switching_costs}")
        
        # Technical summary
        if intelligence.technical_requirements and intelligence.technical_requirements.technology_stack:
            tech_stack = ", ".join(intelligence.technical_requirements.technology_stack[:3])
            summary_parts.append(f"Technology Stack: {tech_stack}")
        
        if not summary_parts:
            return "Document analysis completed with strategic insights extracted for sales intelligence."
        
        return " | ".join(summary_parts)
    
    def _extract_priority_insights(self, intelligence: DocumentIntelligence) -> List[str]:
        """Extract priority insights from analysis"""
        
        insights = []
        
        # Financial insights
        if intelligence.financial_analysis:
            if intelligence.financial_analysis.financial_health_score > 0.7:
                insights.append("Strong financial position supports larger investments")
            elif intelligence.financial_analysis.financial_health_score < 0.4:
                insights.append("Financial constraints may require value-focused approach")
            
            if intelligence.financial_analysis.key_financial_insights:
                insights.extend(intelligence.financial_analysis.key_financial_insights[:2])
        
        # Strategic insights
        if intelligence.strategic_intelligence:
            if intelligence.strategic_intelligence.technology_priorities:
                tech_focus = ", ".join(intelligence.strategic_intelligence.technology_priorities[:2])
                insights.append(f"Technology focus areas: {tech_focus}")
        
        # Presentation insights
        if intelligence.presentation_analysis:
            if intelligence.presentation_analysis.strategic_priorities:
                priorities = ", ".join(intelligence.presentation_analysis.strategic_priorities[:2])
                insights.append(f"Strategic priorities: {priorities}")
        
        return insights[:5]  # Top 5 insights
    
    def _generate_actionable_intelligence(self, intelligence: DocumentIntelligence) -> List[str]:
        """Generate actionable intelligence for sales strategy"""
        
        actions = []
        
        # Financial-based actions
        if intelligence.financial_analysis:
            if intelligence.financial_analysis.runway_months:
                actions.append(f"Timing consideration: {intelligence.financial_analysis.runway_months}")
            
            if intelligence.financial_analysis.customer_metrics:
                actions.append("Customer metrics available for ROI discussions")
        
        # Contract-based actions
        if intelligence.contract_analysis:
            if intelligence.contract_analysis.risk_level == RiskLevel.LOW:
                actions.append("Low switching costs create opportunity for easy transition")
            elif intelligence.contract_analysis.risk_level == RiskLevel.HIGH:
                actions.append("High switching costs require comprehensive migration planning")
        
        # Technical-based actions
        if intelligence.technical_requirements:
            if intelligence.technical_requirements.security_requirements:
                actions.append("Security compliance requirements identified for solution alignment")
            
            if intelligence.technical_requirements.integration_points:
                actions.append("Integration requirements defined for technical discussions")
        
        # Strategic-based actions
        if intelligence.strategic_intelligence:
            if intelligence.strategic_intelligence.competitive_concerns:
                actions.append("Competitive concerns identified for differentiation strategy")
        
        return actions[:6]  # Top 6 actions
    
    def _identify_sales_opportunities(
        self, 
        intelligence: DocumentIntelligence, 
        company_data: Dict[str, Any]
    ) -> List[str]:
        """Identify specific sales opportunities from document analysis"""
        
        opportunities = []
        
        # Financial opportunities
        if intelligence.financial_analysis:
            if intelligence.financial_analysis.financial_health_score > 0.6:
                opportunities.append("Strong financial position supports premium solution positioning")
            
            if "growth" in intelligence.financial_analysis.revenue_growth.lower():
                opportunities.append("Revenue growth trend supports expansion conversation")
        
        # Strategic opportunities
        if intelligence.strategic_intelligence:
            tech_priorities = intelligence.strategic_intelligence.technology_priorities
            if any(tech in ["AI", "automation", "cloud"] for tech in tech_priorities):
                opportunities.append("Technology modernization priorities align with solution capabilities")
        
        # Presentation opportunities
        if intelligence.presentation_analysis:
            if intelligence.presentation_analysis.pain_points_mentioned:
                opportunities.append("Pain points identified for solution positioning")
            
            if intelligence.presentation_analysis.budget_allocation:
                opportunities.append("Budget allocation information available for investment discussions")
        
        # Contract opportunities
        if intelligence.contract_analysis:
            if intelligence.contract_analysis.termination_clauses:
                opportunities.append("Contract termination options provide window for transition")
        
        # Urgency opportunities
        if intelligence.strategic_intelligence and intelligence.strategic_intelligence.risk_factors:
            risk_factors = " ".join(intelligence.strategic_intelligence.risk_factors).lower()
            if any(indicator in risk_factors for indicator in ["q1", "q2", "q3", "q4", "deadline"]):
                opportunities.append("Time-sensitive priorities create urgency for decision")
        
        return opportunities[:5]  # Top 5 opportunities
    
    def _calculate_analysis_confidence(
        self, 
        intelligence: DocumentIntelligence, 
        documents: List[Dict[str, Any]]
    ) -> ConfidenceLevel:
        """Calculate confidence level based on analysis completeness"""
        
        confidence_factors = []
        
        # Document quantity factor
        doc_count = len(documents)
        if doc_count >= 5:
            confidence_factors.append(0.9)
        elif doc_count >= 3:
            confidence_factors.append(0.7)
        elif doc_count >= 1:
            confidence_factors.append(0.5)
        else:
            confidence_factors.append(0.3)
        
        # Analysis completeness factor
        analysis_components = sum([
            bool(intelligence.financial_analysis),
            bool(intelligence.contract_analysis),
            bool(intelligence.presentation_analysis),
            bool(intelligence.technical_requirements),
            bool(intelligence.strategic_intelligence)
        ])
        
        completeness_score = analysis_components / 5.0
        confidence_factors.append(completeness_score)
        
        # Content quality factor
        total_content_length = sum(len(doc.get("content", "")) for doc in documents)
        if total_content_length > 5000:
            confidence_factors.append(0.8)
        elif total_content_length > 2000:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)
        
        # Calculate overall confidence
        avg_confidence = sum(confidence_factors) / len(confidence_factors)
        
        if avg_confidence >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        elif avg_confidence >= 0.7:
            return ConfidenceLevel.HIGH
        elif avg_confidence >= 0.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _assess_extraction_quality(self, documents: List[Dict[str, Any]]) -> float:
        """Assess quality of data extraction from documents"""
        
        quality_factors = []
        
        # Document structure quality
        structured_docs = sum(1 for doc in documents if doc.get("type") and doc.get("metadata"))
        structure_quality = structured_docs / len(documents) if documents else 0
        quality_factors.append(structure_quality)
        
        # Content richness
        avg_content_length = sum(len(doc.get("content", "")) for doc in documents) / len(documents) if documents else 0
        content_quality = min(1.0, avg_content_length / 2000)  # Normalize to 2000 chars
        quality_factors.append(content_quality)
        
        # Metadata completeness
        docs_with_metadata = sum(1 for doc in documents if doc.get("metadata", {}).get("date"))
        metadata_quality = docs_with_metadata / len(documents) if documents else 0
        quality_factors.append(metadata_quality)
        
        return sum(quality_factors) / len(quality_factors)
    
    def _assess_intelligence_quality(self, intelligence: DocumentIntelligence) -> float:
        """Assess quality of extracted intelligence"""
        
        quality_factors = []
        
        # Insights richness
        total_insights = (
            len(intelligence.priority_insights) +
            len(intelligence.actionable_intelligence) +
            len(intelligence.sales_opportunities)
        )
        insights_quality = min(1.0, total_insights / 15)  # Normalize to 15 total insights
        quality_factors.append(insights_quality)
        
        # Analysis depth
        analysis_depth = sum([
            len(intelligence.financial_analysis.key_financial_insights) if intelligence.financial_analysis else 0,
            len(intelligence.strategic_intelligence.business_objectives) if intelligence.strategic_intelligence else 0,
            len(intelligence.presentation_analysis.strategic_priorities) if intelligence.presentation_analysis else 0
        ])
        depth_quality = min(1.0, analysis_depth / 10)  # Normalize to 10 detailed items
        quality_factors.append(depth_quality)
        
        return sum(quality_factors) / len(quality_factors)
    
    # Utility methods for CrewAI integration
    def get_crew_agents(self) -> List[Dict[str, Any]]:
        """Get CrewAI agent definitions for document intelligence"""
        return [
            {
                "role": "Financial Document Analyst",
                "goal": "Extract financial health indicators and business metrics from documents",
                "backstory": "Financial analyst specializing in business health assessment and opportunity sizing",
                "tools": ["financial_analysis", "metrics_extraction", "health_assessment"]
            },
            {
                "role": "Contract Intelligence Specialist",
                "goal": "Analyze contracts and agreements for switching costs and competitive positioning",
                "backstory": "Legal and procurement expert focused on contract analysis and risk assessment",
                "tools": ["contract_analysis", "risk_assessment", "switching_cost_evaluation"]
            },
            {
                "role": "Strategic Document Miner",
                "goal": "Extract strategic insights and business intelligence from corporate documents",
                "backstory": "Business intelligence analyst specialized in strategic document analysis",
                "tools": ["strategic_analysis", "business_intelligence", "opportunity_identification"]
            }
        ]
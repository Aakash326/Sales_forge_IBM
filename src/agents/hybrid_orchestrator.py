"""
Hybrid Orchestrator - Complete Workflow and IBM Agent Integration
Connects all workflow agents (CrewAI tactical) with IBM strategic agents
This is the main orchestrator that coordinates the full 2-tier architecture
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import workflow components
from ..workflow.examples.fast_workflow import FastSalesPipeline

# Import strategic orchestrator for IBM agents
from .strategic_orchestrator import StrategicOrchestrator

# Import IBM client
from ..ibm_integrations.granite_client import create_granite_client

class HybridOrchestrator:
    """
    Hybrid Orchestrator - Complete Sales Intelligence Platform
    
    Coordinates the full 2-tier architecture:
    1. CrewAI Tactical Layer (FastSalesPipeline): Lead research, scoring, outreach
    2. IBM Strategic Layer (StrategicOrchestrator): Market intel, tech arch, executive ROI
    
    Flow: Lead Data � CrewAI (49s) � IBM Strategic (2-5min) � Executive Dashboard
    """
    
    def __init__(self, granite_client=None, config: Dict[str, Any] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        
        # Initialize CrewAI tactical pipeline
        self.crewai_pipeline = FastSalesPipeline()
        self.logger.info("CrewAI tactical pipeline initialized")
        
        # Initialize IBM client if not provided
        if granite_client is None:
            try:
                granite_client = create_granite_client(
                    model_name="granite-3.0-8b-instruct",
                    backend="watsonx"
                )
                self.logger.info("IBM Granite client initialized")
            except Exception as e:
                self.logger.warning(f"IBM client initialization failed: {e}")
                granite_client = None
        
        self.granite_client = granite_client
        
        # Initialize strategic orchestrator with IBM agents
        self.strategic_orchestrator = StrategicOrchestrator(
            granite_client=granite_client,
            config=config or {}
        )
        self.logger.info("Strategic orchestrator initialized")
    
    async def run_complete_intelligence_pipeline(
        self, 
        lead_data: Dict[str, Any],
        include_strategic: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete intelligence pipeline
        
        Args:
            lead_data: Company and contact information
            include_strategic: Whether to run IBM strategic analysis
            
        Returns:
            Complete intelligence report with tactical and strategic layers
        """
        
        self.logger.info(f"Starting complete intelligence pipeline for {lead_data.get('company_name', 'Unknown')}")
        start_time = datetime.now()
        
        # Phase 1: CrewAI Tactical Intelligence
        self.logger.info("Phase 1: Executing CrewAI tactical intelligence")
        tactical_start = datetime.now()
        
        try:
            tactical_results = self.crewai_pipeline.run_fast(lead_data)
            tactical_time = (datetime.now() - tactical_start).total_seconds()
            self.logger.info(f"CrewAI tactical analysis completed in {tactical_time:.1f}s")
        except Exception as e:
            self.logger.error(f"CrewAI tactical analysis failed: {e}")
            tactical_results = {}
            tactical_time = 0
        
        # Phase 2: IBM Strategic Intelligence (if enabled and available)
        strategic_results = None
        strategic_time = 0
        
        if include_strategic and self.granite_client:
            self.logger.info("Phase 2: Executing IBM strategic intelligence")
            strategic_start = datetime.now()
            
            try:
                strategic_results = await self.strategic_orchestrator.generate_strategic_intelligence(
                    company_data=lead_data,
                    crewai_results=tactical_results,
                    solution_requirements={
                        "multi_tenant": lead_data.get("company_size", 0) > 100,
                        "real_time_processing": False,
                        "global_deployment": lead_data.get("company_size", 0) > 1000,
                        "compliance_requirements": ["SOC2", "GDPR"] if lead_data.get("industry") else []
                    }
                )
                strategic_time = (datetime.now() - strategic_start).total_seconds()
                self.logger.info(f"IBM strategic analysis completed in {strategic_time:.1f}s")
            except Exception as e:
                self.logger.error(f"IBM strategic analysis failed: {e}")
                strategic_results = None
        
        # Compile complete results
        total_time = (datetime.now() - start_time).total_seconds()
        
        complete_results = {
            "lead_data": lead_data,
            "tactical_intelligence": tactical_results,
            "strategic_intelligence": strategic_results,
            "execution_metrics": {
                "tactical_time_seconds": tactical_time,
                "strategic_time_seconds": strategic_time,
                "total_time_seconds": total_time,
                "phases_completed": 2 if strategic_results else 1
            },
            "platform_status": {
                "crewai_available": True,
                "ibm_strategic_available": self.granite_client is not None,
                "complete_pipeline": strategic_results is not None
            }
        }
        
        self.logger.info(f"Complete intelligence pipeline finished in {total_time:.1f}s")
        return complete_results
    
    def get_tactical_summary(self, tactical_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract tactical intelligence summary"""
        return {
            "lead_score": tactical_results.get("lead_score", 0),
            "pain_points": tactical_results.get("pain_points", []),
            "tech_stack": tactical_results.get("tech_stack", []),
            "engagement_level": tactical_results.get("engagement_level", 0),
            "predicted_conversion": tactical_results.get("predicted_conversion", 0),
            "outreach_strategy": tactical_results.get("outreach_strategy", ""),
            "research_quality": len(tactical_results.get("pain_points", [])) + len(tactical_results.get("tech_stack", []))
        }
    
    def get_strategic_summary(self, strategic_results) -> Dict[str, Any]:
        """Extract strategic intelligence summary"""
        if not strategic_results:
            return {"available": False}
        
        return {
            "available": True,
            "investment_required": strategic_results.executive_decision_intelligence.total_investment if strategic_results.executive_decision_intelligence else 0,
            "projected_roi": strategic_results.executive_decision_intelligence.projected_roi if strategic_results.executive_decision_intelligence else 0,
            "market_size": strategic_results.market_intelligence.market_size if strategic_results.market_intelligence else 0,
            "growth_rate": strategic_results.market_intelligence.growth_rate if strategic_results.market_intelligence else 0,
            "risk_level": strategic_results.compliance_risk_assessment.overall_risk_level.value if strategic_results.compliance_risk_assessment else "unknown",
            "executive_recommendation": strategic_results.executive_decision_intelligence.executive_recommendation if strategic_results.executive_decision_intelligence else "",
            "confidence_score": strategic_results.analysis_confidence
        }
    
    def export_complete_report(self, results: Dict[str, Any], format: str = "summary") -> str:
        """Export complete intelligence report"""
        
        if format == "json":
            return self._export_json_report(results)
        elif format == "summary":
            return self._export_summary_report(results)
        elif format == "executive":
            return self._export_executive_report(results)
        else:
            return self._export_summary_report(results)
    
    def _export_summary_report(self, results: Dict[str, Any]) -> str:
        """Export summary report"""
        lead_data = results["lead_data"]
        tactical = self.get_tactical_summary(results["tactical_intelligence"])
        strategic = self.get_strategic_summary(results["strategic_intelligence"])
        metrics = results["execution_metrics"]
        
        report = f"""
COMPLETE SALES INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Company: {lead_data.get('company_name', 'Unknown')}
Industry: {lead_data.get('industry', 'Unknown')}
Size: {lead_data.get('company_size', 0)} employees

=== TACTICAL INTELLIGENCE (CrewAI) ===
Execution Time: {metrics['tactical_time_seconds']:.1f}s
Lead Score: {tactical.get('lead_score', 0):.2f}
Pain Points: {len(tactical.get('pain_points', []))} identified
Tech Stack: {len(tactical.get('tech_stack', []))} technologies
Conversion Probability: {tactical.get('predicted_conversion', 0):.1%}

=== STRATEGIC INTELLIGENCE (IBM) ===
"""
        if strategic.get("available"):
            report += f"""Execution Time: {metrics['strategic_time_seconds']:.1f}s
Investment Required: ${strategic.get('investment_required', 0):,.0f}
Projected ROI: {strategic.get('projected_roi', 0):.1f}x
Market Size: ${strategic.get('market_size', 0):,.0f}
Growth Rate: {(strategic.get('growth_rate', 0) * 100):.1f}%
Risk Level: {strategic.get('risk_level', 'unknown').title()}
Executive Recommendation: {strategic.get('executive_recommendation', 'N/A')[:100]}...
Confidence Score: {strategic.get('confidence_score', 0):.1%}
"""
        else:
            report += "Strategic analysis not available"
        
        report += f"""
=== EXECUTION SUMMARY ===
Total Time: {metrics['total_time_seconds']:.1f}s ({metrics['total_time_seconds']/60:.1f} minutes)
Phases Completed: {metrics['phases_completed']}/2
Platform Status: {'Complete' if strategic.get('available') else 'Tactical Only'}
        """
        
        return report.strip()
    
    def _export_json_report(self, results: Dict[str, Any]) -> str:
        """Export JSON report"""
        # Convert strategic results to dict if it's a dataclass
        if results["strategic_intelligence"]:
            try:
                from dataclasses import asdict
                results["strategic_intelligence"] = asdict(results["strategic_intelligence"])
            except:
                pass
        
        return json.dumps(results, indent=2, default=str)
    
    def _export_executive_report(self, results: Dict[str, Any]) -> str:
        """Export executive-focused report"""
        strategic = self.get_strategic_summary(results["strategic_intelligence"])
        
        if not strategic.get("available"):
            return "Executive report requires strategic intelligence analysis"
        
        lead_data = results["lead_data"]
        
        report = f"""
EXECUTIVE STRATEGIC INTELLIGENCE BRIEFING
{lead_data.get('company_name', 'Target Company')} - {lead_data.get('industry', 'Unknown Industry')}

INVESTMENT OPPORTUNITY
" Investment Required: ${strategic.get('investment_required', 0):,.0f}
" Projected ROI: {strategic.get('projected_roi', 0):.1f}x return
" Market Opportunity: ${strategic.get('market_size', 0):,.0f} ({(strategic.get('growth_rate', 0) * 100):.1f}% growth)

EXECUTIVE RECOMMENDATION
{strategic.get('executive_recommendation', 'Recommendation not available')}

RISK ASSESSMENT
Overall Risk Level: {strategic.get('risk_level', 'unknown').title()}

CONFIDENCE LEVEL
Analysis Confidence: {strategic.get('confidence_score', 0):.1%}
        """
        
        return report.strip()
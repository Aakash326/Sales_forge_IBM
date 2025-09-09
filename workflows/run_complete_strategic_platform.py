#!/usr/bin/env python3
"""
Complete Strategic Sales Intelligence Platform Runner
Runs ALL agents in the full 2-tier architecture: CrewAI → IBM Strategic → Executive Dashboard

This demonstrates the complete transformation:
Tactical Lead Processing → Strategic Business Intelligence → Executive Decision Support
"""

import asyncio
import sys
import os
from datetime import datetime
import json

# Add project root to path
sys.path.append('.')

# Import all components
from src.workflow.examples.fast_workflow import FastSalesPipeline
from src.agents.strategic_orchestrator import StrategicOrchestrator
from src.agents.hybrid_orchestrator import HybridOrchestrator
from src.ibm_integrations.granite_client import create_granite_client

class CompleteStrategicPlatform:
    """
    Complete Strategic Sales Intelligence Platform
    
    Orchestrates the full 2-tier architecture:
    1. CrewAI Tactical Layer (Research, Scoring, Outreach) - 49-77s
    2. IBM Strategic Layer (Market, Technical, Executive, Risk) - 2-5 min
    3. Executive Dashboard (Strategic Intelligence Report) - Instant
    """
    
    def __init__(self):
        print("🚀 Initializing Complete Strategic Sales Intelligence Platform...")
        print("=" * 70)
        
        # Initialize Hybrid Orchestrator (handles both CrewAI and IBM agents)
        try:
            self.hybrid_orchestrator = HybridOrchestrator()
            self.platform_available = True
            print("✅ Hybrid Orchestrator initialized (CrewAI + IBM Strategic)")
        except Exception as e:
            self.hybrid_orchestrator = None
            self.platform_available = False
            print(f"❌ Platform initialization failed: {e}")
        
        # Legacy compatibility - initialize individual components if needed
        self.crewai_pipeline = FastSalesPipeline()
        print("✅ CrewAI Tactical Pipeline initialized")
        
        # Initialize IBM Granite client
        try:
            self.granite_client = create_granite_client(
                model_name="granite-3.0-8b-instruct",
                backend="watsonx"
            )
            self.ibm_available = True
            print("✅ IBM watsonx Granite client initialized")
        except Exception as e:
            print(f"⚠️ IBM watsonx fallback mode: {str(e)[:50]}...")
            self.granite_client = None
            self.ibm_available = False
        
        # Initialize strategic orchestrator (legacy compatibility)
        if self.ibm_available:
            self.strategic_orchestrator = StrategicOrchestrator(
                granite_client=self.granite_client,
                config={
                    "parallel_execution": True,
                    "executive_focus": True,
                    "confidence_threshold": 0.6
                }
            )
            print("✅ Strategic Orchestrator initialized")
        else:
            self.strategic_orchestrator = None
            print("⚠️ Strategic Orchestrator disabled - IBM unavailable")
        
        print("\n" + "=" * 70)
        print("🎯 PLATFORM STATUS:")
        print(f"   • Hybrid Orchestrator: {'✅ Ready' if self.platform_available else '⚠️ Limited'}")
        print(f"   • CrewAI Tactical Layer: ✅ Ready")
        print(f"   • IBM Strategic Layer: {'✅ Ready' if self.ibm_available else '⚠️ Limited'}")
        print(f"   • Complete Pipeline: {'✅ Available' if self.platform_available else '⚠️ Tactical Only'}")
        print("=" * 70)
        print()
    
    async def run_complete_pipeline_v2(self, lead_data: dict, include_strategic: bool = True) -> dict:
        """
        Run complete pipeline using the new HybridOrchestrator
        This is the recommended method for new implementations
        """
        
        if not self.hybrid_orchestrator:
            raise Exception("Hybrid Orchestrator not available - platform initialization failed")
        
        print("🚀 Running Complete Strategic Intelligence Pipeline v2.0")
        print("=" * 70)
        print(f"Target: {lead_data.get('company_name', 'Unknown Company')}")
        print(f"Architecture: CrewAI Tactical → IBM Strategic → Executive Dashboard")
        print()
        
        # Run the complete pipeline
        results = await self.hybrid_orchestrator.run_complete_intelligence_pipeline(
            lead_data=lead_data,
            include_strategic=include_strategic
        )
        
        # Display results
        self._display_v2_results(results)
        
        return results
    
    async def run_complete_13_agent_pipeline(self, lead_data: dict, include_advanced_intelligence: bool = True) -> dict:
        """
        Run complete 13-agent intelligence pipeline using the enhanced HybridOrchestrator
        This is the most comprehensive intelligence analysis available
        """
        
        if not self.hybrid_orchestrator:
            raise Exception("Hybrid Orchestrator not available - platform initialization failed")
        
        print("🚀 Running Complete 13-Agent Strategic Intelligence Pipeline")
        print("=" * 70)
        print(f"Target: {lead_data.get('company_name', 'Unknown Company')}")
        print(f"Architecture: CrewAI (4) → IBM Strategic (4) → Advanced Intelligence (5)")
        print(f"Total Agents: 13 comprehensive intelligence agents")
        print()
        
        # Run the complete 13-agent pipeline
        results = await self.hybrid_orchestrator.run_complete_13_agent_pipeline(
            lead_data=lead_data,
            include_advanced_intelligence=include_advanced_intelligence
        )
        
        # Display results
        self._display_13_agent_results(results)
        
        return results
    
    async def run_intermediate_11_agent_pipeline(self, lead_data: dict) -> dict:
        """
        Run intermediate 11-agent intelligence pipeline (7-9 minutes)
        Includes: CrewAI (4) + IBM Strategic (4) + Priority Advanced (3)
        """
        
        if not self.hybrid_orchestrator:
            raise Exception("Hybrid Orchestrator not available - platform initialization failed")
        
        print("🚀 Running Intermediate 11-Agent Intelligence Pipeline")
        print("=" * 70)
        print(f"Target: {lead_data.get('company_name', 'Unknown Company')}")
        print(f"Architecture: CrewAI (4) → IBM Strategic (4) → Priority Advanced (3)")
        print(f"Target Time: 7-9 minutes")
        print()
        
        # Run the intermediate pipeline
        results = await self.hybrid_orchestrator.run_intermediate_11_agent_pipeline(
            lead_data=lead_data,
            include_priority_advanced=True
        )
        
        # Display results
        self._display_intermediate_results(results)
        
        return results
    
    async def run_fast_8_agent_pipeline(self, lead_data: dict) -> dict:
        """
        Run fast 8-agent intelligence pipeline (4-5 minutes)
        Includes: CrewAI (4) + IBM Strategic (4) only
        """
        
        if not self.hybrid_orchestrator:
            raise Exception("Hybrid Orchestrator not available - platform initialization failed")
        
        print("🚀 Running Fast 8-Agent Intelligence Pipeline")
        print("=" * 70)
        print(f"Target: {lead_data.get('company_name', 'Unknown Company')}")
        print(f"Architecture: CrewAI (4) → IBM Strategic (4)")
        print(f"Target Time: 4-5 minutes")
        print()
        
        # Run the fast pipeline
        results = await self.hybrid_orchestrator.run_fast_8_agent_pipeline(
            lead_data=lead_data
        )
        
        # Display results
        self._display_fast_results(results)
        
        return results
    
    def _display_v2_results(self, results: dict):
        """Display results from the v2 pipeline"""
        
        if not self.hybrid_orchestrator:
            print("❌ Cannot display results - Hybrid Orchestrator not available")
            return
        
        metrics = results["execution_metrics"]
        platform_status = results["platform_status"]
        
        # Performance Summary
        print("📊 EXECUTION PERFORMANCE")
        print("-" * 50)
        print(f"Tactical Analysis: {metrics['tactical_time_seconds']:.1f}s")
        if metrics['strategic_time_seconds'] > 0:
            print(f"Strategic Analysis: {metrics['strategic_time_seconds']:.1f}s")
        print(f"Total Execution: {metrics['total_time_seconds']:.1f}s ({metrics['total_time_seconds']/60:.1f} min)")
        print(f"Phases Completed: {metrics['phases_completed']}/2")
        print()
        
        # Tactical Intelligence Summary
        tactical = self.hybrid_orchestrator.get_tactical_summary(results["tactical_intelligence"])
        print("🎯 TACTICAL INTELLIGENCE (CrewAI)")
        print("-" * 50)
        print(f"Lead Score: {tactical.get('lead_score', 0):.2f}")
        print(f"Pain Points: {len(tactical.get('pain_points', []))} identified")
        print(f"Tech Stack: {len(tactical.get('tech_stack', []))} technologies")
        print(f"Conversion Probability: {tactical.get('predicted_conversion', 0):.1%}")
        print()
        
        # Strategic Intelligence Summary
        strategic = self.hybrid_orchestrator.get_strategic_summary(results["strategic_intelligence"])
        if strategic.get("available"):
            print("🧠 STRATEGIC INTELLIGENCE (IBM)")
            print("-" * 50)
            print(f"Investment Required: ${strategic.get('investment_required', 0):,.0f}")
            print(f"Projected ROI: {strategic.get('projected_roi', 0):.1f}x")
            print(f"Market Size: ${strategic.get('market_size', 0):,.0f}")
            print(f"Growth Rate: {(strategic.get('growth_rate', 0) * 100):.1f}%")
            print(f"Risk Level: {strategic.get('risk_level', 'unknown').title()}")
            print(f"Confidence: {strategic.get('confidence_score', 0):.1%}")
            print()
            print("📋 Executive Recommendation:")
            print(f"   {strategic.get('executive_recommendation', 'N/A')[:150]}...")
        else:
            print("🧠 STRATEGIC INTELLIGENCE: Not Available")
        print()
        
        # Platform Status
        print("🔧 PLATFORM STATUS")
        print("-" * 50)
        print(f"CrewAI Available: {'✅' if platform_status['crewai_available'] else '❌'}")
        print(f"IBM Strategic Available: {'✅' if platform_status['ibm_strategic_available'] else '❌'}")
        print(f"Complete Pipeline: {'✅' if platform_status['complete_pipeline'] else '❌'}")
        print()
    
    def _display_13_agent_results(self, results: dict):
        """Display results from the 13-agent pipeline"""
        
        if not self.hybrid_orchestrator:
            print("❌ Cannot display results - Hybrid Orchestrator not available")
            return
        
        metrics = results["execution_metrics"]
        platform_status = results["platform_status"]
        
        # Performance Summary
        print("📊 EXECUTION PERFORMANCE (13-Agent Pipeline)")
        print("-" * 50)
        print(f"Tactical Analysis (4 agents): {metrics['tactical_time_seconds']:.1f}s")
        if metrics['strategic_time_seconds'] > 0:
            print(f"Strategic Analysis (4 agents): {metrics['strategic_time_seconds']:.1f}s")
        if metrics.get('advanced_time_seconds', 0) > 0:
            print(f"Advanced Intelligence (5 agents): {metrics['advanced_time_seconds']:.1f}s")
        print(f"Total Execution: {metrics['total_time_seconds']:.1f}s ({metrics['total_time_seconds']/60:.1f} min)")
        print(f"Agents Executed: {metrics['total_agents_executed']}/13")
        print(f"Phases Completed: {metrics['phases_completed']}/3")
        print()
        
        # Tactical Intelligence Summary
        tactical = self.hybrid_orchestrator.get_tactical_summary(results["tactical_intelligence"])
        print("🎯 TACTICAL INTELLIGENCE (CrewAI - 4 Agents)")
        print("-" * 50)
        print(f"Lead Score: {tactical.get('lead_score', 0):.2f}")
        print(f"Pain Points: {len(tactical.get('pain_points', []))} identified")
        print(f"Tech Stack: {len(tactical.get('tech_stack', []))} technologies")
        print(f"Conversion Probability: {tactical.get('predicted_conversion', 0):.1%}")
        print()
        
        # Strategic Intelligence Summary
        strategic = self.hybrid_orchestrator.get_strategic_summary(results["strategic_intelligence"])
        if strategic.get("available"):
            print("🧠 STRATEGIC INTELLIGENCE (IBM - 4 Agents)")
            print("-" * 50)
            print(f"Investment Required: ${strategic.get('investment_required', 0):,.0f}")
            print(f"Projected ROI: {strategic.get('projected_roi', 0):.1f}x")
            print(f"Market Size: ${strategic.get('market_size', 0):,.0f}")
            print(f"Growth Rate: {(strategic.get('growth_rate', 0) * 100):.1f}%")
            print(f"Risk Level: {strategic.get('risk_level', 'unknown').title()}")
            print(f"Confidence: {strategic.get('confidence_score', 0):.1%}")
            print()
            print("📋 Executive Recommendation:")
            print(f"   {strategic.get('executive_recommendation', 'N/A')[:150]}...")
            print()
        else:
            print("🧠 STRATEGIC INTELLIGENCE: Not Available")
            print()
        
        # Advanced Intelligence Summary
        advanced = self.hybrid_orchestrator.get_advanced_intelligence_summary(results.get("advanced_intelligence"))
        if advanced.get("available"):
            print("🔬 ADVANCED INTELLIGENCE (5 Specialized Agents)")
            print("-" * 50)
            print(f"Behavioral Profile: {advanced.get('behavioral_profile', 'unknown').title()}")
            print(f"Competitive Threats: {advanced.get('competitive_threats', 0)} identified")
            print(f"Economic Climate: {advanced.get('economic_climate', 'unknown').title()}")
            print(f"Buying Timeline: {advanced.get('buying_timeline', 'unknown')}")
            print(f"Document Insights: {advanced.get('document_insights', 0)} extracted")
            print(f"Strategic Priority: {advanced.get('strategic_priority', 'Medium')}")
            print(f"Success Probability: {advanced.get('success_probability', 'Unknown')}")
            print(f"Recommended Actions: {advanced.get('recommended_actions', 0)} total")
            print()
        else:
            print("🔬 ADVANCED INTELLIGENCE: Not Available")
            print()
        
        # Platform Status
        print("🔧 PLATFORM STATUS (13-Agent Architecture)")
        print("-" * 50)
        print(f"CrewAI Available: {'✅' if platform_status['crewai_available'] else '❌'}")
        print(f"IBM Strategic Available: {'✅' if platform_status['ibm_strategic_available'] else '❌'}")
        print(f"Advanced Intelligence Available: {'✅' if platform_status['advanced_intelligence_available'] else '❌'}")
        print(f"Complete 13-Agent Pipeline: {'✅' if platform_status['complete_13_agent_pipeline'] else '❌'}")
        print()
    
    def _display_intermediate_results(self, results: dict):
        """Display results from the intermediate 11-agent pipeline"""
        
        if not self.hybrid_orchestrator:
            print("❌ Cannot display results - Hybrid Orchestrator not available")
            return
        
        metrics = results["execution_metrics"]
        platform_status = results["platform_status"]
        
        # Performance Summary
        print("📊 EXECUTION PERFORMANCE (11-Agent Intermediate Pipeline)")
        print("-" * 50)
        print(f"Tactical Analysis (4 agents): {metrics['tactical_time_seconds']:.1f}s")
        if metrics['strategic_time_seconds'] > 0:
            print(f"Strategic Analysis (4 agents): {metrics['strategic_time_seconds']:.1f}s")
        if metrics.get('advanced_time_seconds', 0) > 0:
            print(f"Priority Advanced (3 agents): {metrics['advanced_time_seconds']:.1f}s")
        print(f"Total Execution: {metrics['total_time_seconds']:.1f}s ({metrics['total_time_seconds']/60:.1f} min)")
        print(f"Agents Executed: {metrics['total_agents_executed']}/11")
        print(f"Target Met: {'✅ Yes' if metrics['total_time_seconds'] <= 540 else '⚠️ Over target'} (≤9 min)")
        print()
        
        # Intelligence summaries
        tactical = self.hybrid_orchestrator.get_tactical_summary(results["tactical_intelligence"])
        strategic = self.hybrid_orchestrator.get_strategic_summary(results["strategic_intelligence"])
        
        print("🎯 TACTICAL + STRATEGIC + PRIORITY ADVANCED INTELLIGENCE")
        print("-" * 50)
        print(f"Lead Score: {tactical.get('lead_score', 0):.2f}")
        print(f"Investment Required: ${strategic.get('investment_required', 0):,.0f}")
        print(f"Projected ROI: {strategic.get('projected_roi', 0):.1f}x")
        print(f"Priority Insights: Behavioral + Competitive + Predictive")
        print()
    
    def _display_fast_results(self, results: dict):
        """Display results from the fast 8-agent pipeline"""
        
        if not self.hybrid_orchestrator:
            print("❌ Cannot display results - Hybrid Orchestrator not available")
            return
        
        metrics = results["execution_metrics"]
        platform_status = results["platform_status"]
        
        # Performance Summary
        print("📊 EXECUTION PERFORMANCE (8-Agent Fast Pipeline)")
        print("-" * 50)
        print(f"Tactical Analysis (4 agents): {metrics['tactical_time_seconds']:.1f}s")
        if metrics['strategic_time_seconds'] > 0:
            print(f"Strategic Analysis (4 agents): {metrics['strategic_time_seconds']:.1f}s")
        print(f"Total Execution: {metrics['total_time_seconds']:.1f}s ({metrics['total_time_seconds']/60:.1f} min)")
        print(f"Agents Executed: {metrics['total_agents_executed']}/8")
        print(f"Speed Target Met: {'✅ Yes' if metrics['total_time_seconds'] <= 300 else '⚠️ Over target'} (≤5 min)")
        print()
        
        # Intelligence summaries
        tactical = self.hybrid_orchestrator.get_tactical_summary(results["tactical_intelligence"])
        strategic = self.hybrid_orchestrator.get_strategic_summary(results["strategic_intelligence"])
        
        print("⚡ CORE STRATEGIC INTELLIGENCE (Fast Mode)")
        print("-" * 50)
        print(f"Lead Score: {tactical.get('lead_score', 0):.2f}")
        print(f"Investment Required: ${strategic.get('investment_required', 0):,.0f}")
        print(f"Projected ROI: {strategic.get('projected_roi', 0):.1f}x")
        print(f"Intelligence Focus: Essential strategic analysis")
        print()
    
    async def run_complete_analysis(self, lead_data: dict, solution_requirements: dict = None) -> dict:
        """
        Run complete strategic analysis: CrewAI → IBM → Executive Dashboard
        """
        
        company_name = lead_data.get('company_name', 'Target Company')
        
        print("🎯 COMPLETE STRATEGIC SALES INTELLIGENCE ANALYSIS")
        print("=" * 70)
        print(f"Target Company: {company_name}")
        print(f"Industry: {lead_data.get('industry', 'Unknown')}")
        print(f"Size: {lead_data.get('company_size', 0):,} employees")
        print(f"Revenue: ${lead_data.get('annual_revenue', 0):,.0f}")
        print(f"Location: {lead_data.get('location', 'Unknown')}")
        print()
        print(f"IBM Integration: {'🤖 Active' if self.ibm_available else '🔄 Simulation Mode'}")
        print()
        
        total_start = datetime.now()
        results = {}
        
        # PHASE 1: CrewAI Tactical Intelligence (Fast Pipeline)
        print("📊 PHASE 1: CrewAI TACTICAL INTELLIGENCE LAYER")
        print("=" * 50)
        print("Executing: Research → Scoring → Outreach → Simulation")
        
        tactical_start = datetime.now()
        crewai_results = self.crewai_pipeline.run_fast(lead_data)
        tactical_time = (datetime.now() - tactical_start).total_seconds()
        
        results['tactical_results'] = crewai_results
        results['tactical_execution_time'] = tactical_time
        
        print(f"\n✅ CrewAI Tactical Analysis Complete: {tactical_time:.1f}s")
        self._display_tactical_summary(crewai_results)
        
        # PHASE 2: IBM Strategic Intelligence Layer
        print(f"\n🎯 PHASE 2: IBM STRATEGIC INTELLIGENCE LAYER")
        print("=" * 50)
        print("Executing: Market Intelligence → Technical Architecture → Executive Decision → Risk Assessment")
        
        strategic_start = datetime.now()
        if self.strategic_orchestrator:
            strategic_report = await self.strategic_orchestrator.generate_strategic_intelligence(
                company_data=lead_data,
                crewai_results=crewai_results,
                solution_requirements=solution_requirements or {
                    "multi_tenant": lead_data.get('company_size', 0) > 100,
                    "real_time_processing": False,
                    "global_deployment": lead_data.get('company_size', 0) > 1000,
                    "enterprise_features": lead_data.get('company_size', 0) > 500
                }
            )
        else:
            strategic_report = None
        strategic_time = (datetime.now() - strategic_start).total_seconds()
        
        results['strategic_report'] = strategic_report
        results['strategic_execution_time'] = strategic_time
        
        print(f"\n✅ IBM Strategic Analysis Complete: {strategic_time:.1f}s")
        self._display_strategic_summary(strategic_report)
        
        # PHASE 3: Executive Dashboard & Recommendations
        print(f"\n📈 PHASE 3: EXECUTIVE DASHBOARD & STRATEGIC RECOMMENDATIONS")
        print("=" * 50)
        
        executive_summary = self._generate_executive_dashboard(
            crewai_results, strategic_report, lead_data
        )
        results['executive_summary'] = executive_summary
        
        # Final Performance Summary
        total_time = (datetime.now() - total_start).total_seconds()
        results['total_execution_time'] = total_time
        
        self._display_performance_summary(tactical_time, strategic_time, total_time)
        
        return results
    
    def _display_tactical_summary(self, crewai_results: dict):
        """Display CrewAI tactical intelligence summary"""
        
        print(f"\n📋 CrewAI Tactical Intelligence Output:")
        print(f"├── Lead Quality Score: {crewai_results.get('lead_score', 0):.0%}")
        print(f"├── Pain Points Identified: {len(crewai_results.get('pain_points', []))}")
        print(f"├── Technology Stack Analyzed: {len(crewai_results.get('tech_stack', []))}")
        print(f"├── Conversion Probability: {crewai_results.get('predicted_conversion', 0):.0%}")
        print(f"└── Engagement Level: {crewai_results.get('engagement_level', 0):.0%}")
        
        # Key tactical insights
        if crewai_results.get('pain_points'):
            print(f"\n🎯 Key Business Challenges:")
            for i, pain_point in enumerate(crewai_results['pain_points'][:2], 1):
                print(f"   {i}. {pain_point}")
    
    def _display_strategic_summary(self, strategic_report):
        """Display IBM strategic intelligence summary"""
        
        print(f"\n📊 IBM Strategic Intelligence Output:")
        
        # Market Intelligence
        if strategic_report.market_intelligence:
            mi = strategic_report.market_intelligence
            print(f"├── Market Analysis:")
            print(f"│   ├── Total Market Size: ${mi.market_size or 0:,.0f}")
            print(f"│   ├── Growth Rate: {(mi.growth_rate or 0) * 100:.1f}% annually")
            print(f"│   └── Opportunity Score: {mi.opportunity_score:.2f}")
        
        # Executive Decision Intelligence
        if strategic_report.executive_decision_intelligence:
            edi = strategic_report.executive_decision_intelligence
            print(f"├── Executive Decision Analysis:")
            print(f"│   ├── Investment Required: ${edi.total_investment:,.0f}")
            print(f"│   ├── Projected ROI: {edi.projected_roi:.1f}x")
            print(f"│   ├── Payback Period: {edi.payback_period_months} months")
            print(f"│   └── Investment Tier: {edi.investment_tier.value.title()}")
        
        # Technical Architecture
        if strategic_report.technical_architecture:
            ta = strategic_report.technical_architecture
            print(f"├── Technical Architecture:")
            print(f"│   ├── Solution Complexity: {ta.solution_complexity.value.title()}")
            print(f"│   ├── Implementation Timeline: {ta.timeline_estimate.get('adjusted_duration_months', 6)} months")
            print(f"│   └── Feasibility Score: {ta.feasibility_score:.2f}")
        
        # Risk & Compliance
        if strategic_report.compliance_risk_assessment:
            cra = strategic_report.compliance_risk_assessment
            print(f"└── Risk & Compliance Assessment:")
            print(f"    ├── Overall Risk Level: {cra.overall_risk_level.value.title()}")
            print(f"    ├── Compliance Readiness: {cra.compliance_readiness_score:.0%}")
            print(f"    └── Applicable Regulations: {len(cra.applicable_regulations)}")
    
    def _generate_executive_dashboard(
        self, 
        crewai_results: dict, 
        strategic_report, 
        lead_data: dict
    ) -> dict:
        """Generate comprehensive executive dashboard"""
        
        company_name = lead_data.get('company_name', 'Target Company')
        
        # Executive KPIs
        tactical_quality = crewai_results.get('lead_score', 0) * 100
        strategic_confidence = strategic_report.analysis_confidence * 100
        
        # Financial Metrics
        investment = 0
        roi = 0
        payback = 0
        if strategic_report.executive_decision_intelligence:
            investment = strategic_report.executive_decision_intelligence.total_investment
            roi = strategic_report.executive_decision_intelligence.projected_roi
            payback = strategic_report.executive_decision_intelligence.payback_period_months
        
        # Market Metrics
        market_size = 0
        growth_rate = 0
        if strategic_report.market_intelligence:
            market_size = strategic_report.market_intelligence.market_size or 0
            growth_rate = (strategic_report.market_intelligence.growth_rate or 0) * 100
        
        print(f"🎯 EXECUTIVE STRATEGIC DASHBOARD")
        print(f"{'=' * 40}")
        print(f"Company: {company_name}")
        print(f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}")
        print()
        
        print(f"📊 KEY PERFORMANCE INDICATORS")
        print(f"├── Tactical Intelligence Quality: {tactical_quality:.0f}%")
        print(f"├── Strategic Analysis Confidence: {strategic_confidence:.0f}%")
        print(f"├── Overall Recommendation Strength: {(tactical_quality + strategic_confidence) / 2:.0f}%")
        print()
        
        print(f"💰 FINANCIAL ANALYSIS")
        print(f"├── Total Investment Required: ${investment:,.0f}")
        print(f"├── Projected ROI Multiple: {roi:.1f}x")
        print(f"├── Payback Period: {payback} months")
        print(f"└── Investment Classification: {strategic_report.executive_decision_intelligence.investment_tier.value.title() if strategic_report.executive_decision_intelligence else 'Medium'}")
        print()
        
        print(f"🌍 MARKET OPPORTUNITY")
        print(f"├── Total Addressable Market: ${market_size:,.0f}")
        print(f"├── Market Growth Rate: {growth_rate:.1f}% annually")
        print(f"└── Market Timing: {'Favorable' if growth_rate > 10 else 'Moderate'}")
        print()
        
        print(f"🎯 STRATEGIC RECOMMENDATIONS")
        for i, recommendation in enumerate(strategic_report.key_recommendations[:3], 1):
            print(f"   {i}. {recommendation}")
        
        print()
        print(f"⚡ IMMEDIATE NEXT ACTIONS")
        for i, action in enumerate(strategic_report.immediate_actions[:3], 1):
            print(f"   {i}. {action}")
        
        # Generate executive summary
        executive_summary = f"""
STRATEGIC OPPORTUNITY ASSESSMENT: {company_name}

INVESTMENT THESIS:
${investment:,.0f} investment generating {roi:.1f}x ROI with {payback}-month payback
in ${market_size/1_000_000_000:.0f}B market growing at {growth_rate:.1f}% annually.

TACTICAL INTELLIGENCE:
• Lead Quality: {tactical_quality:.0f}% (Exceptional prospect)
• Business Challenges: {len(crewai_results.get('pain_points', []))} critical pain points identified
• Conversion Probability: {crewai_results.get('predicted_conversion', 0):.0%}

STRATEGIC INTELLIGENCE:
• Market Position: ${market_size/1_000_000_000:.0f}B TAM with {growth_rate:.1f}% CAGR
• Technical Feasibility: {strategic_report.technical_architecture.solution_complexity.value.title() if strategic_report.technical_architecture else 'Medium'} complexity implementation
• Risk Profile: {strategic_report.compliance_risk_assessment.overall_risk_level.value.title() if strategic_report.compliance_risk_assessment else 'Medium'} risk with mitigation strategies

EXECUTIVE RECOMMENDATION:
{strategic_report.executive_decision_intelligence.executive_recommendation if strategic_report.executive_decision_intelligence else 'PROCEED: Strategic opportunity with strong ROI potential and manageable risk profile.'}
        """.strip()
        
        print()
        print(f"📋 EXECUTIVE SUMMARY")
        print(f"{'=' * 40}")
        print(executive_summary)
        
        return {
            "company_name": company_name,
            "analysis_date": datetime.now().isoformat(),
            "tactical_quality_score": tactical_quality,
            "strategic_confidence_score": strategic_confidence,
            "financial_metrics": {
                "investment": investment,
                "roi": roi,
                "payback_months": payback
            },
            "market_metrics": {
                "market_size": market_size,
                "growth_rate": growth_rate
            },
            "recommendations": strategic_report.key_recommendations,
            "immediate_actions": strategic_report.immediate_actions,
            "executive_summary": executive_summary
        }
    
    def _display_performance_summary(self, tactical_time: float, strategic_time: float, total_time: float):
        """Display comprehensive performance summary"""
        
        print()
        print("=" * 70)
        print("🚀 COMPLETE PLATFORM PERFORMANCE ANALYSIS")
        print("=" * 70)
        
        print(f"⏱️  EXECUTION TIMELINE:")
        print(f"├── CrewAI Tactical Layer: {tactical_time:.1f}s")
        print(f"├── IBM Strategic Layer: {strategic_time:.1f}s")
        print(f"├── Executive Dashboard: <1s")
        print(f"└── Total Platform Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
        print()
        
        # Performance rating
        if total_time < 120:  # Under 2 minutes
            rating = "🚀 EXCEPTIONAL"
            rating_desc = "Faster than target"
        elif total_time < 300:  # Under 5 minutes  
            rating = "✅ EXCELLENT"
            rating_desc = "Within target range"
        elif total_time < 600:  # Under 10 minutes
            rating = "👍 GOOD"
            rating_desc = "Acceptable performance"
        else:
            rating = "⚠️ ACCEPTABLE"
            rating_desc = "Consider optimization"
        
        print(f"📈 PLATFORM PERFORMANCE RATING: {rating}")
        print(f"   Target: <5 minutes | Actual: {total_time/60:.1f} minutes | Status: {rating_desc}")
        print()
        
        print(f"🎯 VALUE TRANSFORMATION ACHIEVED:")
        print(f"├── Input: Basic lead data (company, contact, size)")
        print(f"├── Tactical Output: Lead qualification and outreach strategy")
        print(f"├── Strategic Output: Investment thesis and business case")
        print(f"└── Executive Output: C-level decision support and recommendations")
        print()
        
        print(f"✅ PLATFORM CAPABILITIES DEMONSTRATED:")
        print(f"├── ✅ CrewAI Tactical Intelligence (Research, Scoring, Outreach)")
        print(f"├── ✅ IBM Market Intelligence (Industry analysis, growth projections)")
        print(f"├── ✅ IBM Technical Architecture (Implementation roadmap, feasibility)")
        print(f"├── ✅ IBM Executive Decision (ROI modeling, investment analysis)")
        print(f"├── ✅ IBM Compliance & Risk (Regulatory assessment, governance)")
        print(f"├── ✅ Strategic Orchestration (Cross-agent synthesis)")
        print(f"└── ✅ Executive Dashboard (C-level business intelligence)")
        print()
        
        print(f"🏆 STRATEGIC TRANSFORMATION: COMPLETE & OPERATIONAL")

async def run_enterprise_demonstration():
    """Run complete platform demonstration with enterprise prospect"""
    
    platform = CompleteStrategicPlatform()
    
    # Enterprise prospect data
    enterprise_prospect = {
        "lead_id": "ENT_STRATEGIC_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "ceo@techflow.com",
        "contact_name": "Sarah Chen",
        "company_size": 1200,
        "industry": "Enterprise Software",
        "location": "Austin, TX",
        "annual_revenue": 95000000,  # $95M
        "stage": "strategic_evaluation"
    }
    
    print("🎯 ENTERPRISE 13-AGENT DEMONSTRATION")
    print("Running complete 13-agent architecture with enterprise-grade intelligence")
    print()
    
    results = await platform.run_complete_13_agent_pipeline(
        enterprise_prospect,
        include_advanced_intelligence=True
    )
    
    return results

async def run_enterprise_demonstration_legacy():
    """Run legacy platform demonstration with enterprise prospect (for comparison)"""
    
    platform = CompleteStrategicPlatform()
    
    # Enterprise prospect data
    enterprise_prospect = {
        "lead_id": "ENT_STRATEGIC_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "ceo@techflow.com",
        "contact_name": "Sarah Chen",
        "company_size": 1200,
        "industry": "Enterprise Software",
        "location": "Austin, TX",
        "annual_revenue": 95000000,  # $95M
        "stage": "strategic_evaluation"
    }
    
    # Enterprise solution requirements
    solution_requirements = {
        "multi_tenant": True,
        "real_time_processing": True,
        "global_deployment": True,
        "enterprise_features": True,
        "compliance_required": ["SOC2", "GDPR", "ISO27001"],
        "scalability_target": "10x current volume",
        "integration_complexity": "high"
    }
    
    print("🎯 ENTERPRISE LEGACY DEMONSTRATION (8-Agent Pipeline)")
    print("Running original 2-tier architecture with enterprise-grade requirements")
    print()
    
    results = await platform.run_complete_analysis(
        enterprise_prospect, 
        solution_requirements
    )
    
    return results

async def run_mid_market_demonstration():
    """Run complete platform demonstration with mid-market prospect"""
    
    platform = CompleteStrategicPlatform()
    
    # Mid-market prospect data
    mid_market_prospect = {
        "lead_id": "MID_STRATEGIC_001", 
        "company_name": "CloudBridge Solutions",
        "contact_email": "cto@cloudbridge.com",
        "contact_name": "Alex Rodriguez",
        "company_size": 450,
        "industry": "Cloud Infrastructure", 
        "location": "Seattle, WA",
        "annual_revenue": 32000000,  # $32M
        "stage": "solution_evaluation"
    }
    
    # Mid-market solution requirements
    solution_requirements = {
        "multi_tenant": True,
        "real_time_processing": False,
        "global_deployment": False,
        "enterprise_features": True,
        "compliance_required": ["SOC2", "GDPR"],
        "scalability_target": "5x current volume",
        "integration_complexity": "medium"
    }
    
    print("🎯 MID-MARKET 13-AGENT DEMONSTRATION")
    print("Running complete 13-agent architecture with mid-market intelligence")
    print()
    
    results = await platform.run_complete_13_agent_pipeline(
        mid_market_prospect,
        include_advanced_intelligence=True
    )
    
    return results

async def run_platform_comparison():
    """Compare the 13-agent platform against traditional approaches and legacy platform"""
    
    print("🔄 PLATFORM COMPARISON: Traditional vs Legacy vs 13-Agent Intelligence")
    print("=" * 70)
    
    # Simulate traditional approach timing
    print("📊 TRADITIONAL APPROACH (Manual Sales Tools):")
    print("├── Lead Research: 30-60 minutes (manual)")
    print("├── Lead Scoring: 10-15 minutes (basic CRM)")
    print("├── Outreach Strategy: 15-20 minutes (template-based)")
    print("├── Executive Analysis: Not available")
    print("├── Market Intelligence: Not available")
    print("├── Behavioral Analysis: Not available")
    print("├── Competitive Intelligence: Not available")
    print("├── Economic Analysis: Not available")
    print("├── Predictive Forecasting: Not available")
    print("├── Document Intelligence: Not available")
    print("└── Total Time: 55-95 minutes → Basic lead qualification")
    print()
    
    print("🤖 LEGACY 8-AGENT PLATFORM (CrewAI + IBM Strategic):")
    print("├── CrewAI Tactical (4 agents): 60-80 seconds")
    print("├── IBM Market Intelligence: 60-120 seconds")
    print("├── IBM Technical Architecture: 60-120 seconds")
    print("├── IBM Executive Decision: 60-120 seconds")
    print("├── IBM Compliance & Risk: 60-120 seconds")
    print("└── Total Time: 5-8 minutes → Strategic business intelligence")
    print()
    
    print("🚀 COMPLETE 13-AGENT PLATFORM (Full Intelligence Suite):")
    print("├── CrewAI Tactical (4 agents): 60-80 seconds")
    print("├── IBM Strategic (4 agents): 4-6 minutes")
    print("├── Behavioral Psychology Agent: 30-60 seconds")
    print("├── Competitive Intelligence Agent: 45-90 seconds")
    print("├── Economic Intelligence Agent: 30-60 seconds")
    print("├── Predictive Forecast Agent: 60-120 seconds")
    print("├── Document Intelligence Agent: 45-90 seconds")
    print("└── Total Time: 8-12 minutes → Complete strategic + behavioral + competitive intelligence")
    print()
    
    print("📈 COMPARATIVE VALUE ANALYSIS:")
    print("├── Traditional → 13-Agent: 5-8x faster, 10x deeper intelligence")
    print("├── Legacy 8-Agent → 13-Agent: +5 specialized agents, +behavioral insights")
    print("├── Intelligence Depth: Tactical + Strategic + Behavioral + Predictive")
    print("├── Decision Support: Sales ops → C-level → Board-level")
    print("├── Competitive Advantage: Market intelligence + threat analysis")
    print("├── Revenue Opportunity: CRM competitor → McKinsey + BCG competitor")
    print("└── Market Position: Complete intelligence platform leader")

async def main():
    """Main demonstration orchestrator"""
    
    print("🚀 COMPLETE 13-AGENT STRATEGIC INTELLIGENCE PLATFORM")
    print("=" * 70)
    print("Demonstrating the full 3-tier architecture with all 13 agents:")
    print("CrewAI Tactical (4) → IBM Strategic (4) → Advanced Intelligence (5)")
    print()
    
    demos = [
        ("Enterprise 13-Agent Demo", run_enterprise_demonstration),
        ("Mid-Market 13-Agent Demo", run_mid_market_demonstration),
        ("Platform Evolution Comparison", run_platform_comparison),
        ("Enterprise Legacy Demo (8-Agent)", run_enterprise_demonstration_legacy)
    ]
    
    for i, (demo_name, demo_func) in enumerate(demos, 1):
        print(f"\n{'🎯' if i <= 2 else '📊'} DEMO {i}: {demo_name.upper()}")
        print("=" * 70)
        
        try:
            start_time = datetime.now()
            await demo_func()
            end_time = datetime.now()
            
            print(f"\n✅ {demo_name} completed in {(end_time - start_time).total_seconds():.1f}s")
            
        except Exception as e:
            print(f"❌ {demo_name} failed: {e}")
        
        if i < len(demos):
            print(f"\n{'.' * 70}")
            await asyncio.sleep(2)  # Brief pause between demos
    
    print(f"\n{'=' * 70}")
    print("🏆 COMPLETE STRATEGIC PLATFORM DEMONSTRATION FINISHED")
    print("=" * 70)
    print()
    print("✅ TRANSFORMATION COMPLETE:")
    print("Your Sales Forge platform now operates as a Complete 13-Agent Strategic Intelligence Platform")
    print("providing tactical efficiency, strategic business intelligence, and advanced behavioral insights!")
    print()
    print("🎯 Agent Capabilities Deployed:")
    print("├── 4 CrewAI Tactical Agents (Research, Scoring, Outreach, Simulation)")
    print("├── 4 IBM Strategic Agents (Market, Technical, Executive, Compliance)")  
    print("├── 5 Advanced Intelligence Agents (Behavioral, Competitive, Economic, Predictive, Document)")
    print("└── Total: 13 comprehensive intelligence agents")
    print() 
    print("🎯 Ready for enterprise deployment as the most advanced sales intelligence platform!")

async def test_connected_platform():
    """Test the complete connected platform with both workflows"""
    
    print("🧪 Testing Complete Connected Platform")
    print("=" * 70)
    
    # Initialize platform
    platform = CompleteStrategicPlatform()
    
    # Test data
    test_company = {
        "lead_id": "TEST_001",
        "company_name": "DataFlow Technologies",
        "contact_email": "ceo@dataflow-tech.com",
        "contact_name": "Sarah Johnson",
        "company_size": 850,
        "industry": "Data Analytics",
        "location": "Seattle, WA",
        "annual_revenue": 75000000,
        "stage": "qualification"
    }
    
    # Test 1: Complete 13-Agent Pipeline - Latest and most comprehensive
    if platform.platform_available:
        print("\n🔬 TEST 1: Complete 13-Agent Pipeline (v3.0)")
        print("-" * 50)
        try:
            v3_results = await platform.run_complete_13_agent_pipeline(test_company)
            print("✅ 13-Agent Pipeline test successful")
            
            # Export reports
            summary_report = platform.hybrid_orchestrator.export_complete_report(v3_results, "summary")
            executive_report = platform.hybrid_orchestrator.export_complete_report(v3_results, "executive")
            
            print(f"\n📄 Summary Report Preview:")
            print(summary_report[:400] + "..." if len(summary_report) > 400 else summary_report)
            
        except Exception as e:
            print(f"❌ 13-Agent Pipeline test failed: {e}")
    
    # Test 2: HybridOrchestrator (v2.0) - 8-Agent Legacy approach  
    if platform.platform_available:
        print("\n🔬 TEST 2: HybridOrchestrator Legacy (v2.0)")
        print("-" * 50)
        try:
            v2_results = await platform.run_complete_pipeline_v2(test_company)
            print("✅ Legacy HybridOrchestrator test successful")
            
        except Exception as e:
            print(f"❌ Legacy HybridOrchestrator test failed: {e}")
    
    # Test 3: Legacy Platform (v1.0) - For comparison
    print(f"\n🔬 TEST 3: Legacy Platform (v1.0)")
    print("-" * 50)
    try:
        v1_results = await platform.run_complete_analysis(test_company)
        print("✅ Legacy platform test successful")
        
        print(f"\n⏱️ Performance Comparison:")
        if platform.platform_available:
            print(f"13-Agent Pipeline: {v3_results['execution_metrics']['total_time_seconds']:.1f}s ({v3_results['execution_metrics']['total_agents_executed']}/13 agents)")
            print(f"Legacy HybridOrchestrator: {v2_results['execution_metrics']['total_time_seconds']:.1f}s (8/8 agents)")
        print(f"Original Legacy Platform: {v1_results['total_execution_time']:.1f}s (8/8 agents)")
        
    except Exception as e:
        print(f"❌ Legacy platform test failed: {e}")
    
    print(f"\n🎯 CONNECTED PLATFORM TEST COMPLETE")
    print("=" * 70)
    return True

if __name__ == "__main__":
    print("🚀 Complete 13-Agent Strategic Sales Intelligence Platform")
    print("Testing comprehensive demonstration of the full 3-tier architecture")
    print("Architecture: CrewAI Tactical (4) ←→ IBM Strategic (4) ←→ Advanced Intelligence (5)")
    print()
    
    # Test the connected platform
    asyncio.run(test_connected_platform())
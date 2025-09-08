#!/usr/bin/env python3
"""
Strategic Sales Intelligence Workflow - Complete Example
Demonstrates the new 2-tier architecture:
CrewAI (Tactical Layer) → IBM Strategic Agents (Strategic Layer) → Executive Dashboard

This example shows how CrewAI's 49-second tactical intelligence is transformed
into comprehensive strategic business intelligence for C-level decision making.
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
load_dotenv(os.path.join(project_root, '.env'))
sys.path.insert(0, project_root)

# Import CrewAI tactical workflow
from src.workflow.examples.fast_workflow import FastSalesPipeline

# Import IBM strategic orchestrator
from src.agents.strategic_orchestrator import StrategicOrchestrator

# Import IBM Granite client
from src.ibm_integrations.granite_client import create_granite_client

class StrategicSalesWorkflow:
    """
    Complete Strategic Sales Intelligence Workflow
    
    Architecture:
    1. CrewAI Tactical Layer (49s): Lead research, scoring, outreach
    2. IBM Strategic Layer (2-5 min): Market intel, tech architecture, executive ROI, compliance
    3. Executive Dashboard: Strategic intelligence report with recommendations
    
    Value Transformation:
    Input: Basic lead data (company, contact, size)
    Tactical Output: Lead score, pain points, outreach strategy
    Strategic Output: Market opportunity, ROI analysis, risk assessment, C-level recommendations
    """
    
    def __init__(self):
        self.crewai_pipeline = FastSalesPipeline()
        
        # Initialize IBM Granite client
        self.granite_client = create_granite_client(
            model_name="granite-3.0-8b-instruct",
            backend="watsonx"
        )
        
        # Initialize strategic orchestrator
        self.strategic_orchestrator = StrategicOrchestrator(
            granite_client=self.granite_client,
            config={
                "parallel_execution": True,
                "executive_focus": True,
                "confidence_threshold": 0.6
            }
        )
    
    async def run_complete_strategic_workflow(self, lead_data: dict) -> dict:
        """
        Execute complete strategic workflow: CrewAI → IBM Strategic → Executive Report
        """
        
        print("🚀 Strategic Sales Intelligence Workflow")
        print("=" * 60)
        print(f"Target: {lead_data.get('company_name', 'Unknown Company')}")
        print(f"Industry: {lead_data.get('industry', 'Unknown')}")
        print(f"Size: {lead_data.get('company_size', 0)} employees")
        print()
        
        total_start = datetime.now()
        
        # Phase 1: CrewAI Tactical Intelligence (49 seconds)
        print("📊 PHASE 1: CrewAI Tactical Intelligence")
        print("-" * 40)
        tactical_start = datetime.now()
        
        crewai_results = self.crewai_pipeline.run_fast(lead_data)
        
        tactical_time = (datetime.now() - tactical_start).total_seconds()
        print(f"✅ Tactical analysis completed in {tactical_time:.1f}s")
        
        # Display tactical results summary
        self._display_tactical_summary(crewai_results)
        
        print("\n🎯 PHASE 2: IBM Strategic Intelligence")
        print("-" * 40)
        strategic_start = datetime.now()
        
        # Phase 2: IBM Strategic Intelligence (2-5 minutes)
        strategic_report = await self.strategic_orchestrator.generate_strategic_intelligence(
            company_data=lead_data,
            crewai_results=crewai_results,
            solution_requirements={
                "multi_tenant": True,
                "real_time_processing": False,
                "global_deployment": lead_data.get('company_size', 0) > 1000
            }
        )
        
        strategic_time = (datetime.now() - strategic_start).total_seconds()
        print(f"✅ Strategic analysis completed in {strategic_time:.1f}s")
        
        # Phase 3: Executive Dashboard
        print("\n📈 PHASE 3: Executive Dashboard")
        print("-" * 40)
        self._display_executive_dashboard(strategic_report)
        
        # Summary
        total_time = (datetime.now() - total_start).total_seconds()
        print("\n" + "=" * 60)
        print("🎯 WORKFLOW PERFORMANCE SUMMARY")
        print("=" * 60)
        print(f"CrewAI Tactical Layer: {tactical_time:.1f}s")
        print(f"IBM Strategic Layer: {strategic_time:.1f}s")
        print(f"Total Execution Time: {total_time:.1f}s")
        print()
        
        performance_rating = "🚀 Excellent" if total_time < 300 else "✅ Good" if total_time < 600 else "⚠️ Acceptable"
        print(f"Performance Rating: {performance_rating}")
        print(f"Target: <5 minutes | Actual: {total_time/60:.1f} minutes")
        
        # Return combined results
        return {
            "tactical_results": crewai_results,
            "strategic_intelligence": strategic_report,
            "execution_metrics": {
                "tactical_time_seconds": tactical_time,
                "strategic_time_seconds": strategic_time,
                "total_time_seconds": total_time,
                "performance_rating": performance_rating
            }
        }
    
    def _display_tactical_summary(self, crewai_results: dict):
        """Display summary of CrewAI tactical intelligence"""
        
        print(f"📋 Tactical Intelligence Summary:")
        print(f"   • Lead Score: {crewai_results.get('lead_score', 0):.2f}")
        print(f"   • Pain Points: {len(crewai_results.get('pain_points', []))} identified")
        print(f"   • Tech Stack: {len(crewai_results.get('tech_stack', []))} tools analyzed")
        print(f"   • Engagement Level: {crewai_results.get('engagement_level', 0):.2f}")
        print(f"   • Conversion Probability: {crewai_results.get('predicted_conversion', 0):.1%}")
        
        if crewai_results.get('pain_points'):
            print(f"   • Top Pain Points: {', '.join(crewai_results['pain_points'][:2])}")
    
    def _display_executive_dashboard(self, strategic_report):
        """Display executive strategic intelligence dashboard"""
        
        print("📊 STRATEGIC INTELLIGENCE DASHBOARD")
        print("=" * 50)
        
        # Executive Summary
        print("\n🎯 Executive Summary:")
        print(f"{strategic_report.executive_summary}")
        
        # Financial Metrics
        if strategic_report.strategic_kpis.get('financial_metrics'):
            print(f"\n💰 Financial Analysis:")
            fm = strategic_report.strategic_kpis['financial_metrics']
            print(f"   • Investment Required: {fm.get('total_investment', 'N/A')}")
            print(f"   • Projected ROI: {fm.get('projected_roi', 'N/A')}")
            print(f"   • Payback Period: {fm.get('payback_period', 'N/A')}")
            print(f"   • 3-Year Revenue: {fm.get('3yr_revenue_potential', 'N/A')}")
        
        # Market Intelligence
        if strategic_report.strategic_kpis.get('market_metrics'):
            print(f"\n🌍 Market Intelligence:")
            mm = strategic_report.strategic_kpis['market_metrics']
            print(f"   • Total Market Size: {mm.get('market_size', 'N/A')}")
            print(f"   • Annual Growth Rate: {mm.get('growth_rate', 'N/A')}")
            print(f"   • Market Opportunity Score: {mm.get('opportunity_score', 'N/A')}")
            print(f"   • Timing Score: {mm.get('timing_score', 'N/A')}")
        
        # Technical Architecture
        if strategic_report.strategic_kpis.get('operational_metrics'):
            print(f"\n⚙️ Technical Architecture:")
            om = strategic_report.strategic_kpis['operational_metrics']
            print(f"   • Feasibility Score: {om.get('feasibility_score', 'N/A')}")
            print(f"   • Implementation Timeline: {om.get('implementation_timeline', 'N/A')}")
            print(f"   • Team Size Required: {om.get('team_size_required', 'N/A')}")
            print(f"   • Architecture Score: {om.get('architecture_score', 'N/A')}")
        
        # Risk Assessment
        if strategic_report.strategic_kpis.get('risk_metrics'):
            print(f"\n🛡️ Risk Assessment:")
            rm = strategic_report.strategic_kpis['risk_metrics']
            print(f"   • Overall Risk Level: {rm.get('overall_risk_level', 'N/A').title()}")
            print(f"   • Risk Score: {rm.get('risk_score', 'N/A')}")
            print(f"   • Compliance Readiness: {rm.get('compliance_readiness', 'N/A')}")
            print(f"   • Potential Financial Impact: {rm.get('potential_financial_impact', 'N/A')}")
        
        # Key Recommendations
        print(f"\n🎯 Strategic Recommendations:")
        for i, rec in enumerate(strategic_report.key_recommendations[:3], 1):
            print(f"   {i}. {rec}")
        
        # Immediate Actions
        print(f"\n⚡ Immediate Actions (Next 30 Days):")
        for i, action in enumerate(strategic_report.immediate_actions[:3], 1):
            print(f"   {i}. {action}")
        
        # Strategic Initiatives
        print(f"\n🚀 Strategic Initiatives (3-12 Months):")
        for i, initiative in enumerate(strategic_report.strategic_initiatives[:3], 1):
            print(f"   {i}. {initiative}")
        
        # Analysis Quality
        print(f"\n📈 Analysis Quality:")
        print(f"   • Overall Confidence: {strategic_report.analysis_confidence:.1%}")
        print(f"   • Strategic Synthesis Score: {strategic_report.strategic_synthesis.get('strategic_alignment_score', 0.5):.2f}")
        print(f"   • Investment Coherence: {strategic_report.strategic_synthesis.get('investment_coherence', {}).get('overall_coherence_score', 0.5):.1%}")

async def run_enterprise_demo():
    """Run strategic workflow demo with enterprise prospect"""
    
    enterprise_prospect = {
        "lead_id": "ENT_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "cto@techflowdynamics.com",
        "contact_name": "Sarah Chen",
        "company_size": 1250,
        "industry": "Enterprise Software",
        "location": "Austin, TX",
        "annual_revenue": 180000000,  # $180M revenue
        "stage": "qualification"
    }
    
    workflow = StrategicSalesWorkflow()
    result = await workflow.run_complete_strategic_workflow(enterprise_prospect)
    
    return result

async def run_mid_market_demo():
    """Run strategic workflow demo with mid-market prospect"""
    
    mid_market_prospect = {
        "lead_id": "MID_001", 
        "company_name": "CloudBridge Solutions",
        "contact_email": "vp.engineering@cloudbridge.com",
        "contact_name": "Alex Rodriguez", 
        "company_size": 350,
        "industry": "Cloud Infrastructure",
        "location": "Denver, CO",
        "annual_revenue": 25000000,  # $25M revenue
        "stage": "research"
    }
    
    workflow = StrategicSalesWorkflow()
    result = await workflow.run_complete_strategic_workflow(mid_market_prospect)
    
    return result

async def run_fintech_demo():
    """Run strategic workflow demo with fintech prospect (high compliance requirements)"""
    
    fintech_prospect = {
        "lead_id": "FIN_001",
        "company_name": "PaymentCore Technologies", 
        "contact_email": "chief.architect@paymentcore.com",
        "contact_name": "David Kim",
        "company_size": 580,
        "industry": "Financial Technology",
        "location": "New York, NY", 
        "annual_revenue": 45000000,  # $45M revenue
        "stage": "discovery"
    }
    
    workflow = StrategicSalesWorkflow()
    result = await workflow.run_complete_strategic_workflow(fintech_prospect)
    
    return result

async def compare_tactical_vs_strategic():
    """Compare traditional tactical approach vs new strategic approach"""
    
    test_prospect = {
        "lead_id": "TEST_001",
        "company_name": "DataFlow Analytics",
        "contact_email": "ceo@dataflow.com", 
        "contact_name": "Jennifer Martinez",
        "company_size": 425,
        "industry": "Data Analytics",
        "location": "San Francisco, CA",
        "annual_revenue": 32000000
    }
    
    print("🔄 TACTICAL vs STRATEGIC COMPARISON")
    print("=" * 60)
    
    # Traditional Tactical Approach (CrewAI only)
    print("\n📊 TACTICAL APPROACH (CrewAI Only)")
    print("-" * 40)
    tactical_start = datetime.now()
    
    crewai_pipeline = FastSalesPipeline()
    tactical_only = crewai_pipeline.run_fast(test_prospect)
    
    tactical_time = (datetime.now() - tactical_start).total_seconds()
    print(f"✅ Completed in {tactical_time:.1f}s")
    print(f"Output: Lead score, pain points, outreach strategy")
    
    # Strategic Approach (CrewAI + IBM Strategic)
    print(f"\n🎯 STRATEGIC APPROACH (CrewAI + IBM Strategic)")
    print("-" * 40)
    strategic_start = datetime.now()
    
    workflow = StrategicSalesWorkflow()
    strategic_full = await workflow.run_complete_strategic_workflow(test_prospect)
    
    strategic_time = (datetime.now() - strategic_start).total_seconds()
    print(f"✅ Completed in {strategic_time:.1f}s")
    
    # Value Comparison
    print(f"\n📈 VALUE COMPARISON")
    print("-" * 40)
    print(f"Tactical Approach:")
    print(f"   • Execution Time: {tactical_time:.1f}s")
    print(f"   • Output Depth: Basic lead intelligence")
    print(f"   • Decision Support: Operational")
    print(f"   • ROI Analysis: None")
    print(f"   • Risk Assessment: None")
    print(f"   • Market Intelligence: None")
    
    print(f"\nStrategic Approach:")
    print(f"   • Execution Time: {strategic_time:.1f}s ({strategic_time/tactical_time:.1f}x longer)")
    print(f"   • Output Depth: Executive business intelligence")
    print(f"   • Decision Support: C-level strategic")
    print(f"   • ROI Analysis: Complete financial modeling")
    print(f"   • Risk Assessment: Comprehensive compliance & risk")
    print(f"   • Market Intelligence: Industry analysis & positioning")
    
    roi_multiplier = strategic_report.executive_decision_intelligence.projected_roi if strategic_full.get('strategic_intelligence') and strategic_full['strategic_intelligence'].executive_decision_intelligence else 2.5
    
    print(f"\n🎯 VALUE PROPOSITION")
    print("-" * 40)
    print(f"Time Investment: {(strategic_time - tactical_time)/60:.1f} additional minutes")
    print(f"Value Multiplier: {roi_multiplier:.1f}x ROI potential identified")
    print(f"Strategic Insight: Market opportunity quantified")
    print(f"Executive Readiness: C-level decision support included")
    
    return {
        "tactical_time": tactical_time,
        "strategic_time": strategic_time, 
        "value_multiplier": roi_multiplier,
        "tactical_results": tactical_only,
        "strategic_results": strategic_full
    }

async def main():
    """Main demo function"""
    
    print("🚀 Strategic Sales Intelligence Workflow Demos")
    print("=" * 70)
    print("Demonstrating the new 2-tier architecture:")
    print("CrewAI (Tactical) → IBM Strategic Agents → Executive Intelligence")
    print()
    
    demos = [
        ("Enterprise Prospect Demo", run_enterprise_demo),
        ("Mid-Market Prospect Demo", run_mid_market_demo), 
        ("FinTech Compliance Demo", run_fintech_demo),
        ("Tactical vs Strategic Comparison", compare_tactical_vs_strategic)
    ]
    
    for demo_name, demo_func in demos:
        print(f"\n{'=' * 70}")
        print(f"🎯 {demo_name.upper()}")
        print(f"{'=' * 70}")
        
        try:
            start_time = datetime.now()
            result = await demo_func()
            end_time = datetime.now()
            
            print(f"\n✅ {demo_name} completed successfully")
            print(f"   Execution time: {(end_time - start_time).total_seconds():.1f}s")
            
        except Exception as e:
            print(f"\n❌ {demo_name} failed: {str(e)}")
        
        # Pause between demos
        print(f"\n" + "." * 50)
        await asyncio.sleep(2)
    
    print(f"\n{'=' * 70}")
    print("🎯 ALL DEMOS COMPLETED")
    print(f"{'=' * 70}")
    print("Strategic Sales Intelligence Workflow successfully demonstrated!")
    print()
    print("Key Benefits Demonstrated:")
    print("• CrewAI tactical intelligence (49s) → IBM strategic intelligence (2-5 min)")
    print("• Lead processing → Executive decision support")
    print("• Operational metrics → Strategic business intelligence")
    print("• Basic scoring → Comprehensive ROI modeling")
    print("• Simple outreach → Market positioning strategy")

if __name__ == "__main__":
    # Enable asyncio debugging for development
    import asyncio
    
    # Run the main demo
    asyncio.run(main())
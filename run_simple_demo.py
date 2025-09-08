#!/usr/bin/env python3
"""
Simple Strategic Demo - Works without IBM watsonx credentials
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append('.')

from src.workflow.examples.fast_workflow import FastSalesPipeline

class SimpleStrategicDemo:
    """Simple demo showing tactical vs strategic approach conceptually"""
    
    def __init__(self):
        self.crewai_pipeline = FastSalesPipeline()
    
    async def run_tactical_only(self, lead_data):
        """Run CrewAI tactical analysis only"""
        
        print("📊 TACTICAL ANALYSIS (CrewAI Only)")
        print("=" * 50)
        
        start_time = datetime.now()
        crewai_results = self.crewai_pipeline.run_fast(lead_data)
        tactical_time = (datetime.now() - start_time).total_seconds()
        
        print(f"\n✅ Tactical analysis completed in {tactical_time:.1f}s")
        
        # Show what tactical analysis provides
        print(f"\n📋 Tactical Intelligence Output:")
        print(f"• Lead Score: {crewai_results.get('lead_score', 0):.2f}")
        print(f"• Pain Points: {len(crewai_results.get('pain_points', []))} identified")
        print(f"• Tech Stack: {len(crewai_results.get('tech_stack', []))} tools")
        print(f"• Conversion Probability: {crewai_results.get('predicted_conversion', 0):.1%}")
        print(f"• Recommended Approach: {crewai_results.get('recommended_approach', 'Standard outreach')}")
        
        return crewai_results, tactical_time
    
    def simulate_strategic_analysis(self, crewai_results, lead_data):
        """Simulate what strategic analysis would provide (without IBM watsonx)"""
        
        print(f"\n🎯 STRATEGIC ANALYSIS (Simulated IBM Intelligence)")
        print("=" * 50)
        
        company_size = lead_data.get('company_size', 0)
        industry = lead_data.get('industry', '').lower()
        
        # Simulate market intelligence
        market_size = 150_000_000_000 if 'software' in industry else 75_000_000_000  # $150B vs $75B
        growth_rate = 0.15 if 'software' in industry else 0.08  # 15% vs 8%
        
        # Simulate ROI calculation
        if company_size > 1000:
            investment = 1_500_000
            annual_revenue = 400_000
            roi = 2.4
        elif company_size > 500:
            investment = 750_000
            annual_revenue = 200_000
            roi = 2.1
        else:
            investment = 300_000
            annual_revenue = 100_000
            roi = 1.8
        
        payback_months = int((investment / annual_revenue) * 12)
        
        print(f"🌍 Market Intelligence:")
        print(f"• Total Market Size: ${market_size:,.0f}")
        print(f"• Annual Growth Rate: {growth_rate:.1%}")
        print(f"• Market Timing Score: 0.8 (Favorable)")
        print(f"• Competitive Landscape: Fragmented with opportunities")
        
        print(f"\n💰 Executive Decision Intelligence:")
        print(f"• Investment Required: ${investment:,.0f}")
        print(f"• Projected Annual Revenue: ${annual_revenue:,.0f}")
        print(f"• ROI Multiple: {roi:.1f}x")
        print(f"• Payback Period: {payback_months} months")
        print(f"• 3-Year Revenue Potential: ${annual_revenue * 3 * 1.15:,.0f}")
        
        print(f"\n⚙️ Technical Architecture:")
        complexity = "Enterprise" if company_size > 1000 else "High" if company_size > 500 else "Medium"
        timeline = "12-15 months" if company_size > 1000 else "8-10 months" if company_size > 500 else "6-8 months"
        print(f"• Solution Complexity: {complexity}")
        print(f"• Implementation Timeline: {timeline}")
        print(f"• Feasibility Score: 0.{85 if company_size > 500 else 75}")
        print(f"• Team Size Required: {3 + (company_size // 500)} developers")
        
        print(f"\n🛡️ Compliance & Risk:")
        risk_level = "Medium" if company_size < 1000 else "High"
        frameworks = ["GDPR", "SOC2"] + (["ISO27001"] if company_size > 500 else [])
        print(f"• Overall Risk Level: {risk_level}")
        print(f"• Applicable Frameworks: {', '.join(frameworks)}")
        print(f"• Compliance Readiness: 0.{65 if len(frameworks) > 2 else 75}")
        print(f"• Risk-Adjusted Investment: ${investment * 1.2:,.0f}")
        
        return {
            "market_size": market_size,
            "growth_rate": growth_rate,
            "investment": investment,
            "roi": roi,
            "payback_months": payback_months,
            "complexity": complexity,
            "risk_level": risk_level
        }
    
    def generate_executive_summary(self, tactical_results, strategic_results, lead_data):
        """Generate executive summary combining tactical and strategic intelligence"""
        
        print(f"\n📊 EXECUTIVE SUMMARY")
        print("=" * 50)
        
        company_name = lead_data.get('company_name', 'Target Company')
        
        summary = f"""
🎯 STRATEGIC OPPORTUNITY ASSESSMENT: {company_name}

INVESTMENT THESIS:
${strategic_results['investment']:,.0f} investment generating {strategic_results['roi']:.1f}x ROI 
with {strategic_results['payback_months']}-month payback in ${strategic_results['market_size']/1_000_000_000:.0f}B 
growing market ({strategic_results['growth_rate']:.1%} annually).

TACTICAL INTELLIGENCE:
• Lead Quality: {tactical_results.get('lead_score', 0):.0%} (High-potential prospect)
• Pain Points: {len(tactical_results.get('pain_points', []))} critical business challenges identified
• Conversion Probability: {tactical_results.get('predicted_conversion', 0):.0%}

STRATEGIC INTELLIGENCE:
• Market Position: {strategic_results['market_size']/1_000_000_000:.0f}B market with {strategic_results['growth_rate']:.1%} growth
• Technical Feasibility: {strategic_results['complexity']} implementation complexity
• Risk Assessment: {strategic_results['risk_level']} risk profile with mitigations identified

EXECUTIVE RECOMMENDATION:
PROCEED with phased implementation. Strong market opportunity aligns with 
technical capabilities. Risk-adjusted ROI exceeds corporate hurdle rates.
        """
        
        print(summary)
        
        print(f"\n🚀 KEY DIFFERENTIATORS:")
        print("• CrewAI Tactical (49s): Lead scoring, pain points, outreach strategy")
        print("• IBM Strategic (2-5 min): Market analysis, ROI modeling, risk assessment")
        print("• Combined Value: Operational efficiency + Executive decision support")
        
        return summary

async def main():
    """Run the simple strategic demo"""
    
    # Sample prospect
    test_prospect = {
        "lead_id": "DEMO_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "cto@techflow.com",
        "contact_name": "Sarah Chen", 
        "company_size": 850,
        "industry": "Enterprise Software",
        "location": "Austin, TX",
        "annual_revenue": 75000000,  # $75M
        "stage": "qualification"
    }
    
    print("🚀 STRATEGIC SALES INTELLIGENCE DEMO")
    print("=" * 60)
    print(f"Demonstrating: CrewAI Tactical → IBM Strategic → Executive Intelligence")
    print(f"Target: {test_prospect['company_name']}")
    print(f"Industry: {test_prospect['industry']}")
    print(f"Size: {test_prospect['company_size']} employees")
    print()
    
    demo = SimpleStrategicDemo()
    
    # Phase 1: Tactical Analysis
    tactical_results, tactical_time = await demo.run_tactical_only(test_prospect)
    
    # Phase 2: Strategic Analysis (Simulated)
    strategic_start = datetime.now()
    strategic_results = demo.simulate_strategic_analysis(tactical_results, test_prospect)
    strategic_time = (datetime.now() - strategic_start).total_seconds()
    
    print(f"\n✅ Strategic analysis completed in {strategic_time:.1f}s")
    
    # Phase 3: Executive Summary
    demo.generate_executive_summary(tactical_results, strategic_results, test_prospect)
    
    # Final Summary
    total_time = tactical_time + strategic_time
    print(f"\n" + "=" * 60)
    print(f"🎯 TRANSFORMATION SUMMARY")
    print("=" * 60)
    print(f"Tactical Analysis Time: {tactical_time:.1f}s")
    print(f"Strategic Analysis Time: {strategic_time:.1f}s (simulated)")
    print(f"Total Execution Time: {total_time:.1f}s")
    print()
    print(f"VALUE TRANSFORMATION:")
    print(f"• From: Basic lead scoring and outreach")
    print(f"• To: Executive decision support with ROI modeling")
    print(f"• Audience: Sales ops → C-level executives")
    print(f"• Use Case: Lead processing → Strategic investment analysis")

if __name__ == "__main__":
    asyncio.run(main())
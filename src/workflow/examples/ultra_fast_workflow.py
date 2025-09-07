#!/usr/bin/env python3
"""
Ultra-Fast Sales Pipeline - Completes in 30-60 seconds

Uses intelligent fallbacks and minimal AI calls for maximum speed
"""

import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
load_dotenv(os.path.join(project_root, '.env'))
sys.path.insert(0, project_root)

from src.workflow.states.lead_states import LeadState

class UltraFastPipeline:
    """Ultra-fast pipeline with smart fallbacks"""
    
    def run(self, lead_data):
        """Run ultra-fast analysis"""
        print("⚡ Ultra-Fast Sales Analysis")
        print("=" * 50)
        
        start_time = datetime.now()
        state = LeadState(**lead_data)
        
        # Step 1: Smart Research (5-10 seconds)
        print("\n🔍 Research Analysis...")
        state = self._smart_research(state)
        print(f"   ✅ Found {len(state.pain_points)} pain points")
        
        # Step 2: Mathematical Scoring (2-3 seconds)
        print("\n📊 Lead Scoring...")
        state = self._calculate_scores(state)
        print(f"   ✅ Lead score: {state.lead_score:.2f}")
        
        # Step 3: Outreach Strategy (3-5 seconds)
        print("\n📧 Outreach Planning...")
        state = self._plan_outreach(state)
        print(f"   ✅ Strategy: {state.metadata['outreach_type']}")
        
        # Step 4: Conversion Prediction (2-3 seconds)
        print("\n🎯 Conversion Analysis...")
        state = self._predict_conversion(state)
        print(f"   ✅ Conversion probability: {state.predicted_conversion:.1%}")
        
        # Step 5: Final Assignment (1 second)
        print("\n👤 Sales Assignment...")
        if state.lead_score > 0.6:
            state = self._qualify_and_assign(state)
            print(f"   ✅ Assigned to: {state.assigned_rep}")
        
        execution_time = (datetime.now() - start_time).total_seconds()
        self._print_results(state, execution_time)
        
        return state.model_dump()
    
    def _smart_research(self, state):
        """Intelligent research based on industry and company size"""
        
        industry = (state.industry or "technology").lower()
        size = state.company_size or 250
        
        # Industry-specific pain points
        pain_point_db = {
            "technology": ["Scaling infrastructure", "Technical debt", "Release velocity", "Security compliance"],
            "software": ["User adoption", "Feature complexity", "Performance optimization", "Integration challenges"], 
            "fintech": ["Regulatory compliance", "Security requirements", "Market volatility", "Risk management"],
            "healthcare": ["Data privacy", "Regulatory compliance", "System integration", "Cost optimization"],
            "manufacturing": ["Supply chain", "Quality control", "Automation", "Cost reduction"],
            "retail": ["Customer experience", "Inventory management", "Digital transformation", "Cost control"],
            "saas": ["Customer churn", "Scaling challenges", "Feature development", "Market competition"]
        }
        
        # Size-specific challenges
        if size < 50:
            state.pain_points = ["Resource constraints", "Process standardization", "Growth scaling"]
        elif size < 200:
            state.pain_points = ["Team coordination", "Process optimization", "Technology scaling"]
        else:
            state.pain_points = ["Operational efficiency", "System integration", "Team productivity"]
        
        # Add industry-specific points
        for key, points in pain_point_db.items():
            if key in industry:
                state.pain_points.extend(points[:2])
                break
        
        # Tech stack prediction
        if size < 100:
            state.tech_stack = ["Basic CRM", "Cloud Storage", "Collaboration Tools"]
        elif size < 500:
            state.tech_stack = ["CRM Platform", "Cloud Infrastructure", "Analytics Tools", "Security Suite"]
        else:
            state.tech_stack = ["Enterprise CRM", "Multi-cloud", "Business Intelligence", "Security Platform", "DevOps Tools"]
        
        # Business insights
        state.key_insights = [
            f"Company operates in {industry} sector with {size} employees",
            f"Typical challenges for {size}-person {industry} companies",
            "Growth stage requiring process optimization"
        ]
        
        state.research_completed = True
        return state
    
    def _calculate_scores(self, state):
        """Mathematical scoring algorithm"""
        
        # Base score components
        size_score = self._score_company_size(state.company_size or 250)
        industry_score = self._score_industry_fit(state.industry or "technology")
        pain_score = min(len(state.pain_points) * 0.15, 0.3)
        research_score = 0.2 if state.research_completed else 0
        
        # Calculate lead score
        state.lead_score = min(size_score + industry_score + pain_score + research_score, 1.0)
        
        # Engagement estimation
        if state.company_size and state.company_size > 200:
            state.engagement_level = 0.4
        else:
            state.engagement_level = 0.3
            
        if len(state.pain_points) > 2:
            state.engagement_level += 0.2
        
        # Qualification score
        state.qualification_score = state.lead_score * 0.85
        
        return state
    
    def _score_company_size(self, size):
        """Score based on company size"""
        if size >= 1000:
            return 0.9
        elif size >= 500:
            return 0.8
        elif size >= 200:
            return 0.7
        elif size >= 100:
            return 0.6
        elif size >= 50:
            return 0.5
        else:
            return 0.3
    
    def _score_industry_fit(self, industry):
        """Score based on industry fit"""
        high_fit = ["technology", "software", "saas", "fintech", "healthcare"]
        medium_fit = ["manufacturing", "retail", "finance", "consulting"]
        
        industry_lower = industry.lower()
        
        for fit_industry in high_fit:
            if fit_industry in industry_lower:
                return 0.9
        
        for fit_industry in medium_fit:
            if fit_industry in industry_lower:
                return 0.7
        
        return 0.6  # Default score
    
    def _plan_outreach(self, state):
        """Plan outreach strategy"""
        
        # Determine outreach type
        if state.lead_score > 0.7:
            outreach_type = "High-touch personal outreach"
            channels = ["Email", "LinkedIn", "Phone", "Video message"]
        elif state.lead_score > 0.5:
            outreach_type = "Medium-touch multi-channel"
            channels = ["Email", "LinkedIn", "Follow-up email"]
        else:
            outreach_type = "Low-touch nurture campaign"
            channels = ["Email", "Content nurture"]
        
        # Simulate outreach
        state.outreach_attempts = 1
        state.response_rate = min(state.lead_score * 0.4, 0.8)  # Score influences response rate
        state.last_contact = datetime.now()
        
        # Store strategy
        state.metadata.update({
            "outreach_type": outreach_type,
            "channels": channels,
            "estimated_response_rate": state.response_rate
        })
        
        return state
    
    def _predict_conversion(self, state):
        """Predict conversion probability"""
        
        # Base conversion rate
        base_rate = 0.2
        
        # Adjust for lead score
        score_multiplier = state.lead_score * 1.5
        
        # Adjust for company size
        if state.company_size:
            if state.company_size > 500:
                size_boost = 0.2
            elif state.company_size > 200:
                size_boost = 0.15
            elif state.company_size > 100:
                size_boost = 0.1
            else:
                size_boost = 0.05
        else:
            size_boost = 0.1
        
        # Adjust for pain points
        pain_boost = min(len(state.pain_points) * 0.05, 0.15)
        
        # Calculate final probability
        state.predicted_conversion = min(base_rate + (score_multiplier * 0.3) + size_boost + pain_boost, 0.95)
        
        # Recommended approach
        if state.predicted_conversion > 0.7:
            state.recommended_approach = "Enterprise discovery with C-level engagement"
        elif state.predicted_conversion > 0.5:
            state.recommended_approach = "Technical demo with decision makers"
        elif state.predicted_conversion > 0.3:
            state.recommended_approach = "Standard discovery call"
        else:
            state.recommended_approach = "Nurture campaign with value content"
        
        state.simulation_completed = True
        return state
    
    def _qualify_and_assign(self, state):
        """Qualify lead and assign sales rep"""
        
        if state.qualification_score > 0.7:
            state.stage = "qualified"
            
            # Assign rep based on company size and score
            if state.company_size and state.company_size > 1000:
                state.assigned_rep = "enterprise_rep"
            elif state.company_size and state.company_size > 200:
                state.assigned_rep = "mid_market_rep"
            else:
                state.assigned_rep = "smb_rep"
                
            # If very high score, hand off to sales
            if state.qualification_score > 0.8:
                state.stage = "sales_handoff"
                state.handoff_notes = f"High-quality lead with {state.predicted_conversion:.1%} conversion probability"
        
        return state
    
    def _print_results(self, state, execution_time):
        """Print comprehensive results"""
        
        print("\n" + "="*60)
        print("⚡ ULTRA-FAST ANALYSIS COMPLETE")
        print("="*60)
        
        # Performance
        print(f"⏱️  Execution Time: {execution_time:.1f} seconds")
        if execution_time < 30:
            perf_icon = "🚀"
        elif execution_time < 60:
            perf_icon = "✅"
        else:
            perf_icon = "⚠️"
        print(f"   Performance: {perf_icon} Target: <60s")
        
        # Company overview
        print(f"\n🏢 Company Analysis:")
        print(f"   • {state.company_name} ({state.company_size or 'Unknown'} employees)")
        print(f"   • Industry: {state.industry or 'Unknown'}")
        print(f"   • Contact: {state.contact_name or 'Unknown'}")
        
        # Scoring results
        print(f"\n📊 Lead Intelligence:")
        print(f"   • Lead Score: {state.lead_score:.2f}/1.0 ⭐" + "⭐"*int(state.lead_score*4))
        print(f"   • Qualification: {state.qualification_score:.2f}/1.0")
        print(f"   • Current Stage: {state.stage}")
        
        # Business insights
        print(f"\n🔍 Key Findings:")
        print(f"   • Pain Points: {len(state.pain_points)} identified")
        for i, pain in enumerate(state.pain_points[:3], 1):
            print(f"     {i}. {pain}")
        
        print(f"   • Tech Stack: {len(state.tech_stack)} tools identified")
        
        # Sales recommendations
        print(f"\n🎯 Sales Intelligence:")
        print(f"   • Conversion Probability: {state.predicted_conversion:.1%}")
        print(f"   • Recommended Approach: {state.recommended_approach}")
        print(f"   • Response Rate Est: {state.response_rate:.1%}")
        
        if state.assigned_rep:
            print(f"\n👤 Assignment:")
            print(f"   • Assigned Rep: {state.assigned_rep}")
            if state.handoff_notes:
                print(f"   • Notes: {state.handoff_notes}")
        
        # Next steps
        print(f"\n📋 Immediate Next Steps:")
        if state.lead_score > 0.7:
            print(f"   1. Schedule discovery call within 48 hours")
            print(f"   2. Prepare customized pitch deck")
            print(f"   3. Research key stakeholders")
        elif state.lead_score > 0.5:
            print(f"   1. Send personalized outreach sequence")
            print(f"   2. Share relevant case study")
            print(f"   3. Follow up in 1 week")
        else:
            print(f"   1. Add to nurture campaign")
            print(f"   2. Share valuable content monthly")
            print(f"   3. Monitor for trigger events")


def run_single_ultra_fast():
    """Run single lead through ultra-fast pipeline"""
    
    lead_data = {
        "lead_id": "ultra_001",
        "company_name": "RocketCode Inc",
        "contact_email": "ceo@rocketcode.com", 
        "contact_name": "Jennifer Walsh",
        "company_size": 340,
        "industry": "Software Technology",
        "location": "San Jose, CA"
    }
    
    print("⚡ Ultra-Fast Sales Pipeline Demo")
    print(f"Analyzing: {lead_data['company_name']}")
    
    pipeline = UltraFastPipeline()
    result = pipeline.run(lead_data)
    
    return result


def run_batch_ultra_fast():
    """Process multiple leads in batch"""
    
    leads = [
        {
            "lead_id": "batch_001",
            "company_name": "DataVault Systems",
            "contact_email": "vp@datavault.com",
            "contact_name": "Michael Chen",
            "company_size": 850,
            "industry": "Data Analytics"
        },
        {
            "lead_id": "batch_002", 
            "company_name": "HealthTech Solutions",
            "contact_email": "cto@healthtech.com",
            "contact_name": "Dr. Sarah Johnson",
            "company_size": 120,
            "industry": "Healthcare Technology"
        },
        {
            "lead_id": "batch_003",
            "company_name": "FinanceFlow AI",
            "contact_email": "founder@financeflow.com",
            "contact_name": "Robert Kim",
            "company_size": 65,
            "industry": "FinTech"
        }
    ]
    
    print("⚡ Ultra-Fast Batch Processing")
    print("="*50)
    
    pipeline = UltraFastPipeline()
    results = []
    total_start = datetime.now()
    
    for i, lead in enumerate(leads, 1):
        print(f"\n🔥 Lead {i}/{len(leads)}: {lead['company_name']}")
        print("-" * 30)
        
        lead_start = datetime.now()
        result = pipeline.run(lead)
        lead_time = (datetime.now() - lead_start).total_seconds()
        
        results.append(result)
        print(f"⚡ Completed in {lead_time:.1f}s")
    
    # Batch summary
    total_time = (datetime.now() - total_start).total_seconds()
    
    print("\n" + "="*50)
    print("📊 BATCH SUMMARY")
    print("="*50)
    print(f"Total Leads: {len(results)}")
    print(f"Total Time: {total_time:.1f} seconds")
    print(f"Average: {total_time/len(results):.1f} seconds per lead")
    
    # Analytics
    scores = [r['lead_score'] for r in results]
    conversions = [r['predicted_conversion'] for r in results]
    
    print(f"\n📈 Performance Analytics:")
    print(f"   • Average Lead Score: {sum(scores)/len(scores):.2f}")
    print(f"   • Average Conversion: {sum(conversions)/len(conversions):.1%}")
    print(f"   • High-Quality Leads: {sum(1 for s in scores if s > 0.7)}/{len(scores)}")
    
    return results


if __name__ == "__main__":
    print("⚡ Ultra-Fast Sales Pipeline Examples")
    print("="*50)
    
    # Single lead
    print("\n1️⃣  Single Lead Analysis:")
    run_single_ultra_fast()
    
    # Batch processing
    print("\n\n2️⃣  Batch Processing:")
    run_batch_ultra_fast()
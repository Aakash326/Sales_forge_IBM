#!/usr/bin/env python3
"""
Fast Sales Pipeline Workflow - Completes in 1-2 minutes

This version uses:
- Single AI calls instead of multi-agent crews
- Simplified logic where possible
- Faster execution with same comprehensive output
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
load_dotenv(os.path.join(project_root, '.env'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

from src.workflow.sales_pipeline import SalesPipeline

class FastSalesPipeline(SalesPipeline):
    """Fast version of sales pipeline with optimized execution"""
    
    def __init__(self, config=None):
        """Initialize with fast mode configuration"""
        super().__init__(config)
        self.fast_mode = True
    
    def run_fast(self, initial_state):
        """Run pipeline in fast mode - bypasses LangGraph for speed"""
        from src.workflow.states.lead_states import LeadState
        
        print("🚀 Fast Sales Pipeline - Optimized for 1-2 minute execution")
        print("=" * 60)
        
        # Convert to LeadState
        lead_state = LeadState(**initial_state)
        start_time = datetime.now()
        
        # Step 1: Fast Research (30-45 seconds)
        print("\n📊 Step 1: Research Phase")
        print("-" * 30)
        lead_state = self._fast_research(lead_state)
        self._print_step_results("Research", lead_state)
        
        # Step 2: Fast Scoring (15-20 seconds)  
        print("\n📈 Step 2: Scoring Phase")
        print("-" * 30)
        lead_state = self._fast_scoring(lead_state)
        self._print_step_results("Scoring", lead_state)
        
        # Step 3: Fast Outreach (20-30 seconds)
        print("\n📧 Step 3: Outreach Phase")
        print("-" * 30)
        lead_state = self._fast_outreach(lead_state)
        self._print_step_results("Outreach", lead_state)
        
        # Step 4: Fast Simulation (15-20 seconds)
        print("\n🎭 Step 4: Simulation Phase")
        print("-" * 30)
        lead_state = self._fast_simulation(lead_state)
        self._print_step_results("Simulation", lead_state)
        
        # Step 5: Qualification & Handoff (5 seconds)
        print("\n✅ Step 5: Qualification & Handoff")
        print("-" * 30)
        if lead_state.predicted_conversion > 0.6:
            lead_state = self._qualify_lead(lead_state)
            if lead_state.qualification_score > 0.7:
                lead_state = self._handoff_to_sales(lead_state)
        
        # Final results
        execution_time = (datetime.now() - start_time).total_seconds()
        self._print_final_results(lead_state, execution_time)
        
        return lead_state.model_dump()
    
    def _fast_research(self, state):
        """Fast research using single AI call instead of crew"""
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_research(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Research {company_name} ({industry}, {company_size} employees) and provide:
            
            1. 3 likely pain points for this company size/industry
            2. 3 technology tools they probably use
            3. 2 key business insights
            
            Format as JSON:
            {{
                "pain_points": ["point1", "point2", "point3"],
                "tech_stack": ["tool1", "tool2", "tool3"],
                "insights": ["insight1", "insight2"]
            }}
            
            Keep responses concise and realistic for a {industry} company.
            """)
            
            chain = prompt | llm
            response = chain.invoke({
                "company_name": state.company_name,
                "industry": state.industry or "Technology",
                "company_size": state.company_size or 250
            })
            
            # Parse response (simplified)
            import json
            try:
                result = json.loads(response.content)
                state.pain_points = result.get("pain_points", [])
                state.tech_stack = result.get("tech_stack", [])
                state.key_insights = result.get("insights", [])
            except:
                # Fallback if JSON parsing fails
                state.pain_points = ["Scaling challenges", "Process optimization", "Technology integration"]
                state.tech_stack = ["CRM", "Cloud Services", "Analytics"]
                state.key_insights = ["Growing team needs structure", "Technology modernization opportunity"]
            
            state.research_completed = True
            
        except Exception as e:
            print(f"⚠️  AI research failed, using fallback: {str(e)[:50]}...")
            state = self._fallback_research(state)
        
        return state
    
    def _fast_scoring(self, state):
        """Fast scoring with single AI call"""
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_scoring(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Score this lead on a scale of 0-1:
            
            Company: {company_name} ({company_size} employees, {industry})
            Pain Points: {pain_points}
            
            Provide scores as JSON:
            {{
                "lead_score": 0.75,
                "qualification_score": 0.68,
                "rationale": "Brief explanation"
            }}
            
            Consider company size, industry fit, and pain point alignment.
            """)
            
            chain = prompt | llm
            response = chain.invoke({
                "company_name": state.company_name,
                "company_size": state.company_size or 250,
                "industry": state.industry or "Technology",
                "pain_points": ", ".join(state.pain_points) if state.pain_points else "To be discovered"
            })
            
            # Parse response
            import json
            try:
                result = json.loads(response.content)
                state.lead_score = result.get("lead_score", 0.6)
                state.qualification_score = result.get("qualification_score", 0.5)
            except:
                # Fallback scoring
                base_score = 0.6
                if state.company_size and state.company_size > 200:
                    base_score += 0.1
                if state.pain_points:
                    base_score += 0.1
                state.lead_score = min(base_score, 1.0)
                state.qualification_score = state.lead_score * 0.8
            
        except Exception as e:
            print(f"⚠️  AI scoring failed, using fallback: {str(e)[:50]}...")
            state = self._fallback_scoring(state)
        
        return state
    
    def _fast_outreach(self, state):
        """Fast outreach campaign generation"""
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_outreach(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Create personalized outreach messages for {contact_name} at {company_name}:
            
            Company: {company_size} employees, {industry}
            Pain Points: {pain_points}
            
            Generate as JSON:
            {{
                "email": {{
                    "subject": "Brief, compelling subject line",
                    "body": "Professional email body (2-3 paragraphs, 150 words max)"
                }},
                "linkedin": {{
                    "connection_message": "Brief LinkedIn connection request (under 200 chars)",
                    "follow_up_message": "Follow-up LinkedIn message after connection"
                }},
                "strategy": "Overall approach and timing recommendations"
            }}
            
            Make messages personal, value-focused, and specific to their pain points.
            """)
            
            chain = prompt | llm
            response = chain.invoke({
                "contact_name": state.contact_name or "the contact",
                "company_name": state.company_name,
                "company_size": state.company_size or 250,
                "industry": state.industry or "Technology",
                "pain_points": ", ".join(state.pain_points[:2]) if state.pain_points else "scaling challenges"
            })
            
            # Parse the structured outreach response
            import json
            try:
                outreach_data = json.loads(response.content)
                
                # Store detailed outreach messages
                state.metadata["email_subject"] = outreach_data.get("email", {}).get("subject", "")
                state.metadata["email_body"] = outreach_data.get("email", {}).get("body", "")
                state.metadata["linkedin_connection"] = outreach_data.get("linkedin", {}).get("connection_message", "")
                state.metadata["linkedin_follow_up"] = outreach_data.get("linkedin", {}).get("follow_up_message", "")
                state.metadata["outreach_strategy"] = outreach_data.get("strategy", "")
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                state.metadata["outreach_strategy"] = response.content[:500]
                state.metadata["email_subject"] = "Strategic Partnership Opportunity"
                state.metadata["email_body"] = "Fallback email content generated"
                state.metadata["linkedin_connection"] = "I'd like to connect and discuss potential synergies"
                state.metadata["linkedin_follow_up"] = "Thanks for connecting! I'd love to explore how we can help your team"
            
            # Update outreach metrics
            state.outreach_attempts = 1
            state.engagement_level = 0.4  # Initial engagement
            state.response_rate = 0.25  # Expected response rate
            state.last_contact = datetime.now()
            
        except Exception as e:
            print(f"⚠️  AI outreach failed, using fallback: {str(e)[:50]}...")
            state = self._fallback_outreach(state)
        
        return state
    
    def _fast_simulation(self, state):
        """Fast simulation using single AI call"""
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_simulation(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Simulate sales conversation outcome for {company_name}:
            
            Lead Score: {lead_score}
            Company Size: {company_size} employees
            Pain Points: {pain_points}
            Engagement: {engagement_level}
            
            Predict as JSON:
            {{
                "conversion_probability": 0.65,
                "recommended_approach": "specific strategy",
                "key_objections": ["objection1", "objection2"]
            }}
            """)
            
            chain = prompt | llm
            response = chain.invoke({
                "company_name": state.company_name,
                "lead_score": state.lead_score,
                "company_size": state.company_size or 250,
                "pain_points": ", ".join(state.pain_points[:2]) if state.pain_points else "None identified",
                "engagement_level": state.engagement_level
            })
            
            # Parse simulation results
            import json
            try:
                result = json.loads(response.content)
                state.predicted_conversion = result.get("conversion_probability", 0.5)
                state.recommended_approach = result.get("recommended_approach", "Standard discovery approach")
                state.metadata["simulation_objections"] = result.get("key_objections", [])
            except:
                # Fallback simulation
                base_conversion = 0.4
                if state.lead_score > 0.7:
                    base_conversion += 0.2
                if state.engagement_level > 0.5:
                    base_conversion += 0.1
                state.predicted_conversion = min(base_conversion, 1.0)
                state.recommended_approach = "Discovery call with demo"
            
            state.simulation_completed = True
            
        except Exception as e:
            print(f"⚠️  AI simulation failed, using fallback: {str(e)[:50]}...")
            state = self._fallback_simulation(state)
        
        return state
    
    def _fallback_research(self, state):
        """Fallback research without AI"""
        print("📋 Using fallback research logic")
        industry_pain_points = {
            "technology": ["Scaling challenges", "Technical debt", "Release velocity"],
            "software": ["User adoption", "Feature complexity", "Performance"],
            "fintech": ["Regulatory compliance", "Security", "Market volatility"]
        }
        
        industry_key = (state.industry or "technology").lower()
        for key in industry_pain_points:
            if key in industry_key:
                state.pain_points = industry_pain_points[key]
                break
        else:
            state.pain_points = ["Process optimization", "Cost reduction", "Efficiency"]
        
        state.tech_stack = ["CRM", "Cloud Platform", "Analytics Tools"]
        state.key_insights = [f"Company operates in {state.industry or 'technology'} sector", "Growth stage requires optimization"]
        state.research_completed = True
        return state
    
    def _fallback_scoring(self, state):
        """Fallback scoring without AI"""
        print("📊 Using fallback scoring logic")
        score = 0.5
        if state.company_size and state.company_size > 200:
            score += 0.15
        if state.pain_points:
            score += 0.15
        if state.industry and "tech" in state.industry.lower():
            score += 0.1
        
        state.lead_score = min(score, 1.0)
        state.qualification_score = state.lead_score * 0.85
        return state
    
    def _fallback_outreach(self, state):
        """Fallback outreach without AI"""
        print("📧 Using fallback outreach logic")
        
        company_name = state.company_name or "Your Company"
        contact_name = state.contact_name or "there"
        
        # Generate fallback email and LinkedIn messages
        state.metadata["email_subject"] = f"Strategic Partnership Opportunity with {company_name}"
        state.metadata["email_body"] = f"""Hi {contact_name},

I noticed {company_name} is growing rapidly in the {state.industry or 'technology'} space. We've been helping similar companies tackle {state.pain_points[0] if state.pain_points else 'scaling challenges'}.

Would you be open to a brief conversation about how we might support your team's objectives? I'd be happy to share some insights from similar engagements.

Best regards"""
        
        state.metadata["linkedin_connection"] = f"Hi {contact_name}, I'd love to connect and discuss potential synergies between our companies."
        state.metadata["linkedin_follow_up"] = f"Thanks for connecting! I'd love to explore how we can help {company_name} with your growth objectives."
        state.metadata["outreach_strategy"] = "Multi-channel approach with personalized messaging focusing on growth and efficiency"
        
        state.outreach_attempts = 1
        state.engagement_level = 0.35
        state.response_rate = 0.25
        state.last_contact = datetime.now()
        return state
    
    def _fallback_simulation(self, state):
        """Fallback simulation without AI"""
        print("🎭 Using fallback simulation logic")
        base_conversion = 0.4
        if state.lead_score > 0.6:
            base_conversion += 0.15
        if state.company_size and state.company_size > 100:
            base_conversion += 0.1
        
        state.predicted_conversion = min(base_conversion, 1.0)
        state.recommended_approach = "Discovery call with technical demo"
        state.simulation_completed = True
        return state
    
    def _print_step_results(self, step_name, state):
        """Print results after each step"""
        if step_name == "Research":
            print(f"✅ Research completed: {state.research_completed}")
            print(f"   Pain points: {len(state.pain_points)} identified")
            print(f"   Tech stack: {len(state.tech_stack)} tools")
            
        elif step_name == "Scoring":
            print(f"✅ Lead score: {state.lead_score:.2f}")
            print(f"   Qualification: {state.qualification_score:.2f}")
            
        elif step_name == "Outreach":
            print(f"✅ Outreach attempts: {state.outreach_attempts}")
            print(f"   Engagement level: {state.engagement_level:.2f}")
            
        elif step_name == "Simulation":
            print(f"✅ Conversion probability: {state.predicted_conversion:.2f}")
            print(f"   Approach: {state.recommended_approach}")
    
    def _print_final_results(self, state, execution_time):
        """Print comprehensive final results"""
        print("\n" + "="*60)
        print("🎯 FAST WORKFLOW RESULTS")
        print("="*60)
        
        print(f"\n⏱️  Execution Time: {execution_time:.1f} seconds")
        
        print(f"\n🏢 Company Analysis:")
        print(f"   • Company: {state.company_name}")
        print(f"   • Size: {state.company_size or 'Unknown'} employees")
        print(f"   • Industry: {state.industry or 'Unknown'}")
        print(f"   • Stage: {state.stage}")
        
        print(f"\n📊 Scoring Results:")
        print(f"   • Lead Score: {state.lead_score:.2f}/1.0")
        print(f"   • Qualification: {state.qualification_score:.2f}/1.0")
        print(f"   • Engagement: {state.engagement_level:.2f}/1.0")
        
        print(f"\n🔍 Research Findings:")
        if state.pain_points:
            print(f"   • Pain Points: {', '.join(state.pain_points[:3])}")
        if state.tech_stack:
            print(f"   • Tech Stack: {', '.join(state.tech_stack[:3])}")
        
        print(f"\n🎯 Sales Intelligence:")
        print(f"   • Conversion Probability: {state.predicted_conversion:.1%}")
        print(f"   • Recommended Approach: {state.recommended_approach}")
        print(f"   • Response Rate Estimate: {state.response_rate:.1%}")
        
        # Display generated outreach messages
        print(f"\n📧 Generated Outreach Messages:")
        email_subject = state.metadata.get('email_subject', 'Not generated')
        linkedin_msg = state.metadata.get('linkedin_connection', 'Not generated')
        print(f"   • Email Subject: {email_subject}")
        print(f"   • LinkedIn Connection: {linkedin_msg[:80]}{'...' if len(linkedin_msg) > 80 else ''}")
        
        # Display full email body
        email_body = state.metadata.get('email_body', 'No email body generated')
        if email_body and email_body != 'No email body generated':
            print(f"\n📝 Email Body:")
            print(f"{email_body}")
        
        # Display LinkedIn follow-up
        linkedin_followup = state.metadata.get('linkedin_follow_up', 'No follow-up message generated')
        if linkedin_followup and linkedin_followup != 'No follow-up message generated':
            print(f"\n💼 LinkedIn Follow-up:")
            print(f"{linkedin_followup}")
        
        if state.assigned_rep:
            print(f"\n👤 Sales Assignment:")
            print(f"   • Assigned Rep: {state.assigned_rep}")
            print(f"   • Stage: {state.stage}")
        
        # Performance summary
        if execution_time < 60:
            performance = "🚀 Excellent"
        elif execution_time < 120:
            performance = "✅ Good" 
        else:
            performance = "⚠️  Slower than expected"
            
        print(f"\n📈 Performance: {performance} ({execution_time:.1f}s)")
        print(f"   Target: <120s | Actual: {execution_time:.1f}s")


def run_fast_workflow():
    """Run a single fast workflow example"""
    
    # Sample lead data
    sample_lead = {
        "lead_id": "fast_lead_001",
        "company_name": "TechFlow Inc",
        "contact_email": "cto@techflow.com",
        "contact_name": "Sarah Chen",
        "company_size": 180,
        "industry": "Software Technology",
        "location": "Austin, TX"
    }
    
    print("🚀 Sales Forge - Fast Workflow Demo")
    print(f"Processing: {sample_lead['company_name']}")
    
    # Initialize and run fast pipeline
    pipeline = FastSalesPipeline()
    result = pipeline.run_fast(sample_lead)
    
    return result


def run_multiple_fast_leads():
    """Run fast workflow for multiple leads"""
    
    sample_leads = [
        {
            "lead_id": "fast_001",
            "company_name": "DataStream Corp",
            "contact_email": "vp@datastream.com",
            "contact_name": "Alex Kumar",
            "company_size": 320,
            "industry": "Data Analytics",
            "location": "Seattle, WA"
        },
        {
            "lead_id": "fast_002",
            "company_name": "CloudBridge Solutions", 
            "contact_email": "cto@cloudbridge.com",
            "contact_name": "Maria Rodriguez",
            "company_size": 95,
            "industry": "Cloud Services",
            "location": "Denver, CO"
        },
        {
            "lead_id": "fast_003",
            "company_name": "FinanceAI Labs",
            "contact_email": "founder@financeai.com", 
            "contact_name": "David Park",
            "company_size": 45,
            "industry": "FinTech",
            "location": "New York, NY"
        }
    ]
    
    pipeline = FastSalesPipeline()
    results = []
    total_start = datetime.now()
    
    print("🚀 Sales Forge - Multiple Fast Leads Demo")
    print("=" * 60)
    
    for i, lead_data in enumerate(sample_leads, 1):
        print(f"\n🔥 Processing Lead {i}/3: {lead_data['company_name']}")
        print("-" * 40)
        
        try:
            result = pipeline.run_fast(lead_data)
            results.append(result)
            print(f"✅ Completed: {lead_data['company_name']}")
            
        except Exception as e:
            print(f"❌ Failed: {lead_data['company_name']} - {str(e)[:50]}...")
            results.append(None)
    
    # Summary
    total_time = (datetime.now() - total_start).total_seconds()
    successful = [r for r in results if r is not None]
    
    print("\n" + "="*60)
    print("📊 BATCH PROCESSING SUMMARY")
    print("="*60)
    print(f"Total Leads Processed: {len(successful)}/{len(sample_leads)}")
    print(f"Total Execution Time: {total_time:.1f} seconds")
    print(f"Average Time per Lead: {total_time/len(sample_leads):.1f} seconds")
    
    if successful:
        avg_score = sum(r.get('lead_score', 0) for r in successful) / len(successful)
        avg_conversion = sum(r.get('predicted_conversion', 0) for r in successful) / len(successful)
        
        print(f"\n📈 Performance Metrics:")
        print(f"   • Average Lead Score: {avg_score:.2f}")
        print(f"   • Average Conversion: {avg_conversion:.1%}")
        
        # Stage distribution
        stages = {}
        for result in successful:
            stage = result.get('stage', 'unknown')
            stages[stage] = stages.get(stage, 0) + 1
        
        print(f"   • Stage Distribution:")
        for stage, count in stages.items():
            print(f"     - {stage}: {count}")
    
    return results


if __name__ == "__main__":
    print("Sales Forge - Fast Workflow Examples")
    print("=" * 50)
    
    # Run single lead example
    print("\n1️⃣  Single Lead Fast Workflow:")
    run_fast_workflow()
    
    # Run multiple leads example  
    print("\n\n2️⃣  Multiple Leads Fast Workflow:")
    run_multiple_fast_leads()
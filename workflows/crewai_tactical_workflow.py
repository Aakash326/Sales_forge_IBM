#!/usr/bin/env python3
"""
CrewAI Tactical Intelligence Workflow - 4 Agents
Fast execution tactical analysis (60-80 seconds)

Architecture:
1. Research Agent - Company and market research
2. Scoring Agent - Lead qualification and scoring  
3. Outreach Agent - Personalized outreach strategies
4. Simulation Agent - Conversion probability modeling

This workflow focuses purely on tactical intelligence without strategic analysis.
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
from src.workflow.states.lead_states import LeadState


class CrewAITacticalWorkflow:
    """
    CrewAI Tactical Intelligence Workflow
    
    4 specialized agents for fast tactical analysis:
    - Research Agent: Company and market intelligence
    - Scoring Agent: Lead qualification and priority scoring
    - Outreach Agent: Personalized messaging and campaign strategy
    - Simulation Agent: Conversion probability and success modeling
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.execution_mode = "fast_tactical"
        self.agent_timeout = 20  # 20 seconds per agent
        
    async def run_tactical_workflow(self, lead_data: dict) -> dict:
        """
        Execute 4-agent tactical workflow
        Target execution time: 60-80 seconds
        """
        
        print("🚀 CrewAI Tactical Intelligence Workflow")
        print("=" * 60)
        print(f"Company: {lead_data.get('company_name', 'Unknown')}")
        print(f"Industry: {lead_data.get('industry', 'Unknown')}")
        print(f"Size: {lead_data.get('company_size', 'Unknown')} employees")
        print(f"Target: 60-80 second execution")
        print()
        
        start_time = datetime.now()
        lead_state = LeadState(**lead_data)
        
        # Agent 1: Research Agent (15-20 seconds)
        print("🔍 Agent 1: Research Agent")
        print("-" * 30)
        research_start = datetime.now()
        lead_state = await self._run_research_agent(lead_state)
        research_time = (datetime.now() - research_start).total_seconds()
        print(f"✅ Research completed in {research_time:.1f}s")
        self._display_research_results(lead_state)
        
        # Agent 2: Scoring Agent (10-15 seconds)
        print("\n📊 Agent 2: Scoring Agent") 
        print("-" * 30)
        scoring_start = datetime.now()
        lead_state = await self._run_scoring_agent(lead_state)
        scoring_time = (datetime.now() - scoring_start).total_seconds()
        print(f"✅ Scoring completed in {scoring_time:.1f}s")
        self._display_scoring_results(lead_state)
        
        # Agent 3: Outreach Agent (20-25 seconds)
        print("\n📧 Agent 3: Outreach Agent")
        print("-" * 30) 
        outreach_start = datetime.now()
        lead_state = await self._run_outreach_agent(lead_state)
        outreach_time = (datetime.now() - outreach_start).total_seconds()
        print(f"✅ Outreach completed in {outreach_time:.1f}s")
        self._display_outreach_results(lead_state)
        
        # Agent 4: Simulation Agent (15-20 seconds)
        print("\n🎭 Agent 4: Simulation Agent")
        print("-" * 30)
        simulation_start = datetime.now()
        lead_state = await self._run_simulation_agent(lead_state)
        simulation_time = (datetime.now() - simulation_start).total_seconds()
        print(f"✅ Simulation completed in {simulation_time:.1f}s")
        self._display_simulation_results(lead_state)
        
        # Final tactical intelligence summary
        total_time = (datetime.now() - start_time).total_seconds()
        self._display_tactical_summary(lead_state, total_time, {
            'research_time': research_time,
            'scoring_time': scoring_time, 
            'outreach_time': outreach_time,
            'simulation_time': simulation_time
        })
        
        return lead_state.model_dump()
    
    async def _run_research_agent(self, state: LeadState) -> LeadState:
        """
        Research Agent: Company and market intelligence
        - Company background and competitive landscape
        - Industry trends and market position
        - Pain point identification
        - Technology stack analysis
        """
        
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_research(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            research_prompt = ChatPromptTemplate.from_template("""
            You are a Research Agent specializing in company and market intelligence.
            
            Research {company_name} ({industry}, {company_size} employees, {location}):
            
            PRIMARY RESEARCH OBJECTIVES:
            1. Company Analysis: Business model, competitive position, recent developments
            2. Pain Point Identification: Industry-specific challenges this company likely faces
            3. Technology Assessment: Current tech stack and modernization needs
            4. Market Context: Industry trends, growth drivers, competitive threats
            
            Provide comprehensive analysis as JSON:
            {{
                "company_analysis": {{
                    "business_model": "Brief description of how they make money",
                    "competitive_position": "Market position and key competitors",
                    "recent_developments": "Recent news, funding, or strategic moves"
                }},
                "pain_points": [
                    "Specific operational challenge",
                    "Technology or scalability issue", 
                    "Market or competitive pressure"
                ],
                "technology_assessment": {{
                    "current_stack": ["Technology 1", "Technology 2", "Technology 3"],
                    "modernization_needs": ["Gap 1", "Gap 2"],
                    "tech_maturity_score": 0.65
                }},
                "market_context": {{
                    "industry_trends": ["Trend 1", "Trend 2"],
                    "growth_drivers": ["Driver 1", "Driver 2"],
                    "market_opportunity_score": 0.75
                }},
                "research_confidence": 0.8
            }}
            
            Focus on actionable intelligence that supports tactical sales decisions.
            Be specific and realistic for a {industry} company of {company_size} employees.
            """)
            
            chain = research_prompt | llm
            response = await asyncio.wait_for(
                asyncio.create_task(chain.ainvoke({
                    "company_name": state.company_name,
                    "industry": state.industry or "Technology",
                    "company_size": state.company_size or 250,
                    "location": state.location or "Unknown"
                })),
                timeout=self.agent_timeout
            )
            
            # Parse comprehensive research response
            import json
            try:
                research_data = json.loads(response.content)
                
                # Store company analysis
                company_analysis = research_data.get("company_analysis", {})
                state.metadata["business_model"] = company_analysis.get("business_model", "")
                state.metadata["competitive_position"] = company_analysis.get("competitive_position", "")
                state.metadata["recent_developments"] = company_analysis.get("recent_developments", "")
                
                # Store pain points
                state.pain_points = research_data.get("pain_points", [])
                
                # Store technology assessment
                tech_assessment = research_data.get("technology_assessment", {})
                state.tech_stack = tech_assessment.get("current_stack", [])
                state.metadata["modernization_needs"] = tech_assessment.get("modernization_needs", [])
                state.metadata["tech_maturity_score"] = tech_assessment.get("tech_maturity_score", 0.5)
                
                # Store market context
                market_context = research_data.get("market_context", {})
                state.metadata["industry_trends"] = market_context.get("industry_trends", [])
                state.metadata["growth_drivers"] = market_context.get("growth_drivers", [])
                state.metadata["market_opportunity_score"] = market_context.get("market_opportunity_score", 0.5)
                
                # Store research confidence
                state.metadata["research_confidence"] = research_data.get("research_confidence", 0.6)
                
                state.research_completed = True
                
            except json.JSONDecodeError:
                print("⚠️  JSON parsing failed, using fallback research")
                state = self._fallback_research(state)
                
        except asyncio.TimeoutError:
            print(f"⚠️  Research agent timeout after {self.agent_timeout}s, using fallback")
            state = self._fallback_research(state)
        except Exception as e:
            print(f"⚠️  Research agent failed: {str(e)[:50]}, using fallback")
            state = self._fallback_research(state)
            
        return state
    
    async def _run_scoring_agent(self, state: LeadState) -> LeadState:
        """
        Scoring Agent: Lead qualification and priority scoring
        - Lead quality assessment
        - Qualification score based on fit
        - Priority ranking for sales team
        - Readiness-to-buy indicators
        """
        
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_scoring(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            scoring_prompt = ChatPromptTemplate.from_template("""
            You are a Scoring Agent specializing in lead qualification and priority ranking.
            
            Analyze and score this lead:
            
            COMPANY DATA:
            • Name: {company_name}
            • Size: {company_size} employees  
            • Industry: {industry}
            • Pain Points: {pain_points}
            • Tech Stack: {tech_stack}
            • Market Opportunity: {market_opportunity_score}
            
            SCORING CRITERIA:
            1. Company Fit Score (0-1): How well they match our ICP
            2. Pain Point Alignment (0-1): How well their challenges align with our solutions
            3. Budget Probability (0-1): Likelihood they have budget for our solution
            4. Decision Urgency (0-1): How urgently they need to solve their problems
            5. Technical Readiness (0-1): Their readiness for implementation
            
            Provide detailed scoring as JSON:
            {{
                "lead_scoring": {{
                    "company_fit_score": 0.75,
                    "pain_alignment_score": 0.68,
                    "budget_probability": 0.72,
                    "decision_urgency": 0.55,
                    "technical_readiness": 0.80
                }},
                "composite_scores": {{
                    "lead_score": 0.70,
                    "qualification_score": 0.65,
                    "priority_rank": "high"
                }},
                "scoring_rationale": {{
                    "strengths": ["Key strength 1", "Key strength 2"],
                    "concerns": ["Potential concern 1", "Potential concern 2"],
                    "recommended_approach": "Specific approach recommendation"
                }},
                "next_steps": [
                    "Immediate action 1",
                    "Follow-up action 2" 
                ]
            }}
            
            Be precise and analytical in your scoring methodology.
            """)
            
            chain = scoring_prompt | llm
            response = await asyncio.wait_for(
                asyncio.create_task(chain.ainvoke({
                    "company_name": state.company_name,
                    "company_size": state.company_size or "Unknown",
                    "industry": state.industry or "Unknown", 
                    "pain_points": ", ".join(state.pain_points) if state.pain_points else "None identified",
                    "tech_stack": ", ".join(state.tech_stack) if state.tech_stack else "None identified",
                    "market_opportunity_score": state.metadata.get("market_opportunity_score", 0.5)
                })),
                timeout=self.agent_timeout
            )
            
            # Parse scoring response
            import json
            try:
                scoring_data = json.loads(response.content)
                
                # Store detailed scoring breakdown
                lead_scoring = scoring_data.get("lead_scoring", {})
                state.metadata["company_fit_score"] = lead_scoring.get("company_fit_score", 0.5)
                state.metadata["pain_alignment_score"] = lead_scoring.get("pain_alignment_score", 0.5) 
                state.metadata["budget_probability"] = lead_scoring.get("budget_probability", 0.5)
                state.metadata["decision_urgency"] = lead_scoring.get("decision_urgency", 0.5)
                state.metadata["technical_readiness"] = lead_scoring.get("technical_readiness", 0.5)
                
                # Store composite scores
                composite_scores = scoring_data.get("composite_scores", {})
                state.lead_score = composite_scores.get("lead_score", 0.5)
                state.qualification_score = composite_scores.get("qualification_score", 0.5)
                state.metadata["priority_rank"] = composite_scores.get("priority_rank", "medium")
                
                # Store rationale and recommendations
                rationale = scoring_data.get("scoring_rationale", {})
                state.metadata["scoring_strengths"] = rationale.get("strengths", [])
                state.metadata["scoring_concerns"] = rationale.get("concerns", [])
                state.metadata["recommended_approach"] = rationale.get("recommended_approach", "")
                
                # Store next steps
                state.metadata["scoring_next_steps"] = scoring_data.get("next_steps", [])
                
            except json.JSONDecodeError:
                print("⚠️  JSON parsing failed, using fallback scoring")
                state = self._fallback_scoring(state)
                
        except asyncio.TimeoutError:
            print(f"⚠️  Scoring agent timeout after {self.agent_timeout}s, using fallback")
            state = self._fallback_scoring(state)
        except Exception as e:
            print(f"⚠️  Scoring agent failed: {str(e)[:50]}, using fallback")
            state = self._fallback_scoring(state)
            
        return state
    
    async def _run_outreach_agent(self, state: LeadState) -> LeadState:
        """
        Outreach Agent: Personalized outreach strategies
        - Multi-channel outreach campaigns
        - Personalized messaging based on research
        - Timing and sequencing recommendations
        - Value proposition optimization
        """
        
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_outreach(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            outreach_prompt = ChatPromptTemplate.from_template("""
            You are an Outreach Agent specializing in personalized multi-channel campaigns.
            
            Create comprehensive outreach strategy for {contact_name} at {company_name}:
            
            CONTEXT:
            • Company: {company_name} ({company_size} employees, {industry})
            • Pain Points: {pain_points}
            • Lead Score: {lead_score}
            • Priority: {priority_rank}
            • Tech Readiness: {technical_readiness}
            
            OUTREACH REQUIREMENTS:
            1. Email Campaign: Subject lines, sequences, timing
            2. LinkedIn Strategy: Connection requests, messages, content sharing
            3. Phone/Video: Call scripts, meeting requests, demo positioning
            4. Value Proposition: Customized benefits aligned to their pain points
            
            Generate comprehensive outreach plan as JSON:
            {{
                "email_campaign": {{
                    "primary_email": {{
                        "subject": "Compelling subject line under 60 chars",
                        "body": "Professional email body 150-200 words",
                        "call_to_action": "Specific action request"
                    }},
                    "follow_up_sequence": [
                        {{
                            "timing": "3 days",
                            "subject": "Follow-up subject",
                            "message": "Brief follow-up message"
                        }},
                        {{
                            "timing": "1 week", 
                            "subject": "Value-driven subject",
                            "message": "Value-focused follow-up"
                        }}
                    ]
                }},
                "linkedin_strategy": {{
                    "connection_request": "Brief personalized connection message",
                    "initial_message": "First LinkedIn message after connection",
                    "content_sharing": ["Article topic 1", "Case study topic 2"],
                    "engagement_tactics": ["Strategy 1", "Strategy 2"]
                }},
                "phone_outreach": {{
                    "call_script_intro": "Opening 30-second introduction",
                    "discovery_questions": ["Question 1", "Question 2", "Question 3"],
                    "demo_positioning": "How to position a demo/meeting"
                }},
                "value_proposition": {{
                    "primary_value": "Main value statement tailored to their pain points",
                    "supporting_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
                    "differentiators": ["Key differentiator 1", "Key differentiator 2"]
                }},
                "campaign_metrics": {{
                    "expected_response_rate": 0.25,
                    "optimal_contact_frequency": "2-3 touches per week",
                    "best_contact_times": ["Tuesday 10 AM", "Thursday 2 PM"]
                }}
            }}
            
            Focus on personalization, value, and professional communication.
            """)
            
            chain = outreach_prompt | llm
            response = await asyncio.wait_for(
                asyncio.create_task(chain.ainvoke({
                    "contact_name": state.contact_name or "the contact",
                    "company_name": state.company_name,
                    "company_size": state.company_size or "Unknown",
                    "industry": state.industry or "Unknown",
                    "pain_points": ", ".join(state.pain_points[:3]) if state.pain_points else "scaling challenges",
                    "lead_score": state.lead_score,
                    "priority_rank": state.metadata.get("priority_rank", "medium"),
                    "technical_readiness": state.metadata.get("technical_readiness", 0.5)
                })),
                timeout=self.agent_timeout
            )
            
            # Parse comprehensive outreach response
            import json
            try:
                outreach_data = json.loads(response.content)
                
                # Store email campaign details
                email_campaign = outreach_data.get("email_campaign", {})
                primary_email = email_campaign.get("primary_email", {})
                state.metadata["email_subject"] = primary_email.get("subject", "")
                state.metadata["email_body"] = primary_email.get("body", "")
                state.metadata["email_cta"] = primary_email.get("call_to_action", "")
                state.metadata["follow_up_sequence"] = email_campaign.get("follow_up_sequence", [])
                
                # Store LinkedIn strategy
                linkedin = outreach_data.get("linkedin_strategy", {})
                state.metadata["linkedin_connection"] = linkedin.get("connection_request", "")
                state.metadata["linkedin_initial"] = linkedin.get("initial_message", "")
                state.metadata["linkedin_content"] = linkedin.get("content_sharing", [])
                state.metadata["linkedin_tactics"] = linkedin.get("engagement_tactics", [])
                
                # Store phone outreach
                phone = outreach_data.get("phone_outreach", {})
                state.metadata["call_script"] = phone.get("call_script_intro", "")
                state.metadata["discovery_questions"] = phone.get("discovery_questions", [])
                state.metadata["demo_positioning"] = phone.get("demo_positioning", "")
                
                # Store value proposition  
                value_prop = outreach_data.get("value_proposition", {})
                state.metadata["primary_value"] = value_prop.get("primary_value", "")
                state.metadata["supporting_benefits"] = value_prop.get("supporting_benefits", [])
                state.metadata["differentiators"] = value_prop.get("differentiators", [])
                
                # Store campaign metrics
                campaign_metrics = outreach_data.get("campaign_metrics", {})
                state.response_rate = campaign_metrics.get("expected_response_rate", 0.25)
                state.metadata["contact_frequency"] = campaign_metrics.get("optimal_contact_frequency", "")
                state.metadata["best_contact_times"] = campaign_metrics.get("best_contact_times", [])
                
                # Update outreach status
                state.outreach_attempts = 1
                state.engagement_level = 0.4
                state.last_contact = datetime.now()
                
            except json.JSONDecodeError:
                print("⚠️  JSON parsing failed, using fallback outreach")
                state = self._fallback_outreach(state)
                
        except asyncio.TimeoutError:
            print(f"⚠️  Outreach agent timeout after {self.agent_timeout}s, using fallback")
            state = self._fallback_outreach(state)
        except Exception as e:
            print(f"⚠️  Outreach agent failed: {str(e)[:50]}, using fallback")
            state = self._fallback_outreach(state)
            
        return state
    
    async def _run_simulation_agent(self, state: LeadState) -> LeadState:
        """
        Simulation Agent: Conversion probability modeling
        - Sales cycle duration prediction
        - Conversion probability analysis
        - Deal size estimation
        - Objection handling preparation
        """
        
        if not os.getenv('OPENAI_API_KEY'):
            return self._fallback_simulation(state)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            simulation_prompt = ChatPromptTemplate.from_template("""
            You are a Simulation Agent specializing in sales outcome prediction and modeling.
            
            Simulate sales process for {company_name}:
            
            INPUT VARIABLES:
            • Lead Score: {lead_score}
            • Qualification Score: {qualification_score}
            • Company Size: {company_size} employees
            • Pain Points: {pain_points}
            • Budget Probability: {budget_probability}
            • Decision Urgency: {decision_urgency}
            • Technical Readiness: {technical_readiness}
            
            SIMULATION OBJECTIVES:
            1. Conversion Probability: Likelihood of closing the deal
            2. Sales Cycle Prediction: Expected timeline to close
            3. Deal Size Estimation: Potential contract value
            4. Success Factors: Key drivers for winning
            5. Risk Factors: Potential obstacles and objections
            
            Provide detailed simulation results as JSON:
            {{
                "conversion_analysis": {{
                    "conversion_probability": 0.65,
                    "confidence_interval": {{"low": 0.55, "high": 0.75}},
                    "key_success_factors": ["Factor 1", "Factor 2", "Factor 3"],
                    "primary_risk_factors": ["Risk 1", "Risk 2"]
                }},
                "sales_cycle_prediction": {{
                    "estimated_duration_days": 90,
                    "duration_range": {{"min": 60, "max": 120}},
                    "key_milestones": [
                        {{"milestone": "Discovery call", "days": 7}},
                        {{"milestone": "Technical demo", "days": 21}},
                        {{"milestone": "Proposal", "days": 45}},
                        {{"milestone": "Decision", "days": 75}}
                    ]
                }},
                "deal_value_estimation": {{
                    "estimated_deal_size": 85000,
                    "deal_size_range": {{"min": 65000, "max": 120000}},
                    "pricing_confidence": 0.7,
                    "upsell_potential": 0.3
                }},
                "objection_handling": {{
                    "likely_objections": [
                        {{"objection": "Budget concerns", "probability": 0.7, "response_strategy": "ROI focus"}},
                        {{"objection": "Technical complexity", "probability": 0.5, "response_strategy": "Implementation support"}},
                        {{"objection": "Timeline pressure", "probability": 0.4, "response_strategy": "Phased approach"}}
                    ]
                }},
                "recommended_strategy": {{
                    "primary_approach": "Consultative selling focused on ROI",
                    "key_messaging": ["Message 1", "Message 2"],
                    "demo_focus_areas": ["Feature area 1", "Feature area 2"],
                    "stakeholder_strategy": "Multi-threaded approach with technical and business stakeholders"
                }}
            }}
            
            Base predictions on data-driven analysis and sales methodology best practices.
            """)
            
            chain = simulation_prompt | llm
            response = await asyncio.wait_for(
                asyncio.create_task(chain.ainvoke({
                    "company_name": state.company_name,
                    "lead_score": state.lead_score,
                    "qualification_score": state.qualification_score, 
                    "company_size": state.company_size or "Unknown",
                    "pain_points": ", ".join(state.pain_points[:3]) if state.pain_points else "None identified",
                    "budget_probability": state.metadata.get("budget_probability", 0.5),
                    "decision_urgency": state.metadata.get("decision_urgency", 0.5),
                    "technical_readiness": state.metadata.get("technical_readiness", 0.5)
                })),
                timeout=self.agent_timeout
            )
            
            # Parse simulation results
            import json
            try:
                simulation_data = json.loads(response.content)
                
                # Store conversion analysis
                conversion = simulation_data.get("conversion_analysis", {})
                state.predicted_conversion = conversion.get("conversion_probability", 0.5)
                state.metadata["conversion_confidence"] = conversion.get("confidence_interval", {})
                state.metadata["success_factors"] = conversion.get("key_success_factors", [])
                state.metadata["risk_factors"] = conversion.get("primary_risk_factors", [])
                
                # Store sales cycle prediction
                sales_cycle = simulation_data.get("sales_cycle_prediction", {})
                state.metadata["estimated_duration"] = sales_cycle.get("estimated_duration_days", 90)
                state.metadata["duration_range"] = sales_cycle.get("duration_range", {})
                state.metadata["sales_milestones"] = sales_cycle.get("key_milestones", [])
                
                # Store deal value estimation
                deal_value = simulation_data.get("deal_value_estimation", {})
                state.metadata["estimated_deal_size"] = deal_value.get("estimated_deal_size", 75000)
                state.metadata["deal_size_range"] = deal_value.get("deal_size_range", {})
                state.metadata["pricing_confidence"] = deal_value.get("pricing_confidence", 0.6)
                state.metadata["upsell_potential"] = deal_value.get("upsell_potential", 0.2)
                
                # Store objection handling
                state.metadata["likely_objections"] = simulation_data.get("objection_handling", {}).get("likely_objections", [])
                
                # Store recommended strategy
                strategy = simulation_data.get("recommended_strategy", {})
                state.recommended_approach = strategy.get("primary_approach", "Consultative approach")
                state.metadata["key_messaging"] = strategy.get("key_messaging", [])
                state.metadata["demo_focus"] = strategy.get("demo_focus_areas", [])
                state.metadata["stakeholder_strategy"] = strategy.get("stakeholder_strategy", "")
                
                state.simulation_completed = True
                
            except json.JSONDecodeError:
                print("⚠️  JSON parsing failed, using fallback simulation")
                state = self._fallback_simulation(state)
                
        except asyncio.TimeoutError:
            print(f"⚠️  Simulation agent timeout after {self.agent_timeout}s, using fallback")
            state = self._fallback_simulation(state)
        except Exception as e:
            print(f"⚠️  Simulation agent failed: {str(e)[:50]}, using fallback")
            state = self._fallback_simulation(state)
            
        return state
    
    # Fallback methods for when AI services are unavailable
    def _fallback_research(self, state: LeadState) -> LeadState:
        """Fallback research logic without AI"""
        print("📋 Using fallback research logic")
        
        industry_defaults = {
            "technology": {
                "pain_points": ["Technical debt", "Scaling challenges", "Integration complexity"],
                "tech_stack": ["Cloud Platform", "Microservices", "DevOps Tools"],
                "market_score": 0.75
            },
            "fintech": {
                "pain_points": ["Regulatory compliance", "Security requirements", "Market volatility"],
                "tech_stack": ["Payment Gateway", "Compliance Platform", "Risk Management"],
                "market_score": 0.70
            },
            "healthcare": {
                "pain_points": ["Data privacy", "System integration", "Regulatory compliance"],
                "tech_stack": ["EMR System", "Compliance Tools", "Data Analytics"],
                "market_score": 0.65
            }
        }
        
        industry_key = (state.industry or "technology").lower()
        defaults = industry_defaults.get(
            next((k for k in industry_defaults.keys() if k in industry_key), "technology")
        )
        
        state.pain_points = defaults["pain_points"]
        state.tech_stack = defaults["tech_stack"]
        state.metadata["market_opportunity_score"] = defaults["market_score"]
        state.metadata["research_confidence"] = 0.6
        state.research_completed = True
        
        return state
    
    def _fallback_scoring(self, state: LeadState) -> LeadState:
        """Fallback scoring logic without AI"""
        print("📊 Using fallback scoring logic")
        
        base_score = 0.5
        
        # Company size scoring
        if state.company_size:
            if state.company_size > 500:
                base_score += 0.15
            elif state.company_size > 100:
                base_score += 0.10
            elif state.company_size > 50:
                base_score += 0.05
        
        # Pain points scoring  
        if state.pain_points:
            base_score += len(state.pain_points) * 0.05
        
        # Industry scoring
        high_value_industries = ["fintech", "technology", "software", "saas"]
        if state.industry and any(ind in state.industry.lower() for ind in high_value_industries):
            base_score += 0.10
        
        state.lead_score = min(base_score, 1.0)
        state.qualification_score = state.lead_score * 0.85
        state.metadata["priority_rank"] = "high" if state.lead_score > 0.75 else "medium" if state.lead_score > 0.5 else "low"
        
        return state
    
    def _fallback_outreach(self, state: LeadState) -> LeadState:
        """Fallback outreach logic without AI"""
        print("📧 Using fallback outreach logic")
        
        company_name = state.company_name or "Your Company"
        contact_name = state.contact_name or "there"
        
        # Generate fallback outreach messages
        state.metadata["email_subject"] = f"Strategic Growth Opportunity for {company_name}"
        state.metadata["email_body"] = f"""Hi {contact_name},

I noticed {company_name} is growing rapidly in the {state.industry or 'technology'} space. Based on our work with similar companies, I believe we could help address some of the challenges you're likely facing around {state.pain_points[0] if state.pain_points else 'operational scaling'}.

Would you be open to a brief 15-minute conversation to explore how we might support your team's objectives? I'd be happy to share some relevant insights from similar engagements.

Best regards"""
        
        state.metadata["linkedin_connection"] = f"Hi {contact_name}, I'd love to connect and discuss potential synergies with {company_name}'s growth initiatives."
        state.response_rate = 0.25
        state.outreach_attempts = 1
        state.engagement_level = 0.35
        state.last_contact = datetime.now()
        
        return state
    
    def _fallback_simulation(self, state: LeadState) -> LeadState:
        """Fallback simulation logic without AI"""
        print("🎭 Using fallback simulation logic")
        
        # Base conversion probability
        base_conversion = 0.4
        
        # Adjust based on lead score
        if state.lead_score > 0.7:
            base_conversion += 0.2
        elif state.lead_score > 0.5:
            base_conversion += 0.1
        
        # Adjust based on company size (larger = higher probability)
        if state.company_size and state.company_size > 200:
            base_conversion += 0.1
        
        # Adjust based on pain points identified
        if state.pain_points and len(state.pain_points) >= 2:
            base_conversion += 0.05
        
        state.predicted_conversion = min(base_conversion, 1.0)
        state.recommended_approach = "Discovery call with tailored demo"
        state.metadata["estimated_deal_size"] = 75000 if state.company_size and state.company_size > 100 else 45000
        state.metadata["estimated_duration"] = 75  # days
        state.simulation_completed = True
        
        return state
    
    # Display methods for each agent's results
    def _display_research_results(self, state: LeadState):
        """Display research agent results"""
        print(f"   • Pain Points: {len(state.pain_points)} identified")
        print(f"   • Tech Stack: {len(state.tech_stack)} tools analyzed")
        print(f"   • Market Opportunity: {state.metadata.get('market_opportunity_score', 0.5):.2f}")
        print(f"   • Research Confidence: {state.metadata.get('research_confidence', 0.6):.2f}")
        if state.pain_points:
            print(f"   • Top Pain Points: {', '.join(state.pain_points[:2])}")
    
    def _display_scoring_results(self, state: LeadState):
        """Display scoring agent results"""
        print(f"   • Lead Score: {state.lead_score:.2f}")
        print(f"   • Qualification Score: {state.qualification_score:.2f}")
        print(f"   • Priority Rank: {state.metadata.get('priority_rank', 'medium').title()}")
        print(f"   • Company Fit: {state.metadata.get('company_fit_score', 0.5):.2f}")
        print(f"   • Budget Probability: {state.metadata.get('budget_probability', 0.5):.2f}")
    
    def _display_outreach_results(self, state: LeadState):
        """Display outreach agent results"""
        print(f"   • Email Subject: {state.metadata.get('email_subject', 'Not generated')}")
        print(f"   • Expected Response Rate: {state.response_rate:.1%}")
        print(f"   • LinkedIn Strategy: {'✅ Generated' if state.metadata.get('linkedin_connection') else '❌ Not generated'}")
        print(f"   • Value Proposition: {'✅ Customized' if state.metadata.get('primary_value') else '❌ Standard'}")
        print(f"   • Multi-channel Campaign: {'✅ Complete' if state.metadata.get('call_script') else '❌ Partial'}")
    
    def _display_simulation_results(self, state: LeadState):
        """Display simulation agent results"""
        print(f"   • Conversion Probability: {state.predicted_conversion:.1%}")
        print(f"   • Estimated Deal Size: ${state.metadata.get('estimated_deal_size', 75000):,}")
        print(f"   • Expected Duration: {state.metadata.get('estimated_duration', 90)} days")
        print(f"   • Success Factors: {len(state.metadata.get('success_factors', []))} identified")
        print(f"   • Risk Factors: {len(state.metadata.get('risk_factors', []))} identified")
        print(f"   • Recommended Approach: {state.recommended_approach}")
    
    def _display_tactical_summary(self, state: LeadState, total_time: float, agent_times: dict):
        """Display comprehensive tactical intelligence summary"""
        
        print("\n" + "="*60)
        print("🎯 CREWAI TACTICAL INTELLIGENCE SUMMARY")
        print("="*60)
        
        # Performance metrics
        print(f"\n⏱️  Execution Performance:")
        print(f"   • Total Time: {total_time:.1f} seconds")
        print(f"   • Research Agent: {agent_times['research_time']:.1f}s")
        print(f"   • Scoring Agent: {agent_times['scoring_time']:.1f}s")
        print(f"   • Outreach Agent: {agent_times['outreach_time']:.1f}s")
        print(f"   • Simulation Agent: {agent_times['simulation_time']:.1f}s")
        
        performance_status = "🚀 Excellent" if total_time < 60 else "✅ Good" if total_time < 90 else "⚠️  Acceptable"
        print(f"   • Performance: {performance_status} (Target: <80s)")
        
        # Company analysis
        print(f"\n🏢 Company Intelligence:")
        print(f"   • Company: {state.company_name}")
        print(f"   • Size: {state.company_size or 'Unknown'} employees")
        print(f"   • Industry: {state.industry or 'Unknown'}")
        print(f"   • Business Model: {state.metadata.get('business_model', 'Not analyzed')}")
        
        # Scoring intelligence
        print(f"\n📊 Scoring Intelligence:")
        print(f"   • Lead Score: {state.lead_score:.2f}/1.0 ({state.metadata.get('priority_rank', 'medium').title()} Priority)")
        print(f"   • Qualification Score: {state.qualification_score:.2f}/1.0")
        print(f"   • Company Fit: {state.metadata.get('company_fit_score', 0.5):.2f}/1.0")
        print(f"   • Budget Probability: {state.metadata.get('budget_probability', 0.5):.1%}")
        print(f"   • Decision Urgency: {state.metadata.get('decision_urgency', 0.5):.1%}")
        
        # Research findings
        print(f"\n🔍 Research Findings:")
        if state.pain_points:
            print(f"   • Pain Points ({len(state.pain_points)}): {', '.join(state.pain_points[:3])}")
        if state.tech_stack:
            print(f"   • Tech Stack ({len(state.tech_stack)}): {', '.join(state.tech_stack[:3])}")
        print(f"   • Market Opportunity: {state.metadata.get('market_opportunity_score', 0.5):.2f}/1.0")
        
        # Sales intelligence
        print(f"\n🎯 Sales Intelligence:")
        print(f"   • Conversion Probability: {state.predicted_conversion:.1%}")
        print(f"   • Estimated Deal Size: ${state.metadata.get('estimated_deal_size', 75000):,}")
        print(f"   • Sales Cycle Duration: {state.metadata.get('estimated_duration', 90)} days")
        print(f"   • Expected Response Rate: {state.response_rate:.1%}")
        
        # Outreach strategy
        print(f"\n📧 Outreach Strategy:")
        email_subject = state.metadata.get('email_subject', 'Not generated')
        if email_subject and email_subject != 'Not generated':
            print(f"   • Email Subject: {email_subject}")
        
        linkedin_msg = state.metadata.get('linkedin_connection', '')
        if linkedin_msg:
            preview = linkedin_msg[:60] + '...' if len(linkedin_msg) > 60 else linkedin_msg
            print(f"   • LinkedIn Message: {preview}")
        
        value_prop = state.metadata.get('primary_value', '')
        if value_prop:
            preview = value_prop[:80] + '...' if len(value_prop) > 80 else value_prop
            print(f"   • Value Proposition: {preview}")
        
        # Key recommendations
        print(f"\n🚀 Tactical Recommendations:")
        approach = state.metadata.get('recommended_approach', state.recommended_approach)
        if approach:
            print(f"   • Primary Approach: {approach}")
        
        next_steps = state.metadata.get('scoring_next_steps', [])
        if next_steps:
            for i, step in enumerate(next_steps[:3], 1):
                print(f"   • Next Step {i}: {step}")
        else:
            print(f"   • Next Step 1: Schedule discovery call")
            print(f"   • Next Step 2: Prepare technical demo")
            print(f"   • Next Step 3: Develop custom proposal")
        
        # Success and risk factors
        success_factors = state.metadata.get('success_factors', [])
        if success_factors:
            print(f"\n✅ Success Factors:")
            for factor in success_factors[:3]:
                print(f"   • {factor}")
        
        risk_factors = state.metadata.get('risk_factors', [])
        if risk_factors:
            print(f"\n⚠️  Risk Factors:")
            for risk in risk_factors[:3]:
                print(f"   • {risk}")


# Demo and testing functions
async def run_single_tactical_demo():
    """Run single tactical workflow demo"""
    
    sample_lead = {
        "lead_id": "TACTICAL_001",
        "company_name": "TechFlow Dynamics",
        "contact_email": "sarah.chen@techflow.com",
        "contact_name": "Sarah Chen",
        "company_size": 280,
        "industry": "Enterprise Software",
        "location": "Austin, TX"
    }
    
    print("🚀 CrewAI Tactical Intelligence - Single Lead Demo")
    print(f"Processing: {sample_lead['company_name']}")
    
    workflow = CrewAITacticalWorkflow()
    result = await workflow.run_tactical_workflow(sample_lead)
    
    return result


async def run_multiple_tactical_demo():
    """Run tactical workflow for multiple leads"""
    
    sample_leads = [
        {
            "lead_id": "TAC_001",
            "company_name": "DataStream Analytics",
            "contact_email": "cto@datastream.com", 
            "contact_name": "Alex Kumar",
            "company_size": 420,
            "industry": "Data Analytics",
            "location": "Seattle, WA"
        },
        {
            "lead_id": "TAC_002", 
            "company_name": "CloudBridge Solutions",
            "contact_email": "vp.engineering@cloudbridge.com",
            "contact_name": "Maria Rodriguez",
            "company_size": 150,
            "industry": "Cloud Infrastructure",
            "location": "Denver, CO" 
        },
        {
            "lead_id": "TAC_003",
            "company_name": "FinanceCore Technologies",
            "contact_email": "head.product@financecore.com",
            "contact_name": "David Park",
            "company_size": 75,
            "industry": "FinTech",
            "location": "New York, NY"
        }
    ]
    
    workflow = CrewAITacticalWorkflow()
    results = []
    total_start = datetime.now()
    
    print("🚀 CrewAI Tactical Intelligence - Multiple Leads Demo")
    print("=" * 60)
    
    for i, lead_data in enumerate(sample_leads, 1):
        print(f"\n🔥 Processing Lead {i}/3: {lead_data['company_name']}")
        print("-" * 40)
        
        try:
            result = await workflow.run_tactical_workflow(lead_data)
            results.append(result)
            print(f"✅ Completed: {lead_data['company_name']}")
            
        except Exception as e:
            print(f"❌ Failed: {lead_data['company_name']} - {str(e)[:50]}...")
            results.append(None)
    
    # Batch summary
    total_time = (datetime.now() - total_start).total_seconds()
    successful = [r for r in results if r is not None]
    
    print("\n" + "="*60)
    print("📊 BATCH TACTICAL PROCESSING SUMMARY")  
    print("="*60)
    print(f"Leads Processed: {len(successful)}/{len(sample_leads)}")
    print(f"Total Execution Time: {total_time:.1f} seconds")
    print(f"Average Time per Lead: {total_time/len(sample_leads):.1f} seconds")
    
    if successful:
        avg_score = sum(r.get('lead_score', 0) for r in successful) / len(successful)
        avg_conversion = sum(r.get('predicted_conversion', 0) for r in successful) / len(successful)
        avg_deal_size = sum(r.get('metadata', {}).get('estimated_deal_size', 0) for r in successful) / len(successful)
        
        print(f"\n📈 Performance Metrics:")
        print(f"   • Average Lead Score: {avg_score:.2f}")
        print(f"   • Average Conversion Probability: {avg_conversion:.1%}")
        print(f"   • Average Deal Size: ${avg_deal_size:,.0f}")
        
        # Priority distribution
        priorities = {}
        for result in successful:
            priority = result.get('metadata', {}).get('priority_rank', 'unknown')
            priorities[priority] = priorities.get(priority, 0) + 1
        
        print(f"   • Priority Distribution:")
        for priority, count in priorities.items():
            print(f"     - {priority.title()}: {count}")
    
    return results


if __name__ == "__main__":
    print("CrewAI Tactical Intelligence Workflow")
    print("=" * 50)
    
    # Run demos
    async def main():
        print("\n1️⃣  Single Lead Tactical Demo:")
        await run_single_tactical_demo()
        
        print("\n\n2️⃣  Multiple Leads Tactical Demo:")
        await run_multiple_tactical_demo()
    
    asyncio.run(main())
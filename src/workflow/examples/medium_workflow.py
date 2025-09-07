#!/usr/bin/env python3
"""
Medium Sales Pipeline Workflow - Completes in 3-5 minutes

This version focuses on:
- Smart research and scoring (2-3 minutes)
- Actual email and LinkedIn content generation (2-3 minutes)
- Comprehensive results with actionable content
"""

import sys
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

# Load environment variables from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
load_dotenv(os.path.join(project_root, '.env'))

# Add the project root to the Python path
sys.path.insert(0, project_root)

from src.workflow.states.lead_states import LeadState

class MediumPipeline:
    """Medium-speed pipeline optimized for content generation"""
    
    def __init__(self):
        self.has_openai = bool(os.getenv('OPENAI_API_KEY'))
        if self.has_openai:
            print("✅ OpenAI API detected - using AI-powered content generation")
        else:
            print("⚠️  No OpenAI API - using template-based content generation")
    
    def run(self, lead_data):
        """Run medium-speed pipeline with content generation focus"""
        print("🚀 Medium Sales Pipeline - Content Generation Focus")
        print("=" * 60)
        print(f"Target: 3-5 minute execution with actionable content")
        
        start_time = datetime.now()
        state = LeadState(**lead_data)
        
        # Step 1: Enhanced Research (60-90 seconds)
        print("\n🔍 Step 1: Enhanced Research & Intelligence")
        print("-" * 40)
        state = self._enhanced_research(state)
        self._print_progress("Research", start_time)
        
        # Step 2: Advanced Scoring (30-45 seconds)
        print("\n📊 Step 2: Advanced Lead Scoring")
        print("-" * 40)
        state = self._advanced_scoring(state)
        self._print_progress("Scoring", start_time)
        
        # Step 3: Email Content Generation (90-120 seconds)
        print("\n📧 Step 3: Email Campaign Generation")
        print("-" * 40)
        state = self._generate_email_campaigns(state)
        self._print_progress("Email Generation", start_time)
        
        # Step 4: LinkedIn Content Generation (60-90 seconds)
        print("\n💼 Step 4: LinkedIn Strategy Creation")
        print("-" * 40)
        state = self._generate_linkedin_strategy(state)
        self._print_progress("LinkedIn Generation", start_time)
        
        # Step 5: Final Analysis & Assignment (15-30 seconds)
        print("\n🎯 Step 5: Final Analysis & Assignment")
        print("-" * 40)
        state = self._final_analysis(state)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        self._print_comprehensive_results(state, execution_time)
        
        return state.model_dump()
    
    def _enhanced_research(self, state):
        """Enhanced research with AI or advanced templates"""
        
        if self.has_openai:
            state = self._ai_enhanced_research(state)
        else:
            state = self._template_research(state)
        
        # Add timing intelligence
        current_date = datetime.now()
        quarter = f"Q{((current_date.month-1)//3)+1}"
        
        state.metadata.update({
            "research_date": current_date.isoformat(),
            "fiscal_quarter": quarter,
            "budget_season": quarter in ["Q4", "Q1"],
            "research_confidence": 0.85 if self.has_openai else 0.75
        })
        
        state.research_completed = True
        print(f"   ✅ Research completed with {len(state.pain_points)} pain points")
        print(f"   ✅ {len(state.tech_stack)} technology tools identified")
        print(f"   ✅ {len(state.key_insights)} business insights generated")
        
        return state
    
    def _ai_enhanced_research(self, state):
        """AI-powered research"""
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Conduct comprehensive research for {company_name} ({industry}, {company_size} employees):
            
            Generate detailed analysis as JSON:
            {{
                "pain_points": [
                    "Specific pain point 1",
                    "Specific pain point 2", 
                    "Specific pain point 3",
                    "Specific pain point 4"
                ],
                "tech_stack": [
                    "Tool/Platform 1",
                    "Tool/Platform 2",
                    "Tool/Platform 3",
                    "Tool/Platform 4"
                ],
                "insights": [
                    "Key business insight 1",
                    "Key business insight 2", 
                    "Key business insight 3"
                ],
                "decision_makers": [
                    "CTO/VP Engineering",
                    "Head of Operations", 
                    "CEO/Founder"
                ],
                "competitive_landscape": [
                    "Competitor/Solution 1",
                    "Competitor/Solution 2"
                ]
            }}
            
            Focus on realistic, actionable insights for a {industry} company of this size.
            """)
            
            response = llm.invoke(prompt.format_messages(
                company_name=state.company_name,
                industry=state.industry or "Technology",
                company_size=state.company_size or 250
            ))
            
            # Parse AI response
            try:
                research_data = json.loads(response.content)
                state.pain_points = research_data.get("pain_points", [])
                state.tech_stack = research_data.get("tech_stack", [])
                state.key_insights = research_data.get("insights", [])
                
                # Store additional data in metadata
                state.metadata.update({
                    "decision_makers": research_data.get("decision_makers", []),
                    "competitive_landscape": research_data.get("competitive_landscape", [])
                })
            except json.JSONDecodeError:
                print("   ⚠️  AI response parsing failed, using fallback")
                state = self._template_research(state)
                
        except Exception as e:
            print(f"   ⚠️  AI research failed: {str(e)[:50]}...")
            state = self._template_research(state)
        
        return state
    
    def _template_research(self, state):
        """Template-based research"""
        industry = (state.industry or "technology").lower()
        size = state.company_size or 250
        
        # Industry-specific pain points
        pain_point_db = {
            "technology": ["Legacy system modernization", "Scalability bottlenecks", "Security compliance gaps", "Developer productivity"],
            "software": ["Technical debt accumulation", "Release cycle optimization", "Quality assurance scaling", "Performance monitoring"],
            "fintech": ["Regulatory compliance burden", "Security audit requirements", "Risk management complexity", "Market volatility response"],
            "healthcare": ["HIPAA compliance challenges", "Data integration silos", "Patient experience optimization", "Cost reduction pressure"],
            "manufacturing": ["Supply chain visibility", "Quality control automation", "Operational efficiency gaps", "Digital transformation"],
            "retail": ["Omnichannel integration", "Inventory optimization", "Customer experience personalization", "Cost management"]
        }
        
        # Size-based tech stack
        if size < 100:
            tech_stack = ["Google Workspace", "Slack", "GitHub", "AWS/GCP Basic"]
        elif size < 500:
            tech_stack = ["Microsoft 365/Google Workspace", "Slack/Teams", "GitHub/GitLab", "AWS/Azure", "Salesforce/HubSpot"]
        else:
            tech_stack = ["Enterprise Office Suite", "Microsoft Teams", "Enterprise Git", "Multi-cloud", "Enterprise CRM", "Business Intelligence"]
        
        # Generate insights
        insights = [
            f"Mid-stage {industry} company requiring process optimization",
            f"Team size of {size} suggests need for better coordination tools",
            f"Likely experiencing growing pains typical of {size}-person organizations"
        ]
        
        # Assign data
        for key, points in pain_point_db.items():
            if key in industry:
                state.pain_points = points
                break
        else:
            state.pain_points = ["Process optimization", "Technology scaling", "Team coordination", "Cost management"]
        
        state.tech_stack = tech_stack
        state.key_insights = insights
        
        return state
    
    def _advanced_scoring(self, state):
        """Advanced scoring with multiple factors"""
        
        # Base scoring components
        size_score = self._calculate_size_score(state.company_size or 250)
        industry_score = self._calculate_industry_score(state.industry or "technology")
        pain_score = min(len(state.pain_points) * 0.1, 0.4)
        research_score = 0.2 if state.research_completed else 0
        
        # Advanced factors
        tech_maturity = self._assess_tech_maturity(state.tech_stack)
        market_timing = self._assess_market_timing()
        
        # Calculate composite scores
        state.lead_score = min(size_score + industry_score + pain_score + research_score + tech_maturity, 1.0)
        state.qualification_score = state.lead_score * 0.9
        state.engagement_level = max(0.3, state.lead_score * 0.6)
        
        # Store scoring breakdown
        state.metadata["scoring_breakdown"] = {
            "size_score": size_score,
            "industry_score": industry_score,
            "pain_score": pain_score,
            "research_score": research_score,
            "tech_maturity": tech_maturity,
            "market_timing": market_timing,
            "composite_score": state.lead_score
        }
        
        print(f"   ✅ Lead score: {state.lead_score:.2f} (composite of 6 factors)")
        print(f"   ✅ Qualification: {state.qualification_score:.2f}")
        print(f"   ✅ Engagement estimate: {state.engagement_level:.2f}")
        
        return state
    
    def _calculate_size_score(self, size):
        """Calculate score based on company size"""
        if size >= 1000: return 0.9
        elif size >= 500: return 0.8
        elif size >= 200: return 0.75
        elif size >= 100: return 0.65
        elif size >= 50: return 0.5
        else: return 0.35
    
    def _calculate_industry_score(self, industry):
        """Calculate industry fit score"""
        high_fit = ["technology", "software", "saas", "fintech", "data", "ai", "cloud"]
        medium_fit = ["healthcare", "manufacturing", "retail", "finance", "consulting"]
        
        industry_lower = industry.lower()
        
        for fit in high_fit:
            if fit in industry_lower:
                return 0.85
        
        for fit in medium_fit:
            if fit in industry_lower:
                return 0.7
        
        return 0.6
    
    def _assess_tech_maturity(self, tech_stack):
        """Assess technology maturity level"""
        modern_tools = ["aws", "azure", "gcp", "kubernetes", "docker", "github", "gitlab", "slack", "teams"]
        enterprise_tools = ["salesforce", "microsoft", "oracle", "sap", "tableau"]
        
        stack_lower = [tool.lower() for tool in tech_stack]
        
        modern_count = sum(1 for tool in stack_lower if any(modern in tool for modern in modern_tools))
        enterprise_count = sum(1 for tool in stack_lower if any(ent in tool for ent in enterprise_tools))
        
        return min((modern_count * 0.05) + (enterprise_count * 0.03), 0.15)
    
    def _assess_market_timing(self):
        """Assess current market timing factors"""
        current_month = datetime.now().month
        
        # Q4 budget season
        if current_month in [10, 11, 12]:
            return 0.1
        # Q1 execution season
        elif current_month in [1, 2, 3]:
            return 0.08
        else:
            return 0.05
    
    def _generate_email_campaigns(self, state):
        """Generate email campaign content"""
        
        if self.has_openai:
            emails = self._ai_generate_emails(state)
        else:
            emails = self._template_generate_emails(state)
        
        state.metadata["email_campaigns"] = emails
        
        print(f"   ✅ Generated {len(emails)} email templates")
        print(f"   ✅ Personalized for {state.industry or 'technology'} industry")
        print(f"   ✅ Addressing {len(state.pain_points)} specific pain points")
        
        return state
    
    def _ai_generate_emails(self, state):
        """AI-powered email generation"""
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Create a professional email outreach sequence for {contact_name} at {company_name}:
            
            Company Context:
            - Industry: {industry}
            - Size: {company_size} employees
            - Pain Points: {pain_points}
            - Tech Stack: {tech_stack}
            
            Generate 3 emails as JSON:
            {{
                "email_1_initial": {{
                    "subject": "Subject line",
                    "body": "Email body with personalization"
                }},
                "email_2_value": {{
                    "subject": "Subject line", 
                    "body": "Value-focused follow-up email"
                }},
                "email_3_social_proof": {{
                    "subject": "Subject line",
                    "body": "Case study or social proof email"
                }}
            }}
            
            Make emails:
            - Professional but conversational
            - 150-200 words each
            - Specific to their industry and pain points
            - Include clear call-to-action
            - Personalized with company details
            """)
            
            response = llm.invoke(prompt.format_messages(
                contact_name=state.contact_name or "there",
                company_name=state.company_name,
                industry=state.industry or "Technology",
                company_size=state.company_size or 250,
                pain_points=", ".join(state.pain_points[:3]) if state.pain_points else "operational efficiency",
                tech_stack=", ".join(state.tech_stack[:3]) if state.tech_stack else "standard tools"
            ))
            
            try:
                emails = json.loads(response.content)
                return emails
            except json.JSONDecodeError:
                print("   ⚠️  Email generation parsing failed, using templates")
                return self._template_generate_emails(state)
                
        except Exception as e:
            print(f"   ⚠️  AI email generation failed: {str(e)[:50]}...")
            return self._template_generate_emails(state)
    
    def _template_generate_emails(self, state):
        """Template-based email generation"""
        contact = state.contact_name or "there"
        company = state.company_name
        industry = state.industry or "technology"
        size = state.company_size or 250
        
        main_pain = state.pain_points[0] if state.pain_points else "operational efficiency"
        
        return {
            "email_1_initial": {
                "subject": f"{contact} - quick question about {company}'s scaling challenges",
                "body": f"""Hi {contact},
                
I noticed {company} has grown to around {size} employees - congratulations on the growth! 

I specialize in helping {industry} companies at your stage tackle {main_pain.lower()} without disrupting current operations.

Companies similar to {company} often face challenges around process optimization and team coordination as they scale. I'd love to learn more about your specific priorities.

Would you be open to a brief 15-minute conversation this week to discuss what's working well and where you see the biggest opportunities?

Best regards,
[Your Name]

P.S. If email isn't convenient, feel free to connect with me on LinkedIn - I share practical insights for {industry} leaders."""
            },
            "email_2_value": {
                "subject": f"2 quick wins for {company}'s {industry.lower()} operations",
                "body": f"""Hi {contact},

Following up on my previous email about {company}. I wanted to share two specific strategies that {industry} companies your size use to improve {main_pain.lower()}:

1. **Process Automation**: Implementing smart workflows that reduce manual handoffs by 40-60%
2. **Team Alignment Tools**: Creating visibility systems that improve cross-team coordination

For a {size}-person {industry} company like {company}, these typically show measurable results within 6-8 weeks.

I have a 1-page case study from a similar company that might interest you - they saw 35% improvement in operational efficiency using this approach.

Would you like me to send it over? Or if you prefer, I'm happy to discuss how this might apply to {company} in a brief call.

Best,
[Your Name]"""
            },
            "email_3_social_proof": {
                "subject": f"How [Similar Company] solved their {main_pain.lower()} challenge",
                "body": f"""Hi {contact},

I wanted to share a quick success story that might resonate with {company}'s situation.

We recently worked with a {size}-person {industry} company facing similar {main_pain.lower()} challenges. Here's what we implemented:

**Challenge**: {main_pain} was slowing down their growth
**Solution**: 3-phase optimization program over 8 weeks  
**Results**: 42% improvement in efficiency, $150K annual savings

The key was focusing on quick wins first, then building sustainable processes.

I can send you the full case study (2-page read) if you're interested. It includes the specific steps and timeline we used.

Worth a quick 15-minute conversation to see if something similar might work for {company}?

Best regards,
[Your Name]

P.S. Happy to connect on LinkedIn as well - I regularly share insights from successful implementations like this one."""
            }
        }
    
    def _generate_linkedin_strategy(self, state):
        """Generate LinkedIn outreach strategy"""
        
        if self.has_openai:
            linkedin_strategy = self._ai_generate_linkedin(state)
        else:
            linkedin_strategy = self._template_generate_linkedin(state)
        
        state.metadata["linkedin_strategy"] = linkedin_strategy
        
        print(f"   ✅ Generated LinkedIn connection strategy")
        print(f"   ✅ Created {len(linkedin_strategy.get('messages', []))} message templates")
        print(f"   ✅ Included content engagement plan")
        
        return state
    
    def _ai_generate_linkedin(self, state):
        """AI-powered LinkedIn strategy"""
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = ChatOpenAI(model="gpt-5-mini", temperature=1.0)
            
            prompt = ChatPromptTemplate.from_template("""
            Create a LinkedIn outreach strategy for {contact_name} at {company_name}:
            
            Company: {industry}, {company_size} employees
            Pain Points: {pain_points}
            
            Generate strategy as JSON:
            {{
                "connection_request": "Personalized connection message (300 chars max)",
                "messages": [
                    {{
                        "sequence": 1,
                        "timing": "After connection accepted",
                        "message": "First follow-up message"
                    }},
                    {{
                        "sequence": 2, 
                        "timing": "3-4 days later",
                        "message": "Second follow-up message"
                    }}
                ],
                "content_strategy": [
                    "Content type 1 to engage with",
                    "Content type 2 to share",
                    "Engagement approach"
                ]
            }}
            
            Keep messages professional, valuable, and relationship-focused.
            """)
            
            response = llm.invoke(prompt.format_messages(
                contact_name=state.contact_name or "the contact",
                company_name=state.company_name,
                industry=state.industry or "Technology",
                company_size=state.company_size or 250,
                pain_points=", ".join(state.pain_points[:2]) if state.pain_points else "operational challenges"
            ))
            
            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                print("   ⚠️  LinkedIn generation parsing failed, using templates")
                return self._template_generate_linkedin(state)
                
        except Exception as e:
            print(f"   ⚠️  AI LinkedIn generation failed: {str(e)[:50]}...")
            return self._template_generate_linkedin(state)
    
    def _template_generate_linkedin(self, state):
        """Template-based LinkedIn strategy"""
        contact = state.contact_name or "there"
        company = state.company_name
        industry = state.industry or "technology"
        
        return {
            "connection_request": f"Hi {contact} - I help {industry} companies optimize operations as they scale. Would love to connect and share insights relevant to {company}.",
            "messages": [
                {
                    "sequence": 1,
                    "timing": "After connection accepted",
                    "message": f"Thanks for connecting, {contact}! I noticed {company} is in the {industry} space. I specialize in helping companies your size tackle operational challenges. What's been your biggest priority lately in terms of process optimization?"
                },
                {
                    "sequence": 2,
                    "timing": "3-4 days later", 
                    "message": f"Hi {contact}, I came across an interesting case study of a {industry} company similar to {company} that improved efficiency by 40% with some simple process changes. Would you be interested in a brief overview? Always happy to share insights with fellow {industry} professionals."
                }
            ],
            "content_strategy": [
                f"Engage with {company}'s posts about growth and challenges",
                f"Share relevant {industry} insights and best practices",
                "Comment thoughtfully on industry trends",
                "Share case studies relevant to their company size"
            ]
        }
    
    def _final_analysis(self, state):
        """Final analysis and assignment"""
        
        # Determine conversion probability
        base_conversion = 0.25
        score_boost = state.lead_score * 0.4
        pain_boost = min(len(state.pain_points) * 0.05, 0.15)
        content_boost = 0.1  # Boost for having customized content
        
        state.predicted_conversion = min(base_conversion + score_boost + pain_boost + content_boost, 0.9)
        
        # Assign sales rep and approach
        if state.company_size and state.company_size > 500:
            state.assigned_rep = "enterprise_rep"
            state.recommended_approach = "Enterprise discovery with C-level engagement"
        elif state.company_size and state.company_size > 100:
            state.assigned_rep = "mid_market_rep" 
            state.recommended_approach = "Technical demo with stakeholder alignment"
        else:
            state.assigned_rep = "smb_rep"
            state.recommended_approach = "Value-focused discovery call"
        
        # Set stage based on qualification
        if state.qualification_score > 0.75:
            state.stage = "sales_ready"
        elif state.qualification_score > 0.6:
            state.stage = "qualified"
        else:
            state.stage = "nurture"
        
        # Final metadata
        state.metadata.update({
            "content_ready": True,
            "email_campaigns_count": 3,
            "linkedin_messages_count": 2,
            "personalization_level": "high",
            "next_action_priority": "high" if state.qualification_score > 0.7 else "medium"
        })
        
        print(f"   ✅ Final qualification: {state.qualification_score:.2f}")
        print(f"   ✅ Conversion probability: {state.predicted_conversion:.1%}")
        print(f"   ✅ Stage: {state.stage}")
        print(f"   ✅ Assigned to: {state.assigned_rep}")
        
        return state
    
    def _print_progress(self, step, start_time):
        """Print step progress"""
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"   ⏱️  Step completed in {elapsed:.1f}s (total: {elapsed:.1f}s)")
    
    def _print_comprehensive_results(self, state, execution_time):
        """Print detailed results with all content"""
        print("\n" + "="*70)
        print("🎯 MEDIUM PIPELINE COMPLETE - COMPREHENSIVE RESULTS")
        print("="*70)
        
        # Performance metrics
        print(f"\n⏱️  PERFORMANCE:")
        print(f"   • Execution Time: {execution_time:.1f} seconds")
        
        if execution_time < 180:
            perf_emoji = "🚀"
            perf_text = "Excellent"
        elif execution_time < 300:
            perf_emoji = "✅"
            perf_text = "Good"
        else:
            perf_emoji = "⚠️"
            perf_text = "Acceptable"
        
        print(f"   • Performance Rating: {perf_emoji} {perf_text}")
        print(f"   • Target Range: 180-300s | Actual: {execution_time:.1f}s")
        
        # Company analysis
        print(f"\n🏢 COMPANY ANALYSIS:")
        print(f"   • Company: {state.company_name}")
        print(f"   • Industry: {state.industry or 'Unknown'}")
        print(f"   • Size: {state.company_size or 'Unknown'} employees")
        print(f"   • Contact: {state.contact_name or 'Unknown'}")
        
        # Intelligence scores
        print(f"\n📊 LEAD INTELLIGENCE:")
        stars = "⭐" * min(int(state.lead_score * 5), 5)
        print(f"   • Lead Score: {state.lead_score:.2f}/1.0 {stars}")
        print(f"   • Qualification: {state.qualification_score:.2f}/1.0")
        print(f"   • Engagement Est: {state.engagement_level:.2f}/1.0")
        print(f"   • Conversion Prob: {state.predicted_conversion:.1%}")
        
        # Research findings
        print(f"\n🔍 RESEARCH FINDINGS:")
        print(f"   • Pain Points Identified: {len(state.pain_points)}")
        for i, pain in enumerate(state.pain_points[:4], 1):
            print(f"     {i}. {pain}")
        
        print(f"   • Technology Stack: {len(state.tech_stack)} tools")
        print(f"     - {', '.join(state.tech_stack[:3])}")
        if len(state.tech_stack) > 3:
            print(f"     - Plus {len(state.tech_stack) - 3} more...")
        
        # Email campaigns
        print(f"\n📧 EMAIL CAMPAIGNS GENERATED:")
        emails = state.metadata.get("email_campaigns", {})
        
        if "email_1_initial" in emails:
            print(f"   📩 Email 1 - Initial Outreach:")
            print(f"      Subject: {emails['email_1_initial']['subject']}")
            print(f"      Length: {len(emails['email_1_initial']['body'])} characters")
        
        if "email_2_value" in emails:
            print(f"   📩 Email 2 - Value Follow-up:")
            print(f"      Subject: {emails['email_2_value']['subject']}")
            print(f"      Length: {len(emails['email_2_value']['body'])} characters")
        
        if "email_3_social_proof" in emails:
            print(f"   📩 Email 3 - Social Proof:")
            print(f"      Subject: {emails['email_3_social_proof']['subject']}")
            print(f"      Length: {len(emails['email_3_social_proof']['body'])} characters")
        
        # LinkedIn strategy
        print(f"\n💼 LINKEDIN STRATEGY:")
        linkedin = state.metadata.get("linkedin_strategy", {})
        
        if "connection_request" in linkedin:
            print(f"   🔗 Connection Request:")
            print(f"      \"{linkedin['connection_request'][:100]}...\"")
        
        messages = linkedin.get("messages", [])
        print(f"   💬 Follow-up Messages: {len(messages)} generated")
        for msg in messages:
            print(f"      • Message {msg['sequence']}: {msg['timing']}")
        
        # Sales assignment
        print(f"\n👤 SALES ASSIGNMENT:")
        print(f"   • Stage: {state.stage.upper()}")
        print(f"   • Assigned Rep: {state.assigned_rep}")
        print(f"   • Recommended Approach: {state.recommended_approach}")
        
        # Next actions
        print(f"\n📋 IMMEDIATE NEXT ACTIONS:")
        if state.stage == "sales_ready":
            print(f"   🚀 HIGH PRIORITY:")
            print(f"      1. Send Email 1 within 24 hours")
            print(f"      2. Connect on LinkedIn immediately")
            print(f"      3. Schedule discovery call within 48 hours")
        elif state.stage == "qualified":
            print(f"   ✅ MEDIUM PRIORITY:")
            print(f"      1. Launch email sequence (3 emails over 2 weeks)")
            print(f"      2. LinkedIn outreach with follow-up")
            print(f"      3. Monitor engagement and follow up")
        else:
            print(f"   📚 NURTURE PRIORITY:")
            print(f"      1. Add to nurture campaign")
            print(f"      2. Share valuable content monthly")
            print(f"      3. Monitor for trigger events")
        
        # Content preview
        if emails:
            print(f"\n📝 SAMPLE CONTENT PREVIEW:")
            email1 = emails.get("email_1_initial", {})
            if email1:
                print(f"   First Email Body (preview):")
                body_preview = email1.get("body", "")[:200]
                print(f"   \"{body_preview}...\"")


def run_single_medium():
    """Run single lead through medium pipeline"""
    
    lead_data = {
        "lead_id": "medium_001",
        "company_name": "InnovateTech Systems",
        "contact_email": "vp.eng@innovatetech.com",
        "contact_name": "Alexandra Martinez", 
        "company_size": 275,
        "industry": "Software Technology",
        "location": "Portland, OR"
    }
    
    print("🚀 Medium Sales Pipeline - Content Generation Demo")
    print(f"Processing: {lead_data['company_name']}")
    
    pipeline = MediumPipeline()
    result = pipeline.run(lead_data)
    
    return result


def run_multiple_medium():
    """Run multiple leads through medium pipeline"""
    
    leads = [
        {
            "lead_id": "med_batch_01",
            "company_name": "CloudScale Solutions", 
            "contact_email": "cto@cloudscale.com",
            "contact_name": "David Chen",
            "company_size": 420,
            "industry": "Cloud Services"
        },
        {
            "lead_id": "med_batch_02",
            "company_name": "HealthData Analytics",
            "contact_email": "founder@healthdata.com", 
            "contact_name": "Dr. Emma Thompson",
            "company_size": 95,
            "industry": "Healthcare Technology"
        }
    ]
    
    print("🚀 Medium Pipeline - Batch Processing")
    print("="*50)
    
    pipeline = MediumPipeline()
    results = []
    total_start = datetime.now()
    
    for i, lead in enumerate(leads, 1):
        print(f"\n🔥 Processing Lead {i}/{len(leads)}: {lead['company_name']}")
        print("="*60)
        
        result = pipeline.run(lead)
        results.append(result)
        
        lead_time = (datetime.now() - total_start).total_seconds()
        print(f"\n✅ Lead {i} completed - Running total: {lead_time:.1f}s")
    
    # Final batch summary
    total_time = (datetime.now() - total_start).total_seconds()
    
    print("\n" + "="*60)
    print("📊 BATCH PROCESSING SUMMARY") 
    print("="*60)
    print(f"Total Leads Processed: {len(results)}")
    print(f"Total Execution Time: {total_time:.1f} seconds")
    print(f"Average Time per Lead: {total_time/len(results):.1f} seconds")
    
    # Performance metrics
    scores = [r['lead_score'] for r in results]
    conversions = [r['predicted_conversion'] for r in results]
    
    print(f"\n📈 AGGREGATE ANALYTICS:")
    print(f"   • Average Lead Score: {sum(scores)/len(scores):.2f}")
    print(f"   • Average Conversion: {sum(conversions)/len(conversions):.1%}")
    print(f"   • Content Generated: {len(results) * 3} emails, {len(results) * 2} LinkedIn messages")
    
    return results


if __name__ == "__main__":
    print("🚀 Medium Sales Pipeline - Content Generation Examples")
    print("="*60)
    
    # Single lead with full content generation
    print("\n1️⃣  Single Lead with Full Content:")
    run_single_medium()
    
    # Multiple leads batch processing
    print("\n\n2️⃣  Batch Content Generation:")
    run_multiple_medium()
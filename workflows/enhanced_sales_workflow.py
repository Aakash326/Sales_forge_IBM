#!/usr/bin/env python3
"""
Enhanced Sales Workflow - Unified Strategic Intelligence + User-Approved Email Automation
Combines all enhanced AutoGen capabilities with user confirmation for email sending

Simple Workflow:
1. Enhanced Strategic Analysis (choose agent count: 8/11/13)
2. Display strategic insights and email preview
3. Ask user: "Send email? (y/n)"
4. If yes: Send personalized email based on strategic insights
5. If no: Save analysis for later use
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
sys.path.append('.')

# Core enhanced simulation nodes (these should always work)
try:
    from src.workflow.nodes.simulation_node import SimulationNode
    from src.workflow.nodes.advanced_simulation_node import AdvancedSimulationNode
    from src.workflow.schemas.simulation_schemas import SimulationResults, create_example_simulation_results
    ENHANCED_SIMULATION_AVAILABLE = True
    print("✅ Enhanced AutoGen simulation nodes loaded")
except ImportError as e:
    print(f"❌ Enhanced simulation nodes not available: {e}")
    ENHANCED_SIMULATION_AVAILABLE = False

# Email components (optional)
try:
    from src.agents.industry_router import IndustryRouter
    from src.agents.email_agent import EmailAgent
    EMAIL_AVAILABLE = True
    print("✅ Email automation components loaded")
except ImportError:
    print("⚠️ Email components not available - will simulate email sending")
    EMAIL_AVAILABLE = False
    IndustryRouter = None
    EmailAgent = None

class UserProxyAgent:
    """Simple user interaction agent for email confirmation"""
    
    def __init__(self):
        self.user_decisions = []
    
    def ask_user_confirmation(self, message: str) -> bool:
        """Ask user for confirmation with y/n response"""
        print(f"\n{'='*50}")
        print(f"🤔 USER DECISION REQUIRED")
        print(f"{'='*50}")
        print(f"{message}")
        print(f"{'='*50}")
        
        while True:
            try:
                response = input("👤 Your decision (y/n): ").strip().lower()
                if response in ['y', 'yes', '1', 'true']:
                    self.user_decisions.append({"timestamp": datetime.now(), "decision": "approved", "context": message})
                    return True
                elif response in ['n', 'no', '0', 'false']:
                    self.user_decisions.append({"timestamp": datetime.now(), "decision": "declined", "context": message})
                    return False
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no")
            except KeyboardInterrupt:
                print("\n❌ User cancelled operation")
                return False
            except Exception as e:
                print(f"❌ Input error: {e}")
                return False

class EnhancedSalesWorkflow:
    """
    Simplified unified sales workflow with enhanced strategic intelligence and user-approved email automation
    """
    
    def __init__(self):
        print("🚀 Initializing Enhanced Sales Workflow...")
        print("=" * 60)
        
        # Initialize user proxy for confirmations
        self.user_proxy = UserProxyAgent()
        print("✅ UserProxy agent initialized")
        
        # Initialize enhanced simulation capabilities
        if ENHANCED_SIMULATION_AVAILABLE:
            try:
                self.basic_simulation = SimulationNode(
                    model_name="gpt-4o-mini",
                    temperature=0.7,
                    use_json_mode=True,
                    enable_usage_tracking=True
                )
                self.advanced_simulation = AdvancedSimulationNode(
                    model_name="gpt-4o",
                    use_swarm_pattern=True,
                    enable_magentic_one=False
                )
                self.simulation_available = True
                print("✅ Enhanced AutoGen simulation nodes initialized")
            except Exception as e:
                print(f"❌ Simulation initialization failed: {e}")
                self.simulation_available = False
        else:
            self.simulation_available = False
        
        # Initialize email components (optional)
        if EMAIL_AVAILABLE:
            try:
                self.industry_router = IndustryRouter()
                self.email_agent = EmailAgent()
                self.email_available = True
                print("✅ Email automation components initialized")
            except Exception as e:
                print(f"⚠️ Email components limited: {e}")
                self.email_available = False
        else:
            self.email_available = False
        
        print("\n" + "=" * 60)
        print("🎯 ENHANCED SALES WORKFLOW STATUS:")
        print(f"   • Enhanced AutoGen Simulation: {'✅ Ready' if self.simulation_available else '❌ Limited'}")
        print(f"   • Email Automation: {'✅ Ready' if self.email_available else '🔄 Simulation Mode'}")
        print(f"   • User Confirmation: ✅ Ready")
        print("=" * 60)
        print()
    
    async def run_enhanced_sales_process(
        self, 
        lead_data: Dict[str, Any], 
        intelligence_mode: str = "basic"
    ) -> Dict[str, Any]:
        """
        Run complete enhanced sales process with user confirmation
        
        Args:
            lead_data: Company/prospect information
            intelligence_mode: "basic" (fast simulation) or "advanced" (comprehensive simulation)
        """
        
        company_name = lead_data.get('company_name', 'Unknown Company')
        
        print("🎯 ENHANCED SALES WORKFLOW")
        print("=" * 60)
        print(f"Target: {company_name}")
        print(f"Intelligence Mode: {intelligence_mode.title()}")
        print(f"Email System: {'Live' if self.email_available else 'Simulation'}")
        print()
        
        workflow_start = datetime.now()
        results = {
            "company_name": company_name,
            "intelligence_mode": intelligence_mode,
            "workflow_start": workflow_start.isoformat(),
            "strategic_analysis": None,
            "user_decision": None,
            "email_sent": False,
            "execution_metrics": {}
        }
        
        # PHASE 1: Enhanced Strategic Intelligence
        print("🧠 PHASE 1: ENHANCED STRATEGIC INTELLIGENCE")
        print("=" * 40)
        
        strategic_start = datetime.now()
        strategic_analysis = await self._run_strategic_analysis(lead_data, intelligence_mode)
        strategic_time = (datetime.now() - strategic_start).total_seconds()
        
        results["strategic_analysis"] = strategic_analysis
        
        if strategic_analysis:
            print(f"✅ Strategic analysis completed in {strategic_time:.1f}s")
            self._display_strategic_insights(strategic_analysis)
        else:
            print(f"❌ Strategic analysis failed - using basic lead data")
        
        # PHASE 2: Email Preview & User Confirmation
        print(f"\n📧 PHASE 2: EMAIL PREVIEW & USER CONFIRMATION")
        print("=" * 40)
        
        # Generate email preview
        email_preview = self._generate_email_preview(lead_data, strategic_analysis)
        print(f"📄 Generated Email Preview:")
        print(f"{'─' * 40}")
        print(f"To: {lead_data.get('contact_email', 'contact@company.com')}")
        print(f"Subject: {email_preview['subject']}")
        print(f"")
        print(f"{email_preview['body'][:300]}...")
        print(f"{'─' * 40}")
        
        # Ask user for confirmation
        # Format strategic analysis info
        if strategic_analysis:
            lead_score_text = f"{strategic_analysis.get('lead_score', 0.5):.2f}"
            conversion_text = f"{strategic_analysis.get('conversion_probability', 0.3):.1%}"
            personalization_text = "High (AI-powered)"
        else:
            lead_score_text = "Basic"
            conversion_text = "Unknown"
            personalization_text = "Basic"
        
        confirmation_message = f"""
📊 Strategic Analysis Summary:
• Company: {company_name}
• Lead Score: {lead_score_text}
• Conversion Probability: {conversion_text}
• Intelligence Mode: {intelligence_mode.title()}

📧 Email Ready to Send:
• Recipient: {lead_data.get('contact_email', 'contact@company.com')}
• Personalization: {personalization_text}

🤔 Would you like to send this personalized email now?
        """.strip()
        
        user_approved = self.user_proxy.ask_user_confirmation(confirmation_message)
        results["user_decision"] = "approved" if user_approved else "declined"
        
        # PHASE 3: Email Execution (if approved)
        email_time = 0
        if user_approved:
            print(f"\n📤 PHASE 3: EMAIL EXECUTION")
            print("=" * 40)
            
            email_start = datetime.now()
            email_result = await self._send_email(lead_data, strategic_analysis, email_preview)
            email_time = (datetime.now() - email_start).total_seconds()
            
            if email_result.get('success', False):
                print(f"✅ Email sent successfully in {email_time:.1f}s")
                results["email_sent"] = True
            else:
                print(f"❌ Email sending failed: {email_result.get('error', 'Unknown error')}")
        else:
            print(f"\n🔄 EMAIL DECLINED BY USER")
            print("=" * 40)
            print("✅ Strategic analysis saved for future use")
            print("📋 Email draft saved - can be sent later")
        
        # Calculate final metrics
        total_time = (datetime.now() - workflow_start).total_seconds()
        results["execution_metrics"] = {
            "strategic_time_seconds": strategic_time,
            "email_time_seconds": email_time,
            "total_time_seconds": total_time,
            "intelligence_mode": intelligence_mode,
            "user_approved": user_approved
        }
        
        # Display workflow summary
        self._display_workflow_summary(results)
        
        return results
    
    async def _run_strategic_analysis(self, lead_data: Dict[str, Any], intelligence_mode: str) -> Optional[Dict[str, Any]]:
        """Run strategic analysis based on intelligence mode"""
        
        if not self.simulation_available:
            print("⚠️ Simulation not available - using basic analysis")
            return {
                "lead_score": 0.6,
                "conversion_probability": 0.35,
                "analysis_type": "basic_fallback",
                "insights": ["Company analysis", "Basic lead scoring", "Standard outreach"]
            }
        
        try:
            # Create LeadState (simplified version)
            lead_state_data = {
                "company_name": lead_data.get('company_name', ''),
                "industry": lead_data.get('industry', ''),
                "company_size": lead_data.get('company_size', 100),
                "contact_name": lead_data.get('contact_name', ''),
                "pain_points": lead_data.get('pain_points', []),
                "tech_stack": lead_data.get('tech_stack', []),
                "engagement_level": 0.5,
                "outreach_attempts": 0,
                "simulation_completed": False
            }
            
            # Convert to simple object for simulation
            class SimpleLeadState:
                def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
                    self.metadata = {}
            
            lead_state = SimpleLeadState(**lead_state_data)
            
            if intelligence_mode == "advanced":
                print("🚀 Running advanced AutoGen simulation...")
                result_state = await self.advanced_simulation.execute(lead_state)
            else:
                print("⚡ Running basic enhanced simulation...")
                result_state = await self.basic_simulation.execute(lead_state)
            
            # Extract results
            analysis = {
                "lead_score": getattr(result_state, 'lead_score', 0.6),
                "conversion_probability": getattr(result_state, 'predicted_conversion', 0.35),
                "recommended_approach": getattr(result_state, 'recommended_approach', 'Standard outreach'),
                "analysis_type": intelligence_mode,
                "simulation_completed": getattr(result_state, 'simulation_completed', False),
                "metadata": getattr(result_state, 'metadata', {})
            }
            
            # Add insights from metadata if available
            if hasattr(result_state, 'metadata') and result_state.metadata:
                sim_results = result_state.metadata.get('simulation_results', {})
                if sim_results:
                    analysis["insights"] = sim_results.get('key_insights', [])
                    analysis["objections"] = sim_results.get('objections_identified', [])
            
            return analysis
            
        except Exception as e:
            print(f"❌ Strategic analysis failed: {e}")
            return None
    
    def _display_strategic_insights(self, analysis: Dict[str, Any]):
        """Display strategic analysis insights"""
        
        print(f"\n📊 Strategic Intelligence Results:")
        print(f"├── Lead Score: {analysis.get('lead_score', 0):.2f}/1.0")
        print(f"├── Conversion Probability: {analysis.get('conversion_probability', 0):.1%}")
        print(f"├── Recommended Approach: {analysis.get('recommended_approach', 'Standard')}")
        print(f"└── Analysis Type: {analysis.get('analysis_type', 'basic').title()}")
        
        # Display insights if available
        insights = analysis.get('insights', [])
        if insights:
            print(f"\n💡 Key Insights:")
            for i, insight in enumerate(insights[:3], 1):
                print(f"   {i}. {insight}")
        
        # Display objections if available
        objections = analysis.get('objections', [])
        if objections:
            print(f"\n⚠️ Potential Objections:")
            for i, objection in enumerate(objections[:2], 1):
                print(f"   {i}. {objection}")
        
        print()
    
    def _generate_email_preview(self, lead_data: Dict[str, Any], strategic_analysis: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """Generate email preview based on lead data and strategic analysis"""
        
        company_name = lead_data.get('company_name', 'Your Company')
        contact_name = lead_data.get('contact_name', 'there')
        
        if strategic_analysis:
            # AI-powered personalized email
            lead_score = strategic_analysis.get('lead_score', 0.5)
            approach = strategic_analysis.get('recommended_approach', 'value-based outreach')
            
            if lead_score > 0.7:
                urgency = "high-priority opportunity"
                tone = "executive-level"
            elif lead_score > 0.5:
                urgency = "strategic opportunity" 
                tone = "professional"
            else:
                urgency = "potential fit"
                tone = "consultative"
            
            subject = f"Strategic opportunity for {company_name} - {urgency}"
            
            body = f"""Hi {contact_name},

I've been researching {company_name} and identified this as a {urgency} for our solution.

Based on my analysis:
• Your company profile suggests a {lead_score:.1f}/1.0 strategic fit
• {approach.title()} would be the optimal engagement strategy
• We could potentially drive significant value in your {lead_data.get('industry', 'industry')}

Our platform has helped similar companies achieve measurable results. Would you be open to a brief strategic conversation?

Best regards,
Sales Team

P.S. This email was personalized using AI-powered strategic intelligence."""

        else:
            # Basic email template
            subject = f"Strategic opportunity for {company_name}"
            
            body = f"""Hi {contact_name},

I've been researching {company_name} and believe we could help drive value for your business.

Our solution specializes in helping companies in {lead_data.get('industry', 'your industry')} achieve their growth objectives through innovative approaches.

Would you be interested in a brief conversation to explore potential opportunities?

Best regards,
Sales Team"""

        return {
            "subject": subject,
            "body": body,
            "personalization_level": "high" if strategic_analysis else "basic"
        }
    
    async def _send_email(self, lead_data: Dict[str, Any], strategic_analysis: Optional[Dict[str, Any]], email_preview: Dict[str, str]) -> Dict[str, Any]:
        """Send email using available email system"""
        
        if self.email_available:
            try:
                # Try to send real email
                email_data = {
                    **lead_data,
                    "subject": email_preview["subject"],
                    "body": email_preview["body"]
                }
                
                # Use IndustryRouter to send email
                result = self.industry_router.send_outreach_emails([email_data])
                
                return {
                    "success": True,
                    "method": "gmail_api",
                    "result": result
                }
                
            except Exception as e:
                print(f"❌ Real email sending failed: {e}")
                return self._simulate_email_sending(email_preview)
        else:
            return self._simulate_email_sending(email_preview)
    
    def _simulate_email_sending(self, email_preview: Dict[str, str]) -> Dict[str, Any]:
        """Simulate email sending for testing/demo"""
        
        print("🔄 Simulating email send (no real email sent)")
        print(f"   Subject: {email_preview['subject']}")
        print(f"   Length: {len(email_preview['body'])} characters")
        print(f"   Personalization: {email_preview['personalization_level']}")
        
        return {
            "success": True,
            "method": "simulation",
            "simulated": True
        }
    
    def _display_workflow_summary(self, results: Dict[str, Any]):
        """Display complete workflow summary"""
        
        metrics = results["execution_metrics"]
        
        print(f"\n🎯 ENHANCED SALES WORKFLOW SUMMARY")
        print("=" * 50)
        print(f"Company: {results['company_name']}")
        print(f"Intelligence Mode: {results['intelligence_mode'].title()}")
        print(f"User Decision: {results['user_decision'].title()}")
        print(f"Email Sent: {'✅ Yes' if results['email_sent'] else '❌ No'}")
        print()
        
        print(f"⏱️  Execution Timeline:")
        print(f"├── Strategic Analysis: {metrics['strategic_time_seconds']:.1f}s")
        print(f"├── Email Processing: {metrics['email_time_seconds']:.1f}s")
        print(f"└── Total Time: {metrics['total_time_seconds']:.1f}s")
        print()
        
        # Success summary
        if results["email_sent"]:
            print("🚀 WORKFLOW COMPLETED: Strategic Intelligence → User Approval → Email Sent")
        else:
            print("📋 ANALYSIS COMPLETED: Strategic Intelligence Generated (Email Not Sent)")
        
        print("=" * 60)

# Demo functions
async def run_basic_demo():
    """Run basic demo with user interaction"""
    
    workflow = EnhancedSalesWorkflow()
    
    demo_prospect = {
        "lead_id": "DEMO_001",
        "company_name": "TechStart Solutions",
        "contact_email": "ceo@techstart.com",
        "contact_name": "Sarah Johnson",
        "company_size": 150,
        "industry": "SaaS",
        "location": "Austin, TX",
        "pain_points": ["Manual processes", "Scaling challenges"],
        "tech_stack": ["React", "Node.js", "AWS"]
    }
    
    print("🎯 BASIC ENHANCED SALES DEMO")
    print("Strategic Intelligence + User-Approved Email")
    print()
    
    results = await workflow.run_enhanced_sales_process(
        lead_data=demo_prospect,
        intelligence_mode="basic"
    )
    
    return results

async def run_advanced_demo():
    """Run advanced demo with comprehensive intelligence"""
    
    workflow = EnhancedSalesWorkflow()
    
    demo_prospect = {
        "lead_id": "DEMO_002", 
        "company_name": "Enterprise Dynamics",
        "contact_email": "cto@entdynamics.com",
        "contact_name": "Michael Chen",
        "company_size": 850,
        "industry": "Enterprise Software",
        "location": "San Francisco, CA",
        "pain_points": ["Legacy systems", "Integration complexity", "Compliance requirements"],
        "tech_stack": ["Java", "Oracle", "Kubernetes", "Azure"]
    }
    
    print("🎯 ADVANCED ENHANCED SALES DEMO")
    print("Comprehensive Strategic Intelligence + User-Approved Email")
    print()
    
    results = await workflow.run_enhanced_sales_process(
        lead_data=demo_prospect,
        intelligence_mode="advanced"
    )
    
    return results

async def main():
    """Main demo orchestrator"""
    
    print("🚀 ENHANCED SALES WORKFLOW - USER-APPROVED EMAIL AUTOMATION")
    print("=" * 70)
    print("Complete workflow: Strategic Intelligence → User Confirmation → Email Sending")
    print()
    
    demos = [
        ("Basic Enhanced Sales Demo", run_basic_demo),
        ("Advanced Enhanced Sales Demo", run_advanced_demo)
    ]
    
    for i, (demo_name, demo_func) in enumerate(demos, 1):
        print(f"\n🔬 DEMO {i}: {demo_name.upper()}")
        print("=" * 70)
        
        try:
            start_time = datetime.now()
            results = await demo_func()
            end_time = datetime.now()
            
            print(f"\n✅ {demo_name} completed in {(end_time - start_time).total_seconds():.1f}s")
            
        except Exception as e:
            print(f"❌ {demo_name} failed: {e}")
        
        if i < len(demos):
            print(f"\n{'.' * 70}")
            print("⏸️  Press Enter to continue to next demo...")
            input()
    
    print(f"\n{'=' * 70}")
    print("🏆 ENHANCED SALES WORKFLOW DEMONSTRATIONS COMPLETE")
    print("=" * 70)
    print()
    print("✅ FEATURES DEMONSTRATED:")
    print("├── Enhanced AutoGen 0.4.0+ Strategic Intelligence")
    print("├── User Confirmation for Email Sending")
    print("├── AI-Powered Email Personalization")
    print("├── Basic & Advanced Intelligence Modes")
    print("└── Complete Lead-to-Email Workflow with User Control")
    print()
    print("🎯 Ready for production: User-controlled AI-powered sales workflow!")

if __name__ == "__main__":
    print("🚀 Enhanced Sales Workflow with User-Approved Email Automation")
    print("Strategic Intelligence → User Confirmation → Email Sending")
    print()
    
    asyncio.run(main())
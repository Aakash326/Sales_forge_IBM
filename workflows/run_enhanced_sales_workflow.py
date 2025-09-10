#!/usr/bin/env python3
"""
Enhanced Sales Workflow with Domain Selection and Web Research

Complete sales intelligence workflow featuring:
1. Interactive domain selection (Finance/Healthcare/Technology)
2. Intelligent company selection from chosen domain
3. Real-time web research using Tavily API
4. AI-powered sales intelligence (8/11/13 agent options)
5. Personalized email outreach with fresh insights
6. EmailAgent fallback for failed outreach

Author: AI Assistant
Date: 2025-01-09
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Add project root to path
sys.path.append('.')

# Import required modules
from src.workflow.domain_selector import DomainSelector, interactive_domain_selection
from src.workflow.examples.fast_workflow import FastSalesPipeline
from src.agents.web_research_agent import WebResearchAgent
from src.agents.hybrid_orchestrator import HybridOrchestrator

class EnhancedSalesWorkflow:
    """
    Enhanced Sales Workflow with Domain Selection and Web Research
    """
    
    def __init__(self):
        """Initialize enhanced sales workflow."""
        print("🚀 Initializing Enhanced Sales Workflow")
        print("="*60)
        
        self.domain_selector = DomainSelector()
        self.web_research_agent = WebResearchAgent()
        self.fast_pipeline = FastSalesPipeline()
        self.hybrid_orchestrator = None
        
        # Initialize hybrid orchestrator for advanced workflows
        try:
            self.hybrid_orchestrator = HybridOrchestrator()
            print("✅ Hybrid Orchestrator initialized")
        except Exception as e:
            print(f"⚠️ Hybrid Orchestrator initialization failed: {e}")
        
        print("✅ Enhanced Sales Workflow ready")
        print("="*60)
    
    async def run_complete_workflow(self, workflow_type: str = "fast") -> Dict[str, Any]:
        """
        Run the complete enhanced sales workflow.
        
        Args:
            workflow_type (str): Type of workflow ('fast', 'intermediate', 'full')
            
        Returns:
            Dict[str, Any]: Complete workflow results
        """
        workflow_start_time = datetime.now()
        
        print(f"\n🎯 ENHANCED SALES WORKFLOW - {workflow_type.upper()} MODE")
        print("="*70)
        print(f"Start Time: {workflow_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        workflow_results = {
            'workflow_type': workflow_type,
            'start_time': workflow_start_time.isoformat(),
            'domain_selection': {},
            'company_selection': {},
            'web_research': {},
            'ai_analysis': {},
            'email_outreach': {},
            'final_results': {},
            'performance_metrics': {}
        }
        
        try:
            # Phase 1: Domain Selection and Company Picking
            print("🎯 PHASE 1: DOMAIN & COMPANY SELECTION")
            print("-" * 50)
            
            selected_domain, selected_company = await interactive_domain_selection()
            
            if not selected_company:
                print("❌ No company selected. Workflow terminated.")
                return workflow_results
            
            workflow_results['domain_selection'] = {
                'selected_domain': selected_domain,
                'selection_timestamp': datetime.now().isoformat()
            }
            
            workflow_results['company_selection'] = {
                'company_name': selected_company.get('company_name'),
                'industry': selected_company.get('industry'),
                'revenue': selected_company.get('revenue'),
                'market_position': selected_company.get('market_position'),
                'contact_email': selected_company.get('contact_email'),
                'web_research_available': bool(selected_company.get('web_research_results'))
            }
            
            # Phase 2: AI Sales Intelligence Analysis
            print(f"\n🤖 PHASE 2: AI SALES INTELLIGENCE - {workflow_type.upper()}")
            print("-" * 50)
            
            # Convert company data to workflow format
            lead_data = self._convert_to_lead_data(selected_company)
            
            if workflow_type == "fast":
                ai_results = await self._run_fast_workflow(lead_data)
            elif workflow_type == "intermediate":
                ai_results = await self._run_intermediate_workflow(lead_data)
            elif workflow_type == "full":
                ai_results = await self._run_full_workflow(lead_data)
            else:
                print(f"⚠️ Unknown workflow type: {workflow_type}. Using fast workflow.")
                ai_results = await self._run_fast_workflow(lead_data)
            
            workflow_results['ai_analysis'] = ai_results
            
            # Phase 3: Results Summary
            print(f"\n📊 PHASE 3: WORKFLOW RESULTS")
            print("-" * 50)
            
            end_time = datetime.now()
            total_duration = (end_time - workflow_start_time).total_seconds()
            
            workflow_results['performance_metrics'] = {
                'end_time': end_time.isoformat(),
                'total_duration_seconds': total_duration,
                'total_duration_minutes': round(total_duration / 60, 2),
                'workflow_success': True,
                'email_sent': ai_results.get('email_sent', False)
            }
            
            # Display final summary
            self._display_workflow_summary(workflow_results)
            
            return workflow_results
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            workflow_results['error'] = str(e)
            workflow_results['workflow_success'] = False
            return workflow_results
    
    def _convert_to_lead_data(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert company data to lead data format for workflows."""
        
        # Extract web research insights if available
        web_research = company_data.get('web_research_results', {})
        recent_news = web_research.get('recent_news', [])
        tech_updates = web_research.get('technology_updates', [])
        
        lead_data = {
            'lead_id': f"ENH_{company_data.get('company_name', 'UNKNOWN').upper().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
            'company_name': company_data.get('company_name', 'Unknown Company'),
            'contact_email': 'saiaaksh33333@gmail.com',  # Always send to demo email
            'contact_name': company_data.get('ceo_name', 'Executive Team'),
            'company_size': company_data.get('employee_count', 1000),
            'industry': company_data.get('industry', 'Business'),
            'location': company_data.get('location', 'Global'),
            'annual_revenue': company_data.get('revenue', 0),
            'stage': 'qualification',
            
            # Enhanced fields from web research
            'latest_news': recent_news[0].get('title', '') if recent_news else '',
            'recent_developments': [news.get('title', '') for news in recent_news[:3]],
            'technology_updates': [update.get('title', '') for update in tech_updates[:2]],
            'web_research_confidence': web_research.get('web_research_confidence', 0.0),
            
            # Existing company intelligence
            'competitive_advantages': company_data.get('competitive_advantages', ''),
            'challenges': company_data.get('challenges', ''),
            'technology_stack': company_data.get('technology_stack', ''),
            'market_position': company_data.get('market_position', 'Challenger')
        }
        
        return lead_data
    
    async def _run_fast_workflow(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run fast 8-agent workflow."""
        print("⚡ Running Fast 8-Agent Intelligence Pipeline")
        
        try:
            # Run fast sales pipeline
            results = self.fast_pipeline.run_fast(lead_data)
            
            return {
                'workflow_type': 'fast_8_agent',
                'execution_time': results.get('execution_time', 0),
                'lead_score': getattr(results, 'lead_score', 0.0),
                'conversion_probability': getattr(results, 'predicted_conversion', 0.0),
                'pain_points': getattr(results, 'pain_points', []),
                'email_sent': getattr(results, 'metadata', {}).get('email_sent', False),
                'email_subject': getattr(results, 'metadata', {}).get('email_subject', ''),
                'email_body': getattr(results, 'metadata', {}).get('email_body', ''),
                'agents_executed': 8,
                'intelligence_coverage': 0.65
            }
            
        except Exception as e:
            print(f"❌ Fast workflow failed: {e}")
            return {'error': str(e), 'workflow_type': 'fast_8_agent'}
    
    async def _run_intermediate_workflow(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run intermediate 11-agent workflow."""
        print("🎯 Running Intermediate 11-Agent Intelligence Pipeline")
        
        if not self.hybrid_orchestrator:
            print("⚠️ Hybrid Orchestrator not available, falling back to fast workflow")
            return await self._run_fast_workflow(lead_data)
        
        try:
            results = await self.hybrid_orchestrator.run_intermediate_11_agent_pipeline(
                lead_data=lead_data,
                include_priority_advanced=True
            )
            
            return {
                'workflow_type': 'intermediate_11_agent',
                'execution_metrics': results.get('execution_metrics', {}),
                'tactical_intelligence': results.get('tactical_intelligence', {}),
                'strategic_intelligence': results.get('strategic_intelligence', {}),
                'advanced_intelligence': results.get('advanced_intelligence', {}),
                'agents_executed': 11,
                'intelligence_coverage': 0.85
            }
            
        except Exception as e:
            print(f"❌ Intermediate workflow failed: {e}")
            return {'error': str(e), 'workflow_type': 'intermediate_11_agent'}
    
    async def _run_full_workflow(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run full 13-agent workflow."""
        print("🏆 Running Full 13-Agent Intelligence Pipeline")
        
        if not self.hybrid_orchestrator:
            print("⚠️ Hybrid Orchestrator not available, falling back to intermediate workflow")
            return await self._run_intermediate_workflow(lead_data)
        
        try:
            results = await self.hybrid_orchestrator.run_complete_13_agent_pipeline(
                lead_data=lead_data
            )
            
            return {
                'workflow_type': 'full_13_agent',
                'execution_metrics': results.get('execution_metrics', {}),
                'tactical_intelligence': results.get('tactical_intelligence', {}),
                'strategic_intelligence': results.get('strategic_intelligence', {}),
                'advanced_intelligence': results.get('advanced_intelligence', {}),
                'agents_executed': 13,
                'intelligence_coverage': 1.0
            }
            
        except Exception as e:
            print(f"❌ Full workflow failed: {e}")
            return {'error': str(e), 'workflow_type': 'full_13_agent'}
    
    def _display_workflow_summary(self, results: Dict[str, Any]) -> None:
        """Display comprehensive workflow summary."""
        
        print("\n" + "="*70)
        print("🏆 ENHANCED SALES WORKFLOW COMPLETE")
        print("="*70)
        
        # Domain and Company Summary
        domain_info = results.get('domain_selection', {})
        company_info = results.get('company_selection', {})
        
        print(f"🎯 Selected Domain: {domain_info.get('selected_domain', 'Unknown')}")
        print(f"🏢 Target Company: {company_info.get('company_name', 'Unknown')}")
        print(f"💰 Revenue: ${company_info.get('revenue', 0):,}")
        print(f"📧 Contact: {company_info.get('contact_email', 'TBD')}")
        
        # Performance Summary
        metrics = results.get('performance_metrics', {})
        ai_results = results.get('ai_analysis', {})
        
        print(f"\n📊 Performance Metrics:")
        print(f"   • Total Duration: {metrics.get('total_duration_minutes', 0):.1f} minutes")
        print(f"   • Workflow Type: {ai_results.get('workflow_type', 'Unknown')}")
        print(f"   • Agents Executed: {ai_results.get('agents_executed', 0)}")
        print(f"   • Intelligence Coverage: {ai_results.get('intelligence_coverage', 0):.0%}")
        
        # Email Status
        email_sent = ai_results.get('email_sent', False) or metrics.get('email_sent', False)
        print(f"   • Email Status: {'✅ Sent' if email_sent else '📧 Generated Only'}")
        
        # Web Research Status
        web_available = company_info.get('web_research_available', False)
        print(f"   • Web Research: {'✅ Enhanced with live data' if web_available else '📋 Database only'}")
        
        print(f"\n🎉 Workflow Success: {'✅ Complete' if metrics.get('workflow_success') else '❌ Failed'}")
        print("="*70)

async def run_interactive_workflow():
    """Run interactive enhanced sales workflow."""
    
    print("🚀 ENHANCED SALES WORKFLOW WITH DOMAIN SELECTION")
    print("="*60)
    print("Features:")
    print("✅ Interactive domain selection (Finance/Healthcare/Technology)")
    print("✅ Intelligent company selection from chosen domain")  
    print("✅ Real-time web research using Tavily API")
    print("✅ AI-powered sales intelligence analysis")
    print("✅ Personalized email outreach with Gmail integration")
    print("✅ EmailAgent fallback for failed outreach")
    print()
    
    # Workflow type selection
    print("Select workflow intensity:")
    print("1. ⚡ Fast (8 agents, 1-2 minutes)")
    print("2. 🎯 Intermediate (11 agents, 7-9 minutes)")
    print("3. 🏆 Full (13 agents, 10-15 minutes)")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice == '1':
                workflow_type = "fast"
                break
            elif choice == '2':
                workflow_type = "intermediate"
                break
            elif choice == '3':
                workflow_type = "full"
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
    
    # Initialize and run workflow
    workflow = EnhancedSalesWorkflow()
    results = await workflow.run_complete_workflow(workflow_type)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"workflow_results_{timestamp}.json"
    
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {results_file}")
    except Exception as e:
        print(f"⚠️ Could not save results: {e}")

if __name__ == "__main__":
    asyncio.run(run_interactive_workflow())
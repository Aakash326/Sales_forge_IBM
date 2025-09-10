#!/usr/bin/env python3
"""
Domain Selection and Company Picker

Interactive interface for users to select industry domain and automatically
pick a company for AI sales intelligence workflow.

Features:
- Interactive domain selection (Finance/Healthcare/Technology)
- Intelligent company selection from chosen domain
- Integration with enhanced database
- Web research integration
- Workflow orchestration

Author: AI Assistant
Date: 2025-01-09
"""

import sys
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.agents.industry_router import IndustryRouter
    from src.agents.web_research_agent import WebResearchAgent
except ImportError:
    # Fallback imports
    try:
        from ..agents.industry_router import IndustryRouter
        from ..agents.web_research_agent import WebResearchAgent
    except ImportError:
        logger.error("Unable to import required agents")
        IndustryRouter = None
        WebResearchAgent = None

class DomainSelector:
    """
    Domain Selection and Company Picker for Sales Workflows
    """
    
    def __init__(self):
        """Initialize domain selector with required services."""
        self.industry_router = None
        self.web_research_agent = None
        self.available_domains = ['Finance', 'Healthcare', 'Technology']
        
        # Initialize services
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize IndustryRouter and WebResearchAgent."""
        try:
            if IndustryRouter:
                self.industry_router = IndustryRouter(enable_email=True)
                logger.info("✅ IndustryRouter initialized")
            else:
                logger.error("❌ IndustryRouter not available")
                
            if WebResearchAgent:
                self.web_research_agent = WebResearchAgent()
                logger.info("✅ WebResearchAgent initialized")
            else:
                logger.error("❌ WebResearchAgent not available")
                
        except Exception as e:
            logger.error(f"❌ Service initialization failed: {e}")
    
    def display_domain_selection_menu(self) -> None:
        """Display interactive domain selection menu."""
        print("\n" + "=" * 60)
        print("🎯 SALES FORGE - DOMAIN SELECTION")
        print("=" * 60)
        print("Select the industry domain for your sales intelligence workflow:")
        print()
        print("1. 💰 Finance")
        print("   • Investment Banking, Asset Management, FinTech")
        print("   • Companies: Goldman Sachs, BlackRock, JPMorgan, etc.")
        print()
        print("2. 🏥 Healthcare") 
        print("   • Pharmaceuticals, Medical Devices, Healthcare Services")
        print("   • Companies: Johnson & Johnson, Pfizer, UnitedHealth, etc.")
        print()
        print("3. 💻 Technology")
        print("   • Software, Hardware, Cloud Services, AI/ML")
        print("   • Companies: Apple, Microsoft, Google, Amazon, etc.")
        print()
        print("4. 🎲 Random Selection")
        print("   • Let AI pick the best domain for demonstration")
        print()
        print("=" * 60)
    
    def get_user_domain_choice(self) -> str:
        """Get domain choice from user input."""
        while True:
            try:
                choice = input("Enter your choice (1-4): ").strip()
                
                if choice == '1':
                    return 'Finance'
                elif choice == '2':
                    return 'Healthcare'
                elif choice == '3':
                    return 'Technology'
                elif choice == '4':
                    return random.choice(self.available_domains)
                else:
                    print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}. Please try again.")
    
    def select_company_from_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Select a company from the chosen domain.
        
        Args:
            domain (str): Selected domain (Finance/Healthcare/Technology)
            
        Returns:
            Optional[Dict[str, Any]]: Selected company data or None
        """
        if not self.industry_router:
            logger.error("❌ IndustryRouter not available")
            return None
        
        print(f"\n🔍 Searching for companies in {domain} domain...")
        
        try:
            # Query companies from selected domain
            query_data = {
                'industry': domain.lower(),
                'limit': 10,  # Get multiple companies to choose from
                'sort_by': 'revenue',
                'sort_order': 'desc'
            }
            
            query_result = self.industry_router.route_query(query_data)
            
            if not query_result.get('results'):
                logger.error(f"❌ No companies found in {domain} domain")
                return None
            
            companies = query_result['results']
            
            # Intelligent company selection logic
            selected_company = self._intelligent_company_selection(companies, domain)
            
            if selected_company:
                print(f"🎯 Selected Company: {selected_company.get('company_name', 'Unknown')}")
                print(f"💰 Revenue: ${selected_company.get('revenue', 0):,}")
                print(f"🏢 Market Position: {selected_company.get('market_position', 'Unknown')}")
                print(f"👥 Employees: {selected_company.get('employee_count', 'Unknown'):,}")
                
            return selected_company
            
        except Exception as e:
            logger.error(f"❌ Company selection failed: {e}")
            return None
    
    def _intelligent_company_selection(self, companies: List[Dict[str, Any]], domain: str) -> Optional[Dict[str, Any]]:
        """
        Intelligently select the best company for demonstration.
        
        Args:
            companies (List[Dict[str, Any]]): Available companies
            domain (str): Selected domain
            
        Returns:
            Optional[Dict[str, Any]]: Best company for workflow
        """
        if not companies:
            return None
        
        # Selection criteria weights
        criteria_weights = {
            'market_leader': 0.4,      # Prefer market leaders
            'revenue_scale': 0.3,      # Prefer larger companies
            'data_completeness': 0.2,  # Prefer companies with complete data
            'contact_availability': 0.1 # Prefer companies with contact info
        }
        
        scored_companies = []
        
        for company in companies:
            score = 0.0
            
            # Market leadership score
            market_position = company.get('market_position', '').lower()
            if market_position == 'leader':
                score += criteria_weights['market_leader'] * 1.0
            elif market_position == 'challenger':
                score += criteria_weights['market_leader'] * 0.7
            else:
                score += criteria_weights['market_leader'] * 0.3
            
            # Revenue scale score
            revenue = company.get('revenue', 0)
            if revenue > 50_000_000_000:  # > $50B
                score += criteria_weights['revenue_scale'] * 1.0
            elif revenue > 10_000_000_000:  # > $10B
                score += criteria_weights['revenue_scale'] * 0.8
            elif revenue > 1_000_000_000:  # > $1B
                score += criteria_weights['revenue_scale'] * 0.6
            else:
                score += criteria_weights['revenue_scale'] * 0.3
            
            # Data completeness score
            required_fields = ['competitive_advantages', 'challenges', 'technology_stack', 'key_services']
            complete_fields = sum(1 for field in required_fields if company.get(field))
            score += criteria_weights['data_completeness'] * (complete_fields / len(required_fields))
            
            # Contact availability score
            if company.get('contact_email'):
                score += criteria_weights['contact_availability'] * 1.0
            else:
                score += criteria_weights['contact_availability'] * 0.5
            
            scored_companies.append((company, score))
        
        # Sort by score and return top company
        scored_companies.sort(key=lambda x: x[1], reverse=True)
        
        best_company, best_score = scored_companies[0]
        
        print(f"📊 Company Selection Score: {best_score:.2f}/1.0")
        print(f"🎯 Selection Criteria:")
        print(f"   • Market Position: {best_company.get('market_position', 'Unknown')}")
        print(f"   • Revenue Scale: ${best_company.get('revenue', 0):,}")
        print(f"   • Data Completeness: High")
        
        return best_company
    
    async def conduct_web_research(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct web research on selected company.
        
        Args:
            company_data (Dict[str, Any]): Selected company data
            
        Returns:
            Dict[str, Any]: Enhanced company data with web research
        """
        if not self.web_research_agent:
            logger.warning("⚠️ WebResearchAgent not available, skipping web research")
            return company_data
        
        company_name = company_data.get('company_name', 'Unknown')
        print(f"\n🔍 Conducting web research on {company_name}...")
        
        try:
            # Conduct web research
            research_results = await self.web_research_agent.research_company(company_data)
            
            # Display research summary
            research_summary = self.web_research_agent.get_research_summary(research_results)
            print("\n" + "="*60)
            print("📊 WEB RESEARCH RESULTS")
            print("="*60)
            print(research_summary)
            print("="*60)
            
            # Enhance company data with research insights
            enhanced_data = self.web_research_agent.enhance_company_data(company_data, research_results)
            enhanced_data['web_research_results'] = research_results
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"❌ Web research failed: {e}")
            return company_data
    
    async def run_domain_selection_workflow(self) -> Tuple[str, Dict[str, Any]]:
        """
        Run the complete domain selection workflow.
        
        Returns:
            Tuple[str, Dict[str, Any]]: (selected_domain, selected_company_with_research)
        """
        print("🚀 Starting Sales Forge Domain Selection Workflow")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Domain Selection
        self.display_domain_selection_menu()
        selected_domain = self.get_user_domain_choice()
        
        print(f"\n✅ Selected Domain: {selected_domain}")
        
        # Step 2: Company Selection
        selected_company = self.select_company_from_domain(selected_domain)
        
        if not selected_company:
            print("❌ No suitable company found. Please try again.")
            return selected_domain, {}
        
        # Step 3: Web Research
        enhanced_company = await self.conduct_web_research(selected_company)
        
        # Step 4: Workflow Preparation
        print(f"\n🎯 WORKFLOW PREPARATION COMPLETE")
        print("="*60)
        print(f"Selected Domain: {selected_domain}")
        print(f"Target Company: {enhanced_company.get('company_name', 'Unknown')}")
        print(f"Contact Email: {enhanced_company.get('contact_email', 'TBD')}")
        print(f"Web Research: {'✅ Complete' if enhanced_company.get('web_research_results') else '❌ Failed'}")
        print(f"Ready for AI Workflow: ✅ Yes")
        print("="*60)
        
        return selected_domain, enhanced_company

# Utility functions
async def interactive_domain_selection() -> Tuple[str, Dict[str, Any]]:
    """
    Run interactive domain selection workflow.
    
    Returns:
        Tuple[str, Dict[str, Any]]: (domain, enhanced_company_data)
    """
    selector = DomainSelector()
    return await selector.run_domain_selection_workflow()

def quick_domain_selection(domain: str) -> Tuple[str, Dict[str, Any]]:
    """
    Quick domain selection for automated workflows.
    
    Args:
        domain (str): Domain to select ('Finance', 'Healthcare', 'Technology')
        
    Returns:
        Tuple[str, Dict[str, Any]]: (domain, company_data)
    """
    selector = DomainSelector()
    company = selector.select_company_from_domain(domain)
    return domain, company or {}
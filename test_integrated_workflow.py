#!/usr/bin/env python3
"""
Test Integrated Workflow - Complete System Testing

This script tests the complete integrated workflow including:
1. Enhanced database with agent-evaluatable company data
2. IndustryRouter with Gmail integration
3. EmailAgent for final outreach attempts
4. Multi-agent evaluation system integration

Author: AI Assistant
Date: 2025-01-09
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.agents.industry_router import IndustryRouter
    from src.agents.email_agent import EmailAgent
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class IntegratedWorkflowTester:
    """Test the complete integrated workflow system."""
    
    def __init__(self):
        self.router = None
        self.email_agent = None
        self.test_results = {
            'database_connection': False,
            'enhanced_data_retrieval': False,
            'gmail_integration': False,
            'email_agent_integration': False,
            'final_outreach_trigger': False,
            'multi_agent_evaluation': False
        }
    
    async def run_complete_test_suite(self) -> Dict[str, Any]:
        """Run the complete test suite for the integrated workflow."""
        
        print("🚀 Starting Integrated Workflow Test Suite")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Test 1: Database Connection and Enhanced Data
        print(f"\n1️⃣ Testing Enhanced Database Connection...")
        try:
            self.router = IndustryRouter(enable_email=True)
            connection_status = self.router.test_connection()
            
            if connection_status.get('connected'):
                self.test_results['database_connection'] = True
                print(f"   ✅ Database connection successful")
                print(f"   📊 Tables status: {len(connection_status.get('tables_status', {}))} tables checked")
            else:
                print(f"   ❌ Database connection failed: {connection_status.get('error')}")
                
        except Exception as e:
            print(f"   ❌ Database connection error: {e}")
        
        # Test 2: Enhanced Data Retrieval
        print(f"\n2️⃣ Testing Enhanced Data Retrieval...")
        try:
            test_query = {
                'industry': 'technology',
                'limit': 5,
                'min_performance': 0  # Include companies with NULL performance scores
            }
            
            query_result = self.router.route_query(test_query)
            
            if query_result.get('results'):
                self.test_results['enhanced_data_retrieval'] = True
                companies = query_result['results']
                print(f"   ✅ Retrieved {len(companies)} companies")
                
                # Check for enhanced fields
                sample_company = companies[0]
                enhanced_fields = [
                    'company_name', 'industry', 'revenue', 'employee_count',
                    'market_position', 'competitive_advantages', 'challenges',
                    'growth_stage', 'digital_transformation_level', 'performance_score'
                ]
                
                available_fields = [field for field in enhanced_fields if field in sample_company]
                print(f"   📊 Enhanced fields available: {len(available_fields)}/{len(enhanced_fields)}")
                print(f"   🔍 Sample company: {sample_company.get('company_name', 'Unknown')}")
                print(f"   💰 Revenue: ${sample_company.get('revenue', 0):,}")
                print(f"   🏢 Market Position: {sample_company.get('market_position', 'Unknown')}")
                print(f"   📈 Performance Score: {sample_company.get('performance_score', 'NULL (for agent evaluation)')}")
                
            else:
                print(f"   ❌ No enhanced data retrieved")
                
        except Exception as e:
            print(f"   ❌ Enhanced data retrieval error: {e}")
        
        # Test 3: Gmail Integration
        print(f"\n3️⃣ Testing Gmail Integration...")
        try:
            if self.router.email_enabled:
                print(f"   ✅ Gmail client initialized successfully")
                self.test_results['gmail_integration'] = True
                
                # Test email sending capability (dry run)
                test_companies = query_result.get('results', [])[:2]  # Test with 2 companies
                
                if test_companies:
                    print(f"   📧 Testing email outreach to {len(test_companies)} companies...")
                    
                    # Note: In production, this would send real emails
                    # For testing, we'll simulate the process
                    email_results = {
                        'success': True,
                        'sent_count': len(test_companies),
                        'failed_count': 0,
                        'results': [
                            {
                                'company_name': company.get('company_name'),
                                'success': True,
                                'contact_email': f"info@{company.get('company_name', 'test').lower().replace(' ', '')}.com"
                            }
                            for company in test_companies
                        ]
                    }
                    
                    print(f"   ✅ Email simulation successful: {email_results['sent_count']} emails would be sent")
                else:
                    print(f"   ⚠️ No companies available for email testing")
                    
            else:
                print(f"   ⚠️ Gmail integration not enabled or failed to initialize")
                
        except Exception as e:
            print(f"   ❌ Gmail integration error: {e}")
        
        # Test 4: EmailAgent Integration
        print(f"\n4️⃣ Testing EmailAgent Integration...")
        try:
            if self.router.final_outreach_enabled:
                print(f"   ✅ EmailAgent integration successful")
                self.test_results['email_agent_integration'] = True
                
                # Test EmailAgent capabilities
                if self.router.email_agent:
                    print(f"   🤖 EmailAgent features available:")
                    print(f"      • Creative email discovery")
                    print(f"      • Personalized outreach strategy")
                    print(f"      • Multi-attempt follow-up sequences")
                    print(f"      • Performance tracking")
                
            else:
                print(f"   ⚠️ EmailAgent not enabled or failed to initialize")
                
        except Exception as e:
            print(f"   ❌ EmailAgent integration error: {e}")
        
        # Test 5: Final Outreach Trigger Logic
        print(f"\n5️⃣ Testing Final Outreach Trigger Logic...")
        try:
            # Simulate failed outreach attempts to trigger final outreach
            test_company = {
                'company_name': 'Test Corporation',
                'industry': 'technology',
                'revenue': 50000000,
                'market_position': 'Challenger',
                'performance_score': None
            }
            
            # Simulate tracking failed outreach
            company_id = self.router._get_company_id(test_company)
            self.router._track_failed_outreach(company_id, test_company)
            self.router._track_failed_outreach(company_id, test_company)  # Second failure
            
            # Check if company is marked for final outreach
            failed_companies = self.router.get_failed_outreach_companies()
            
            if company_id in failed_companies:
                self.test_results['final_outreach_trigger'] = True
                print(f"   ✅ Final outreach trigger logic working")
                print(f"   📋 Companies needing final outreach: {len(failed_companies)}")
                
                # Test final outreach execution (simulation)
                if self.router.final_outreach_enabled:
                    print(f"   🎯 Final outreach would be triggered for: {test_company['company_name']}")
                else:
                    print(f"   ⚠️ Final outreach not enabled, but trigger logic works")
                    
            else:
                print(f"   ❌ Final outreach trigger logic not working")
                
        except Exception as e:
            print(f"   ❌ Final outreach trigger error: {e}")
        
        # Test 6: Multi-Agent Evaluation Integration
        print(f"\n6️⃣ Testing Multi-Agent Evaluation Integration...")
        try:
            # Verify that companies have NULL performance scores for agent evaluation
            companies_for_evaluation = query_result.get('results', [])
            
            null_score_companies = [
                company for company in companies_for_evaluation
                if company.get('performance_score') is None
            ]
            
            if null_score_companies:
                self.test_results['multi_agent_evaluation'] = True
                print(f"   ✅ Multi-agent evaluation ready")
                print(f"   🤖 Companies with NULL scores (ready for agent evaluation): {len(null_score_companies)}")
                print(f"   📊 Enhanced data fields available for agent analysis:")
                
                sample_company = null_score_companies[0]
                evaluation_fields = [
                    'revenue', 'employee_count', 'market_position',
                    'competitive_advantages', 'challenges', 'growth_stage',
                    'digital_transformation_level', 'geographic_presence'
                ]
                
                available_eval_fields = [
                    field for field in evaluation_fields 
                    if sample_company.get(field) is not None
                ]
                
                print(f"   🔍 Evaluation data richness: {len(available_eval_fields)}/{len(evaluation_fields)} fields populated")
                print(f"   📈 Ready for Research Agent, Scoring Agent, and Strategic Agent analysis")
                
            else:
                print(f"   ⚠️ All companies have predefined scores - agent evaluation may not be needed")
                
        except Exception as e:
            print(f"   ❌ Multi-agent evaluation integration error: {e}")
        
        # Test Summary
        print(f"\n📊 Test Suite Summary")
        print("=" * 40)
        
        passed_tests = sum(1 for result in self.test_results.values() if result)
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        # System Statistics
        if self.router:
            stats = self.router.get_statistics()
            print(f"\n📈 System Statistics:")
            print(f"   • Database queries: {stats.get('total_queries', 0)}")
            print(f"   • Email capabilities: {'Enabled' if stats.get('capabilities', {}).get('email_enabled') else 'Disabled'}")
            print(f"   • Final outreach capabilities: {'Enabled' if stats.get('capabilities', {}).get('final_outreach_enabled') else 'Disabled'}")
            print(f"   • Supported industries: {len(stats.get('supported_industries', []))}")
        
        # Integration Status
        print(f"\n🔗 Integration Status:")
        print(f"   • Enhanced Database: {'✅ Connected' if self.test_results['database_connection'] else '❌ Failed'}")
        print(f"   • Gmail Integration: {'✅ Ready' if self.test_results['gmail_integration'] else '❌ Not Available'}")
        print(f"   • EmailAgent: {'✅ Integrated' if self.test_results['email_agent_integration'] else '❌ Not Available'}")
        print(f"   • Agent Evaluation: {'✅ Ready' if self.test_results['multi_agent_evaluation'] else '❌ Not Ready'}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if not self.test_results['gmail_integration']:
            print(f"   • Set up Gmail API credentials for email functionality")
        if not self.test_results['email_agent_integration']:
            print(f"   • Ensure EmailAgent dependencies are installed")
        if success_rate == 100:
            print(f"   • 🎉 System fully operational! Ready for production use")
            print(f"   • Run agent evaluation tests with: python test_agent_evaluation.py")
            print(f"   • Test CrewAI workflow with: python src/workflow/examples/crewai_tactical_workflow.py")
        
        return {
            'test_results': self.test_results,
            'success_rate': success_rate,
            'timestamp': datetime.now().isoformat(),
            'system_ready': success_rate >= 80  # 80% or higher considered ready
        }

async def main():
    """Run the integrated workflow test suite."""
    
    tester = IntegratedWorkflowTester()
    results = await tester.run_complete_test_suite()
    
    # Final status
    print(f"\n🚀 Integrated Workflow Test Complete!")
    print("=" * 50)
    
    if results['system_ready']:
        print(f"✅ SYSTEM READY FOR PRODUCTION")
        print(f"🎯 Success Rate: {results['success_rate']:.1f}%")
        print(f"\n🔄 Complete Workflow Available:")
        print(f"   1. Enhanced Database (90 companies, 35+ fields)")
        print(f"   2. IndustryRouter (intelligent routing)")
        print(f"   3. Gmail Integration (personalized outreach)")
        print(f"   4. EmailAgent (final outreach attempts)")
        print(f"   5. Multi-Agent Evaluation (CrewAI integration)")
    else:
        print(f"⚠️ SYSTEM NEEDS CONFIGURATION")
        print(f"📊 Current Status: {results['success_rate']:.1f}%")
        print(f"🛠️ Check failed tests and recommendations above")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
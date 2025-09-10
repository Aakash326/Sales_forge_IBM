#!/usr/bin/env python3
"""
Email Agent - Final Outreach Specialist

This agent handles final outreach attempts when other contact methods
have been unsuccessful. It focuses on creative email discovery,
personalized messaging, and persistent follow-up strategies.
"""

import os
import re
import time
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailAgent:
    """
    Email Agent for final outreach attempts
    
    Features:
    - Creative email discovery and validation
    - Personalized messaging based on company intelligence
    - Multi-attempt follow-up sequences
    - Success tracking and optimization
    - Integration with Gmail API for sending
    """
    
    def __init__(self, gmail_client=None):
        """Initialize Email Agent with optional Gmail client"""
        self.gmail_client = gmail_client
        self.outreach_attempts = {}
        self.success_metrics = {
            'emails_discovered': 0,
            'emails_sent': 0,
            'responses_received': 0,
            'meetings_scheduled': 0
        }
        
    async def final_outreach_attempt(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute final outreach attempt for a company
        
        Args:
            company_data: Comprehensive company information
            
        Returns:
            Dict with outreach results and next steps
        """
        
        print(f"📧 Email Agent: Final Outreach - {company_data.get('company_name')}")
        print("-" * 60)
        
        start_time = datetime.now()
        company_name = company_data.get('company_name', 'Unknown Company')
        
        try:
            # Step 1: Discover email addresses
            print("🔍 Step 1: Email Discovery & Validation")
            email_candidates = await self._discover_email_addresses(company_data)
            
            if not email_candidates:
                return {
                    'success': False,
                    'error': 'No email addresses could be discovered',
                    'company_name': company_name,
                    'attempts': 0
                }
            
            print(f"   ✅ Found {len(email_candidates)} potential email addresses")
            
            # Step 2: Create personalized outreach strategy
            print("🎯 Step 2: Personalized Outreach Strategy")
            outreach_strategy = await self._create_final_outreach_strategy(company_data)
            
            # Step 3: Execute email campaign
            print("📤 Step 3: Execute Final Email Campaign")
            campaign_results = await self._execute_final_email_campaign(
                company_data, email_candidates, outreach_strategy
            )
            
            # Step 4: Track and analyze results
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'success': campaign_results['emails_sent'] > 0,
                'company_name': company_name,
                'emails_discovered': len(email_candidates),
                'emails_sent': campaign_results['emails_sent'],
                'email_addresses': email_candidates,
                'outreach_strategy': outreach_strategy,
                'campaign_results': campaign_results,
                'processing_time': f"{processing_time:.2f}s",
                'timestamp': datetime.now().isoformat(),
                'next_steps': self._generate_next_steps(campaign_results)
            }
            
            # Update success metrics
            self.success_metrics['emails_discovered'] += len(email_candidates)
            self.success_metrics['emails_sent'] += campaign_results['emails_sent']
            
            print(f"✅ Final outreach completed in {processing_time:.1f}s")
            print(f"   • Emails discovered: {len(email_candidates)}")
            print(f"   • Emails sent: {campaign_results['emails_sent']}")
            print(f"   • Success rate: {(campaign_results['emails_sent']/len(email_candidates)*100):.1f}%")
            
            return result
            
        except Exception as e:
            logger.error(f"Email agent final outreach failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'company_name': company_name,
                'timestamp': datetime.now().isoformat()
            }
    
    async def _discover_email_addresses(self, company_data: Dict[str, Any]) -> List[str]:
        """
        Discover potential email addresses for the company
        
        Uses multiple strategies:
        1. Known contact emails from database
        2. Website domain-based generation
        3. Common business email patterns
        4. Leadership and department-specific emails
        """
        
        email_candidates = []
        company_name = company_data.get('company_name', '')
        website_url = company_data.get('website_url', '')
        
        # Strategy 1: Use known contact email
        if company_data.get('contact_email'):
            email_candidates.append(company_data['contact_email'])
        
        # Strategy 2: Extract domain from website
        domain = self._extract_domain_from_url(website_url)
        if not domain:
            domain = self._generate_domain_from_company_name(company_name)
        
        if domain:
            # Strategy 3: Generate common business email patterns
            business_emails = self._generate_business_email_patterns(domain)
            email_candidates.extend(business_emails)
            
            # Strategy 4: Generate leadership emails
            leadership_emails = self._generate_leadership_emails(company_data, domain)
            email_candidates.extend(leadership_emails)
            
            # Strategy 5: Generate department-specific emails
            department_emails = self._generate_department_emails(company_data, domain)
            email_candidates.extend(department_emails)
        
        # Remove duplicates and validate format
        unique_emails = list(set(email_candidates))
        valid_emails = [email for email in unique_emails if self._is_valid_email_format(email)]
        
        return valid_emails[:10]  # Limit to top 10 candidates
    
    def _extract_domain_from_url(self, website_url: str) -> Optional[str]:
        """Extract domain name from website URL"""
        if not website_url:
            return None
        
        # Remove protocol and www
        domain = website_url.replace('https://', '').replace('http://', '').replace('www.', '')
        
        # Extract base domain
        if '/' in domain:
            domain = domain.split('/')[0]
        
        return domain if '.' in domain else None
    
    def _generate_domain_from_company_name(self, company_name: str) -> Optional[str]:
        """Generate likely domain from company name"""
        if not company_name:
            return None
        
        # Clean company name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', company_name.lower())
        words = clean_name.split()
        
        if not words:
            return None
        
        # Common domain patterns
        patterns = [
            f"{words[0]}.com",
            f"{''.join(words[:2])}.com" if len(words) > 1 else f"{words[0]}.com",
            f"{words[0]}{words[1]}.com" if len(words) > 1 else f"{words[0]}.com"
        ]
        
        return patterns[0]  # Return most likely pattern
    
    def _generate_business_email_patterns(self, domain: str) -> List[str]:
        """Generate common business email patterns"""
        return [
            f"info@{domain}",
            f"contact@{domain}",
            f"hello@{domain}",
            f"sales@{domain}",
            f"business@{domain}",
            f"partnerships@{domain}",
            f"inquiries@{domain}"
        ]
    
    def _generate_leadership_emails(self, company_data: Dict[str, Any], domain: str) -> List[str]:
        """Generate leadership-specific email addresses"""
        emails = []
        
        # CEO email if known
        ceo_name = company_data.get('ceo_name', '')
        if ceo_name:
            ceo_emails = self._generate_person_emails(ceo_name, domain)
            emails.extend(ceo_emails)
        
        # Common executive emails
        executive_roles = ['ceo', 'cto', 'cfo', 'coo', 'president', 'founder']
        for role in executive_roles:
            emails.append(f"{role}@{domain}")
        
        return emails
    
    def _generate_department_emails(self, company_data: Dict[str, Any], domain: str) -> List[str]:
        """Generate department-specific emails based on company profile"""
        departments = ['marketing', 'business', 'partnerships', 'development']
        
        # Add industry-specific departments
        industry = company_data.get('industry', '').lower()
        if 'technology' in industry or 'software' in industry:
            departments.extend(['engineering', 'product', 'innovation'])
        elif 'finance' in industry:
            departments.extend(['investments', 'client', 'advisory'])
        elif 'healthcare' in industry:
            departments.extend(['medical', 'clinical', 'research'])
        
        return [f"{dept}@{domain}" for dept in departments[:5]]  # Limit to top 5
    
    def _generate_person_emails(self, person_name: str, domain: str) -> List[str]:
        """Generate email patterns for a specific person"""
        if not person_name:
            return []
        
        # Clean and split name
        clean_name = re.sub(r'[^a-zA-Z\s]', '', person_name.lower())
        parts = clean_name.split()
        
        if len(parts) < 2:
            return []
        
        first_name = parts[0]
        last_name = parts[-1]
        
        # Common personal email patterns
        patterns = [
            f"{first_name}.{last_name}@{domain}",
            f"{first_name[0]}{last_name}@{domain}",
            f"{first_name}@{domain}",
            f"{first_name}_{last_name}@{domain}"
        ]
        
        return patterns
    
    def _is_valid_email_format(self, email: str) -> bool:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    async def _create_final_outreach_strategy(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create personalized final outreach strategy
        """
        
        company_name = company_data.get('company_name', 'your company')
        industry = company_data.get('industry', 'technology')
        company_size = company_data.get('company_size', 'medium')
        
        # Analyze company for personalization
        pain_points = self._identify_final_outreach_pain_points(company_data)
        value_propositions = self._create_final_value_propositions(company_data)
        urgency_factors = self._identify_urgency_factors(company_data)
        
        strategy = {
            'approach_type': 'final_persistent',
            'personalization_level': 'high',
            'message_tone': 'professional_urgent',
            'sequence_length': 3,  # 3 email sequence
            'timing_strategy': 'accelerated',  # Faster follow-up
            'pain_points': pain_points,
            'value_propositions': value_propositions,
            'urgency_factors': urgency_factors,
            'subject_lines': self._generate_final_outreach_subjects(company_data),
            'email_templates': self._create_final_email_templates(company_data)
        }
        
        return strategy
    
    def _identify_final_outreach_pain_points(self, company_data: Dict[str, Any]) -> List[str]:
        """Identify pain points for final outreach messaging"""
        
        industry = company_data.get('industry', '').lower()
        challenges = company_data.get('challenges', '')
        growth_stage = company_data.get('growth_stage', '')
        
        pain_points = []
        
        # Industry-specific pain points
        if 'technology' in industry:
            pain_points.extend([
                'Scaling technical infrastructure',
                'Competitive market pressure',
                'Talent acquisition challenges'
            ])
        elif 'finance' in industry:
            pain_points.extend([
                'Regulatory compliance complexity',
                'Digital transformation urgency',
                'Market volatility management'
            ])
        elif 'healthcare' in industry:
            pain_points.extend([
                'Patient data security',
                'Operational efficiency',
                'Regulatory compliance'
            ])
        
        # Growth stage specific
        if growth_stage == 'Growth':
            pain_points.append('Rapid scaling challenges')
        elif growth_stage == 'Mature':
            pain_points.append('Market position defense')
        
        # Extract from known challenges
        if challenges:
            pain_points.append(challenges.split(',')[0].strip())
        
        return pain_points[:3]  # Top 3 most relevant
    
    def _create_final_value_propositions(self, company_data: Dict[str, Any]) -> List[str]:
        """Create compelling value propositions for final outreach"""
        
        company_size = company_data.get('employee_count', 0)
        revenue = company_data.get('revenue', 0)
        industry = company_data.get('industry', '').lower()
        
        value_props = [
            'Proven ROI within 90 days',
            'Risk-free implementation approach',
            'Industry-specific solution expertise'
        ]
        
        # Size-specific value props
        if company_size > 10000:
            value_props.append('Enterprise-scale deployment experience')
        elif company_size > 1000:
            value_props.append('Mid-market optimization specialists')
        else:
            value_props.append('Agile implementation for growing companies')
        
        # Revenue-specific
        if revenue > 1_000_000_000:  # > $1B
            value_props.append('Fortune 500 client success stories')
        
        return value_props[:4]  # Top 4 most relevant
    
    def _identify_urgency_factors(self, company_data: Dict[str, Any]) -> List[str]:
        """Identify urgency factors for final outreach"""
        
        urgency_factors = [
            'Limited-time opportunity',
            'Q4 budget availability',
            'Competitive advantage window'
        ]
        
        # Add industry-specific urgency
        industry = company_data.get('industry', '').lower()
        if 'technology' in industry:
            urgency_factors.append('Rapid market evolution')
        elif 'finance' in industry:
            urgency_factors.append('Regulatory deadline compliance')
        
        return urgency_factors[:3]
    
    def _generate_final_outreach_subjects(self, company_data: Dict[str, Any]) -> List[str]:
        """Generate compelling subject lines for final outreach"""
        
        company_name = company_data.get('company_name', 'your company')
        
        subjects = [
            f"Final opportunity for {company_name}",
            f"Time-sensitive: {company_name} strategic initiative",
            f"Last chance: Exclusive offer for {company_name}",
            f"{company_name}: Don't miss this opportunity",
            f"Urgent: Strategic partnership with {company_name}",
            f"Final outreach: {company_name} growth acceleration",
            f"Time running out: {company_name} competitive advantage"
        ]
        
        return subjects
    
    def _create_final_email_templates(self, company_data: Dict[str, Any]) -> List[str]:
        """Create email templates for final outreach sequence"""
        
        company_name = company_data.get('company_name', 'your company')
        ceo_name = company_data.get('ceo_name', 'leadership team')
        industry = company_data.get('industry', 'industry')
        
        templates = [
            # Email 1: Final opportunity
            f"""Hi there,

I've been trying to connect with {company_name} regarding a strategic opportunity that could significantly impact your {industry} operations.

This is my final outreach attempt, and I wanted to make sure you didn't miss this time-sensitive opportunity.

We've helped similar companies in your industry achieve:
• 40% improvement in operational efficiency
• 60% reduction in manual processes  
• 25% increase in revenue growth

I have just 2 spots remaining in our Q4 implementation schedule, specifically reserved for companies like {company_name}.

Would you be open to a brief 15-minute call this week to discuss how we can accelerate your growth initiatives?

Best regards,
Strategic Partnerships Team

P.S. This offer expires at the end of this week due to our limited capacity.""",

            # Email 2: Urgent follow-up
            f"""Hi {ceo_name.split()[0] if ' ' in ceo_name else 'there'},

I sent a message about a strategic opportunity for {company_name} but haven't heard back.

I understand you're extremely busy running a {industry} company, but this is genuinely time-sensitive.

We have ONE remaining implementation slot for Q4, and I'd hate for {company_name} to miss out on the competitive advantage this could provide.

Quick question: Are you currently satisfied with your operational efficiency, or would a 40% improvement in the next 90 days be valuable?

If yes, let's talk. If no, I'll stop reaching out.

Reply with "YES" for a 15-minute call or "NO" to be removed from my outreach.

Best,
Strategic Partnerships

P.S. Our current clients wish they had started sooner.""",

            # Email 3: Final farewell
            f"""Hi there,

This is my absolute final message regarding the strategic opportunity for {company_name}.

Since I haven't heard back, I'm assuming you're either:
1) Not interested (totally fine!)
2) Too busy (I get it!)
3) My emails aren't reaching you (happens!)

If it's #3 and you ARE interested in learning how companies like {company_name} are achieving 40% efficiency improvements in 90 days, please reply "INTERESTED" and I'll send you our exclusive case study.

Otherwise, I'll take the hint and won't reach out again.

Either way, I wish {company_name} continued success in {industry}.

Best regards,
Strategic Partnerships Team

P.S. If you change your mind in the future, you know where to find me."""
        ]
        
        return templates
    
    async def _execute_final_email_campaign(
        self, 
        company_data: Dict[str, Any], 
        email_candidates: List[str], 
        strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the final email campaign
        """
        
        if not self.gmail_client:
            print("   ⚠️  No Gmail client available - simulating email send")
            return {
                'emails_sent': len(email_candidates),
                'simulation_mode': True,
                'email_addresses': email_candidates,
                'strategy_applied': strategy['approach_type']
            }
        
        sent_count = 0
        failed_count = 0
        results = []
        
        # Get email content
        subject_lines = strategy['subject_lines']
        email_templates = strategy['email_templates']
        
        # Send to each email candidate
        for i, email_address in enumerate(email_candidates):
            try:
                # Use first email template and subject for initial send
                subject = subject_lines[0] if subject_lines else "Strategic Partnership Opportunity"
                body = email_templates[0] if email_templates else self._get_default_final_email(company_data)
                
                # Send email via Gmail client
                send_result = self.gmail_client.send_email(
                    to=email_address,
                    subject=subject,
                    body=body
                )
                
                if send_result.get('success'):
                    sent_count += 1
                    results.append({
                        'email': email_address,
                        'status': 'sent',
                        'message_id': send_result.get('message_id')
                    })
                    print(f"   ✅ Email sent to: {email_address}")
                else:
                    failed_count += 1
                    results.append({
                        'email': email_address,
                        'status': 'failed',
                        'error': send_result.get('error')
                    })
                    print(f"   ❌ Failed to send to: {email_address}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                failed_count += 1
                results.append({
                    'email': email_address,
                    'status': 'error',
                    'error': str(e)
                })
                print(f"   ❌ Error sending to {email_address}: {str(e)[:50]}")
        
        return {
            'emails_sent': sent_count,
            'emails_failed': failed_count,
            'total_attempts': len(email_candidates),
            'success_rate': (sent_count / len(email_candidates)) * 100 if email_candidates else 0,
            'results': results,
            'strategy_applied': strategy['approach_type']
        }
    
    def _get_default_final_email(self, company_data: Dict[str, Any]) -> str:
        """Get default final outreach email template"""
        
        company_name = company_data.get('company_name', 'your company')
        industry = company_data.get('industry', 'industry')
        
        return f"""Hi there,

I've been trying to reach {company_name} about a strategic opportunity that's specifically relevant to {industry} companies.

This is my final outreach attempt, and I wanted to ensure you didn't miss this time-sensitive opportunity.

We've recently helped similar companies achieve:
• 40% improvement in operational efficiency
• 60% reduction in manual processes
• 25% increase in revenue growth

I have limited availability remaining in Q4 for new implementations.

Would you be open to a brief 15-minute conversation about how we could help {company_name} achieve similar results?

Best regards,
Strategic Partnerships Team

P.S. If you're not the right person, could you please forward this to whoever handles strategic initiatives at {company_name}?"""
    
    def _generate_next_steps(self, campaign_results: Dict[str, Any]) -> List[str]:
        """Generate recommended next steps based on campaign results"""
        
        sent_count = campaign_results.get('emails_sent', 0)
        success_rate = campaign_results.get('success_rate', 0)
        
        next_steps = []
        
        if sent_count > 0:
            next_steps.append("Monitor email responses over next 3-5 days")
            next_steps.append("Prepare follow-up sequence for non-responders")
            
            if success_rate > 70:
                next_steps.append("High success rate - prioritize this company for follow-up")
            elif success_rate > 30:
                next_steps.append("Moderate success - continue with planned sequence")
            else:
                next_steps.append("Low delivery rate - investigate email validation tools")
            
            next_steps.append("Track opens and clicks if email tracking available")
            next_steps.append("Prepare LinkedIn outreach as backup channel")
        else:
            next_steps.append("Email delivery failed - try LinkedIn or phone outreach")
            next_steps.append("Research additional contact methods")
            next_steps.append("Consider company website contact form")
        
        next_steps.append("Schedule follow-up review in 1 week")
        
        return next_steps
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get email agent performance metrics"""
        
        total_attempts = self.success_metrics['emails_sent']
        
        return {
            'emails_discovered': self.success_metrics['emails_discovered'],
            'emails_sent': self.success_metrics['emails_sent'],
            'responses_received': self.success_metrics['responses_received'],
            'meetings_scheduled': self.success_metrics['meetings_scheduled'],
            'response_rate': (self.success_metrics['responses_received'] / total_attempts * 100) if total_attempts > 0 else 0,
            'meeting_conversion_rate': (self.success_metrics['meetings_scheduled'] / total_attempts * 100) if total_attempts > 0 else 0,
            'last_updated': datetime.now().isoformat()
        }


# Integration function for IndustryRouter
def add_final_email_outreach(router, gmail_client=None):
    """
    Add final email outreach capability to IndustryRouter
    
    Args:
        router: IndustryRouter instance
        gmail_client: Optional Gmail client for sending emails
    """
    
    # Create email agent
    email_agent = EmailAgent(gmail_client=gmail_client or router.gmail_client)
    
    # Add method to router
    async def final_email_outreach(company_data):
        """Execute final email outreach for a company"""
        return await email_agent.final_outreach_attempt(company_data)
    
    # Attach to router
    router.final_email_outreach = final_email_outreach
    router.email_agent = email_agent
    
    print("✅ Email Agent integrated with IndustryRouter")
    print("   • Final outreach capability added")
    print("   • Creative email discovery enabled")
    print("   • Persistent follow-up sequences ready")
    
    return router


# Factory function
def create_email_agent(gmail_client=None) -> EmailAgent:
    """
    Factory function to create Email Agent
    
    Args:
        gmail_client: Optional Gmail client for sending emails
        
    Returns:
        EmailAgent: Configured Email Agent instance
    """
    return EmailAgent(gmail_client=gmail_client)


if __name__ == "__main__":
    # Demo usage
    import asyncio
    
    async def demo_email_agent():
        """Demonstrate Email Agent functionality"""
        
        print("🤖 Email Agent Demo")
        print("=" * 50)
        
        # Sample company data
        sample_company = {
            'company_name': 'TechFlow Dynamics',
            'industry': 'Technology',
            'website_url': 'https://www.techflow.com',
            'employee_count': 250,
            'revenue': 50000000,
            'ceo_name': 'Sarah Chen',
            'growth_stage': 'Growth',
            'challenges': 'Scaling technical infrastructure, Talent acquisition'
        }
        
        # Create email agent
        email_agent = EmailAgent()
        
        # Execute final outreach
        result = await email_agent.final_outreach_attempt(sample_company)
        
        print("\n📊 Demo Results:")
        print(f"Success: {result.get('success')}")
        print(f"Emails Discovered: {result.get('emails_discovered', 0)}")
        print(f"Campaign Strategy: {result.get('outreach_strategy', {}).get('approach_type', 'N/A')}")
        
        return result
    
    # Run demo
    asyncio.run(demo_email_agent())
#!/usr/bin/env python3
"""
IndustryRouter - Supabase Integration Module

This module provides intelligent industry detection and routing to appropriate
Supabase database tables for company data retrieval.

Classes:
    IndustryRouter: Main class for industry detection and database routing

Dependencies:
    - supabase: Python client for Supabase
    - python-dotenv: Environment variable management
    - re: Regular expression operations
    - typing: Type hints

Author: AI Assistant
Date: 2025-01-09
"""

import os
import re
import time
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dotenv import load_dotenv

try:
    from supabase import create_client, Client
except ImportError:
    raise ImportError(
        "supabase library not found. Install with: pip install supabase"
    )

try:
    from src.integrations.gmail_client import GmailClient
except ImportError:
    try:
        from ..integrations.gmail_client import GmailClient
    except ImportError:
        print("⚠️ GmailClient not available. Email functionality disabled.")
        GmailClient = None

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndustryRouter:
    """
    IndustryRouter detects company industry and routes queries to appropriate Supabase tables.
    
    This class provides intelligent routing based on company industry detection,
    connecting to Supabase database tables for finance, healthcare, and technology companies.
    
    Attributes:
        supabase_client (Client): Supabase client instance
        industry_mappings (Dict): Mapping of industry keywords to database tables
        supported_industries (List): List of supported industry categories
    """
    
    def __init__(self, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None, enable_email: bool = True):
        """
        Initialize IndustryRouter with Supabase connection and optional email capabilities.
        
        Args:
            supabase_url (Optional[str]): Supabase project URL (defaults to env var)
            supabase_key (Optional[str]): Supabase anon key (defaults to env var)
            enable_email (bool): Whether to enable Gmail integration for sending emails
            
        Raises:
            ValueError: If Supabase credentials are not provided
            ConnectionError: If unable to connect to Supabase
        """
        
        # Get Supabase credentials
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_ANON_KEY "
                "environment variables or pass them as parameters."
            )
        
        # Initialize Supabase client
        try:
            self.supabase_client: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info("Successfully connected to Supabase")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {str(e)}")
            raise ConnectionError(f"Unable to connect to Supabase: {str(e)}")
        
        # Industry mapping configuration
        self.industry_mappings = {
            'finance': {
                'table': 'finance_companies',
                'keywords': [
                    'finance', 'financial', 'bank', 'banking', 'investment', 'capital',
                    'credit', 'loan', 'mortgage', 'insurance', 'fintech', 'trading',
                    'securities', 'asset', 'wealth', 'fund', 'payment', 'paypal',
                    'visa', 'mastercard', 'american express', 'goldman sachs', 'jpmorgan',
                    'wells fargo', 'citigroup', 'morgan stanley', 'charles schwab'
                ]
            },
            'healthcare': {
                'table': 'healthcare_companies', 
                'keywords': [
                    'healthcare', 'health', 'medical', 'medicine', 'hospital', 'clinic',
                    'pharmaceutical', 'pharma', 'biotech', 'biotechnology', 'drug',
                    'therapy', 'treatment', 'diagnostic', 'device', 'medtech',
                    'johnson', 'pfizer', 'merck', 'abbott', 'novartis', 'roche',
                    'glaxosmithkline', 'bristol myers', 'astrazeneca', 'unitedhealth'
                ]
            },
            'technology': {
                'table': 'tech_companies',
                'keywords': [
                    'technology', 'tech', 'software', 'hardware', 'computer', 'internet',
                    'cloud', 'ai', 'artificial intelligence', 'machine learning', 'data',
                    'analytics', 'saas', 'platform', 'mobile', 'app', 'digital',
                    'cybersecurity', 'semiconductor', 'apple', 'microsoft', 'google',
                    'amazon', 'meta', 'tesla', 'nvidia', 'intel', 'ibm', 'oracle'
                ]
            }
        }
        
        self.supported_industries = list(self.industry_mappings.keys())
        
        # Initialize Gmail client if enabled
        self.gmail_client = None
        self.email_enabled = False
        
        if enable_email and GmailClient:
            try:
                credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'client_secret.json')
                token_path = os.getenv('GMAIL_TOKEN_PATH', 'gmail_token.json')
                
                self.gmail_client = GmailClient(
                    credentials_path=credentials_path,
                    token_path=token_path
                )
                self.email_enabled = True
                logger.info("Gmail client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Gmail client: {e}. Email functionality disabled.")
                self.gmail_client = None
                self.email_enabled = False
        
        # Performance tracking
        self._query_stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'average_response_time': 0.0,
            'emails_sent': 0,
            'email_failures': 0
        }
    
    def route_query(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to handle industry detection and data routing.
        
        Args:
            input_data (Dict[str, Any]): Input data containing company/query information
                Expected keys:
                - 'company_name' (optional): Name of the company
                - 'industry' (optional): Industry category
                - 'query' (optional): Search query string
                - 'location' (optional): Location filter
                - 'min_performance' (optional): Minimum performance score filter
                - 'limit' (optional): Maximum number of results
        
        Returns:
            Dict[str, Any]: Response containing:
                - 'industry': Detected industry
                - 'database_table': Target database table
                - 'results': Query results from database
                - 'processing_time': Time taken to process the request
                - 'query_metadata': Additional query information
        
        Example:
            >>> router = IndustryRouter()
            >>> input_data = {
            ...     "company_name": "FinTech Corp",
            ...     "industry": "Finance", 
            ...     "query": "What are the top-performing finance companies in NY?"
            ... }
            >>> result = router.route_query(input_data)
        """
        
        start_time = time.time()
        self._query_stats['total_queries'] += 1
        
        try:
            # Validate input data
            if not isinstance(input_data, dict):
                raise ValueError("input_data must be a dictionary")
            
            # Detect industry
            detected_industry = self.detect_industry(input_data)
            
            if not detected_industry:
                logger.warning("Unable to detect industry from input data")
                return {
                    'industry': 'unknown',
                    'database_table': None,
                    'results': [],
                    'processing_time': f"{time.time() - start_time:.3f}s",
                    'error': 'Unable to detect industry',
                    'query_metadata': {
                        'input_keys': list(input_data.keys()),
                        'supported_industries': self.supported_industries
                    }
                }
            
            # Get database table
            database_table = self.get_database_table(detected_industry)
            
            # Build query parameters
            query_params = self._build_query_params(input_data)
            
            # Fetch data from appropriate table
            results = self.fetch_data_from_table(database_table, query_params)
            
            processing_time = time.time() - start_time
            self._query_stats['successful_queries'] += 1
            self._update_average_response_time(processing_time)
            
            response = {
                'industry': detected_industry,
                'database_table': database_table,
                'results': results,
                'processing_time': f"{processing_time:.3f}s",
                'query_metadata': {
                    'total_results': len(results),
                    'query_params': query_params,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            logger.info(f"Successfully routed query: {detected_industry} -> {database_table} ({len(results)} results)")
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._query_stats['failed_queries'] += 1
            
            logger.error(f"Error in route_query: {str(e)}")
            return {
                'industry': 'error',
                'database_table': None,
                'results': [],
                'processing_time': f"{processing_time:.3f}s",
                'error': str(e),
                'query_metadata': {
                    'error_type': type(e).__name__,
                    'timestamp': datetime.now().isoformat()
                }
            }
    
    def detect_industry(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Detects the industry from input data using keyword matching and heuristics.
        
        Args:
            input_data (Dict[str, Any]): Input data to analyze
        
        Returns:
            Optional[str]: Detected industry name or None if no match found
        
        Algorithm:
            1. Check explicit industry field
            2. Analyze company name for industry keywords
            3. Parse query text for industry indicators
            4. Use weighted scoring for best match
        """
        
        # Priority 1: Explicit industry field
        explicit_industry = input_data.get('industry', '').lower().strip()
        if explicit_industry:
            # Direct mapping check
            for industry, config in self.industry_mappings.items():
                if explicit_industry in config['keywords'] or explicit_industry == industry:
                    logger.debug(f"Industry detected via explicit field: {industry}")
                    return industry
        
        # Priority 2: Combine all text for analysis
        text_to_analyze = []
        
        if input_data.get('company_name'):
            text_to_analyze.append(input_data['company_name'].lower())
        
        if input_data.get('query'):
            text_to_analyze.append(input_data['query'].lower())
        
        if explicit_industry:
            text_to_analyze.append(explicit_industry)
        
        combined_text = ' '.join(text_to_analyze)
        
        if not combined_text.strip():
            logger.warning("No text available for industry detection")
            return None
        
        # Priority 3: Keyword matching with scoring
        industry_scores = {}
        
        for industry, config in self.industry_mappings.items():
            score = 0
            keywords_found = []
            
            for keyword in config['keywords']:
                # Exact match gets higher score
                if keyword in combined_text:
                    if keyword == combined_text.strip():
                        score += 10  # Exact match
                    else:
                        score += 5   # Partial match
                    keywords_found.append(keyword)
                
                # Fuzzy matching for company names
                elif input_data.get('company_name'):
                    company_name = input_data['company_name'].lower()
                    if self._fuzzy_match(keyword, company_name):
                        score += 8
                        keywords_found.append(f"{keyword} (fuzzy)")
            
            if score > 0:
                industry_scores[industry] = {
                    'score': score,
                    'keywords': keywords_found
                }
        
        # Return industry with highest score
        if industry_scores:
            best_industry = max(industry_scores.keys(), key=lambda x: industry_scores[x]['score'])
            logger.debug(f"Industry detected via keyword matching: {best_industry} "
                        f"(score: {industry_scores[best_industry]['score']}, "
                        f"keywords: {industry_scores[best_industry]['keywords']})")
            return best_industry
        
        # Priority 4: Pattern-based detection
        pattern_industry = self._detect_by_patterns(combined_text)
        if pattern_industry:
            logger.debug(f"Industry detected via pattern matching: {pattern_industry}")
            return pattern_industry
        
        logger.debug("No industry detected")
        return None
    
    def get_database_table(self, industry: str) -> str:
        """
        Returns the correct Supabase table name for the given industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            str: Database table name
            
        Raises:
            ValueError: If industry is not supported
        """
        
        if industry not in self.industry_mappings:
            raise ValueError(f"Unsupported industry: {industry}. "
                           f"Supported industries: {self.supported_industries}")
        
        return self.industry_mappings[industry]['table']
    
    def fetch_data_from_table(self, table: str, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetches data from the specified Supabase table with query parameters.
        
        Args:
            table (str): Database table name
            query_params (Dict[str, Any]): Query parameters for filtering and sorting
        
        Returns:
            List[Dict[str, Any]]: Query results
            
        Raises:
            Exception: If database query fails
        """
        
        try:
            # Start with base query
            query = self.supabase_client.table(table).select("*")
            
            # Apply filters
            if query_params.get('location'):
                location_filter = query_params['location']
                query = query.ilike('location', f'%{location_filter}%')
            
            if query_params.get('company_name'):
                company_filter = query_params['company_name']
                query = query.ilike('company_name', f'%{company_filter}%')
            
            if query_params.get('min_performance'):
                min_perf = query_params['min_performance']
                query = query.gte('performance_score', min_perf)
            
            if query_params.get('max_performance'):
                max_perf = query_params['max_performance']
                query = query.lte('performance_score', max_perf)
            
            # Apply sorting
            sort_by = query_params.get('sort_by', 'performance_score')
            sort_order = query_params.get('sort_order', 'desc')
            
            if sort_order.lower() == 'desc':
                query = query.order(sort_by, desc=True)
            else:
                query = query.order(sort_by)
            
            # Apply limit
            limit = min(query_params.get('limit', 50), 100)  # Max 100 results
            query = query.limit(limit)
            
            # Execute query
            response = query.execute()
            
            if response.data:
                logger.info(f"Successfully fetched {len(response.data)} records from {table}")
                return response.data
            else:
                logger.warning(f"No data found in {table} with given parameters")
                return []
                
        except Exception as e:
            logger.error(f"Database query failed for table {table}: {str(e)}")
            raise Exception(f"Database query failed: {str(e)}")
    
    def _build_query_params(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Builds query parameters from input data.
        
        Args:
            input_data (Dict[str, Any]): Input data
            
        Returns:
            Dict[str, Any]: Query parameters
        """
        
        query_params = {}
        
        # Location filter
        if input_data.get('location'):
            query_params['location'] = input_data['location']
        
        # Company name filter  
        if input_data.get('company_name'):
            query_params['company_name'] = input_data['company_name']
        
        # Performance score filters
        if input_data.get('min_performance'):
            query_params['min_performance'] = int(input_data['min_performance'])
        
        if input_data.get('max_performance'):
            query_params['max_performance'] = int(input_data['max_performance'])
        
        # Sorting options
        if input_data.get('sort_by'):
            query_params['sort_by'] = input_data['sort_by']
        
        if input_data.get('sort_order'):
            query_params['sort_order'] = input_data['sort_order']
        
        # Result limit
        if input_data.get('limit'):
            query_params['limit'] = int(input_data['limit'])
        
        return query_params
    
    def _fuzzy_match(self, keyword: str, text: str, threshold: float = 0.8) -> bool:
        """
        Performs fuzzy string matching.
        
        Args:
            keyword (str): Keyword to match
            text (str): Text to search in
            threshold (float): Similarity threshold (0.0-1.0)
            
        Returns:
            bool: True if fuzzy match found
        """
        
        # Simple fuzzy matching using substring and edit distance concepts
        if keyword in text:
            return True
        
        # Check for partial matches
        words = text.split()
        for word in words:
            if len(word) > 3 and (keyword.startswith(word[:3]) or word.startswith(keyword[:3])):
                return True
        
        return False
    
    def _detect_by_patterns(self, text: str) -> Optional[str]:
        """
        Detects industry using regex patterns.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Optional[str]: Detected industry or None
        """
        
        patterns = {
            'finance': [
                r'\b(bank|banking|financial|investment|capital|fund|trading|securities)\b',
                r'\b(loan|mortgage|credit|insurance|fintech|payment)\b'
            ],
            'healthcare': [
                r'\b(medical|healthcare|hospital|clinic|pharmaceutical|biotech)\b',
                r'\b(drug|therapy|treatment|diagnostic|medtech|pharma)\b'
            ],
            'technology': [
                r'\b(tech|technology|software|hardware|computer|internet|cloud|ai)\b',
                r'\b(saas|platform|mobile|app|digital|cybersecurity|semiconductor)\b'
            ]
        }
        
        for industry, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text, re.IGNORECASE):
                    return industry
        
        return None
    
    def _update_average_response_time(self, response_time: float) -> None:
        """Updates the average response time statistic."""
        current_avg = self._query_stats['average_response_time']
        total_successful = self._query_stats['successful_queries']
        
        if total_successful == 1:
            self._query_stats['average_response_time'] = response_time
        else:
            self._query_stats['average_response_time'] = (
                (current_avg * (total_successful - 1) + response_time) / total_successful
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Returns performance and usage statistics.
        
        Returns:
            Dict[str, Any]: Statistics dictionary
        """
        
        return {
            'total_queries': self._query_stats['total_queries'],
            'successful_queries': self._query_stats['successful_queries'],
            'failed_queries': self._query_stats['failed_queries'],
            'success_rate': (
                self._query_stats['successful_queries'] / max(self._query_stats['total_queries'], 1) * 100
            ),
            'average_response_time_seconds': round(self._query_stats['average_response_time'], 3),
            'supported_industries': self.supported_industries,
            'table_mappings': {industry: config['table'] for industry, config in self.industry_mappings.items()}
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Tests the Supabase connection and returns status.
        
        Returns:
            Dict[str, Any]: Connection status and information
        """
        
        try:
            # Test connection by querying a small amount of data from each table
            connection_status = {
                'connected': True,
                'supabase_url': self.supabase_url,
                'timestamp': datetime.now().isoformat(),
                'tables_status': {}
            }
            
            for industry, config in self.industry_mappings.items():
                table = config['table']
                try:
                    response = self.supabase_client.table(table).select("id").limit(1).execute()
                    connection_status['tables_status'][table] = {
                        'accessible': True,
                        'sample_count': len(response.data) if response.data else 0
                    }
                except Exception as e:
                    connection_status['tables_status'][table] = {
                        'accessible': False,
                        'error': str(e)
                    }
            
            return connection_status
            
        except Exception as e:
            return {
                'connected': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def send_outreach_emails(self, companies: List[Dict[str, Any]], outreach_content: Optional[Dict[str, Any]] = None, template_type: str = "initial_outreach") -> Dict[str, Any]:
        """
        Send personalized outreach emails to a list of companies.
        
        Args:
            companies (List[Dict]): List of company data from database queries
            outreach_content (Optional[Dict]): Custom outreach content for personalization
            template_type (str): Type of email template to use
            
        Returns:
            Dict[str, Any]: Email sending results and statistics
        """
        
        if not self.email_enabled:
            return {
                "success": False,
                "error": "Email functionality not available. Gmail client not initialized.",
                "sent_count": 0,
                "failed_count": 0,
                "results": []
            }
        
        if not companies:
            return {
                "success": False, 
                "error": "No companies provided for outreach",
                "sent_count": 0,
                "failed_count": 0,
                "results": []
            }
        
        results = []
        sent_count = 0
        failed_count = 0
        
        logger.info(f"Starting email outreach to {len(companies)} companies")
        
        for company in companies:
            try:
                # Generate contact email if not provided
                contact_email = self._generate_contact_email(company)
                
                if not contact_email:
                    result = {
                        "company_name": company.get('company_name', 'Unknown'),
                        "success": False,
                        "error": "No contact email available",
                        "email": None
                    }
                    results.append(result)
                    failed_count += 1
                    continue
                
                # Prepare lead data for email generation
                lead_data = {
                    "contact_email": contact_email,
                    "company_name": company.get('company_name', 'Unknown Company'),
                    "contact_name": self._extract_contact_name(company),
                    "industry": company.get('industry', 'Unknown'),
                    "location": company.get('location', 'Unknown'),
                    "performance_score": company.get('performance_score'),
                    "pain_points": self._identify_pain_points(company)
                }
                
                # Use custom outreach content or generate default
                email_content = outreach_content or self._generate_default_outreach_content(lead_data)
                
                # Send email
                if self.gmail_client:
                    send_result = self.gmail_client.send_sales_outreach_email(
                        lead_data=lead_data,
                        outreach_content=email_content,
                        template_type=template_type
                    )
                else:
                    send_result = {
                        "success": False,
                        "error": "Gmail client not initialized"
                    }
                
                if send_result.get('success'):
                    sent_count += 1
                    self._query_stats['emails_sent'] += 1
                    logger.info(f"Email sent successfully to {lead_data['company_name']}")
                else:
                    failed_count += 1
                    self._query_stats['email_failures'] += 1
                    logger.error(f"Failed to send email to {lead_data['company_name']}: {send_result.get('error')}")
                
                # Add company info to result
                send_result.update({
                    "company_name": lead_data['company_name'],
                    "contact_email": contact_email,
                    "industry": lead_data['industry']
                })
                
                results.append(send_result)
                
                # Add small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                error_result = {
                    "company_name": company.get('company_name', 'Unknown'),
                    "success": False,
                    "error": f"Unexpected error: {str(e)}",
                    "contact_email": contact_email if 'contact_email' in locals() else None
                }
                results.append(error_result)
                failed_count += 1
                self._query_stats['email_failures'] += 1
                logger.error(f"Unexpected error sending email to {company.get('company_name')}: {e}")
        
        success_rate = (sent_count / len(companies)) * 100 if companies else 0
        
        logger.info(f"Email outreach completed: {sent_count} sent, {failed_count} failed ({success_rate:.1f}% success rate)")
        
        return {
            "success": sent_count > 0,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "total_companies": len(companies),
            "success_rate": success_rate,
            "results": results,
            "template_type": template_type,
            "timestamp": datetime.now().isoformat()
        }

    def route_and_email(self, input_data: Dict[str, Any], outreach_content: Optional[Dict[str, Any]] = None, template_type: str = "initial_outreach") -> Dict[str, Any]:
        """
        Combined method to route query to get companies and send outreach emails.
        
        Args:
            input_data (Dict): Input data for company query
            outreach_content (Optional[Dict]): Custom outreach content
            template_type (str): Type of email template
            
        Returns:
            Dict[str, Any]: Combined results with query results and email sending status
        """
        
        # First, get companies using normal routing
        query_result = self.route_query(input_data)
        
        if query_result.get('industry') == 'error' or not query_result.get('results'):
            return {
                **query_result,
                "email_results": {
                    "success": False,
                    "error": "No companies found to send emails to",
                    "sent_count": 0,
                    "failed_count": 0
                }
            }
        
        # Then send emails to found companies
        email_results = self.send_outreach_emails(
            companies=query_result['results'],
            outreach_content=outreach_content,
            template_type=template_type
        )
        
        # Combine results
        return {
            **query_result,
            "email_results": email_results,
            "total_workflow_time": f"{float(query_result['processing_time'][:-1]) + 2:.3f}s"  # Estimate email time
        }

    def _generate_contact_email(self, company: Dict[str, Any]) -> Optional[str]:
        """Generate or extract contact email for a company."""
        
        # If email is directly provided
        if company.get('contact_email'):
            return company['contact_email']
        
        # If email field exists in database
        if company.get('email'):
            return company['email']
        
        # Generate generic email based on company name
        company_name = company.get('company_name', '').lower()
        
        if not company_name:
            return None
        
        # Clean company name for email generation
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', company_name)
        words = clean_name.split()
        
        if not words:
            return None
        
        # Generate email patterns
        domain_name = words[0] if len(words) == 1 else ''.join(words[:2])
        
        # Common email patterns for business outreach
        email_patterns = [
            f"info@{domain_name}.com",
            f"hello@{domain_name}.com", 
            f"contact@{domain_name}.com",
            f"sales@{domain_name}.com"
        ]
        
        # Return first pattern (could be enhanced to validate emails)
        logger.debug(f"Generated email for {company.get('company_name')}: {email_patterns[0]}")
        return email_patterns[0]

    def _extract_contact_name(self, company: Dict[str, Any]) -> str:
        """Extract or generate contact name from company data."""
        
        if company.get('contact_name'):
            return company['contact_name']
        
        if company.get('contact_person'):
            return company['contact_person']
        
        # Generate generic contact name based on company
        company_name = company.get('company_name', 'Team')
        
        # Extract first word as potential contact
        words = company_name.split()
        if words:
            return f"{words[0]} Team"
        
        return "Team"

    def _identify_pain_points(self, company: Dict[str, Any]) -> List[str]:
        """Identify potential pain points based on company data and industry."""
        
        pain_points = []
        industry = company.get('industry', '').lower()
        performance_score = company.get('performance_score', 0)
        
        # Industry-specific pain points
        if 'finance' in industry:
            pain_points.extend([
                "Regulatory compliance complexity",
                "Digital transformation challenges",
                "Risk management optimization"
            ])
        elif 'healthcare' in industry:
            pain_points.extend([
                "Patient data management",
                "Regulatory compliance",
                "Operational efficiency"
            ])
        elif 'technology' in industry:
            pain_points.extend([
                "Scalability challenges",
                "Security concerns", 
                "Market competition"
            ])
        
        # Performance-based pain points
        if performance_score < 70:
            pain_points.extend([
                "Performance optimization needs",
                "Competitive positioning"
            ])
        
        return pain_points[:3]  # Limit to top 3

    def _generate_default_outreach_content(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate default outreach content for personalized emails."""
        
        company_name = lead_data.get('company_name', 'your company')
        industry = lead_data.get('industry', 'industry')
        
        return {
            "email_subject": f"Strategic Growth Opportunity for {company_name}",
            "personalized_email": f"""Hi there,

I hope this email finds you well. I've been researching {company_name} and I'm impressed by your work in the {industry} sector.

I noticed you might be facing some common challenges that we've helped similar companies overcome:
• Optimizing operational efficiency
• Streamlining business processes  
• Accelerating growth initiatives

We've recently helped companies like yours achieve:
✓ 40% improvement in operational efficiency
✓ 60% reduction in manual processes
✓ 25% increase in revenue growth

Would you be open to a brief 15-minute conversation about how we could help {company_name} achieve similar results?

I'm available for a call this week at your convenience.

Best regards,
Sales Team

P.S. I'd be happy to share a case study of how we helped a similar company in your industry.""",
            "value_proposition": "Operational efficiency and growth acceleration",
            "call_to_action": "Schedule a 15-minute strategic consultation"
        }


# Utility functions for easy usage
def create_industry_router(supabase_url: Optional[str] = None, 
                          supabase_key: Optional[str] = None) -> IndustryRouter:
    """
    Factory function to create an IndustryRouter instance.
    
    Args:
        supabase_url (Optional[str]): Supabase project URL
        supabase_key (Optional[str]): Supabase anon key
        
    Returns:
        IndustryRouter: Configured IndustryRouter instance
    """
    return IndustryRouter(supabase_url, supabase_key)


def quick_query(input_data: Dict[str, Any], 
               supabase_url: Optional[str] = None,
               supabase_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick utility function for one-off queries.
    
    Args:
        input_data (Dict[str, Any]): Query input data
        supabase_url (Optional[str]): Supabase project URL  
        supabase_key (Optional[str]): Supabase anon key
        
    Returns:
        Dict[str, Any]: Query results
    """
    router = IndustryRouter(supabase_url, supabase_key)
    return router.route_query(input_data)
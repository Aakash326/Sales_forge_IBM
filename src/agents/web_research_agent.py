#!/usr/bin/env python3
"""
Tavily Web Research Agent

This agent uses Tavily API to conduct real-time web research on companies,
providing fresh insights for AI-driven sales intelligence and outreach.

Features:
- Real-time company research
- News and recent developments
- Financial and market insights
- Competitive landscape analysis
- Technology and innovation updates

Author: AI Assistant
Date: 2025-01-09
"""

import os
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebResearchAgent:
    """
    Web Research Agent using Tavily API for real-time company intelligence.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Web Research Agent with Tavily API.
        
        Args:
            api_key (Optional[str]): Tavily API key (defaults to env var)
        """
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        self.tavily_available = bool(self.api_key and self.api_key != 'your_tavily_api_key_here')
        
        if self.tavily_available:
            try:
                from tavily import TavilyClient
                self.client = TavilyClient(api_key=self.api_key)
                logger.info("✅ Tavily Web Research Agent initialized successfully")
            except ImportError:
                self.tavily_available = False
                self.client = None
                logger.warning("⚠️ Tavily library not installed. Run: pip install tavily-python")
            except Exception as e:
                self.tavily_available = False
                self.client = None
                logger.warning(f"⚠️ Tavily initialization failed: {e}")
        else:
            self.client = None
            logger.warning("⚠️ Tavily API key not configured. Web research will use fallback mode.")
        
        # Research cache for rate limiting
        self._research_cache = {}
        self._last_request_time = {}
    
    async def research_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct comprehensive web research on a company.
        
        Args:
            company_data (Dict[str, Any]): Company information from database
            
        Returns:
            Dict[str, Any]: Web research results with recent insights
        """
        company_name = company_data.get('company_name', 'Unknown Company')
        
        logger.info(f"🔍 Starting web research for {company_name}")
        
        if not self.tavily_available:
            return self._fallback_research(company_data)
        
        # Check cache first
        cache_key = f"{company_name}_{datetime.now().date()}"
        if cache_key in self._research_cache:
            logger.info(f"📋 Using cached research for {company_name}")
            return self._research_cache[cache_key]
        
        # Rate limiting
        self._apply_rate_limit(company_name)
        
        try:
            # Multi-query research strategy
            research_queries = self._generate_research_queries(company_data)
            
            research_results = {
                'company_name': company_name,
                'research_timestamp': datetime.now().isoformat(),
                'recent_news': [],
                'financial_insights': {},
                'market_position': {},
                'technology_updates': [],
                'competitive_landscape': {},
                'strategic_initiatives': [],
                'challenges_opportunities': {},
                'leadership_changes': [],
                'web_research_confidence': 0.0,
                'sources_count': 0
            }
            
            all_sources = []
            
            # Execute research queries
            for query_type, query in research_queries.items():
                try:
                    logger.info(f"🔍 Researching: {query_type}")
                    
                    search_results = self.client.search(
                        query=query,
                        search_depth="advanced",
                        max_results=5,
                        include_domains=["bloomberg.com", "reuters.com", "wsj.com", "ft.com", "forbes.com", "cnbc.com", "techcrunch.com", "businesswire.com"],
                        exclude_domains=["wikipedia.org", "investopedia.com"]
                    )
                    
                    if search_results and 'results' in search_results:
                        results = search_results['results']
                        all_sources.extend(results)
                        
                        # Process results by query type
                        self._process_query_results(query_type, results, research_results)
                        
                        time.sleep(0.5)  # Small delay between queries
                        
                except Exception as e:
                    logger.warning(f"⚠️ Query '{query_type}' failed: {e}")
                    continue
            
            # Calculate confidence score
            research_results['sources_count'] = len(all_sources)
            research_results['web_research_confidence'] = min(len(all_sources) / 10.0, 1.0)
            
            # Cache results
            self._research_cache[cache_key] = research_results
            
            logger.info(f"✅ Web research completed for {company_name}: {len(all_sources)} sources, {research_results['web_research_confidence']:.1%} confidence")
            
            return research_results
            
        except Exception as e:
            logger.error(f"❌ Web research failed for {company_name}: {e}")
            return self._fallback_research(company_data)
    
    def _generate_research_queries(self, company_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate targeted research queries based on company data."""
        company_name = company_data.get('company_name', '')
        industry = company_data.get('industry', '')
        
        # Get recent date for news queries
        recent_date = (datetime.now() - timedelta(days=90)).strftime('%Y')
        
        queries = {
            'recent_news': f'"{company_name}" news {recent_date} earnings financial results',
            'financial_performance': f'"{company_name}" revenue growth financial performance {recent_date}',
            'market_position': f'"{company_name}" market share competitive position {industry}',
            'technology_innovation': f'"{company_name}" technology innovation digital transformation AI',
            'strategic_initiatives': f'"{company_name}" acquisitions partnerships strategy {recent_date}',
            'leadership': f'"{company_name}" CEO leadership changes executive team {recent_date}',
            'challenges': f'"{company_name}" challenges risks regulatory issues {recent_date}'
        }
        
        return queries
    
    def _process_query_results(self, query_type: str, results: List[Dict], research_results: Dict[str, Any]) -> None:
        """Process search results by query type."""
        
        for result in results[:3]:  # Top 3 results per query
            title = result.get('title', '')
            content = result.get('content', '')
            url = result.get('url', '')
            published_date = result.get('published_date', '')
            
            result_data = {
                'title': title,
                'content': content[:500],  # Truncate content
                'url': url,
                'published_date': published_date,
                'relevance_score': result.get('score', 0.0)
            }
            
            # Categorize by query type
            if query_type == 'recent_news':
                research_results['recent_news'].append(result_data)
            elif query_type == 'financial_performance':
                if 'earnings' in title.lower() or 'revenue' in title.lower():
                    research_results['financial_insights']['latest_earnings'] = result_data
            elif query_type == 'technology_innovation':
                if 'AI' in content or 'digital' in content.lower() or 'technology' in content.lower():
                    research_results['technology_updates'].append(result_data)
            elif query_type == 'strategic_initiatives':
                if 'acquisition' in content.lower() or 'partnership' in content.lower():
                    research_results['strategic_initiatives'].append(result_data)
            elif query_type == 'leadership':
                if 'CEO' in content or 'executive' in content.lower():
                    research_results['leadership_changes'].append(result_data)
    
    def _apply_rate_limit(self, company_name: str) -> None:
        """Apply rate limiting to prevent API abuse."""
        current_time = time.time()
        last_request = self._last_request_time.get(company_name, 0)
        
        if current_time - last_request < 2.0:  # 2 second minimum between requests for same company
            time.sleep(2.0 - (current_time - last_request))
        
        self._last_request_time[company_name] = current_time
    
    def _fallback_research(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide fallback research when Tavily is unavailable."""
        company_name = company_data.get('company_name', 'Unknown')
        industry = company_data.get('industry', 'Unknown')
        
        return {
            'company_name': company_name,
            'research_timestamp': datetime.now().isoformat(),
            'recent_news': [{
                'title': f'{company_name} continues growth in {industry} sector',
                'content': f'Based on available data, {company_name} remains active in the {industry} industry with ongoing business operations.',
                'url': company_data.get('website_url', '#'),
                'published_date': datetime.now().date().isoformat(),
                'relevance_score': 0.5
            }],
            'financial_insights': {
                'revenue': company_data.get('revenue', 0),
                'market_position': company_data.get('market_position', 'Unknown')
            },
            'market_position': {
                'position': company_data.get('market_position', 'Unknown'),
                'industry': industry
            },
            'technology_updates': [{
                'title': f'{company_name} technology capabilities',
                'content': f"Technology stack includes: {company_data.get('technology_stack', 'Standard business technologies')}",
                'relevance_score': 0.3
            }],
            'competitive_landscape': {
                'advantages': company_data.get('competitive_advantages', 'Market presence'),
                'challenges': company_data.get('challenges', 'Standard industry challenges')
            },
            'strategic_initiatives': [{
                'title': f'{company_name} strategic focus',
                'content': f"Company focus areas: {company_data.get('key_services', 'Core business services')}",
                'relevance_score': 0.4
            }],
            'challenges_opportunities': {
                'challenges': company_data.get('challenges', 'Competitive market dynamics'),
                'opportunities': f'Growth potential in {industry} sector'
            },
            'leadership_changes': [],
            'web_research_confidence': 0.2,  # Low confidence for fallback
            'sources_count': 1,
            'fallback_mode': True
        }
    
    def get_research_summary(self, research_results: Dict[str, Any]) -> str:
        """Generate a concise research summary for agents."""
        company_name = research_results.get('company_name', 'Company')
        confidence = research_results.get('web_research_confidence', 0.0)
        sources_count = research_results.get('sources_count', 0)
        
        summary_parts = [
            f"🔍 Web Research Summary for {company_name}",
            f"📊 Confidence: {confidence:.1%} ({sources_count} sources)",
            ""
        ]
        
        # Recent news highlights
        recent_news = research_results.get('recent_news', [])
        if recent_news:
            summary_parts.append("📰 Recent Developments:")
            for news in recent_news[:2]:
                summary_parts.append(f"• {news.get('title', 'News update')}")
            summary_parts.append("")
        
        # Financial insights
        financial = research_results.get('financial_insights', {})
        if financial:
            summary_parts.append("💰 Financial Insights:")
            if 'latest_earnings' in financial:
                summary_parts.append(f"• {financial['latest_earnings'].get('title', 'Recent earnings update')}")
            summary_parts.append("")
        
        # Technology updates
        tech_updates = research_results.get('technology_updates', [])
        if tech_updates:
            summary_parts.append("🚀 Technology & Innovation:")
            for update in tech_updates[:1]:
                summary_parts.append(f"• {update.get('title', 'Technology update')}")
            summary_parts.append("")
        
        # Strategic initiatives
        strategic = research_results.get('strategic_initiatives', [])
        if strategic:
            summary_parts.append("🎯 Strategic Initiatives:")
            for initiative in strategic[:1]:
                summary_parts.append(f"• {initiative.get('title', 'Strategic initiative')}")
        
        return "\n".join(summary_parts)
    
    def enhance_company_data(self, company_data: Dict[str, Any], research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance company data with web research insights."""
        enhanced_data = company_data.copy()
        
        # Add web research metadata
        enhanced_data['web_research_timestamp'] = research_results.get('research_timestamp')
        enhanced_data['web_research_confidence'] = research_results.get('web_research_confidence', 0.0)
        enhanced_data['web_sources_count'] = research_results.get('sources_count', 0)
        
        # Extract key insights for agent use
        recent_news = research_results.get('recent_news', [])
        if recent_news:
            enhanced_data['latest_news_headline'] = recent_news[0].get('title', '')
            enhanced_data['recent_developments'] = [news.get('title', '') for news in recent_news[:3]]
        
        # Financial updates
        financial = research_results.get('financial_insights', {})
        if financial and 'latest_earnings' in financial:
            enhanced_data['latest_financial_news'] = financial['latest_earnings'].get('title', '')
        
        # Technology insights
        tech_updates = research_results.get('technology_updates', [])
        if tech_updates:
            enhanced_data['recent_tech_initiatives'] = [update.get('title', '') for update in tech_updates[:2]]
        
        return enhanced_data

# Utility function for easy import
def create_web_research_agent(api_key: Optional[str] = None) -> WebResearchAgent:
    """
    Factory function to create a WebResearchAgent.
    
    Args:
        api_key (Optional[str]): Tavily API key
        
    Returns:
        WebResearchAgent: Configured web research agent
    """
    return WebResearchAgent(api_key=api_key)
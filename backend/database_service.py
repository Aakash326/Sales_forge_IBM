#!/usr/bin/env python3
"""
Database Service for Sales Forge
Handles database connections and company data retrieval
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
import asyncpg
from datetime import datetime

class DatabaseService:
    """Service for managing database connections and company data"""
    
    def __init__(self):
        # Default to mock data if no database connection
        self.use_mock_data = True
        self.connection_string = os.getenv('DATABASE_URL') or None
        
    async def get_companies_by_industry(self, industry: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get companies from database by industry"""
        
        if self.use_mock_data or not self.connection_string:
            return self._get_mock_companies_by_industry(industry, limit)
        
        try:
            # Try to connect to actual database
            conn = await asyncpg.connect(self.connection_string)
            
            table_name = f"{industry.lower()}_companies"
            query = f"""
                SELECT company_name, industry, location, performance_score, created_at
                FROM {table_name}
                ORDER BY performance_score DESC
                LIMIT $1
            """
            
            rows = await conn.fetch(query, limit)
            await conn.close()
            
            companies = []
            for row in rows:
                companies.append({
                    'company_name': row['company_name'],
                    'industry': row['industry'],
                    'location': row['location'],
                    'performance_score': row['performance_score'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                    # Generate additional data for workflows
                    'company_size': self._estimate_company_size(row['performance_score']),
                    'annual_revenue': self._estimate_revenue(row['performance_score']),
                    'contact_name': self._generate_contact_name(),
                    'contact_email': self._generate_contact_email(row['company_name']),
                    'pain_points': self._get_industry_pain_points(industry),
                    'tech_stack': self._get_industry_tech_stack(industry)
                })
            
            return companies
            
        except Exception as e:
            print(f"Database connection failed: {e}, using mock data")
            return self._get_mock_companies_by_industry(industry, limit)
    
    async def get_all_companies(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Get companies from all industries"""
        finance_companies = await self.get_companies_by_industry('Finance', limit // 3)
        healthcare_companies = await self.get_companies_by_industry('Healthcare', limit // 3)
        tech_companies = await self.get_companies_by_industry('Technology', limit // 3)
        
        return finance_companies + healthcare_companies + tech_companies
    
    def _get_mock_companies_by_industry(self, industry: str, limit: int) -> List[Dict[str, Any]]:
        """Generate mock company data when database is not available"""
        
        mock_companies = {
            'Finance': [
                {'company_name': 'Goldman Sachs', 'location': 'New York, NY', 'performance_score': 95},
                {'company_name': 'JPMorgan Chase', 'location': 'New York, NY', 'performance_score': 92},
                {'company_name': 'Bank of America', 'location': 'Charlotte, NC', 'performance_score': 88},
                {'company_name': 'Wells Fargo', 'location': 'San Francisco, CA', 'performance_score': 85},
                {'company_name': 'Morgan Stanley', 'location': 'New York, NY', 'performance_score': 90},
            ],
            'Healthcare': [
                {'company_name': 'Johnson & Johnson', 'location': 'New Brunswick, NJ', 'performance_score': 94},
                {'company_name': 'Pfizer', 'location': 'New York, NY', 'performance_score': 91},
                {'company_name': 'UnitedHealth Group', 'location': 'Minnetonka, MN', 'performance_score': 93},
                {'company_name': 'Abbott Laboratories', 'location': 'Abbott Park, IL', 'performance_score': 89},
                {'company_name': 'Merck & Co.', 'location': 'Kenilworth, NJ', 'performance_score': 90},
            ],
            'Technology': [
                {'company_name': 'Apple Inc.', 'location': 'Cupertino, CA', 'performance_score': 98},
                {'company_name': 'Microsoft Corporation', 'location': 'Redmond, WA', 'performance_score': 97},
                {'company_name': 'Alphabet Inc.', 'location': 'Mountain View, CA', 'performance_score': 96},
                {'company_name': 'Amazon.com Inc.', 'location': 'Seattle, WA', 'performance_score': 95},
                {'company_name': 'Meta Platforms Inc.', 'location': 'Menlo Park, CA', 'performance_score': 91},
            ]
        }
        
        companies_data = mock_companies.get(industry, [])[:limit]
        
        # Enhance with additional fields for workflows
        enhanced_companies = []
        for comp in companies_data:
            enhanced_companies.append({
                **comp,
                'industry': industry,
                'created_at': datetime.now().isoformat(),
                'company_size': self._estimate_company_size(comp['performance_score']),
                'annual_revenue': self._estimate_revenue(comp['performance_score']),
                'contact_name': self._generate_contact_name(),
                'contact_email': self._generate_contact_email(comp['company_name']),
                'pain_points': self._get_industry_pain_points(industry),
                'tech_stack': self._get_industry_tech_stack(industry)
            })
        
        return enhanced_companies
    
    def _estimate_company_size(self, performance_score: int) -> int:
        """Estimate company size based on performance score"""
        if performance_score >= 95:
            return 50000 + (performance_score - 95) * 10000
        elif performance_score >= 90:
            return 10000 + (performance_score - 90) * 8000
        elif performance_score >= 85:
            return 5000 + (performance_score - 85) * 1000
        else:
            return 1000 + performance_score * 50
    
    def _estimate_revenue(self, performance_score: int) -> int:
        """Estimate annual revenue based on performance score"""
        return int((performance_score / 100) * 100000000 * (1 + performance_score / 200))
    
    def _generate_contact_name(self) -> str:
        """Generate a realistic contact name"""
        import random
        first_names = ['Sarah', 'Michael', 'Jennifer', 'David', 'Lisa', 'Robert', 'Emily', 'James', 'Michelle', 'John']
        last_names = ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_contact_email(self, company_name: str) -> str:
        """Generate a realistic contact email"""
        domain = company_name.lower().replace(' ', '').replace('.', '').replace(',', '')
        if 'inc' in domain:
            domain = domain.replace('inc', '')
        if 'corp' in domain:
            domain = domain.replace('corp', '')
        domain = domain[:20]  # Limit domain length
        
        import random
        contacts = ['sales', 'business', 'partnerships', 'info', 'contact']
        return f"{random.choice(contacts)}@{domain}.com"
    
    def _get_industry_pain_points(self, industry: str) -> List[str]:
        """Get industry-specific pain points"""
        pain_points = {
            'Finance': ['Regulatory compliance complexity', 'Legacy system modernization', 'Cybersecurity threats', 'Digital transformation delays'],
            'Healthcare': ['Patient data integration', 'Regulatory compliance', 'Operational efficiency', 'Technology adoption'],
            'Technology': ['Scalability challenges', 'Market competition', 'Talent acquisition', 'Innovation speed']
        }
        return pain_points.get(industry, ['General operational challenges', 'Technology modernization', 'Process optimization'])
    
    def _get_industry_tech_stack(self, industry: str) -> List[str]:
        """Get industry-specific tech stack"""
        tech_stacks = {
            'Finance': ['Java', 'Oracle', 'Mainframe', 'Python', 'AWS', 'Kubernetes'],
            'Healthcare': ['C#', '.NET', 'SQL Server', 'Azure', 'HL7', 'FHIR'],
            'Technology': ['Python', 'React', 'Node.js', 'PostgreSQL', 'Docker', 'Kubernetes']
        }
        return tech_stacks.get(industry, ['Python', 'JavaScript', 'SQL', 'Cloud'])

# Global database service instance
db_service = DatabaseService()

# Global workflow cancellation tracking
active_workflows = {}

class WorkflowCancellation(Exception):
    """Exception raised when workflow is cancelled"""
    pass

import threading
import time

def cleanup_orphaned_workflows():
    """Background task to clean up orphaned workflows"""
    while True:
        try:
            current_time = datetime.now()
            orphaned_workflows = []
            
            for workflow_id, workflow_data in active_workflows.items():
                # Check if workflow has been running for more than 30 minutes (definitely orphaned)
                start_time = datetime.fromisoformat(workflow_data['start_time'])
                runtime = (current_time - start_time).total_seconds()
                
                # Mark as orphaned if:
                # 1. Running longer than 30 minutes OR
                # 2. No heartbeat for more than 2 minutes
                if (runtime > 1800 or  # 30 minutes
                    workflow_data.get('status') == 'running' and 
                    workflow_data.get('last_heartbeat') and
                    (current_time - datetime.fromisoformat(workflow_data['last_heartbeat'])).total_seconds() > 120):
                    
                    orphaned_workflows.append(workflow_id)
            
            # Cancel orphaned workflows
            for workflow_id in orphaned_workflows:
                active_workflows[workflow_id]['cancelled'] = True
                active_workflows[workflow_id]['status'] = 'cancelled'
                active_workflows[workflow_id]['end_time'] = current_time.isoformat()
                active_workflows[workflow_id]['cancellation_reason'] = 'orphaned'
                print(f"🧹 Cancelled orphaned workflow: {workflow_id}")
            
            # Clean up old completed/cancelled workflows (keep only last 50)
            if len(active_workflows) > 50:
                completed_workflows = [
                    (wid, wdata) for wid, wdata in active_workflows.items()
                    if wdata.get('status') in ['completed', 'cancelled', 'failed']
                ]
                
                if len(completed_workflows) > 30:
                    # Sort by end_time and keep only newest 30
                    completed_workflows.sort(key=lambda x: x[1].get('end_time', ''), reverse=True)
                    workflows_to_remove = completed_workflows[30:]
                    
                    for workflow_id, _ in workflows_to_remove:
                        del active_workflows[workflow_id]
                    
                    print(f"🧹 Cleaned up {len(workflows_to_remove)} old workflows")
            
        except Exception as e:
            print(f"❌ Error in workflow cleanup: {e}")
        
        # Run cleanup every 60 seconds
        time.sleep(60)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_orphaned_workflows, daemon=True)
cleanup_thread.start()
print("🧹 Started workflow cleanup service")
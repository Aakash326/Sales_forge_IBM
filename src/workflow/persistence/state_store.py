import json
import sqlite3
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from ..states.lead_states import LeadState

class StateStore:
    """Manages persistent storage of lead states"""
    
    def __init__(self, db_path: str = "sales_pipeline.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Lead states table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lead_states (
                    lead_id TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    contact_email TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    lead_score REAL DEFAULT 0.0,
                    engagement_level REAL DEFAULT 0.0,
                    qualification_score REAL DEFAULT 0.0,
                    outreach_attempts INTEGER DEFAULT 0,
                    response_rate REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    state_data TEXT  -- JSON blob for full state
                )
            """)
            
            # Workflow execution history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workflow_executions (
                    execution_id TEXT PRIMARY KEY,
                    lead_id TEXT NOT NULL,
                    workflow_name TEXT NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    status TEXT DEFAULT 'running',
                    result_data TEXT,  -- JSON blob for results
                    FOREIGN KEY (lead_id) REFERENCES lead_states (lead_id)
                )
            """)
            
            # Node execution tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS node_executions (
                    execution_id TEXT PRIMARY KEY,
                    workflow_execution_id TEXT NOT NULL,
                    node_name TEXT NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    status TEXT DEFAULT 'running',
                    input_data TEXT,
                    output_data TEXT,
                    error_message TEXT,
                    FOREIGN KEY (workflow_execution_id) REFERENCES workflow_executions (execution_id)
                )
            """)
            
            conn.commit()
    
    def save_lead_state(self, state: LeadState) -> bool:
        """Save or update lead state"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Convert state to JSON for storage
                state_json = json.dumps(state.dict(), default=str)
                
                cursor.execute("""
                    INSERT OR REPLACE INTO lead_states (
                        lead_id, company_name, contact_email, stage,
                        lead_score, engagement_level, qualification_score,
                        outreach_attempts, response_rate, updated_at, state_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    state.lead_id,
                    state.company_name,
                    state.contact_email,
                    state.stage,
                    state.lead_score,
                    state.engagement_level,
                    state.qualification_score,
                    state.outreach_attempts,
                    state.response_rate,
                    datetime.now().isoformat(),
                    state_json
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving lead state: {e}")
            return False
    
    def load_lead_state(self, lead_id: str) -> Optional[LeadState]:
        """Load lead state by ID"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT state_data FROM lead_states WHERE lead_id = ?
                """, (lead_id,))
                
                result = cursor.fetchone()
                if result:
                    state_data = json.loads(result[0])
                    return LeadState(**state_data)
                    
                return None
                
        except Exception as e:
            print(f"Error loading lead state: {e}")
            return None
    
    def get_leads_by_stage(self, stage: str) -> List[LeadState]:
        """Get all leads in a specific stage"""
        
        leads = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT state_data FROM lead_states WHERE stage = ?
                    ORDER BY updated_at DESC
                """, (stage,))
                
                results = cursor.fetchall()
                for result in results:
                    state_data = json.loads(result[0])
                    leads.append(LeadState(**state_data))
                    
        except Exception as e:
            print(f"Error getting leads by stage: {e}")
            
        return leads
    
    def get_high_score_leads(self, min_score: float = 0.7) -> List[LeadState]:
        """Get leads with high scores"""
        
        leads = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT state_data FROM lead_states 
                    WHERE lead_score >= ?
                    ORDER BY lead_score DESC
                """, (min_score,))
                
                results = cursor.fetchall()
                for result in results:
                    state_data = json.loads(result[0])
                    leads.append(LeadState(**state_data))
                    
        except Exception as e:
            print(f"Error getting high score leads: {e}")
            
        return leads
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        
        stats = {}
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Stage distribution
                cursor.execute("""
                    SELECT stage, COUNT(*) as count 
                    FROM lead_states 
                    GROUP BY stage
                """)
                stage_counts = dict(cursor.fetchall())
                
                # Score distribution
                cursor.execute("""
                    SELECT 
                        AVG(lead_score) as avg_score,
                        AVG(engagement_level) as avg_engagement,
                        AVG(qualification_score) as avg_qualification
                    FROM lead_states
                """)
                averages = cursor.fetchone()
                
                # Recent activity
                cursor.execute("""
                    SELECT COUNT(*) as recent_updates
                    FROM lead_states 
                    WHERE updated_at >= datetime('now', '-7 days')
                """)
                recent_updates = cursor.fetchone()[0]
                
                stats = {
                    "total_leads": sum(stage_counts.values()),
                    "stage_distribution": stage_counts,
                    "average_scores": {
                        "lead_score": averages[0] or 0.0,
                        "engagement_level": averages[1] or 0.0,
                        "qualification_score": averages[2] or 0.0
                    },
                    "recent_activity": recent_updates
                }
                
        except Exception as e:
            print(f"Error getting pipeline stats: {e}")
            
        return stats
    
    def delete_lead_state(self, lead_id: str) -> bool:
        """Delete a lead state"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM lead_states WHERE lead_id = ?", (lead_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error deleting lead state: {e}")
            return False
    
    def search_leads(self, query: str) -> List[LeadState]:
        """Search leads by company name or email"""
        
        leads = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT state_data FROM lead_states 
                    WHERE company_name LIKE ? OR contact_email LIKE ?
                    ORDER BY updated_at DESC
                """, (f"%{query}%", f"%{query}%"))
                
                results = cursor.fetchall()
                for result in results:
                    state_data = json.loads(result[0])
                    leads.append(LeadState(**state_data))
                    
        except Exception as e:
            print(f"Error searching leads: {e}")
            
        return leads
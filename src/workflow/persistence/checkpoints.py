import json
import sqlite3
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

class CheckpointManager:
    """Manages workflow checkpoints for recovery and resume functionality"""
    
    def __init__(self, db_path: str = "workflow_checkpoints.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize checkpoint database"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Workflow checkpoints table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workflow_checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    lead_id TEXT NOT NULL,
                    node_name TEXT NOT NULL,
                    checkpoint_data TEXT,  -- JSON blob
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Workflow execution logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS execution_logs (
                    log_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    lead_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,  -- 'start', 'node_complete', 'error', 'complete'
                    node_name TEXT,
                    message TEXT,
                    data TEXT,  -- JSON blob
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def create_checkpoint(self, workflow_id: str, lead_id: str, node_name: str, 
                         state_data: Dict[str, Any]) -> str:
        """Create a checkpoint for workflow state"""
        
        checkpoint_id = str(uuid.uuid4())
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO workflow_checkpoints (
                        checkpoint_id, workflow_id, lead_id, node_name, checkpoint_data
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    checkpoint_id,
                    workflow_id,
                    lead_id,
                    node_name,
                    json.dumps(state_data, default=str)
                ))
                
                conn.commit()
                
                # Log checkpoint creation
                self.log_event(
                    workflow_id, lead_id, "checkpoint_created", 
                    node_name, f"Checkpoint created at {node_name}"
                )
                
                return checkpoint_id
                
        except Exception as e:
            print(f"Error creating checkpoint: {e}")
            return ""
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific checkpoint"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT workflow_id, lead_id, node_name, checkpoint_data 
                    FROM workflow_checkpoints 
                    WHERE checkpoint_id = ? AND status = 'active'
                """, (checkpoint_id,))
                
                result = cursor.fetchone()
                if result:
                    return {
                        "workflow_id": result[0],
                        "lead_id": result[1],
                        "node_name": result[2],
                        "state_data": json.loads(result[3])
                    }
                    
                return None
                
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return None
    
    def get_latest_checkpoint(self, workflow_id: str, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest checkpoint for a workflow"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT checkpoint_id, node_name, checkpoint_data, created_at
                    FROM workflow_checkpoints 
                    WHERE workflow_id = ? AND lead_id = ? AND status = 'active'
                    ORDER BY created_at DESC 
                    LIMIT 1
                """, (workflow_id, lead_id))
                
                result = cursor.fetchone()
                if result:
                    return {
                        "checkpoint_id": result[0],
                        "node_name": result[1],
                        "state_data": json.loads(result[2]),
                        "created_at": result[3]
                    }
                    
                return None
                
        except Exception as e:
            print(f"Error getting latest checkpoint: {e}")
            return None
    
    def resume_workflow(self, workflow_id: str, lead_id: str) -> Optional[Dict[str, Any]]:
        """Resume workflow from latest checkpoint"""
        
        checkpoint = self.get_latest_checkpoint(workflow_id, lead_id)
        
        if checkpoint:
            self.log_event(
                workflow_id, lead_id, "workflow_resumed",
                checkpoint["node_name"], 
                f"Resuming from checkpoint at {checkpoint['node_name']}"
            )
            
            return checkpoint
        
        return None
    
    def mark_checkpoint_complete(self, checkpoint_id: str):
        """Mark checkpoint as complete"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE workflow_checkpoints 
                    SET status = 'completed' 
                    WHERE checkpoint_id = ?
                """, (checkpoint_id,))
                
                conn.commit()
                
        except Exception as e:
            print(f"Error marking checkpoint complete: {e}")
    
    def log_event(self, workflow_id: str, lead_id: str, event_type: str, 
                  node_name: str = None, message: str = "", data: Dict[str, Any] = None):
        """Log workflow execution event"""
        
        log_id = str(uuid.uuid4())
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO execution_logs (
                        log_id, workflow_id, lead_id, event_type, 
                        node_name, message, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    log_id,
                    workflow_id,
                    lead_id,
                    event_type,
                    node_name,
                    message,
                    json.dumps(data or {}, default=str)
                ))
                
                conn.commit()
                
        except Exception as e:
            print(f"Error logging event: {e}")
    
    def get_workflow_history(self, workflow_id: str, lead_id: str) -> List[Dict[str, Any]]:
        """Get execution history for a workflow"""
        
        history = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT event_type, node_name, message, data, timestamp
                    FROM execution_logs 
                    WHERE workflow_id = ? AND lead_id = ?
                    ORDER BY timestamp ASC
                """, (workflow_id, lead_id))
                
                results = cursor.fetchall()
                for result in results:
                    history.append({
                        "event_type": result[0],
                        "node_name": result[1],
                        "message": result[2],
                        "data": json.loads(result[3]) if result[3] else {},
                        "timestamp": result[4]
                    })
                    
        except Exception as e:
            print(f"Error getting workflow history: {e}")
            
        return history
    
    def cleanup_old_checkpoints(self, days_old: int = 30):
        """Clean up old checkpoints"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Mark old checkpoints as archived
                cursor.execute("""
                    UPDATE workflow_checkpoints 
                    SET status = 'archived' 
                    WHERE created_at < datetime('now', '-{} days')
                    AND status = 'active'
                """.format(days_old))
                
                # Delete very old logs
                cursor.execute("""
                    DELETE FROM execution_logs 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(days_old * 2))
                
                conn.commit()
                
        except Exception as e:
            print(f"Error cleaning up checkpoints: {e}")
    
    def get_failed_workflows(self) -> List[Dict[str, Any]]:
        """Get workflows that failed and might need retry"""
        
        failed_workflows = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT DISTINCT workflow_id, lead_id, MAX(timestamp) as last_event
                    FROM execution_logs 
                    WHERE event_type = 'error'
                    AND workflow_id NOT IN (
                        SELECT workflow_id FROM execution_logs 
                        WHERE event_type = 'complete'
                    )
                    GROUP BY workflow_id, lead_id
                    ORDER BY last_event DESC
                """)
                
                results = cursor.fetchall()
                for result in results:
                    failed_workflows.append({
                        "workflow_id": result[0],
                        "lead_id": result[1],
                        "last_error": result[2]
                    })
                    
        except Exception as e:
            print(f"Error getting failed workflows: {e}")
            
        return failed_workflows
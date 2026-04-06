"""
Memory Manager for storing decision history
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class MemoryManager:
    """
    Manages memory and history for decision-making sessions
    """
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.sessions = []
        self.current_session = None
    
    def start_session(self, task: str, situation: str) -> str:
        """
        Start a new decision session
        
        Returns:
            Session ID
        """
        session_id = f"session_{len(self.sessions)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_session = {
            "id": session_id,
            "task": task,
            "situation": situation,
            "started_at": datetime.now().isoformat(),
            "actions": [],
            "observations": [],
            "rewards": [],
            "total_reward": 0.0
        }
        
        return session_id
    
    def record_step(self, action: str, observation: Dict[str, Any], reward: float):
        """
        Record a step in current session
        """
        if self.current_session is None:
            return
        
        self.current_session["actions"].append(action)
        self.current_session["observations"].append(observation)
        self.current_session["rewards"].append(reward)
        self.current_session["total_reward"] += reward
    
    def end_session(self, final_decision: str = None):
        """
        End current session and save to history
        """
        if self.current_session is None:
            return
        
        self.current_session["ended_at"] = datetime.now().isoformat()
        self.current_session["final_decision"] = final_decision
        
        self.sessions.append(self.current_session)
        
        # Limit history size
        if len(self.sessions) > self.max_history:
            self.sessions = self.sessions[-self.max_history:]
        
        self.current_session = None
    
    def get_session_history(self, session_id: str = None) -> Dict[str, Any]:
        """
        Get history for a specific session
        """
        if session_id is None and self.current_session:
            return self.current_session
        
        for session in self.sessions:
            if session["id"] == session_id:
                return session
        
        return None
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """
        Get all session history
        """
        return self.sessions
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics across all sessions
        """
        if not self.sessions:
            return {
                "total_sessions": 0,
                "average_reward": 0.0,
                "total_steps": 0
            }
        
        total_reward = sum(s["total_reward"] for s in self.sessions)
        total_steps = sum(len(s["actions"]) for s in self.sessions)
        
        return {
            "total_sessions": len(self.sessions),
            "average_reward": total_reward / len(self.sessions),
            "total_steps": total_steps,
            "average_steps_per_session": total_steps / len(self.sessions)
        }
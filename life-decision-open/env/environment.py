"""
Life Decision Environment - OpenEnv Compliant
"""

from typing import Dict, Any, Tuple, Optional
import copy

from .reward import RewardSystem
from tasks.easy_task import EASY_TASK
from tasks.medium_task import MEDIUM_TASK
from tasks.hard_task import HARD_TASK


class LifeDecisionEnv:
    """
    Reinforcement Learning Environment for Life Decision Making
    
    Observation Space:
        - situation: str (description of the decision scenario)
        - goal: str (desired outcome)
        - progress: float (completion progress 0.0 to 1.0)
        - history: list (action history)
    
    Action Space:
        - analyze_problem
        - identify_factors
        - generate_options
        - evaluate_options
        - recommend_decision
    """
    
    def __init__(self):
        # Action space definition
        self.action_space = [
            "analyze_problem",
            "identify_factors",
            "generate_options",
            "evaluate_options",
            "recommend_decision"
        ]
        
        # Reward system
        self.reward_system = RewardSystem()
        
        # Task definitions
        self.tasks = {
            "easy": EASY_TASK,
            "medium": MEDIUM_TASK,
            "hard": HARD_TASK
        }
        
        # State
        self.current_state = None
        self.current_task = None
        self.step_count = 0
        self.max_steps = 10
        
    def reset(self, task: str = "easy") -> Dict[str, Any]:
        """
        Reset environment to initial state
        
        Args:
            task: Task difficulty level ("easy", "medium", "hard")
            
        Returns:
            Initial observation
        """
        if task not in self.tasks:
            task = "easy"
        
        self.current_task = task
        task_data = self.tasks[task]
        
        # Initialize state
        self.current_state = {
            "situation": task_data["situation"],
            "goal": task_data["goal"],
            "progress": 0.0,
            "history": []
        }
        
        self.step_count = 0
        self.reward_system.reset()
        
        return copy.deepcopy(self.current_state)
    
    def step(self, action: str) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Execute one step in the environment
        
        Args:
            action: Action to take
            
        Returns:
            Tuple of (observation, reward, done, info)
        """
        if self.current_state is None:
            raise ValueError("Environment not initialized. Call reset() first.")
        
        # Validate action
        if action not in self.action_space:
            reward = -0.1
            done = False
            info = {"error": "Invalid action", "valid_actions": self.action_space}
            return copy.deepcopy(self.current_state), reward, done, info
        
        # Calculate reward
        reward = self.reward_system.calculate_reward(action)
        
        # Update state
        self.current_state["history"].append(action)
        self.step_count += 1
        
        # Update progress
        self.current_state["progress"] = min(1.0, len(self.current_state["history"]) / len(self.action_space))
        
        # Check if done
        done = (
            action == "recommend_decision" or 
            self.step_count >= self.max_steps or
            self.current_state["progress"] >= 1.0
        )
        
        # Info
        info = {
            "step": self.step_count,
            "action_sequence": self.current_state["history"],
            "task": self.current_task,
            "total_reward": self.reward_system.total_reward
        }
        
        return copy.deepcopy(self.current_state), reward, done, info
    
    def state(self) -> Optional[Dict[str, Any]]:
        """
        Get current environment state
        
        Returns:
            Current state dictionary or None
        """
        if self.current_state is None:
            return None
        
        return {
            **copy.deepcopy(self.current_state),
            "step_count": self.step_count,
            "task": self.current_task,
            "total_reward": self.reward_system.total_reward,
            "action_space": self.action_space
        }
    
    def render(self) -> str:
        """
        Render current state as string
        
        Returns:
            String representation of state
        """
        if self.current_state is None:
            return "Environment not initialized"
        
        return f"""
Life Decision Environment State:
================================
Task: {self.current_task}
Situation: {self.current_state['situation']}
Goal: {self.current_state['goal']}
Progress: {self.current_state['progress']:.2%}
Steps: {self.step_count}/{self.max_steps}
History: {' -> '.join(self.current_state['history'])}
Total Reward: {self.reward_system.total_reward:.2f}
"""
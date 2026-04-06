"""
Reward System for Life Decision Environment
"""

from typing import Dict


class RewardSystem:
    """
    Deterministic reward calculation system
    
    Reward Structure:
        - analyze_problem: +0.2
        - identify_factors: +0.2
        - generate_options: +0.2
        - evaluate_options: +0.2
        - recommend_decision: +0.2
        - invalid action: -0.1
        
    Maximum total reward: 1.0
    """
    
    def __init__(self):
        self.reward_mapping = {
            "analyze_problem": 0.2,
            "identify_factors": 0.2,
            "generate_options": 0.2,
            "evaluate_options": 0.2,
            "recommend_decision": 0.2
        }
        
        self.invalid_action_penalty = -0.1
        self.total_reward = 0.0
        self.action_history = []
    
    def calculate_reward(self, action: str) -> float:
        """
        Calculate reward for given action
        
        Args:
            action: Action taken
            
        Returns:
            Reward value
        """
        if action in self.reward_mapping:
            reward = self.reward_mapping[action]
            self.action_history.append(action)
        else:
            reward = self.invalid_action_penalty
        
        self.total_reward += reward
        return reward
    
    def reset(self):
        """Reset reward tracking"""
        self.total_reward = 0.0
        self.action_history = []
    
    def get_total_reward(self) -> float:
        """Get cumulative reward"""
        return self.total_reward
    
    def get_max_possible_reward(self) -> float:
        """Get maximum possible reward"""
        return sum(self.reward_mapping.values())
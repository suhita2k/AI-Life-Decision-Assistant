"""
Decision Agent - Uses OpenAI API for reasoning
"""

from typing import Dict, Any, List
import json


class DecisionAgent:
    """
    AI Agent for life decision making
    Uses OpenAI-compatible API for reasoning
    """
    
    def __init__(self, client, model: str):
        self.client = client
        self.model = model
        self.system_prompt = """You are a professional life decision advisor with expertise in:
- Critical thinking and problem analysis
- Multi-factor decision making
- Risk assessment
- Long-term planning
- Personal development

Your role is to help people make well-informed decisions by:
1. Analyzing the problem thoroughly
2. Identifying all relevant factors
3. Generating possible options
4. Evaluating each option objectively
5. Providing clear recommendations

Always be thoughtful, balanced, and consider multiple perspectives."""
    
    def choose_action(self, observation: Dict[str, Any]) -> str:
        """
        Choose next action based on current observation
        
        Args:
            observation: Current environment observation
            
        Returns:
            Action to take
        """
        history = observation.get("history", [])
        progress = observation.get("progress", 0.0)
        
        # Deterministic action sequence
        action_sequence = [
            "analyze_problem",
            "identify_factors",
            "generate_options",
            "evaluate_options",
            "recommend_decision"
        ]
        
        # Choose next action based on history
        for action in action_sequence:
            if action not in history:
                return action
        
        # All actions completed
        return "recommend_decision"
    
    def analyze_decision(self, situation: str, goal: str) -> Dict[str, Any]:
        """
        Perform full decision analysis
        
        Args:
            situation: Description of the decision scenario
            goal: Desired outcome
            
        Returns:
            Analysis dictionary
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"""
Please analyze this decision:

Situation: {situation}

Goal: {goal}

Provide a structured analysis covering:
1. Problem Analysis
2. Key Factors to Consider
3. Possible Options
4. Evaluation of Each Option
5. Final Recommendation

Be thorough and practical.
"""}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                "analysis": analysis_text,
                "model": self.model,
                "situation": situation,
                "goal": goal
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "analysis": "Unable to generate analysis at this time.",
                "situation": situation,
                "goal": goal
            }
    
    def reason_step(self, observation: Dict[str, Any], action: str) -> str:
        """
        Generate reasoning for a specific action step
        
        Args:
            observation: Current observation
            action: Action being taken
            
        Returns:
            Reasoning text
        """
        situation = observation.get("situation", "")
        goal = observation.get("goal", "")
        
        prompts = {
            "analyze_problem": f"Analyze this decision problem: {situation}. What are the core issues?",
            "identify_factors": f"Given the goal '{goal}', what are the key factors to consider?",
            "generate_options": f"What are the possible options for: {situation}?",
            "evaluate_options": "Evaluate the pros and cons of each option.",
            "recommend_decision": "What is your final recommendation and why?"
        }
        
        prompt = prompts.get(action, "Provide your reasoning.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Reasoning unavailable: {str(e)}"
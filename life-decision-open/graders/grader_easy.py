"""
Grader for Easy Task - Programming Language Selection
"""

from typing import Dict, Any


def grade_easy(agent_output: Dict[str, Any]) -> float:
    """
    Deterministic grading for easy task
    
    Scoring criteria:
    - 0.2: Completed analyze_problem action
    - 0.2: Completed identify_factors action
    - 0.2: Completed generate_options action
    - 0.2: Completed evaluate_options action
    - 0.2: Completed recommend_decision action
    
    Args:
        agent_output: Dictionary containing agent's actions and reasoning
        
    Returns:
        Score between 0.0 and 1.0
    """
    score = 0.0
    
    # Get action history
    history = agent_output.get("history", [])
    final_observation = agent_output.get("final_observation", {})
    
    # Check action sequence
    required_actions = [
        "analyze_problem",
        "identify_factors",
        "generate_options",
        "evaluate_options",
        "recommend_decision"
    ]
    
    for action in required_actions:
        if action in history:
            score += 0.2
    
    # Additional quality checks on reasoning (if available)
    reasoning_text = str(agent_output).lower()
    
    # Check for key reasoning elements
    reasoning_keywords = {
        "beginner": 0.05,
        "python": 0.05,
        "web development": 0.05,
        "data science": 0.05,
        "learning": 0.05
    }
    
    bonus_score = 0.0
    for keyword, value in reasoning_keywords.items():
        if keyword in reasoning_text:
            bonus_score += value
    
    # Cap bonus at 0.15
    bonus_score = min(0.15, bonus_score)
    
    final_score = min(1.0, score + bonus_score)
    
    return round(final_score, 2)


def evaluate_easy_task(history: list, reasoning: str = "") -> Dict[str, Any]:
    """
    Evaluate easy task completion
    
    Returns detailed evaluation
    """
    agent_output = {
        "history": history,
        "reasoning": reasoning
    }
    
    score = grade_easy(agent_output)
    
    completed_actions = len([a for a in history if a in [
        "analyze_problem",
        "identify_factors",
        "generate_options",
        "evaluate_options",
        "recommend_decision"
    ]])
    
    return {
        "score": score,
        "completed_actions": completed_actions,
        "total_actions": 5,
        "passed": score >= 0.7,
        "feedback": _generate_feedback(score, completed_actions)
    }


def _generate_feedback(score: float, completed: int) -> str:
    """Generate feedback based on score"""
    if score >= 0.9:
        return "Excellent! All required actions completed with good reasoning."
    elif score >= 0.7:
        return "Good job! Most actions completed successfully."
    elif score >= 0.5:
        return "Partial completion. Consider completing all decision steps."
    else:
        return "Incomplete. Make sure to follow the full decision-making process."
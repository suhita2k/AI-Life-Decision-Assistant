"""
Grader for Medium Task - Job Offer Selection
"""

from typing import Dict, Any


def grade_medium(agent_output: Dict[str, Any]) -> float:
    """
    Deterministic grading for medium task
    
    Scoring criteria:
    - 0.15: Completed analyze_problem action
    - 0.15: Completed identify_factors action
    - 0.2: Completed generate_options action
    - 0.25: Completed evaluate_options action (critical for job comparison)
    - 0.25: Completed recommend_decision action
    
    Args:
        agent_output: Dictionary containing agent's actions and reasoning
        
    Returns:
        Score between 0.0 and 1.0
    """
    score = 0.0
    
    # Get action history
    history = agent_output.get("history", [])
    
    # Weighted action scoring for medium task
    action_weights = {
        "analyze_problem": 0.15,
        "identify_factors": 0.15,
        "generate_options": 0.2,
        "evaluate_options": 0.25,  # Most important for comparison
        "recommend_decision": 0.25
    }
    
    for action, weight in action_weights.items():
        if action in history:
            score += weight
    
    # Check for quality indicators
    reasoning_text = str(agent_output).lower()
    
    # Key factors for job decision
    quality_keywords = {
        "salary": 0.03,
        "equity": 0.03,
        "culture": 0.03,
        "remote": 0.02,
        "stability": 0.03,
        "startup": 0.02,
        "corporation": 0.02,
        "risk": 0.03,
        "growth": 0.03,
        "balance": 0.02
    }
    
    bonus_score = 0.0
    for keyword, value in quality_keywords.items():
        if keyword in reasoning_text:
            bonus_score += value
    
    # Cap bonus
    bonus_score = min(0.2, bonus_score)
    
    final_score = min(1.0, score + bonus_score)
    
    return round(final_score, 2)


def evaluate_medium_task(history: list, reasoning: str = "") -> Dict[str, Any]:
    """
    Evaluate medium task completion
    
    Returns detailed evaluation
    """
    agent_output = {
        "history": history,
        "reasoning": reasoning
    }
    
    score = grade_medium(agent_output)
    
    # Check if critical actions were completed
    critical_actions = ["evaluate_options", "recommend_decision"]
    critical_completed = all(action in history for action in critical_actions)
    
    return {
        "score": score,
        "completed_actions": len(history),
        "critical_actions_completed": critical_completed,
        "passed": score >= 0.75,
        "feedback": _generate_feedback(score, critical_completed)
    }


def _generate_feedback(score: float, critical_completed: bool) -> str:
    """Generate feedback based on score"""
    if score >= 0.9:
        return "Excellent! Comprehensive job offer analysis with all factors considered."
    elif score >= 0.75:
        return "Good analysis! Major decision factors were evaluated."
    elif score >= 0.6:
        return "Adequate analysis, but some important factors may have been missed."
    elif critical_completed:
        return "Decision was made, but analysis could be more thorough."
    else:
        return "Incomplete analysis. Make sure to evaluate options before deciding."
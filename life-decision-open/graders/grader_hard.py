"""
Grader for Hard Task - Higher Studies vs Career Switch
"""

from typing import Dict, Any


def grade_hard(agent_output: Dict[str, Any]) -> float:
    """
    Deterministic grading for hard task
    
    Scoring criteria (strict):
    - 0.15: Completed analyze_problem action
    - 0.2: Completed identify_factors action (many factors to consider)
    - 0.2: Completed generate_options action
    - 0.25: Completed evaluate_options action (critical multi-factor analysis)
    - 0.2: Completed recommend_decision action with justification
    
    Args:
        agent_output: Dictionary containing agent's actions and reasoning
        
    Returns:
        Score between 0.0 and 1.0
    """
    score = 0.0
    
    # Get action history
    history = agent_output.get("history", [])
    
    # Weighted action scoring for hard task
    action_weights = {
        "analyze_problem": 0.15,
        "identify_factors": 0.2,
        "generate_options": 0.2,
        "evaluate_options": 0.25,
        "recommend_decision": 0.2
    }
    
    for action, weight in action_weights.items():
        if action in history:
            score += weight
    
    # Check for comprehensive reasoning
    reasoning_text = str(agent_output).lower()
    
    # Critical factors that should be considered
    critical_factors = {
        # Financial factors
        "cost": 0.025,
        "debt": 0.025,
        "salary": 0.025,
        "savings": 0.025,
        
        # Career factors
        "mba": 0.02,
        "ai": 0.02,
        "ml": 0.02,
        "engineer": 0.02,
        
        # Personal factors
        "family": 0.025,
        "spouse": 0.02,
        "age": 0.02,
        
        # Risk analysis
        "risk": 0.03,
        "opportunity": 0.025,
        
        # Time factors
        "years": 0.02,
        "timeline": 0.02,
        
        # Strategic thinking
        "long-term": 0.03,
        "growth": 0.025,
        "impact": 0.02
    }
    
    bonus_score = 0.0
    factors_considered = 0
    
    for factor, value in critical_factors.items():
        if factor in reasoning_text:
            bonus_score += value
            factors_considered += 1
    
    # Additional bonus for comprehensive analysis (many factors considered)
    if factors_considered >= 10:
        bonus_score += 0.05
    elif factors_considered >= 7:
        bonus_score += 0.03
    
    # Cap bonus
    bonus_score = min(0.3, bonus_score)
    
    final_score = min(1.0, score + bonus_score)
    
    return round(final_score, 2)


def evaluate_hard_task(history: list, reasoning: str = "") -> Dict[str, Any]:
    """
    Evaluate hard task completion
    
    Returns detailed evaluation
    """
    agent_output = {
        "history": history,
        "reasoning": reasoning
    }
    
    score = grade_hard(agent_output)
    
    # Count factors considered
    reasoning_lower = reasoning.lower()
    factor_categories = {
        "financial": ["cost", "debt", "salary", "savings"],
        "career": ["mba", "ai", "ml", "engineer", "growth"],
        "personal": ["family", "spouse", "age", "balance"],
        "strategic": ["risk", "long-term", "opportunity", "impact"]
    }
    
    categories_covered = 0
    for category, keywords in factor_categories.items():
        if any(keyword in reasoning_lower for keyword in keywords):
            categories_covered += 1
    
    # Check if all required actions completed
    all_actions_completed = len(history) >= 5
    
    return {
        "score": score,
        "completed_actions": len(history),
        "categories_covered": categories_covered,
        "total_categories": len(factor_categories),
        "all_actions_completed": all_actions_completed,
        "passed": score >= 0.8,
        "feedback": _generate_feedback(score, categories_covered, all_actions_completed)
    }


def _generate_feedback(score: float, categories: int, all_actions: bool) -> str:
    """Generate feedback based on score"""
    if score >= 0.9:
        return "Outstanding! Comprehensive multi-factor analysis considering financial, career, personal, and strategic dimensions."
    elif score >= 0.8:
        return "Excellent analysis covering most critical factors for this complex decision."
    elif score >= 0.7:
        return "Good effort, but this complex decision requires deeper analysis of multiple factor categories."
    elif score >= 0.6:
        return "Partial analysis. Consider financial, career, personal, and strategic factors more thoroughly."
    elif all_actions:
        return "All decision steps completed, but analysis lacks depth for this complex scenario."
    else:
        return "Incomplete decision process. This hard task requires thorough analysis of all factors."
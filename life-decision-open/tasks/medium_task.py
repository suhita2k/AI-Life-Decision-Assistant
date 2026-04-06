"""
Medium Task: Choosing between two job offers
"""

MEDIUM_TASK = {
    "difficulty": "medium",
    "name": "Job Offer Selection",
    "situation": """
    You have received two job offers:
    
    Offer A: Startup Company
    - Salary: $80,000
    - Equity: 0.5% stock options
    - Work culture: Fast-paced, innovative, flexible hours
    - Location: Remote
    - Risk: Company is 2 years old, uncertain stability
    
    Offer B: Established Corporation
    - Salary: $95,000
    - Equity: None
    - Work culture: Structured, 9-5, corporate environment
    - Location: Office-based, 1-hour commute
    - Stability: Fortune 500 company
    
    You value work-life balance, career growth, and financial security.
    """,
    "goal": "Choose the job offer that best aligns with your career goals and personal values",
    "context": {
        "offers": ["Startup (Offer A)", "Corporation (Offer B)"],
        "values": ["work-life balance", "career growth", "financial security"],
        "family_status": "single, no dependents",
        "career_stage": "early career, 3 years experience"
    },
    "expected_actions": [
        "analyze_problem",
        "identify_factors",
        "generate_options",
        "evaluate_options",
        "recommend_decision"
    ],
    "optimal_decision": "Context-dependent, requires thorough analysis",
    "reasoning": "Decision depends on risk tolerance, personal priorities, and long-term career vision."
}
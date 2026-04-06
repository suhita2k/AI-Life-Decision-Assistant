"""
Hard Task: Choosing between higher studies and career switch
"""

HARD_TASK = {
    "difficulty": "hard",
    "name": "Higher Studies vs Career Switch",
    "situation": """
    You are a 28-year-old software engineer with 5 years of experience earning $110,000/year.
    You are considering a major life decision between three paths:
    
    Option 1: Pursue MBA at top business school
    - Cost: $150,000 in tuition + 2 years opportunity cost
    - Potential: Switch to product management, eventual C-suite path
    - Risk: High debt, uncertain ROI, 2 years out of workforce
    
    Option 2: Switch to AI/ML specialization
    - Cost: $30,000 bootcamp + 6 months part-time
    - Potential: Join emerging field, higher salary potential
    - Risk: Competitive field, need to prove yourself again
    
    Option 3: Stay current path, pursue senior engineering track
    - Cost: None
    - Potential: Become principal engineer, technical leadership
    - Risk: Missing out on other opportunities, potential regret
    
    Considerations:
    - You have $50,000 in savings
    - You're married, spouse earns $60,000/year
    - You want to start a family in 3-5 years
    - You value intellectual challenge and impact
    - You're unsure about long-term coding vs management preference
    """,
    "goal": "Make a strategic career decision that optimizes for long-term fulfillment, financial security, and personal growth",
    "context": {
        "age": 28,
        "current_salary": 110000,
        "savings": 50000,
        "spouse_income": 60000,
        "options": ["MBA", "AI/ML Specialization", "Stay Current Path"],
        "timeline": "3-5 years to start family",
        "values": ["intellectual challenge", "impact", "financial security", "family"]
    },
    "expected_actions": [
        "analyze_problem",
        "identify_factors",
        "generate_options",
        "evaluate_options",
        "recommend_decision"
    ],
    "optimal_decision": "Highly context-dependent, requires comprehensive multi-factor analysis",
    "reasoning": "Complex decision involving financial, personal, professional, and temporal factors requiring deep reasoning."
}
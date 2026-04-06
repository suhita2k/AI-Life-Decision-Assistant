"""
Easy Task: Choosing a programming language to learn
"""

EASY_TASK = {
    "difficulty": "easy",
    "name": "Programming Language Selection",
    "situation": """
    You are a beginner who wants to start learning programming. 
    You have heard about Python, JavaScript, and Java, but you're not sure which one to start with.
    You have 3 months to dedicate to learning, and you're interested in web development and data science.
    """,
    "goal": "Choose the most suitable programming language to learn first",
    "context": {
        "time_available": "3 months",
        "interests": ["web development", "data science"],
        "experience_level": "beginner",
        "options": ["Python", "JavaScript", "Java"]
    },
    "expected_actions": [
        "analyze_problem",
        "identify_factors",
        "generate_options",
        "evaluate_options",
        "recommend_decision"
    ],
    "optimal_decision": "Python",
    "reasoning": "Python is beginner-friendly, widely used in both web development and data science, and has extensive learning resources."
}
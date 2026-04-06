"""
AI Life Decision Assistant - OpenEnv Compliant
Main Entrypoint for FastAPI Application
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# OpenAI Client
from openai import OpenAI
client = OpenAI(base_url=API_BASE_URL)

# Import environment
from env.environment import LifeDecisionEnv
from backend.agent import DecisionAgent

# Pydantic Models
class Observation(BaseModel):
    situation: str
    goal: str
    progress: float
    history: list

class Action(BaseModel):
    action: str

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"

# Initialize FastAPI
app = FastAPI(
    title="AI Life Decision Assistant - OpenEnv",
    description="Reinforcement Learning Environment for Life Decision Making",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env_instance = None
agent_instance = None

# Initialize environment
def get_env():
    global env_instance
    if env_instance is None:
        env_instance = LifeDecisionEnv()
    return env_instance

def get_agent():
    global agent_instance
    if agent_instance is None:
        agent_instance = DecisionAgent(client=client, model=MODEL_NAME)
    return agent_instance

# ========================================
# API ENDPOINTS
# ========================================

@app.get("/")
async def root():
    """Serve the frontend"""
    return FileResponse("frontend/index.html")

@app.post("/reset")
async def reset_environment(request: ResetRequest = None):
    """
    Reset the environment to initial state
    """
    print("START")
    print("STEP: Received reset request")
    
    env = get_env()
    task_type = request.task if request else "easy"
    
    print(f"STEP: Resetting environment with task: {task_type}")
    observation = env.reset(task=task_type)
    
    print("STEP: Environment reset complete")
    print("END")
    
    return {
        "observation": observation,
        "message": "Environment reset successfully"
    }

@app.post("/step")
async def step_environment(action: Action):
    """
    Execute one step in the environment
    """
    print("START")
    print(f"STEP: Received step request with action: {action.action}")
    
    env = get_env()
    
    if env.current_state is None:
        print("STEP: Environment not initialized")
        print("END")
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    print("STEP: Executing environment step")
    observation, reward, done, info = env.step(action.action)
    
    print(f"STEP: Step executed - Reward: {reward}, Done: {done}")
    print("END")
    
    return StepResponse(
        observation=Observation(**observation),
        reward=reward,
        done=done,
        info=info
    )

@app.get("/state")
async def get_state():
    """
    Get current environment state
    """
    print("START")
    print("STEP: Received state request")
    
    env = get_env()
    
    if env.current_state is None:
        print("STEP: No active state")
        print("END")
        return {"state": None, "message": "No active environment state"}
    
    state = env.state()
    print("STEP: State retrieved successfully")
    print("END")
    
    return {"state": state}

@app.post("/analyze")
async def analyze_decision(request: Dict[str, Any]):
    """
    Full decision analysis endpoint (preserves existing functionality)
    """
    print("START")
    print("STEP: Received analysis request")
    
    situation = request.get("situation", "")
    goal = request.get("goal", "")
    
    agent = get_agent()
    
    print("STEP: Performing decision analysis")
    analysis = agent.analyze_decision(situation, goal)
    
    print("STEP: Analysis complete")
    print("END")
    
    return {
        "analysis": analysis,
        "status": "success"
    }

@app.get("/actions")
async def get_available_actions():
    """
    Get available actions in the environment
    """
    env = get_env()
    return {
        "actions": env.action_space,
        "count": len(env.action_space)
    }

@app.get("/tasks")
async def get_available_tasks():
    """
    Get available task definitions
    """
    return {
        "tasks": ["easy", "medium", "hard"],
        "descriptions": {
            "easy": "Choosing which programming language to learn",
            "medium": "Choosing between two job offers",
            "hard": "Choosing between higher studies and switching careers"
        }
    }

@app.post("/baseline")
async def run_baseline(request: Dict[str, Any]):
    """
    Run baseline inference loop
    """
    print("START")
    print("STEP: Running baseline inference loop")
    
    task_type = request.get("task", "easy")
    env = get_env()
    agent = get_agent()
    
    print(f"STEP: Starting baseline on {task_type} task")
    
    # Reset environment
    observation = env.reset(task=task_type)
    done = False
    total_reward = 0
    steps = 0
    trajectory = []
    
    while not done and steps < 10:
        # Agent chooses action
        action = agent.choose_action(observation)
        
        # Environment step
        observation, reward, done, info = env.step(action)
        
        total_reward += reward
        steps += 1
        
        trajectory.append({
            "step": steps,
            "action": action,
            "reward": reward,
            "progress": observation["progress"]
        })
        
        print(f"STEP: Baseline step {steps} - Action: {action}, Reward: {reward}")
    
    print(f"STEP: Baseline complete - Total Reward: {total_reward}")
    print("END")
    
    return {
        "task": task_type,
        "total_reward": total_reward,
        "steps": steps,
        "trajectory": trajectory,
        "final_observation": observation
    }

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
except:
    pass

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "api_base": API_BASE_URL,
        "environment": "LifeDecisionEnv"
    }

if __name__ == "__main__":
    uvicorn.run("inference:app", host="0.0.0.0", port=8000, reload=True)
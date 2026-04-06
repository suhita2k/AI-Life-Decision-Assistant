"""
AI Life Decision Assistant - OpenEnv
Single File - All In One
"""

import os
import copy
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn

# ========================================
# ENVIRONMENT VARIABLES
# ========================================
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "mixtral-8x7b-32768")
HF_TOKEN = os.getenv("HF_TOKEN")
API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")

print(f"API_BASE_URL: {API_BASE_URL}")
print(f"MODEL_NAME: {MODEL_NAME}")
print(f"API_KEY configured: {bool(API_KEY)}")

# ========================================
# OPENAI CLIENT
# ========================================
client = None
try:
    from openai import OpenAI
    if API_KEY:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
        print("OpenAI client initialized successfully.")
    else:
        print("WARNING: No API key found. LLM features disabled.")
except Exception as e:
    print(f"Client init error: {e}")

# ========================================
# TASKS
# ========================================
TASKS = {
    "easy": {
        "difficulty": "easy",
        "name": "Programming Language Selection",
        "situation": "You are a beginner who wants to start learning programming. You have heard about Python, JavaScript, and Java, but you are not sure which one to start with. You have 3 months to dedicate to learning, and you are interested in web development and data science.",
        "goal": "Choose the most suitable programming language to learn first",
        "context": {"time_available": "3 months", "interests": ["web development", "data science"], "experience_level": "beginner", "options": ["Python", "JavaScript", "Java"]}
    },
    "medium": {
        "difficulty": "medium",
        "name": "Job Offer Selection",
        "situation": "You have received two job offers. Offer A: Startup Company - Salary 80000 dollars, Equity 0.5 percent, Remote, Fast-paced, Risk of instability. Offer B: Established Corporation - Salary 95000 dollars, No equity, Office-based with 1-hour commute, Fortune 500 stability. You value work-life balance, career growth, and financial security.",
        "goal": "Choose the job offer that best aligns with your career goals and personal values",
        "context": {"offers": ["Startup (Offer A)", "Corporation (Offer B)"], "values": ["work-life balance", "career growth", "financial security"]}
    },
    "hard": {
        "difficulty": "hard",
        "name": "Higher Studies vs Career Switch",
        "situation": "You are a 28-year-old software engineer with 5 years of experience earning 110000 dollars per year. Option 1: Pursue MBA at top business school - Cost 150000 dollars plus 2 years, potential product management career. Option 2: AI ML Specialization bootcamp - Cost 30000 dollars plus 6 months, join emerging field. Option 3: Stay on senior engineering track - No cost, technical leadership path. You have 50000 dollars savings, married, want to start family in 3-5 years.",
        "goal": "Make a strategic career decision optimizing for long-term fulfillment, financial security, and personal growth",
        "context": {"options": ["MBA", "AI/ML Specialization", "Stay Current Path"], "values": ["intellectual challenge", "impact", "financial security", "family"]}
    }
}

# ========================================
# REWARD SYSTEM
# ========================================
REWARD_MAP = {
    "analyze_problem": 0.2,
    "identify_factors": 0.2,
    "generate_options": 0.2,
    "evaluate_options": 0.2,
    "recommend_decision": 0.2
}
INVALID_PENALTY = -0.1
ACTION_SPACE = list(REWARD_MAP.keys())

# ========================================
# ENVIRONMENT
# ========================================
class LifeDecisionEnv:
    def __init__(self):
        self.current_state = None
        self.current_task = None
        self.step_count = 0
        self.max_steps = 10
        self.total_reward = 0.0

    def reset(self, task="easy"):
        if task not in TASKS:
            task = "easy"
        self.current_task = task
        t = TASKS[task]
        self.current_state = {
            "situation": t["situation"],
            "goal": t["goal"],
            "progress": 0.0,
            "history": []
        }
        self.step_count = 0
        self.total_reward = 0.0
        return copy.deepcopy(self.current_state)

    def step(self, action):
        if self.current_state is None:
            raise ValueError("Call reset first")
        if action not in ACTION_SPACE:
            self.total_reward += INVALID_PENALTY
            return copy.deepcopy(self.current_state), INVALID_PENALTY, False, {"error": "Invalid action", "valid_actions": ACTION_SPACE}
        reward = REWARD_MAP[action]
        self.total_reward += reward
        self.current_state["history"].append(action)
        self.step_count += 1
        self.current_state["progress"] = min(1.0, len(self.current_state["history"]) / len(ACTION_SPACE))
        done = action == "recommend_decision" or self.step_count >= self.max_steps or self.current_state["progress"] >= 1.0
        info = {"step": self.step_count, "total_reward": self.total_reward, "task": self.current_task}
        return copy.deepcopy(self.current_state), reward, done, info

    def state(self):
        if self.current_state is None:
            return None
        return {
            **copy.deepcopy(self.current_state),
            "step_count": self.step_count,
            "task": self.current_task,
            "total_reward": self.total_reward,
            "action_space": ACTION_SPACE
        }

# ========================================
# AGENT
# ========================================
class DecisionAgent:
    def __init__(self, c, m):
        self.client = c
        self.model = m

    def choose_action(self, obs):
        history = obs.get("history", [])
        for a in ACTION_SPACE:
            if a not in history:
                return a
        return "recommend_decision"

    def analyze(self, situation, goal):
        try:
            r = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional life decision advisor."},
                    {"role": "user", "content": f"Analyze: {situation}. Goal: {goal}. Give structured analysis."}
                ],
                max_tokens=1000
            )
            return r.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# ========================================
# INSTANCES
# ========================================
env = LifeDecisionEnv()
agent = DecisionAgent(client, MODEL_NAME) if client else None

# ========================================
# HTML
# ========================================
HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Life Decision Assistant</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:1rem}
.c{max-width:1000px;margin:0 auto;background:#f8fafc;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,.2);padding:2rem}
h{text-align:center;display:block;margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:2px solid #e2e8f0}
h h1{color:#6366f1;font-size:2rem}
.su{color:#64748b;margin-top:.3rem}
.s{background:#fff;border-radius:12px;padding:1.5rem;margin-bottom:1.2rem;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.s h2{color:#1e293b;font-size:1.2rem;margin-bottom:1rem}
.b{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.8rem}
.tb{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border:none;border-radius:10px;padding:1.1rem;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .3s}
.tb:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(99,102,241,.4)}
.tb span{display:block;font-size:.7rem;font-weight:400;margin-top:.2rem;opacity:.8}
.ab{background:#fff;border:2px solid #6366f1;color:#6366f1;border-radius:8px;padding:.7rem;font-size:.85rem;font-weight:600;cursor:pointer;transition:all .3s}
.ab:hover:not(:disabled){background:#6366f1;color:#fff}
.ab:disabled{opacity:.3;cursor:not-allowed}
.ab.dn{background:#10b981;border-color:#10b981;color:#fff}
.bb{background:#8b5cf6;color:#fff;border:none;border-radius:8px;padding:.7rem;font-size:.85rem;font-weight:600;cursor:pointer}
.bb:hover{background:#6366f1}
.si{margin-bottom:.8rem}
.si strong{display:block;color:#1e293b;margin-bottom:.3rem}
.si p{color:#64748b;padding:.5rem;background:#f1f5f9;border-radius:6px;border-left:4px solid #6366f1;line-height:1.5;font-size:.85rem}
.bar{position:relative;width:100%;height:26px;background:#e2e8f0;border-radius:13px;overflow:hidden}
.fill{height:100%;background:linear-gradient(90deg,#10b981,#6366f1);transition:width .5s;border-radius:13px}
.bt{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-weight:700;font-size:.8rem}
.sb{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;margin-bottom:.8rem}
.sc{background:#fff;padding:.5rem;border-radius:8px;text-align:center;border:1px solid #e2e8f0}
.sc .l{color:#64748b;font-size:.7rem}
.sc .v{color:#6366f1;font-size:1.1rem;font-weight:700}
.hc{max-height:200px;overflow-y:auto}
.hi{background:#f1f5f9;padding:.5rem;border-radius:6px;margin-bottom:.3rem;border-left:4px solid #6366f1;display:flex;justify-content:space-between;align-items:center}
.hr{background:#10b981;color:#fff;padding:.1rem .5rem;border-radius:10px;font-size:.75rem;font-weight:700}
.hr.n{background:#ef4444}
.em{text-align:center;color:#64748b;padding:1rem;font-style:italic;font-size:.85rem}
footer{text-align:center;margin-top:1rem;padding-top:.8rem;border-top:2px solid #e2e8f0;color:#64748b;font-size:.8rem}
</style>
</head><body>
<div class="c">
<h><h1>AI Life Decision Assistant</h1><p class="su">OpenEnv RL Environment</p></h>
<div class="s">
<h2>Status</h2>
<div class="sb">
<div class="sc"><div class="l">Progress</div><div class="v" id="pd">0%</div></div>
<div class="sc"><div class="l">Reward</div><div class="v" id="rd">0.00</div></div>
<div class="sc"><div class="l">Steps</div><div class="v" id="sd">0</div></div>
<div class="sc"><div class="l">Status</div><div class="v" id="std">Ready</div></div>
</div>
<div class="bar"><div class="fill" id="pf" style="width:0%"></div><span class="bt" id="pt">0%</span></div>
</div>
<div class="s">
<h2>Select Task</h2>
<div class="b">
<button class="tb" onclick="rst('easy')">Easy<span>Programming Language</span></button>
<button class="tb" onclick="rst('medium')">Medium<span>Job Offers</span></button>
<button class="tb" onclick="rst('hard')">Hard<span>Career Path</span></button>
</div>
</div>
<div class="s">
<h2>Situation</h2>
<div class="si"><p id="sit">Select a task above.</p></div>
<div class="si"><strong>Goal:</strong><p id="gl">-</p></div>
</div>
<div class="s">
<h2>Actions</h2>
<div class="b">
<button class="ab" id="a0" onclick="stp('analyze_problem')">Analyze Problem</button>
<button class="ab" id="a1" onclick="stp('identify_factors')">Identify Factors</button>
<button class="ab" id="a2" onclick="stp('generate_options')">Generate Options</button>
<button class="ab" id="a3" onclick="stp('evaluate_options')">Evaluate Options</button>
<button class="ab" id="a4" onclick="stp('recommend_decision')">Recommend Decision</button>
</div>
</div>
<div class="s">
<h2>History</h2>
<div class="hc" id="hi"><p class="em">No actions yet.</p></div>
</div>
<div class="s">
<h2>Baseline</h2>
<div class="b">
<button class="bb" onclick="bln('easy')">Run Easy</button>
<button class="bb" onclick="bln('medium')">Run Medium</button>
<button class="bb" onclick="bln('hard')">Run Hard</button>
</div>
<div id="br"></div>
</div>
<footer>
<p>OpenEnv | Groq LLM | FastAPI</p>
<div id="ax">Checking...</div>
</footer>
</div>
<script>
var tr=0,sc=0,B=location.origin;
function f(a){return a.split('_').map(w=>w[0].toUpperCase()+w.slice(1)).join(' ')}
function uP(p){var c=Math.round(p*100);document.getElementById('pf').style.width=c+'%';document.getElementById('pt').textContent=c+'%';document.getElementById('pd').textContent=c+'%'}
function uD(){document.getElementById('rd').textContent=tr.toFixed(2);document.getElementById('sd').textContent=sc}
async function rst(t){
try{
var r=await fetch(B+'/reset',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task:t})});
var d=await r.json();
if(d.error){alert('Error: '+d.error);return}
var o=d.observation;
document.getElementById('sit').textContent=o.situation;
document.getElementById('gl').textContent=o.goal;
uP(o.progress);tr=0;sc=0;uD();
document.getElementById('hi').innerHTML='<p class="em">Actions:</p>';
document.getElementById('std').textContent='Running';
document.getElementById('br').innerHTML='';
for(var i=0;i<5;i++){var e=document.getElementById('a'+i);e.disabled=false;e.classList.remove('dn')}
}catch(e){alert('Reset error: '+e.message)}
}
async function stp(a){
try{
var r=await fetch(B+'/step',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:a})});
var d=await r.json();
if(d.error){alert('Error: '+d.error);return}
tr+=d.reward;sc++;uP(d.observation.progress);uD();
var idx=['analyze_problem','identify_factors','generate_options','evaluate_options','recommend_decision'].indexOf(a);
document.getElementById('a'+idx).classList.add('dn');
var hc=document.getElementById('hi');
if(hc.querySelector('.em'))hc.innerHTML='';
var el=document.createElement('div');el.className='hi';
el.innerHTML='<span>'+f(a)+'</span><span class="hr'+(d.reward<0?' n':'')+'">+'+d.reward.toFixed(2)+'</span>';
hc.appendChild(el);hc.scrollTop=hc.scrollHeight;
if(d.done){
for(var j=0;j<5;j++)document.getElementById('a'+j).disabled=true;
document.getElementById('std').textContent='Done';
var m=tr>=0.9?'Perfect!':'Good!';
var dl=document.createElement('div');dl.className='hi';dl.style.background='#d1fae5';
dl.innerHTML='<strong>'+m+' Score: '+tr.toFixed(2)+'</strong>';hc.appendChild(dl);
}
}catch(e){alert('Step error: '+e.message)}
}
async function bln(t){
document.getElementById('br').innerHTML='<p>Running...</p>';
try{
var r=await fetch(B+'/baseline',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task:t})});
var d=await r.json();
var h='<div class="s"><h2>Baseline: '+t.toUpperCase()+'</h2>';
h+='<div class="sb"><div class="sc"><div class="l">Reward</div><div class="v">'+(d.total_reward||0).toFixed(2)+'</div></div>';
h+='<div class="sc"><div class="l">Steps</div><div class="v">'+(d.steps||0)+'</div></div></div>';
if(d.trajectory){d.trajectory.forEach(function(s){h+='<div class="hi"><span>S'+s.step+': '+f(s.action)+'</span><span class="hr">+'+s.reward.toFixed(2)+'</span></div>'})}
h+='</div>';document.getElementById('br').innerHTML=h;
}catch(e){document.getElementById('br').innerHTML='<p style="color:red">'+e.message+'</p>'}
}
fetch(B+'/health').then(r=>r.json()).then(d=>{
document.getElementById('ax').innerHTML=d.api_key_configured?'<span style="color:#10b981">API Ready</span>':'<span style="color:#f59e0b">No Key</span>';
}).catch(()=>{document.getElementById('ax').innerHTML='Offline'});
</script>
</body></html>"""

# ========================================
# MODELS
# ========================================
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

# ========================================
# APP
# ========================================
app = FastAPI(title="AI Life Decision Assistant", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ========================================
# ENDPOINTS
# ========================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "provider": "Groq",
        "model": MODEL_NAME,
        "api_key_configured": bool(API_KEY),
        "client_available": client is not None
    }

# POST /reset
@app.post("/reset")
async def post_reset(request: ResetRequest = None):
    print("START")
    print("STEP: Reset request")
    task = request.task if request else "easy"
    obs = env.reset(task=task)
    print(f"STEP: Reset done with task={task}")
    print("END")
    return {"observation": obs, "message": "Reset successful"}

# GET /reset (fallback)
@app.get("/reset")
async def get_reset(task: str = Query(default="easy")):
    print("START")
    print("STEP: Reset request (GET)")
    obs = env.reset(task=task)
    print(f"STEP: Reset done with task={task}")
    print("END")
    return {"observation": obs, "message": "Reset successful"}

# POST /step
@app.post("/step")
async def post_step(action: Action):
    print("START")
    print(f"STEP: Action={action.action}")
    if env.current_state is None:
        print("STEP: Not initialized")
        print("END")
        raise HTTPException(400, "Call /reset first")
    obs, reward, done, info = env.step(action.action)
    print(f"STEP: Reward={reward}, Done={done}")
    print("END")
    return StepResponse(observation=Observation(**obs), reward=reward, done=done, info=info)

# GET /step (fallback)
@app.get("/step")
async def get_step(action: str = Query(...)):
    print("START")
    print(f"STEP: Action={action} (GET)")
    if env.current_state is None:
        print("END")
        raise HTTPException(400, "Call /reset first")
    obs, reward, done, info = env.step(action)
    print(f"STEP: Reward={reward}, Done={done}")
    print("END")
    return StepResponse(observation=Observation(**obs), reward=reward, done=done, info=info)

# GET /state
@app.get("/state")
async def get_state():
    s = env.state()
    return {"state": s}

# GET /actions
@app.get("/actions")
async def get_actions():
    return {"actions": ACTION_SPACE}

# GET /tasks
@app.get("/tasks")
async def get_tasks():
    return {"tasks": list(TASKS.keys())}

# POST /analyze
@app.post("/analyze")
async def post_analyze(request: Dict[str, Any]):
    if not agent:
        return {"analysis": "No API key", "status": "error"}
    sit = request.get("situation", "")
    goal = request.get("goal", "")
    result = agent.analyze(sit, goal)
    return {"analysis": result, "status": "success"}

# POST /baseline
@app.post("/baseline")
async def post_baseline(request: Dict[str, Any]):
    print("START")
    task = request.get("task", "easy")
    obs = env.reset(task=task)
    done = False
    total = 0.0
    steps = 0
    traj = []
    while not done and steps < 10:
        if agent:
            a = agent.choose_action(obs)
        else:
            a = ACTION_SPACE[steps] if steps < len(ACTION_SPACE) else "recommend_decision"
        obs, reward, done, info = env.step(a)
        total += reward
        steps += 1
        traj.append({"step": steps, "action": a, "reward": reward, "progress": obs["progress"]})
    print(f"STEP: Baseline done: total={total}")
    print("END")
    return {"task": task, "total_reward": total, "steps": steps, "trajectory": traj}

if __name__ == "__main__":
    uvicorn.run("inference:app", host="0.0.0.0", port=8000)

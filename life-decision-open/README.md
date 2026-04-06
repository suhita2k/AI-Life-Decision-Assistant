# 🧠 AI Life Decision Assistant - OpenEnv Compliant

A fully-featured Reinforcement Learning environment for life decision-making, compliant with OpenEnv standards.

## 🌟 Features

- ✅ **OpenEnv Compliant** - Passes all automated checks
- 🎯 **RL Environment Interface** - Complete `reset()`, `step()`, `state()` implementation
- 🌐 **REST API** - FastAPI-based endpoints for environment interaction
- 🤖 **LLM Integration** - OpenAI-compatible reasoning agent
- 📊 **Deterministic Tasks** - Three difficulty levels (Easy, Medium, Hard)
- 📈 **Automated Grading** - Deterministic scoring system
- 🎨 **Modern UI** - Responsive frontend for human interaction
- 🔄 **Baseline Agent** - Reference implementation for evaluation

---

## 🏗️ Architecture

### Environment

**Class**: `LifeDecisionEnv`  
**Location**: `env/environment.py`

#### Observation Space
```python
{
    "situation": str,      # Decision scenario description
    "goal": str,          # Desired outcome
    "progress": float,    # Completion (0.0 to 1.0)
    "history": list       # Action sequence
}
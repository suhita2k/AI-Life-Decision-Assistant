[project]
name = "life-decision-openenv"
version = "2.0.0"
description = "AI Life Decision Assistant - OpenEnv RL Environment"
requires-python = ">=3.11"
license = "MIT"
dependencies = [
    "openenv-core>=0.2.0",
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
    "openai>=1.3.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
]

[project.scripts]
server = "server.app:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

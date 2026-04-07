FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

RUN printf '[project]\nname = "life-decision-openenv"\nversion = "2.0.0"\nrequires-python = ">=3.11"\ndependencies = [\n    "openenv-core>=0.2.0",\n    "fastapi>=0.104.0",\n    "uvicorn[standard]>=0.24.0",\n    "pydantic>=2.5.0",\n    "openai>=1.3.0",\n    "python-dotenv>=1.0.0",\n    "requests>=2.31.0",\n]\n[project.scripts]\nopenenv = "server.app:main"\n' > /app/pyproject.toml

RUN uv lock

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "server/app.py"]

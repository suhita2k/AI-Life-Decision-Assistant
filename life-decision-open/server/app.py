from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Life Decision Assistant running successfully"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import uuid
import random

from models import Action, Observation, State, StepResult
from server.environment import EmailEnvironment
from server.grader import grade_response

app = FastAPI(title="Email Environment API", version="1.0.0")

# Store active environments
env_store = {}

class ResetRequest(BaseModel):
    pass

class StepRequest(BaseModel):
    action: Action

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Email Environment API is ready",
        "endpoints": {
            "reset": "POST /reset",
            "step": "POST /step",
            "state": "GET /state/{episode_id}"
        }
    }

@app.post("/reset", response_model=StepResult)
async def reset_environment():
    """
    Start a new episode and get the first email
    
    This endpoint accepts POST requests and returns initial observation.
    Compatible with OpenEnv validation requirements.
    """
    # Create new environment instance
    episode_id = str(uuid.uuid4())
    env = EmailEnvironment()
    
    # Initialize and get first observation
    observation = env.reset()
    
    # Store environment
    env_store[episode_id] = {
        "env": env,
        "step_count": 0,
        "episode_id": episode_id
    }
    
    # Return StepResult as required by OpenEnv spec
    return StepResult(
        observation=observation,
        reward=0.0,
        done=False
    )

@app.post("/step", response_model=StepResult)
async def step_episode(episode_id: str, request: StepRequest):
    """
    Submit a response and get the next observation
    """
    if episode_id not in env_store:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    env_data = env_store[episode_id]
    env = env_data["env"]
    step_count = env_data["step_count"]
    
    # Execute action
    observation, reward, done = env.step(request.action)
    
    # Update step count
    step_count += 1
    env_data["step_count"] = step_count
    
    # Clean up if episode is done
    if done:
        del env_store[episode_id]
    
    return StepResult(
        observation=observation,
        reward=reward,
        done=done
    )

@app.get("/state/{episode_id}", response_model=State)
async def get_state(episode_id: str):
    """
    Get current episode metadata
    """
    if episode_id not in env_store:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    env_data = env_store[episode_id]
    
    return State(
        episode_id=episode_id,
        step_count=env_data["step_count"]
    )

@app.get("/docs")
async def get_docs():
    """Swagger UI documentation"""
    return {
        "message": "Visit /docs for interactive API documentation"
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()

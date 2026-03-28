from pydantic import BaseModel

class Action(BaseModel):
    response: str

class Observation(BaseModel):
    email: str
    difficulty: str

class State(BaseModel):
    episode_id: str
    step_count: int

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
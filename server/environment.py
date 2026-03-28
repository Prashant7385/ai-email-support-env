from typing import Tuple
from models import Action, Observation
import random

class EmailEnvironment:
    """
    Email simulation environment for training AI agents.
    
    The environment presents customer emails with varying difficulty levels
    and evaluates agent responses based on politeness, helpfulness, and relevance.
    """
    
    # Sample customer emails by difficulty
    EMAILS = {
        "easy": [
            "Hi, I just wanted to ask if you offer international shipping? Thanks!",
            "Hello, what are your business hours? I'd like to visit your store.",
            "Can you tell me more about your warranty policy? Thank you.",
            "Do you have a loyalty program? I shop here frequently.",
        ],
        "medium": [
            "I ordered a blue shirt but received a red one. Can you help me exchange it?",
            "My package was supposed to arrive yesterday but it's still showing 'in transit'. What's happening?",
            "The product I received doesn't match the description on your website. It's missing several features.",
            "I've been trying to reach customer service for 3 days with no response. This is frustrating.",
        ],
        "hard": [
            "This is the third time I'm writing! My refund still hasn't been processed after 2 weeks. I want my money back NOW!",
            "Your product broke after one use and your support team has been completely unhelpful. I'm disputing this with my credit card company!",
            "I'm extremely disappointed. The item arrived damaged, and now you're asking me to pay for return shipping? Unacceptable!",
            "I've been a loyal customer for 5 years but this experience has made me reconsider. Fix this immediately or I'm taking my business elsewhere!",
        ]
    }
    
    def __init__(self, max_steps: int = 10):
        self.max_steps = max_steps
        self.current_step = 0
        self.current_email = None
        self.current_difficulty = None
        self.episode_history = []
        
    def reset(self) -> Observation:
        """
        Start a new episode with a random email.
        
        Returns:
            Observation containing the email and difficulty level
        """
        self.current_step = 0
        self.episode_history = []
        
        # Randomly select difficulty and email
        self.current_difficulty = random.choice(["easy", "medium", "hard"])
        self.current_email = random.choice(self.EMAILS[self.current_difficulty])
        
        return Observation(
            email=self.current_email,
            difficulty=self.current_difficulty
        )
    
    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        """
        Process agent's action (response) and return results.
        
        Args:
            action: Agent's response to the email
            
        Returns:
            Tuple of (observation, reward, done)
            - observation: Next observation (None if episode ends)
            - reward: Score from 0.0 to 1.0
            - done: Whether the episode is complete
        """
        self.current_step += 1
        
        # Grade the response
        from server.grader import grade_response
        reward = grade_response(
            email=self.current_email,
            response=action.response,
            difficulty=self.current_difficulty
        )
        
        # Store in history
        self.episode_history.append({
            "step": self.current_step,
            "email": self.current_email,
            "response": action.response,
            "reward": reward
        })
        
        # Check if episode should end
        done = self.current_step >= self.max_steps
        
        # Get next observation if not done
        if not done:
            # Move to next difficulty level or stay at same
            self.current_difficulty = random.choice(["easy", "medium", "hard"])
            self.current_email = random.choice(self.EMAILS[self.current_difficulty])
            
            observation = Observation(
                email=self.current_email,
                difficulty=self.current_difficulty
            )
        else:
            observation = None
            
        return observation, reward, done
    
    def get_state(self) -> dict:
        """Get current environment state"""
        return {
            "step": self.current_step,
            "max_steps": self.max_steps,
            "difficulty": self.current_difficulty,
            "history": self.episode_history
        }

import re

def grade_response(email: str, response: str, difficulty: str) -> float:
    """
    Grade the agent's response based on multiple criteria.
    
    Args:
        email: The customer's email
        response: The agent's response
        difficulty: Difficulty level (easy, medium, hard)
        
    Returns:
        Reward score from 0.0 to 1.0
    """
    # Initialize scores for each criterion
    politeness_score = 0.0
    helpfulness_score = 0.0
    relevance_score = 0.0
    
    # Convert to lowercase for analysis
    response_lower = response.lower()
    email_lower = email.lower()
    
    # === 1. Politeness Score (0.3 weight) ===
    polite_indicators = [
        "thank", "thanks", "please", "dear", "regards", 
        "sincerely", "appreciate", "sorry", "apologize",
        "happy to help", "welcome", "kindly"
    ]
    
    polite_count = sum(1 for indicator in polite_indicators if indicator in response_lower)
    politeness_score = min(polite_count * 0.15, 1.0)  # Cap at 1.0
    
    # Check for professional greeting and closing
    has_greeting = bool(re.search(r'^(hi|hello|dear|good morning|good afternoon)', response_lower))
    has_closing = bool(re.search(r'(regards|thanks|sincerely|best|warmly)$', response_lower.strip()))
    
    if has_greeting:
        politeness_score = min(politeness_score + 0.2, 1.0)
    if has_closing:
        politeness_score = min(politeness_score + 0.2, 1.0)
    
    # === 2. Helpfulness Score (0.3 weight) ===
    helpful_indicators = [
        "can help", "will help", "solution", "resolve", "fix",
        "assist", "support", "refund", "exchange", "replacement",
        "tracking", "shipping", "delivery", "order", "information"
    ]
    
    helpful_count = sum(1 for indicator in helpful_indicators if indicator in response_lower)
    helpfulness_score = min(helpful_count * 0.12, 1.0)  # Cap at 1.0
    
    # Check if response provides actionable information
    action_words = ["will", "can", "let me", "i'll", "we can", "we will"]
    if any(word in response_lower for word in action_words):
        helpfulness_score = min(helpfulness_score + 0.2, 1.0)
    
    # === 3. Context Relevance Score (0.4 weight) ===
    # Check if response mentions key terms from the email
    email_words = set(email_lower.split())
    response_words = set(response_lower.split())
    
    # Remove common stop words
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being"}
    email_words = email_words - stop_words
    
    if email_words:
        overlap = len(email_words & response_words)
        relevance_score = min(overlap / max(len(email_words), 1), 1.0)
    
    # Bonus for addressing specific issues based on difficulty
    if difficulty == "easy":
        if any(word in response_lower for word in ["question", "inquiry", "information"]):
            relevance_score = min(relevance_score + 0.2, 1.0)
    elif difficulty == "medium":
        if any(word in response_lower for word in ["issue", "problem", "concern", "understand"]):
            relevance_score = min(relevance_score + 0.2, 1.0)
    elif difficulty == "hard":
        if any(word in response_lower for word in ["apologize", "sorry", "urgent", "priority", "escalate"]):
            relevance_score = min(relevance_score + 0.3, 1.0)
    
    # === Calculate Final Weighted Score ===
    final_score = (
        politeness_score * 0.3 +      # 30% politeness
        helpfulness_score * 0.3 +     # 30% helpfulness
        relevance_score * 0.4         # 40% relevance
    )
    
    # Ensure score is between 0.0 and 1.0
    return max(0.0, min(1.0, final_score))


# Test function for debugging
if __name__ == "__main__":
    test_email = "I ordered a blue shirt but received a red one. Can you help me exchange it?"
    test_response = """Dear Customer,

Thank you for reaching out. I sincerely apologize for the mix-up with your order. We understand how frustrating this must be.

We will be happy to help you with an exchange. Please let us know your preferred color, and we'll arrange for a replacement to be sent immediately.

Best regards,
Customer Support"""
    
    score = grade_response(test_email, test_response, "medium")
    print(f"Response Score: {score:.2f}")

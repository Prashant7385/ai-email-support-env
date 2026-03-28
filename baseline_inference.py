"""
Baseline Inference Script for Email Environment

This script demonstrates the email environment with baseline agent responses
and provides reproducible scores for evaluation.

Usage:
    python baseline_inference.py
    
    Or with custom episodes:
    python baseline_inference.py --episodes 5
"""

import argparse
import json
from typing import List, Dict
from server.environment import EmailEnvironment
from server.grader import grade_response
from models import Action


# Baseline response templates by difficulty
BASELINE_RESPONSES = {
    "easy": [
        "Hello! Thank you for your inquiry. Yes, we do offer international shipping to most countries. Shipping costs and delivery times vary by location. Please visit our shipping page for detailed information. Is there anything else I can help you with? Best regards, Customer Support",
        "Hi there! Thanks for reaching out. Our business hours are Monday-Friday 9AM-6PM EST, and Saturday 10AM-4PM EST. We're closed on Sundays. Feel free to visit us during these times! Regards, The Team",
        "Dear Customer, Thank you for your interest in our warranty policy. All our products come with a standard 1-year manufacturer warranty covering defects. Extended warranty options are also available at checkout. Happy to help if you have more questions! Sincerely, Support Team",
        "Hello! Yes, we do have a loyalty program called 'VIP Rewards'. You earn points on every purchase which can be redeemed for discounts. Sign up is free on our website! Thanks for being a valued customer. Best, Customer Care"
    ],
    "medium": [
        "Dear Valued Customer, I sincerely apologize for the mix-up with your order. This is not the level of service we strive for. I will immediately arrange an exchange for the correct blue shirt. You'll receive a prepaid return label via email within 2 hours. The replacement will be shipped express at no cost. Again, my apologies for this inconvenience. Warm regards, Support Manager",
        "Hello, I understand your concern about the delayed package. Let me help you with this. I've checked with our shipping partner and your package is currently in transit. Due to high volume, there's a 1-2 day delay. Your package should arrive by tomorrow evening. I'll send you updated tracking info right away. Thank you for your patience. Best regards, Customer Service",
        "Dear Customer, I apologize that the product didn't match the description. This is concerning feedback. I'd like to make this right immediately. I can offer you either a full refund including shipping, or we can send the correct product with all features as described. Please let me know your preference. We value your business! Sincerely, Customer Relations",
        "Hello, I sincerely apologize for the lack of response from our team. This is unacceptable. I'm escalating your case to priority status. A senior support agent will contact you within 4 hours via phone or email, whichever you prefer. Your issue is important to us and we will resolve this today. My deepest apologies for the frustration caused. Kind regards, Support Director"
    ],
    "hard": [
        "Dear Valued Customer, I am deeply sorry for the unacceptable delay in processing your refund. This falls far short of our standards. I have personally escalated this to our finance team and your refund has been processed immediately - you should see it in 2-3 business days. Additionally, I'm adding a 20% credit to your account for this trouble. I will personally monitor this to ensure it's resolved. My sincerest apologies. Direct line: 555-0123. Respectfully, VP Customer Experience",
        "Dear Customer, I am truly horrified to hear about your experience. This is absolutely not acceptable. I am taking personal responsibility for this situation. First, we will send a replacement product overnight at our expense. Second, I'm issuing a full refund for your original purchase. Third, I'm adding a $50 credit for the frustration caused. You have my word this will be fixed TODAY. I'll call you personally within 1 hour. Deepest apologies, CEO Office",
        "Hello, I completely understand your anger and frustration. You're absolutely right - asking you to pay return shipping for a damaged item is wrong. Here's what I'm doing immediately: 1) Full refund processed today, 2) Prepaid return label sent (no cost to you), 3) $30 credit for the inconvenience, 4) Free expedited shipping on your next order. I know this doesn't undo the frustration, but I hope it shows we're committed to making this right. Sincerely apologetic, Customer Experience Manager",
        "Dear Loyal Customer, First, thank you for 5 years of trust in us. I am heartbroken that we've disappointed you now. I've reviewed your entire history and this situation. Here's my commitment: 1) Immediate full refund + 25% bonus for your loyalty, 2) Free return shipping with prepaid label, 3) Priority VIP status on all future orders, 4) Personal guarantee from me on any future issues. I know trust is earned, and I hope we can rebuild yours. You mean everything to us. With sincere gratitude and apologies, Head of Customer Success"
    ]
}


def run_baseline_episode(env: EmailEnvironment, episode_num: int) -> Dict:
    """Run a single episode with baseline responses"""
    print(f"\n{'='*60}")
    print(f"EPISODE {episode_num}")
    print('='*60)
    
    # Reset environment
    observation = env.reset()
    total_reward = 0.0
    step_count = 0
    rewards = []
    
    print(f"\n📧 EMAIL #{step_count + 1}")
    print(f"Difficulty: {observation.difficulty.upper()}")
    print(f"Message: \"{observation.email}\"")
    
    while True:
        # Select baseline response based on difficulty
        difficulty = observation.difficulty
        response_text = BASELINE_RESPONSES[difficulty][0]  # Use first template
        
        # Create action
        action = Action(response=response_text)
        
        # Take step
        next_observation, reward, done = env.step(action)
        
        step_count += 1
        total_reward += reward
        rewards.append(reward)
        
        print(f"\n✅ Step {step_count}:")
        print(f"   Reward: {reward:.3f}")
        print(f"   Response length: {len(response_text)} chars")
        
        # Show grading breakdown
        politeness = sum(1 for word in ["thank", "please", "regards", "apologize", "sorry"] 
                        if word in response_text.lower()) * 0.15
        helpfulness = sum(1 for word in ["help", "resolve", "fix", "support", "refund"] 
                         if word in response_text.lower()) * 0.12
        relevance = len(set(observation.email.lower().split()) & set(response_text.lower().split())) / 10
        
        print(f"   → Politeness: ~{min(politeness + 0.4, 1.0):.2f}")
        print(f"   → Helpfulness: ~{min(helpfulness + 0.4, 1.0):.2f}")
        print(f"   → Relevance: ~{min(relevance, 1.0):.2f}")
        
        if done or next_observation is None:
            break
            
        observation = next_observation
        
        # Show next email if continuing
        if step_count < env.max_steps:
            print(f"\n📧 EMAIL #{step_count + 1}")
            print(f"Difficulty: {observation.difficulty.upper()}")
            print(f"Message: \"{observation.email}\"")
    
    avg_reward = total_reward / step_count
    
    results = {
        "episode": episode_num,
        "total_steps": step_count,
        "total_reward": round(total_reward, 4),
        "average_reward": round(avg_reward, 4),
        "rewards_per_step": [round(r, 4) for r in rewards]
    }
    
    print(f"\n📊 EPISODE {episode_num} SUMMARY:")
    print(f"   Steps: {step_count}")
    print(f"   Total Reward: {total_reward:.4f}")
    print(f"   Average Reward: {avg_reward:.4f}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Baseline Inference for Email Environment")
    parser.add_argument("--episodes", type=int, default=3, 
                       help="Number of episodes to run (default: 3)")
    parser.add_argument("--output", type=str, default=None,
                       help="Output file to save results (JSON format)")
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🤖 EMAIL ENVIRONMENT - BASELINE INFERENCE")
    print("="*60)
    print("\nRunning baseline agent with pre-defined response templates...")
    print(f"Number of episodes: {args.episodes}")
    
    all_results = []
    all_rewards = []
    
    for i in range(args.episodes):
        env = EmailEnvironment(max_steps=5)  # Shorter episodes for demo
        results = run_baseline_episode(env, i + 1)
        all_results.append(results)
        all_rewards.extend(results["rewards_per_step"])
    
    # Overall statistics
    overall_avg = sum(all_rewards) / len(all_rewards) if all_rewards else 0.0
    min_reward = min(all_rewards) if all_rewards else 0.0
    max_reward = max(all_rewards) if all_rewards else 0.0
    
    print("\n" + "="*60)
    print("📈 OVERALL RESULTS")
    print("="*60)
    print(f"Total Episodes: {args.episodes}")
    print(f"Total Steps: {len(all_rewards)}")
    print(f"Average Reward: {overall_avg:.4f}")
    print(f"Min Reward: {min_reward:.4f}")
    print(f"Max Reward: {max_reward:.4f}")
    print(f"Reward Range: 0.0 - 1.0")
    print("="*60 + "\n")
    
    # Save results if requested
    if args.output:
        output_data = {
            "config": {
                "episodes": args.episodes,
                "steps_per_episode": 5
            },
            "episodes": all_results,
            "summary": {
                "total_episodes": args.episodes,
                "total_steps": len(all_rewards),
                "average_reward": round(overall_avg, 4),
                "min_reward": round(min_reward, 4),
                "max_reward": round(max_reward, 4)
            }
        }
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"💾 Results saved to: {args.output}\n")
    
    return overall_avg


if __name__ == "__main__":
    main()

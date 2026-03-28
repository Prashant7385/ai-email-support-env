"""
OpenEnv Inference Script

This is the main inference script for the email environment.
Run this to test your environment with baseline responses.

Usage:
    python inference.py
    
Or with arguments:
    python inference.py --episodes 5 --verbose
"""

import argparse
import json
import sys
from typing import List, Dict, Tuple
from datetime import datetime

# Import environment components
from server.environment import EmailEnvironment
from server.grader import grade_response
from models import Action, Observation, StepResult


class BaselineAgent:
    """Simple rule-based agent for baseline inference"""
    
    def __init__(self):
        self.response_templates = {
            "easy": self._get_easy_responses(),
            "medium": self._get_medium_responses(),
            "hard": self._get_hard_responses()
        }
    
    def _get_easy_responses(self) -> List[str]:
        return [
            "Hello! Thank you for contacting us. Yes, we offer international shipping to most countries worldwide. Shipping costs vary by location, typically ranging from $10-30. Delivery time is usually 7-14 business days. You can find detailed shipping information on our website's FAQ page. Is there anything else I can assist you with today? Best regards, Customer Support Team",
            "Hi there! Thanks for reaching out. Our store hours are Monday through Friday, 9:00 AM to 6:00 PM Eastern Time, and Saturday 10:00 AM to 4:00 PM. We're closed on Sundays and major holidays. You can visit us at our downtown location or shop online 24/7! Feel free to call us at 1-800-EXAMPLE during business hours. Warm regards, The Team",
            "Dear Valued Customer, Thank you for your inquiry about our warranty policy. All our products come with a comprehensive 2-year manufacturer warranty that covers any defects in materials or workmanship. Extended warranty plans are also available for purchase. If you experience any issues, simply contact our support team and we'll handle it promptly. Happy shopping! Sincerely, Customer Care",
            "Hello! Absolutely, we have an excellent loyalty program called 'Rewards Plus'! It's completely free to join and you'll earn points on every purchase (1 point per $1 spent). Points can be redeemed for discounts, free shipping, or exclusive products. Members also get early access to sales and birthday rewards! Sign up takes just 2 minutes on our website. Thanks for being a valued customer! Best, Customer Relations"
        ]
    
    def _get_medium_responses(self) -> List[str]:
        return [
            "Dear Valued Customer, I sincerely apologize for the confusion with your order. I completely understand how frustrating it must be to receive the wrong item. This is not the standard of service we strive for. I'm immediately arranging an exchange for the correct blue shirt in your size. You'll receive a prepaid return shipping label via email within the next hour, and I'm expediting the replacement at no additional cost. The new item will arrive within 2-3 business days. Again, my deepest apologies for this inconvenience. Please don't hesitate to contact me directly if you need anything else. Warm regards, Sarah M., Customer Support Manager",
            "Hello, Thank you for your patience. I've looked into your order status and I see that your package is currently in transit. Due to unexpectedly high order volumes this week, there has been a slight delay of 1-2 days beyond our usual delivery timeframe. According to the latest tracking update, your package is at the regional distribution center and should be delivered by tomorrow evening (by 8 PM). I've sent you the updated tracking link to your email. As a gesture of goodwill for this delay, I've added a $5 credit to your account. We truly appreciate your understanding. Best regards, Michael T., Logistics Support",
            "Dear Customer, I'm genuinely concerned to hear that the product didn't match our website description. This is very important feedback and I take it seriously. First, I want to make this absolutely right for you. I can offer you two options: 1) A full refund including your original shipping costs, processed immediately, or 2) We send you the correct product with all features as described, plus a 20% discount on your next order as an apology. Both options include free return shipping for the incorrect item. Please let me know which solution you prefer, and I'll personally ensure it's handled today. We value your trust and want to restore your confidence in us. Sincerely, Jennifer L., Customer Relations Director",
            "Hello, I am truly sorry for the lack of response from our team over the past 3 days. This falls far short of our commitment to responsive customer service, and I understand your frustration. I'm escalating your case to priority status immediately. Here's what will happen: Within the next 2 hours, one of our senior support specialists will contact you via your preferred method (phone or email) to resolve your issue. I'm also adding a $15 credit to your account for this unacceptable delay. Your issue is now flagged as urgent and will be resolved today. My personal apologies for letting you down. Kind regards, David R., Support Team Lead"
        ]
    
    def _get_hard_responses(self) -> List[str]:
        return [
            "Dear Valued Customer, I am deeply apologetic and embarrassed by the unacceptable delay in processing your refund. You have every right to be upset - waiting 2 weeks is inexcusable. I've personally intervened and contacted our finance department. Your refund has been processed RIGHT NOW with priority status - you will see the funds in your account within 24-48 hours (expedited at our expense). Additionally, I'm adding a 25% credit ($XX.XX) to your account as compensation for this terrible experience. I've also attached a direct phone number (555-0199) where you can reach me personally if you need anything. This is on us, and we will do better. My sincerest apologies, Robert K., VP of Customer Experience",
            "Dear Customer, I am horrified to read about your experience. A product breaking after one use is completely unacceptable, and the lack of helpful response from our team compounds this failure. I am taking personal responsibility for this situation. Here's what I'm doing immediately: 1) Sending a brand new replacement via overnight express shipping (arrives tomorrow), 2) Issuing a full refund of your original purchase price, 3) Adding a $75 credit to your account for the frustration and inconvenience caused. I know this doesn't undo your negative experience, but I hope it demonstrates our commitment to making this right. I will also be conducting a thorough review with our quality and support teams to prevent this from happening again. You deserve so much better. Deepest apologies, Amanda Chen, Chief Operations Officer",
            "Hello, You are absolutely right - asking you to pay return shipping for a damaged item is wrong, and I apologize without reservation. This is not how we treat valued customers, especially when we failed to deliver a product in acceptable condition. Here's my commitment to you: 1) Full refund processed TODAY (you'll receive confirmation email within 1 hour), 2) Prepaid return label sent to your email - completely free, no cost whatsoever to you, 3) $40 credit added to your account immediately for the inconvenience and frustration, 4) Free expedited shipping on your next three orders, no minimum purchase required. I understand if you've lost trust in us, but I hope these actions show we're serious about earning back your business. With sincere apologies, Marcus Thompson, Head of Customer Success",
            "Dear Loyal Customer, First and foremost, thank you for 5 years of trust and support. Reading that we've disappointed you after all this time breaks my heart. I've personally reviewed your entire customer history and the details of this situation. You've been more than patient, and we've fallen short. Here's my commitment to you: 1) Immediate full refund PLUS a 30% bonus credit for your loyalty, 2) Free prepaid return shipping - just print the label I'm emailing you, 3) Lifetime VIP status on your account - priority support, exclusive discounts, and free expedited shipping on ALL future orders, 4) My personal guarantee that any future issues will be handled immediately by me directly. I know trust is earned over time, and I hope we can rebuild yours. You mean everything to us, and we will do better. With profound gratitude and apologies, Patricia Williams, Chief Customer Officer, Direct line: 555-0123"
        ]
    
    def get_response(self, observation: Observation) -> str:
        """Generate response based on email difficulty"""
        difficulty = observation.difficulty
        templates = self.response_templates.get(difficulty, self.response_templates["easy"])
        
        # Select template based on email content hash for consistency
        email_hash = hash(observation.email) % len(templates)
        return templates[email_hash]


def run_episode(env: EmailEnvironment, agent: BaselineAgent, episode_num: int, verbose: bool = True) -> Dict:
    """Run a single episode"""
    if verbose:
        print(f"\n{'='*70}")
        print(f"EPISODE {episode_num}")
        print('='*70)
    
    # Reset environment
    observation = env.reset()
    total_reward = 0.0
    step_count = 0
    rewards = []
    interactions = []
    
    if verbose:
        print(f"\n📧 EMAIL #{step_count + 1}")
        print(f"Difficulty: {observation.difficulty.upper()}")
        print(f"Message: \"{observation.email}\"\n")
    
    while True:
        # Get agent response
        response_text = agent.get_response(observation)
        action = Action(response=response_text)
        
        # Take step
        next_observation, reward, done = env.step(action)
        
        step_count += 1
        total_reward += reward
        rewards.append(reward)
        
        # Store interaction
        interactions.append({
            "step": step_count,
            "email": observation.email,
            "difficulty": observation.difficulty,
            "response_length": len(response_text),
            "reward": round(reward, 4)
        })
        
        if verbose:
            print(f"✅ Step {step_count}:")
            print(f"   Reward: {reward:.4f}")
            print(f"   Response: {len(response_text)} characters")
            
            # Show approximate breakdown
            politeness_indicators = sum(1 for word in ["thank", "please", "regards", "apologize", "sorry"] 
                                      if word in response_text.lower())
            helpfulness_indicators = sum(1 for word in ["help", "resolve", "fix", "support", "refund"] 
                                       if word in response_text.lower())
            
            print(f"   → Politeness indicators: ~{politeness_indicators}")
            print(f"   → Helpfulness indicators: ~{helpfulness_indicators}")
            print(f"   → Estimated score: {reward:.2f}/1.00")
        
        # Check if done
        if done or next_observation is None:
            break
        
        observation = next_observation
        
        if verbose and step_count < env.max_steps:
            print(f"\n📧 EMAIL #{step_count + 1}")
            print(f"Difficulty: {observation.difficulty.upper()}")
            print(f"Message: \"{observation.email}\"\n")
    
    avg_reward = total_reward / step_count if step_count > 0 else 0.0
    
    results = {
        "episode": episode_num,
        "total_steps": step_count,
        "total_reward": round(total_reward, 4),
        "average_reward": round(avg_reward, 4),
        "rewards_per_step": [round(r, 4) for r in rewards],
        "interactions": interactions
    }
    
    if verbose:
        print(f"\n📊 EPISODE {episode_num} SUMMARY:")
        print(f"   Steps completed: {step_count}")
        print(f"   Total reward: {total_reward:.4f}")
        print(f"   Average reward: {avg_reward:.4f}")
        print(f"   Min reward: {min(rewards):.4f}")
        print(f"   Max reward: {max(rewards):.4f}")
    
    return results


def validate_environment() -> bool:
    """Validate that the environment meets OpenEnv requirements"""
    print("\n" + "="*70)
    print("🔍 OPENENV VALIDATION")
    print("="*70)
    
    checks_passed = 0
    total_checks = 7
    
    # Check 1: Environment initialization
    try:
        env = EmailEnvironment()
        print("✓ Environment initializes correctly")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Environment initialization failed: {e}")
        return False
    
    # Check 2: Reset returns Observation
    try:
        obs = env.reset()
        assert isinstance(obs, Observation), "Reset must return Observation"
        assert hasattr(obs, 'email'), "Observation must have 'email' field"
        assert hasattr(obs, 'difficulty'), "Observation must have 'difficulty' field"
        print("✓ reset() returns valid Observation")
        checks_passed += 1
    except Exception as e:
        print(f"✗ reset() validation failed: {e}")
    
    # Check 3: Step returns correct tuple
    reward_check = None
    try:
        agent = BaselineAgent()
        response = agent.get_response(obs)
        action = Action(response=response)
        next_obs, reward_check, done = env.step(action)
        assert next_obs is None or isinstance(next_obs, Observation), "Step must return Observation or None"
        assert isinstance(reward_check, (int, float)), "Reward must be a number"
        assert isinstance(done, bool), "Done must be boolean"
        print("✓ step() returns (observation, reward, done)")
        checks_passed += 1
    except Exception as e:
        print(f"✗ step() validation failed: {e}")
    
    # Check 4: Reward range is 0.0 to 1.0
    try:
        if reward_check is not None:
            assert 0.0 <= reward_check <= 1.0, f"Reward must be in [0.0, 1.0], got {reward_check}"
            print("✓ Reward in valid range [0.0, 1.0]")
            checks_passed += 1
        else:
            print("✗ Reward range check skipped (no reward from step)")
    except Exception as e:
        print(f"✗ Reward range validation failed: {e}")
    
    # Check 5: Multiple difficulty levels exist
    try:
        difficulties_seen = set()
        for _ in range(20):
            env2 = EmailEnvironment()
            obs2 = env2.reset()
            difficulties_seen.add(obs2.difficulty)
        
        assert len(difficulties_seen) >= 3, "Must have at least 3 difficulty levels"
        print(f"✓ Multiple difficulty levels present: {difficulties_seen}")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Difficulty levels validation failed: {e}")
    
    # Check 6: Models are properly typed
    try:
        from models import Action, Observation, State, StepResult
        assert Action.model_fields is not None, "Action must be a Pydantic model"
        assert Observation.model_fields is not None, "Observation must be a Pydantic model"
        print("✓ Typed Pydantic models defined")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Model typing validation failed: {e}")
    
    # Check 7: openenv.yaml exists
    try:
        import yaml
        with open('openenv.yaml', 'r') as f:
            config = yaml.safe_load(f)
        assert 'name' in config, "openenv.yaml must have 'name' field"
        assert 'description' in config, "openenv.yaml must have 'description' field"
        print("✓ openenv.yaml configuration present")
        checks_passed += 1
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
    
    print("\n" + "="*70)
    print(f"VALIDATION RESULT: {checks_passed}/{total_checks} checks passed")
    print("="*70)
    
    return checks_passed == total_checks


def main():
    parser = argparse.ArgumentParser(description="OpenEnv Inference Script")
    parser.add_argument("--episodes", type=int, default=3, 
                       help="Number of episodes to run (default: 3)")
    parser.add_argument("--output", type=str, default=None,
                       help="Save results to JSON file")
    parser.add_argument("--validate", action="store_true",
                       help="Run validation checks before inference")
    parser.add_argument("--quiet", action="store_true",
                       help="Minimal output (only summary)")
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    print("\n" + "="*70)
    print("🤖 OPENENV EMAIL ENVIRONMENT - INFERENCE")
    print("="*70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Episodes: {args.episodes}")
    print(f"Max steps per episode: 5")
    
    # Run validation if requested
    if args.validate:
        is_valid = validate_environment()
        if not is_valid:
            print("\n⚠️  Validation failed! Proceeding anyway...")
        else:
            print("\n✅ All validation checks passed!")
    
    # Initialize agent and run episodes
    agent = BaselineAgent()
    all_results = []
    all_rewards = []
    
    for i in range(args.episodes):
        env = EmailEnvironment(max_steps=5)
        results = run_episode(env, agent, i + 1, verbose=verbose)
        all_results.append(results)
        all_rewards.extend(results["rewards_per_step"])
    
    # Calculate overall statistics
    overall_avg = sum(all_rewards) / len(all_rewards) if all_rewards else 0.0
    min_reward = min(all_rewards) if all_rewards else 0.0
    max_reward = max(all_rewards) if all_rewards else 0.0
    std_dev = (sum((r - overall_avg)**2 for r in all_rewards) / len(all_rewards))**0.5 if all_rewards else 0.0
    
    # Print final summary
    print("\n" + "="*70)
    print("📈 OVERALL RESULTS")
    print("="*70)
    print(f"Total Episodes:     {args.episodes}")
    print(f"Total Steps:        {len(all_rewards)}")
    print(f"Average Reward:     {overall_avg:.4f}")
    print(f"Std Deviation:      {std_dev:.4f}")
    print(f"Minimum Reward:     {min_reward:.4f}")
    print(f"Maximum Reward:     {max_reward:.4f}")
    print(f"Reward Range:       0.0 - 1.0")
    print("="*70 + "\n")
    
    # Save results if requested
    if args.output:
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "environment": "email-support-env",
                "agent": "baseline-rule-based"
            },
            "config": {
                "episodes": args.episodes,
                "max_steps_per_episode": 5
            },
            "episodes": all_results,
            "summary": {
                "total_episodes": args.episodes,
                "total_steps": len(all_rewards),
                "average_reward": round(overall_avg, 4),
                "std_deviation": round(std_dev, 4),
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

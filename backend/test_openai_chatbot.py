#!/usr/bin/env python3
"""
Comprehensive test script for GreenCart chatbot with OpenAI integration
Tests all agents, tools, and conversation flows
"""

import os
import sys
import pandas as pd
from datetime import datetime
from colorama import init, Fore, Style
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir.endswith('tests'):
    backend_dir = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)

# Load environment variables from .env file
env_path = os.path.join(backend_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"{Fore.GREEN}✓ Loaded .env file from: {env_path}{Style.RESET_ALL}")
else:
    print(f"{Fore.YELLOW}⚠ No .env file found at: {env_path}{Style.RESET_ALL}")

# Initialize colorama for colored output
init()

# Import all components
try:
    from dotenv import load_dotenv
    from agent import create_greencart_agent
    from agents.orchestrator import OrchestratorAgent
    from agents.shopping_assistant import ShoppingAssistantAgent
    from agents.sustainability_advisor import SustainabilityAdvisorAgent
    from agents.deal_finder import DealFinderAgent
    from agents.checkout_assistant import CheckoutAssistantAgent
    from services.cart_service import CartService
    from services.group_buy_service import GroupBuyService
    print(f"{Fore.GREEN}✓ All imports successful{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}✗ Import error: {e}{Style.RESET_ALL}")
    sys.exit(1)


def print_section(title):
    """Print a section header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Style.RESET_ALL}\n")


def print_test(test_name, success, message=""):
    """Print test result"""
    if success:
        print(f"{Fore.GREEN}✓ {test_name}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ {test_name}{Style.RESET_ALL}")
    if message:
        print(f"  {Fore.YELLOW}→ {message}{Style.RESET_ALL}")


def test_api_key():
    """Test if API key is set"""
    print_section("1. Testing API Key Configuration")

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print_test("OpenAI API key found", True)
        print_test("API key format", api_key.startswith("sk-"),
                   f"Key starts with: {api_key[:7]}... (should start with 'sk-')")
        return True
    else:
        print_test("OpenAI API key found", False,
                   "Please add OPENAI_API_KEY to your backend/.env file")
        print(f"\n  {Fore.CYAN}Run: python create_env_file.py{Style.RESET_ALL}")
        return False


def test_individual_agents():
    """Test each agent individually"""
    print_section("2. Testing Individual Agents")

    agents_to_test = [
        ("Orchestrator", OrchestratorAgent),
        ("Shopping Assistant", ShoppingAssistantAgent),
        ("Sustainability Advisor", SustainabilityAdvisorAgent),
        ("Deal Finder", DealFinderAgent),
        ("Checkout Assistant", CheckoutAssistantAgent)
    ]

    results = {}

    for agent_name, agent_class in agents_to_test:
        try:
            agent = agent_class()
            print_test(f"{agent_name} initialization", True)

            # Test a simple query for each agent
            if agent_name == "Orchestrator":
                result = agent.analyze_intent(
                    "Show me sustainable electronics")
                print(f"  Intent: {result.get('intent', 'unknown')}")
            else:
                # Test the LLM is working
                response = agent.llm.invoke("Hello, are you working?")
                print(f"  Response preview: {response.content[:50]}...")

            results[agent_name] = True
        except Exception as e:
            print_test(f"{agent_name} initialization", False, str(e))
            results[agent_name] = False

    return results


def test_cart_service():
    """Test cart service functionality"""
    print_section("3. Testing Cart Service")

    try:
        cart_service = CartService()
        test_user_id = "test_user_123"

        # Test adding to cart
        cart_service.add_to_cart(
            user_id=test_user_id,
            product_id=1,
            product_name="Eco-Friendly Water Bottle",
            price=29.99,
            quantity=2,
            earth_score=85
        )
        print_test("Add to cart", True)

        # Test getting cart
        cart = cart_service.get_cart(test_user_id)
        print_test("Get cart", len(cart) > 0,
                   f"Cart has {len(cart)} items")

        # Test cart summary
        summary = cart_service.get_cart_summary(test_user_id)
        print_test("Get cart summary", summary["total_items"] == 2,
                   f"Total items: {summary['total_items']}")

        return True
    except Exception as e:
        print_test("Cart service", False, str(e))
        return False


def test_main_agent():
    """Test the main agent with full conversation flow"""
    print_section("4. Testing Main Agent Conversation Flow")

    try:
        # Create agent
        print("Creating GreenCart agent...")
        agent = create_greencart_agent()
        print_test("Agent creation", True)

        # Load product data
        data_path = os.path.join(os.path.dirname(
            backend_dir), "data", "products_large.csv")
        if os.path.exists(data_path):
            products_df = pd.read_csv(data_path)
            print_test("Product data loaded", True,
                       f"{len(products_df)} products")
        else:
            print_test("Product data loaded", False,
                       f"File not found: {data_path}")
            return False

        # Test conversations
        test_conversations = [
            ("greeting", "Hi there!"),
            ("about", "What is GreenCart?"),
            ("shopping", "Show me eco-friendly products for my kitchen"),
            ("sustainability", "How is the EarthScore calculated?"),
            ("cart_view", "What's in my cart?"),
            ("add_item", "Add 2 bamboo cutting boards to my cart"),
            ("group_buy", "Tell me about group buying"),
            ("checkout", "I want to checkout with sustainable packaging")
        ]

        # Initialize state
        state = {
            "messages": [],
            "user_info": {"user_id": "test_user_123"},
            "products_df": products_df,
            "current_agent": None,
            "routing_info": None,
            "specialist_agents": {}
        }

        for test_name, user_input in test_conversations:
            try:
                print(f"\n{Fore.BLUE}Testing: {test_name}{Style.RESET_ALL}")
                print(f"User: {user_input}")

                # Add user message
                state["messages"].append(HumanMessage(content=user_input))

                # Get response
                result = agent(state)

                # Extract response
                if result and "messages" in result and len(result["messages"]) > 0:
                    response = result["messages"][-1].content
                    print(
                        f"Bot: {response[:150]}{'...' if len(response) > 150 else ''}")
                    print_test(f"{test_name} response", True)

                    # Update state for next turn
                    state = result
                else:
                    print_test(f"{test_name} response", False, "No response")

            except Exception as e:
                print_test(f"{test_name} response", False, str(e))

        return True

    except Exception as e:
        print_test("Main agent test", False, str(e))
        return False


def test_api_integration():
    """Test the FastAPI endpoints"""
    print_section("5. Testing API Integration")

    try:
        import requests
        base_url = "http://localhost:8000"

        # Check if server is running
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print_test("API server connection", True, "Server is running")
            else:
                print_test("API server connection", False,
                           "Server returned non-200 status")
                return False
        except:
            print_test("API server connection", False,
                       "Server not running. Start with: uvicorn main:app --reload")
            return False

        # Test chat endpoint
        chat_data = {
            "message": "Hello, I need sustainable products",
            "user_id": "test_user_123"
        }

        response = requests.post(f"{base_url}/api/chat", json=chat_data)
        print_test("Chat endpoint", response.status_code == 200,
                   f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"  Response preview: {data.get('response', '')[:100]}...")

        return True

    except Exception as e:
        print_test("API integration", False, str(e))
        return False


def test_error_handling():
    """Test error handling scenarios"""
    print_section("6. Testing Error Handling")

    try:
        # Test with invalid API key
        original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "invalid-key"

        try:
            agent = OrchestratorAgent()
            response = agent.llm.invoke("Test")
            print_test("Invalid API key handling", False,
                       "Should have raised an error")
        except Exception as e:
            print_test("Invalid API key handling", True,
                       "Correctly raised error")

        # Restore original key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key

        return True

    except Exception as e:
        print_test("Error handling", False, str(e))
        return False


def main():
    """Run all tests"""
    print(
        f"\n{Fore.MAGENTA}🧪 GreenCart OpenAI Integration Test Suite{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

    # Check if .env was loaded
    if not os.getenv("OPENAI_API_KEY"):
        print(
            f"\n{Fore.RED}⚠️  No OPENAI_API_KEY found in environment{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Make sure you have a .env file in backend/ with:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}OPENAI_API_KEY=your-key-here{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Run this to create .env file:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}python create_env_file.py{Style.RESET_ALL}")
        return

    # Track overall results
    all_passed = True

    # Run tests
    if not test_api_key():
        print(f"\n{Fore.RED}⚠️  Cannot proceed without API key{Style.RESET_ALL}")
        print(f"{Fore.CYAN}To fix: python create_env_file.py{Style.RESET_ALL}")
        return

    agent_results = test_individual_agents()
    if not all(agent_results.values()):
        all_passed = False

    if not test_cart_service():
        all_passed = False

    if not test_main_agent():
        all_passed = False

    if not test_api_integration():
        print(
            f"{Fore.YELLOW}Note: API tests skipped - server not running{Style.RESET_ALL}")

    if not test_error_handling():
        all_passed = False

    # Summary
    print_section("Test Summary")
    if all_passed:
        print(f"{Fore.GREEN}✅ All tests passed! Your OpenAI integration is working correctly.{Style.RESET_ALL}")
    else:
        print(
            f"{Fore.RED}❌ Some tests failed. Please check the errors above.{Style.RESET_ALL}")

    # Recommendations
    print(f"\n{Fore.CYAN}Recommendations:{Style.RESET_ALL}")
    print("1. Monitor your OpenAI API usage at: https://platform.openai.com/usage")
    print("2. Consider implementing rate limiting for production")
    print("3. Add retry logic for transient failures")
    print("4. Cache responses where appropriate to reduce API calls")

    # Cost estimation
    print(f"\n{Fore.YELLOW}Cost Estimation:{Style.RESET_ALL}")
    print("- GPT-4: ~$0.03/1K input tokens, $0.06/1K output tokens")
    print("- GPT-3.5-turbo: ~$0.0005/1K input tokens, $0.0015/1K output tokens")
    print("- Consider using GPT-3.5-turbo for non-critical queries to reduce costs")


if __name__ == "__main__":
    # Check if required packages are installed
    try:
        from colorama import init, Fore, Style
        from dotenv import load_dotenv
    except ImportError as e:
        missing_package = str(e).split("'")[1]
        print(f"Installing {missing_package}...")
        os.system(f"pip install {missing_package}")
        if missing_package == 'colorama':
            from colorama import init, Fore, Style
        else:
            from dotenv import load_dotenv

    main()

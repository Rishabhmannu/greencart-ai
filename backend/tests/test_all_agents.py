# tests/test_all_agents.py
"""Test all agents working together"""

import pandas as pd
from agents.checkout_assistant import CheckoutAssistantAgent
from agents.deal_finder import DealFinderAgent
from agents.sustainability_advisor import SustainabilityAdvisorAgent
from agents.shopping_assistant import ShoppingAssistantAgent
from agents.orchestrator import OrchestratorAgent
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_complete_flow():
    """Test a complete shopping flow with all agents"""
    print("🛍️ Testing Complete Shopping Flow\n")

    # Initialize all agents
    orchestrator = OrchestratorAgent()
    agents = {
        "shopping_assistant": ShoppingAssistantAgent(),
        "sustainability_advisor": SustainabilityAdvisorAgent(),
        "deal_finder": DealFinderAgent(),
        "checkout_assistant": CheckoutAssistantAgent()
    }

    # Load product data
    products_df = pd.DataFrame({
        'product_id': [1, 2, 3],
        'product_name': ['Bamboo Kitchen Set', 'Eco Water Bottle', 'Organic Towels'],
        'price': [24.99, 19.99, 15.99],
        'category': ['Kitchen', 'Kitchen', 'Home'],
        'earth_score': [92, 88, 85]
    })

    # User context
    user_context = {"user_id": "test_user", "location": "Mumbai"}

    # Simulate conversation
    queries = [
        "Show me eco-friendly kitchen products",
        "What makes bamboo sustainable?",
        "Are there any group buys available?",
        "Add the bamboo kitchen set to my cart",
        "Show me my cart with packaging options"
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"👤 User: {query}")

        # Route through orchestrator
        routing = orchestrator.route_message(query, user_context)
        print(f"🧭 Routing to: {routing['routing']['delegate_to']}")

        # Get response from appropriate agent
        for agent_name in routing['routing']['delegate_to']:
            if agent_name in agents:
                agent = agents[agent_name]

                if agent_name == "shopping_assistant":
                    result = agent.handle_request(
                        query, products_df, user_context)
                else:
                    result = agent.handle_request(query, user_context)

                print(
                    f"\n{result['agent'].upper()}: {result['response'][:300]}...")


if __name__ == "__main__":
    test_complete_flow()

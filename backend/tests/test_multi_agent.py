# tests/test_multi_agent.py
"""Test the multi-agent system components"""

import pandas as pd
from agents.sustainability_advisor import SustainabilityAdvisorAgent
from agents.shopping_assistant import ShoppingAssistantAgent
from agents.orchestrator import OrchestratorAgent
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_orchestrator():
    """Test the orchestrator routing"""
    print("🎯 Testing Orchestrator\n")

    orchestrator = OrchestratorAgent()

    test_cases = [
        "Show me bamboo kitchen products",
        "What's the environmental impact of this purchase?",
        "I want to join a group buy"
    ]

    for msg in test_cases:
        print(f"User: {msg}")
        result = orchestrator.route_message(msg, {"user_id": "test"})
        print(f"Routes to: {result['routing']['delegate_to']}\n")


def test_agents_together():
    """Test agents working together"""
    print("\n🤝 Testing Agents Together\n")

    # Initialize agents
    orchestrator = OrchestratorAgent()
    shopping = ShoppingAssistantAgent()
    advisor = SustainabilityAdvisorAgent()

    # Better sample data with bamboo products
    products_df = pd.DataFrame({
        'product_id': [1, 2, 3, 4],
        'product_name': [
            'Bamboo Kitchen Utensils Set',
            'Bamboo Cutting Board',
            'Eco-Friendly Dish Soap',
            'Recycled Paper Towels'
        ],
        'price': [24.99, 34.99, 8.99, 12.99],
        'category': ['Kitchen', 'Kitchen', 'Kitchen', 'Kitchen'],
        'earth_score': [92, 90, 87, 85]
    })

    # Test different queries
    test_queries = [
        "Show me bamboo products",
        "What's the environmental impact of bamboo?",
        "I want to join a group buy for kitchen items"
    ]

    for user_message in test_queries:
        print(f"\n{'='*60}")
        print(f"👤 User: {user_message}")

        # Route message
        routing = orchestrator.route_message(user_message, {"user_id": "test"})
        print(f"🧭 Routes to: {routing['routing']['delegate_to']}")

        # Get responses from relevant agents
        if "shopping_assistant" in routing['routing']['delegate_to']:
            shopping_result = shopping.handle_request(
                user_message, products_df)
            print(f"🛍️ Shopping: {shopping_result['response']}")
            if shopping_result['products']:
                print(
                    f"   Found products: {[p['product_name'] for p in shopping_result['products']]}")

        if "sustainability_advisor" in routing['routing']['delegate_to']:
            advisor_result = advisor.handle_request(user_message)
            print(f"🌱 Sustainability: {advisor_result['response'][:200]}...")

if __name__ == "__main__":
    test_orchestrator()
    test_agents_together()

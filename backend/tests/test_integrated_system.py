# tests/test_integrated_system.py
"""Test the fully integrated multi-agent system"""

import pandas as pd
from langchain_core.messages import HumanMessage
from agent import create_greencart_agent
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_complete_shopping_flow():
    """Test a complete shopping flow with the integrated system"""
    print("🛍️ Testing Complete Integrated Shopping Flow\n")

    # Create agent
    agent = create_greencart_agent()

    # Load product data
    products_df = pd.read_csv("data/products_large.csv")

    # Test conversation
    queries = [
        "Show me eco-friendly kitchen products",
        "What makes bamboo sustainable?",
        "Add the bamboo kitchen utensils to my cart",
        "Show me my cart",
        "Are there any group buys available?"
    ]

    # Initialize state
    state = {
        "messages": [],
        "user_info": {"user_id": "test_user"},
        "products_df": products_df,
        "current_agent": None,
        "routing_info": None,
        "specialist_agents": {}
    }

    for query in queries:
        print(f"\n{'='*60}")
        print(f"👤 User: {query}")

        # Add user message
        state["messages"].append(HumanMessage(content=query))

        # Process through agent
        state = agent(state)

        # Get response
        response = state["messages"][-1].content
        print(f"\n🤖 Assistant: {response[:300]}...")

        if state.get("current_agent"):
            print(f"   [Handled by: {state['current_agent']}]")


if __name__ == "__main__":
    test_complete_shopping_flow()

# backend/tests/test_enhanced_agent.py
"""Test the enhanced agent with cart functionality"""

import pandas as pd
from langchain_core.messages import HumanMessage
from agent import create_agent_graph
import sys
import os

# Get the absolute path to the backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Debug: Print paths to verify
print(f"Current file: {__file__}")
print(f"Backend dir: {backend_dir}")
print(f"Python path: {sys.path[0]}")

# NOW import after path is set


def test_agent_conversation():
    """Test a full conversation with the enhanced agent"""

    # Create the agent
    print("🤖 Creating enhanced agent...")
    agent = create_agent_graph()

    # Load product data - fix the path
    data_path = os.path.join(os.path.dirname(
        backend_dir), "data", "products_large.csv")
    products_df = pd.read_csv(data_path)
    print(f"📦 Loaded {len(products_df)} products\n")

    # Test conversation
    conversations = [
        "Hi! I'm looking for sustainable products for my home",
        "Show me what's in my cart",
        "Tell me more about the first product you mentioned",
        "Add 2 of those to my cart",
        "What's in my cart now?"
    ]

    # Initialize state
    state = {
        "messages": [],
        "user_info": {"user_id": "test_user_123"},
        "products_df": products_df
    }

    for user_input in conversations:
        print(f"\n👤 User: {user_input}")

        # Add user message to state
        state["messages"].append(HumanMessage(content=user_input))

        # Get agent response
        result = agent.invoke(state)

        # Get the last message (agent's response)
        agent_response = result["messages"][-1].content
        print(f"🤖 GreenCart: {agent_response}")

        # Update state for next turn
        state = result


if __name__ == "__main__":
    print("\n🧪 Testing Enhanced Agent with Cart Functionality\n")
    test_agent_co

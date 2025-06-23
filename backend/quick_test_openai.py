#!/usr/bin/env python3
"""
Quick test script to verify OpenAI integration is working
Run this first for a basic check, then run the comprehensive test
"""

import os
import sys
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
    print(f"✅ Loaded .env file from: {env_path}\n")
else:
    print(f"⚠️  No .env file found at: {env_path}")
    print("Make sure you have a .env file in your backend directory\n")


def quick_test():
    print("🧪 Quick OpenAI Integration Test\n")

    # 1. Check API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("Please add it to your backend/.env file:")
        print("OPENAI_API_KEY=your-openai-key")
        return False

    print(f"✅ API Key found: {api_key[:20]}...")

    # 2. Test Direct OpenAI Connection
    try:
        from langchain_openai import ChatOpenAI

        print("\n📡 Testing OpenAI connection...")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Using cheaper model for test
            openai_api_key=api_key,
            temperature=0.7
        )

        response = llm.invoke(
            "Say 'GreenCart is working with OpenAI!' if you can hear me.")
        print(f"✅ OpenAI Response: {response.content}")

    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False

    # 3. Test Agent Creation
    try:
        print("\n🤖 Testing GreenCart Agent...")
        from agent import create_greencart_agent
        import pandas as pd
        from langchain_core.messages import HumanMessage

        # Load products
        data_path = os.path.join(os.path.dirname(
            backend_dir), "data", "products_large.csv")
        products_df = pd.read_csv(data_path)

        # Create agent
        agent = create_greencart_agent()

        # Test conversation
        state = {
            "messages": [HumanMessage(content="Hi! Show me eco-friendly kitchen products")],
            "user_info": {"user_id": "test_user"},
            "products_df": products_df,
            "current_agent": None,
            "routing_info": None,
            "specialist_agents": {}
        }

        result = agent(state)
        response = result["messages"][-1].content

        print(f"✅ Agent Response: {response[:200]}...")

    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

    # 4. Test Individual Agents
    try:
        print("\n👥 Testing Individual Agents...")
        from agents.shopping_assistant import ShoppingAssistantAgent

        shopping_agent = ShoppingAssistantAgent()
        test_response = shopping_agent.llm.invoke(
            "What products do you recommend?")
        print(f"✅ Shopping Assistant: {test_response.content[:100]}...")

    except Exception as e:
        print(f"❌ Individual agent test failed: {e}")
        return False

    print("\n✅ All basic tests passed! Your OpenAI integration is working.")
    print("\n💡 Next steps:")
    print("1. Run the comprehensive test: python test_openai_chatbot.py")
    print("2. Start the server: uvicorn main:app --reload")
    print("3. Test the API endpoints")

    return True


if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)

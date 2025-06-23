import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main():
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

    try:
        llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key)
        response = llm.invoke("Hello, are you working?")
        print(f"Response: {response.content}")
        print("Test Passed: Successfully connected to OpenAI API.")
    except Exception as e:
        print(f"Test Failed: {e}")


if __name__ == "__main__":
    main()

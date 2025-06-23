#!/usr/bin/env python3
"""
Troubleshooting script for OpenAI migration issues
Helps identify and fix common problems
"""

import os
import sys
import subprocess
import importlib.util
from dotenv import load_dotenv

# Load environment variables from .env file


def load_env():
    """Load .env file from backend directory"""
    # Try current directory first
    if os.path.exists('.env'):
        load_dotenv('.env')
        return True

    # Try backend directory
    backend_path = os.path.join(os.getcwd(), 'backend', '.env')
    if os.path.exists(backend_path):
        load_dotenv(backend_path)
        return True

    # Try parent directory
    parent_env = os.path.join(os.path.dirname(os.getcwd()), '.env')
    if os.path.exists(parent_env):
        load_dotenv(parent_env)
        return True

    return False


# Load environment variables
env_loaded = load_env()
if env_loaded:
    print("✅ Loaded .env file")
else:
    print("⚠️  No .env file found")


def check_issue(description, check_func, fix_suggestion):
    """Run a check and provide fix if needed"""
    print(f"\n🔍 Checking: {description}")
    try:
        result, details = check_func()
        if result:
            print(f"✅ {details}")
        else:
            print(f"❌ {details}")
            print(f"💡 Fix: {fix_suggestion}")
        return result
    except Exception as e:
        print(f"❌ Error during check: {e}")
        print(f"💡 Fix: {fix_suggestion}")
        return False


def check_environment():
    """Check environment setup"""
    def check():
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return True, f"API key is set (starts with {api_key[:7]})"
        return False, "OPENAI_API_KEY not found in environment"

    return check_issue(
        "Environment variables",
        check,
        "Add OPENAI_API_KEY='your-key-here' to your backend/.env file"
    )


def check_env_file():
    """Check if .env file exists"""
    def check():
        if os.path.exists('.env'):
            # Check if it contains OPENAI_API_KEY
            with open('.env', 'r') as f:
                content = f.read()
                if 'OPENAI_API_KEY' in content:
                    return True, ".env file exists with OPENAI_API_KEY"
                else:
                    return False, ".env file exists but missing OPENAI_API_KEY"
        return False, ".env file not found"

    return check_issue(
        ".env file",
        check,
        "Run: python create_env_file.py"
    )


def check_dependencies():
    """Check if required packages are installed"""
    def check():
        missing = []
        packages = {
            'langchain_openai': 'langchain-openai',
            'langchain': 'langchain',
            'langchain_core': 'langchain-core',
            'pandas': 'pandas',
            'fastapi': 'fastapi',
            'redis': 'redis'
        }

        for module, package in packages.items():
            if importlib.util.find_spec(module) is None:
                missing.append(package)

        if missing:
            return False, f"Missing packages: {', '.join(missing)}"
        return True, "All required packages installed"

    return check_issue(
        "Python dependencies",
        check,
        "Run: pip install langchain-openai langchain pandas fastapi redis"
    )


def check_imports():
    """Check if imports work correctly"""
    def check():
        try:
            from langchain_openai import ChatOpenAI
            return True, "langchain_openai imports successfully"
        except ImportError as e:
            return False, f"Import error: {e}"

    return check_issue(
        "LangChain OpenAI imports",
        check,
        "Run: pip install --upgrade langchain-openai"
    )


def check_file_modifications():
    """Check if key files have been modified"""
    def check():
        files_to_check = [
            'agent.py',
            'agents/orchestrator.py',
            'agents/shopping_assistant.py'
        ]

        unmodified = []
        for file in files_to_check:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    content = f.read()
                    if 'ChatGoogleGenerativeAI' in content:
                        unmodified.append(file)

        if unmodified:
            return False, f"Files still using Gemini: {', '.join(unmodified)}"
        return True, "All files appear to be updated"

    return check_issue(
        "File modifications",
        check,
        "Update imports from ChatGoogleGenerativeAI to ChatOpenAI in all agent files"
    )


def check_api_connection():
    """Test actual API connection"""
    def check():
        try:
            from langchain_openai import ChatOpenAI
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                return False, "No API key to test with"

            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                openai_api_key=api_key,
                max_retries=1,
                request_timeout=10
            )

            response = llm.invoke("Say 'test' if you're working")
            return True, f"API connection successful"

        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                return False, "Invalid API key (401 Unauthorized)"
            elif "429" in error_msg:
                return False, "Rate limit exceeded (429)"
            elif "timeout" in error_msg:
                return False, "Connection timeout"
            else:
                return False, f"API error: {error_msg}"

    return check_issue(
        "OpenAI API connection",
        check,
        "Verify your API key at https://platform.openai.com/api-keys"
    )


def check_redis():
    """Check Redis connection"""
    def check():
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            r.ping()
            return True, "Redis is running and accessible"
        except:
            return False, "Redis not accessible"

    return check_issue(
        "Redis connection",
        check,
        "Start Redis with: redis-server (or brew services start redis on Mac)"
    )


def suggest_fixes():
    """Provide additional suggestions"""
    print("\n📋 Additional Troubleshooting Steps:")
    print("\n1. If getting 'module not found' errors:")
    print("   - Make sure you're in the backend directory")
    print("   - Activate your virtual environment")
    print("   - Run: pip install -r requirements.txt")

    print("\n2. If API key is not found:")
    print("   - Run: python create_env_file.py")
    print("   - Or manually add OPENAI_API_KEY to backend/.env")

    print("\n3. If API calls are failing:")
    print("   - Check your OpenAI account has credits")
    print("   - Verify API key permissions")
    print("   - Try using gpt-3.5-turbo instead of gpt-4")

    print("\n4. Common import fixes:")
    print("   - Replace: from langchain_google_genai import ChatGoogleGenerativeAI")
    print("   - With: from langchain_openai import ChatOpenAI")

    print("\n5. Model name mappings:")
    print("   - gemini-1.5-pro-latest → gpt-4 or gpt-3.5-turbo")
    print("   - gemini-pro → gpt-3.5-turbo")


def main():
    print("🔧 OpenAI Migration Troubleshooter")
    print("==================================")

    # Change to backend directory if needed
    if 'backend' not in os.getcwd():
        backend_path = os.path.join(os.getcwd(), 'backend')
        if os.path.exists(backend_path):
            os.chdir(backend_path)
            print(f"Changed directory to: {os.getcwd()}")

    all_passed = True

    # Run all checks
    all_passed &= check_env_file()
    all_passed &= check_environment()
    all_passed &= check_dependencies()
    all_passed &= check_imports()
    all_passed &= check_file_modifications()
    all_passed &= check_api_connection()
    all_passed &= check_redis()

    print("\n" + "="*50)
    if all_passed:
        print("✅ All checks passed! Your migration appears successful.")
        print("\nNext steps:")
        print("1. Run quick test: python quick_test_openai.py")
        print("2. Run full test: python test_openai_chatbot.py")
        print("3. Start server: uvicorn main:app --reload")
    else:
        print("❌ Some issues found. Please fix them and run again.")
        suggest_fixes()


if __name__ == "__main__":
    main()

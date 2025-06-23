#!/usr/bin/env python3
"""
Debug script to test frontend-backend connection issues
"""

import requests
import json
from colorama import init, Fore, Style

init()


def test_backend_endpoints():
    """Test all backend endpoints to ensure they're working"""

    print(f"{Fore.CYAN}🔍 Testing Backend API Endpoints{Style.RESET_ALL}")
    print("="*50)

    base_url = "http://localhost:8000"

    # 1. Test health endpoint
    print(f"\n{Fore.YELLOW}1. Testing Health Check:{Style.RESET_ALL}")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print(f"\n{Fore.RED}Backend server is not running!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Start it with: uvicorn main:app --reload{Style.RESET_ALL}")
        return False

    # 2. Test CORS headers
    print(f"\n{Fore.YELLOW}2. Testing CORS Headers:{Style.RESET_ALL}")
    try:
        # Simulate browser request with Origin header
        headers = {
            "Origin": "http://localhost:3111",
            "Content-Type": "application/json"
        }
        response = requests.options(f"{base_url}/api/chat", headers=headers)

        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
        }

        for header, value in cors_headers.items():
            if value:
                print(f"✅ {header}: {value}")
            else:
                print(f"❌ {header}: Missing")

    except Exception as e:
        print(f"❌ CORS test failed: {e}")

    # 3. Test chat endpoint
    print(f"\n{Fore.YELLOW}3. Testing Chat Endpoint:{Style.RESET_ALL}")
    try:
        chat_data = {
            "message": "Hello from debug script",
            "user_id": "debug_user_123"
        }

        response = requests.post(
            f"{base_url}/api/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"✅ Chat endpoint status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received:")
            print(f"   {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Error response: {response.text}")

    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")

    # 4. Test products endpoint
    print(f"\n{Fore.YELLOW}4. Testing Products Endpoint:{Style.RESET_ALL}")
    try:
        response = requests.get(f"{base_url}/api/products")
        print(f"✅ Products endpoint: {response.status_code}")
        print(f"   Products count: {len(response.json())}")
    except Exception as e:
        print(f"❌ Products endpoint failed: {e}")

    return True


def check_frontend_config():
    """Check frontend configuration"""
    print(f"\n{Fore.CYAN}🔍 Checking Frontend Configuration{Style.RESET_ALL}")
    print("="*50)

    import os

    # Check if we can find frontend .env
    frontend_env_paths = [
        "../frontend/.env",
        "../../frontend/.env",
        "../greencart-hackathon/frontend/.env"
    ]

    frontend_env_found = False
    for path in frontend_env_paths:
        if os.path.exists(path):
            frontend_env_found = True
            print(f"\n✅ Found frontend .env at: {os.path.abspath(path)}")

            with open(path, 'r') as f:
                content = f.read()

            if 'REACT_APP_API_URL' in content:
                for line in content.split('\n'):
                    if line.startswith('REACT_APP_API_URL'):
                        api_url = line.split('=')[1].strip()
                        print(f"✅ REACT_APP_API_URL is set to: {api_url}")

                        if api_url != "http://localhost:8000":
                            print(
                                f"{Fore.YELLOW}⚠️  API URL mismatch!{Style.RESET_ALL}")
                            print(f"   Expected: http://localhost:8000")
                            print(f"   Found: {api_url}")
            else:
                print(f"❌ REACT_APP_API_URL not found in frontend .env")
                print(f"   Add: REACT_APP_API_URL=http://localhost:8000")
            break

    if not frontend_env_found:
        print(f"❌ Frontend .env file not found")
        print(f"   Create one at: frontend/.env")
        print(f"   With content: REACT_APP_API_URL=http://localhost:8000")


def suggest_fixes():
    """Suggest fixes for common issues"""
    print(f"\n{Fore.CYAN}🔧 Common Fixes{Style.RESET_ALL}")
    print("="*50)

    print(
        f"\n{Fore.YELLOW}1. Update your backend/main.py CORS settings:{Style.RESET_ALL}")
    print("""
# In main.py, update the CORS configuration:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3111",  # Your frontend port
        "http://localhost:3001",
        "*"  # For development only
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
""")

    print(f"\n{Fore.YELLOW}2. Check your frontend API service:{Style.RESET_ALL}")
    print("""
// In frontend/src/services/api.ts or api.js:
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Make sure the chat endpoint is called correctly:
export const sendChatMessage = async (message: string, userId: string) => {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message, user_id: userId }),
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
};
""")

    print(f"\n{Fore.YELLOW}3. Check browser console for errors:{Style.RESET_ALL}")
    print("1. Open Chrome DevTools (F12)")
    print("2. Go to Console tab")
    print("3. Look for red error messages")
    print("4. Check Network tab for failed requests")

    print(f"\n{Fore.YELLOW}4. Restart both servers:{Style.RESET_ALL}")
    print("Terminal 1 (Backend):")
    print("  cd backend")
    print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\nTerminal 2 (Frontend):")
    print("  cd frontend")
    print("  npm start")


def main():
    print(f"{Fore.MAGENTA}🐛 GreenCart Frontend Connection Debugger{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}========================================{Style.RESET_ALL}\n")

    # Test backend
    backend_running = test_backend_endpoints()

    if not backend_running:
        print(
            f"\n{Fore.RED}❌ Backend is not running. Start it first!{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Run: cd backend && uvicorn main:app --reload{Style.RESET_ALL}")
        return

    # Check frontend config
    check_frontend_config()

    # Suggest fixes
    suggest_fixes()

    print(f"\n{Fore.GREEN}Next Steps:{Style.RESET_ALL}")
    print("1. Apply the CORS fix to your backend/main.py")
    print("2. Restart the backend server")
    print("3. Check frontend API configuration")
    print("4. Try the chat again")
    print("5. Check browser console for specific errors")


if __name__ == "__main__":
    main()

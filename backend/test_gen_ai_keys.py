#!/usr/bin/env python3
import requests
import sys
import os
from dotenv import load_dotenv

# ───────────────────────────────────────────────────────────
# 1. Drop your two keys in here:
#    Set API_KEY_1 and API_KEY_2 in backend/.env file, not here.
#    Example .env:
#    API_KEY_1=...
#    API_KEY_2=...
# ───────────────────────────────────────────────────────────

API_KEYS = [API_KEY_1, API_KEY_2]
BASE_URL = "https://generativelanguage.googleapis.com/v1beta2"


def list_models(key: str):
    """Attempts to list the available models for a given API key."""
    try:
        resp = requests.get(f"{BASE_URL}/models",
                            params={"key": key}, timeout=10)
        return resp.status_code, resp.json() if resp.headers.get("Content-Type", "").startswith("application/json") else resp.text
    except requests.exceptions.RequestException as e:
        return None, f"A network error occurred: {e}"


def test_generate(key: str, model: str = "text-bison-001"):
    """Attempts to generate text using a specified model and API key."""
    url = f"{BASE_URL}/models/{model}:generateText"
    payload = {
        "prompt": {"text": "Ping"},
        "temperature": 0.0,
        "maxOutputTokens": 1
    }
    try:
        resp = requests.post(
            url, params={"key": key}, json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.status_code, resp.json()
        else:
            return resp.status_code, resp.json().get("error", {}).get("message", resp.text)
    except requests.exceptions.RequestException as e:
        return None, f"A network error occurred: {e}"


def analyze_error(code: int, response: str):
    """Provides a detailed analysis of the error."""
    print(f"  ❌ FAILED (HTTP {code})")
    print(f"     Raw Error: {response}")
    print("     Analysis and Next Steps:")
    if code == 400:
        if "API key not valid" in response:
            print("     - The API key is invalid. Please double-check that you have copied the entire key correctly.")
            print("     - Ensure there are no extra spaces or characters.")
        elif "API key not found" in response:
            print("     - This API key does not exist. It might have been deleted.")
            print("     - Please generate a new API key from your Google Cloud Console.")
        elif "Generative Language API has not been used in project" in response:
            print(
                "     - The Generative Language API is not enabled for the project associated with this key.")
            print("     - Go to the Google Cloud Console, select the correct project, and enable the 'Generative Language API'.")
        else:
            print("     - This is a general 'Bad Request' error. It could be an issue with the request format, but with a valid key, it often points to a configuration issue.")
    elif code == 403:
        print("     - This 'Permission Denied' error usually means the API key does not have the necessary permissions.")
        print("     - Check the API key restrictions in your Google Cloud Console. Ensure that the 'Generative Language API' is not in the 'denied' list.")
        print("     - If you have IP or referrer restrictions, make sure your testing environment complies with them.")
    elif code == 429:
        print("     - You have exceeded your quota for the API.")
        print("     - Check your usage limits in the Google Cloud Console.")
        print("     - You may need to request a quota increase if you consistently hit this limit.")
    elif code is None:  # For network errors
        print(f"    - {response}")
        print("    - Check your internet connection and any firewall settings that might be blocking the request.")
    else:
        print(
            f"     - An unexpected error occurred with HTTP status {code}. Please check the Google Cloud documentation for this status code or try again later.")


def main():
    """Main function to test the provided API keys."""
    for i, key in enumerate(API_KEYS, 1):
        # Hide most of the key for security
        print(f"\n🔑 Testing Key #{i}: ...{key[-4:]}")

        # Test 1: List Models
        print("\n  [Test 1/2] Listing available models...")
        code, models_response = list_models(key)
        if code == 200:
            print(
                f"  ✅ SUCCESS: Can list models ({len(models_response.get('models', []))} available).")
            for m in models_response.get("models", []):
                print("     -", m.get("name"))
        else:
            analyze_error(code, models_response)

        # Test 2: Generate Text
        print("\n  [Test 2/2] Generating text with 'text-bison-001'...")
        code, generate_response = test_generate(key)
        if code == 200:
            output_text = generate_response.get('candidates', [{}])[
                0].get('output', 'No output found')
            print(f"  ✅ SUCCESS: generateText OK → “{output_text}”")
        else:
            analyze_error(code, generate_response)


if __name__ == "__main__":
    if "YOUR_API_KEY_1" in API_KEY_1 or "YOUR_API_KEY_2" in API_KEY_2:
        print("👉 Please replace 'YOUR_API_KEY_1' and 'YOUR_API_KEY_2' in the script with your actual Google API keys.")
        sys.exit(1)
    main()

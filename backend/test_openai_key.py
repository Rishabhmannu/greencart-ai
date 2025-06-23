#!/usr/bin/env python3
import requests
import sys
import os
from dotenv import load_dotenv

# ───────────────────────────────────────────────────────────
# 1. Drop your two OpenAI keys in here:
#    Set OPENAI_KEY_1 and OPENAI_KEY_2 in backend/.env file, not here.
#    Example .env:
#    OPENAI_KEY_1=REMOVED
#    OPENAI_KEY_2=REMOVED
# ───────────────────────────────────────────────────────────

OPENAI_KEYS = [os.getenv("OPENAI_KEY_1", ""), os.getenv("OPENAI_KEY_2", "")]
BASE_URL = "https://api.openai.com/v1"


def list_models(api_key: str):
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(f"{BASE_URL}/models", headers=headers, timeout=10)
    return resp.status_code, resp.json()


def test_model(api_key: str, model_id: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # pick endpoint + payload based on model type
    if model_id.startswith("gpt-"):
        url = f"{BASE_URL}/chat/completions"
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": "Ping"}],
            "max_tokens": 1
        }
    else:
        url = f"{BASE_URL}/completions"
        payload = {
            "model": model_id,
            "prompt": "Ping",
            "max_tokens": 1
        }

    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        # extract the returned text/token
        if model_id.startswith("gpt-"):
            out = data["choices"][0]["message"]["content"].strip()
        else:
            out = data["choices"][0].get("text", "").strip()
        return True, out or "<no text>"
    else:
        err = resp.json().get("error", {}).get("message", resp.text)
        return False, f"HTTP {resp.status_code}: {err}"


def main():
    for key in OPENAI_KEYS:
        if "YOUR_OPENAI_KEY" in key:
            print(
                "👉 Please replace YOUR_OPENAI_KEY_1 / YOUR_OPENAI_KEY_2 with real keys.")
            sys.exit(1)

        print(f"\n🔑 Testing key: {key}")
        code, models = list_models(key)
        if code == 200:
            model_list = models.get("data", [])
            print(
                f"  ✅ Can list {len(model_list)} models. Testing first one: {model_list[0]['id']}")
            chosen = model_list[0]["id"]
        else:
            print(f"  ❌ list models failed (HTTP {code}): {models}")
            continue

        ok, result = test_model(key, chosen)
        if ok:
            print(f"  ✅ {chosen!r} responded → “{result}”")
        else:
            print(f"  ❌ test failed on {chosen!r}: {result}")


if __name__ == "__main__":
    main()

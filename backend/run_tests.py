# backend/run_tests.py
"""Test runner for all backend tests"""

import subprocess
import sys
import os


def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)

    result = subprocess.run([sys.executable, test_file],
                            capture_output=False,
                            text=True)

    return result.returncode == 0


def main():
    """Run all tests"""
    test_files = [
        "tests/test_cart_integration.py",
        "tests/test_enhanced_agent.py"
    ]

    print("🧪 Running all backend tests...\n")

    passed = 0
    failed = 0

    for test_file in test_files:
        if os.path.exists(test_file):
            if run_test(test_file):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️  Test file not found: {test_file}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print('='*60)


if __name__ == "__main__":
    main()

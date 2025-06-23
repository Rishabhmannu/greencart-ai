# backend/tests/test_config.py
"""Configuration for tests to properly import modules"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Verify the path
print(f"Test config loaded. Backend dir: {backend_dir}")

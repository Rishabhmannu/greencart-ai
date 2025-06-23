# backend/tests/test_cart_integration.py
"""Test the cart integration with agent tools"""

from agent_tools import implement_add_to_cart, implement_view_cart
import pandas as pd
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

# Create sample product data
products_data = {
    'product_id': [1, 2, 3],
    'product_name': ['Eco Water Bottle', 'Bamboo Notebook', 'Organic Cotton Shirt'],
    'price': [24.99, 15.99, 39.99],
    'category': ['Home', 'Office', 'Apparel'],
    'earth_score': [85, 92, 78]
}
products_df = pd.DataFrame(products_data)

print("\n🧪 Testing Cart Integration\n")

# Test adding to cart
result1 = implement_add_to_cart("user123", "water bottle", 2, products_df)
print(f"Add to cart result: {result1}\n")

# Test viewing cart
result2 = implement_view_cart("user123")
print(f"View cart result: {result2}\n")

# Add another item
result3 = implement_add_to_cart("user123", "bamboo", 1, products_df)
print(f"Add another item: {result3}\n")

# View updated cart
result4 = implement_view_cart("user123")
print(f"Updated cart: {result4}")

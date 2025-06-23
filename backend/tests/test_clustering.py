#!/usr/bin/env python3
import json
from clustering_service import GroupBuyClusteringService
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_clustering():
    """Test the clustering service with various scenarios"""

    # Initialize service
    print("Initializing clustering service...")
    service = GroupBuyClusteringService('../../data/users_pincodes.csv')

    print("\n" + "="*50)
    print("CLUSTERING SERVICE TEST")
    print("="*50)

    # Test case 1: Mumbai pincode with kitchen items
    print("\n📍 Test 1: Pincode 400705 (Mumbai) with kitchen items")
    cart_items = [
        {
            'id': 1,
            'name': 'Bamboo Utensils',
            'category': 'kitchen',
            'price': 15.99,
            'quantity': 1
        },
        {
            'id': 2,
            'name': 'Reusable Food Wraps',
            'category': 'kitchen',
            'price': 24.99,
            'quantity': 2
        }
    ]

    results = service.find_optimal_groups('400705', cart_items, radius_km=5.0)
    print(f"\n✅ Found {len(results)} group(s)")

    for i, group in enumerate(results, 1):
        print(f"\nGroup {i}: {group['name']}")
        print(f"  - Participants: {len(group['participants'])}")
        print(
            f"  - Savings: ${group['savings']['cost']} ({group['savings']['percentage']}%)")
        print(f"  - CO2 Saved: {group['savings']['co2']}kg")
        print(f"  - Matching Products: {', '.join(group['matchingProducts'])}")
        print(f"  - Status: {group['status']}")

    # Test case 2: Different area with electronics
    print("\n" + "-"*50)
    print("\n📍 Test 2: Pincode 400701 with electronics")
    cart_items2 = [
        {
            'id': 3,
            'name': 'Solar Power Bank',
            'category': 'electronics',
            'price': 49.99,
            'quantity': 1
        }
    ]

    results2 = service.find_optimal_groups(
        '400701', cart_items2, radius_km=3.0)
    print(f"\n✅ Found {len(results2)} group(s)")

    for i, group in enumerate(results2, 1):
        print(f"\nGroup {i}: {group['name']}")
        print(f"  - Participants: {len(group['participants'])}")

    # Test case 3: Test with clothing category
    print("\n" + "-"*50)
    print("\n📍 Test 3: Pincode 400703 with clothing")
    cart_items3 = [
        {
            'id': 4,
            'name': 'Organic Cotton T-Shirt',
            'category': 'clothing',
            'price': 29.99,
            'quantity': 2
        }
    ]

    results3 = service.find_optimal_groups(
        '400703', cart_items3, radius_km=5.0)
    print(f"\n✅ Found {len(results3)} group(s)")

    # Test case 4: Invalid pincode
    print("\n" + "-"*50)
    print("\n📍 Test 4: Invalid pincode (should use default)")
    results4 = service.find_optimal_groups(
        '999999', cart_items, radius_km=5.0)
    print(f"\n✅ Found {len(results4)} group(s) (using default location)")

    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"✓ Test 1 (400705 - kitchen): {len(results)} groups found")
    print(f"✓ Test 2 (400701 - electronics): {len(results2)} groups found")
    print(f"✓ Test 3 (400703 - clothing): {len(results3)} groups found")
    print(f"✓ Test 4 (invalid pincode): {len(results4)} groups found")
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    test_clustering()

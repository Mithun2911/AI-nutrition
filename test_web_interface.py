#!/usr/bin/env python3
"""
Test script for the NutriVision AI web interface
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running.")
        return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_manual_food_analysis():
    """Test the manual food analysis endpoint"""
    try:
        test_foods = ['apple', 'chicken', 'rice']
        data = {
            'foods': test_foods,
            'user_preferences': {}
        }
        
        response = requests.post(
            'http://localhost:5000/analyze_foods',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Manual food analysis working")
            print(f"Analyzed foods: {test_foods}")
            print(f"Total calories: {result.get('total_nutrition', {}).get('calories', 'N/A')}")
            print(f"Total protein: {result.get('total_nutrition', {}).get('protein', 'N/A')}g")
            print(f"Total carbs: {result.get('total_nutrition', {}).get('carbs', 'N/A')}g")
            print(f"Health score: {result.get('health_score', 'N/A')}")
            print(f"Suggestions: {len(result.get('suggestions', []))}")
            return True
        else:
            print(f"❌ Manual food analysis failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing manual food analysis: {e}")
        return False

def test_vdic_endpoint():
    """Test the VDIC information endpoint"""
    try:
        test_food = 'apple'
        data = {'food_name': test_food}
        
        response = requests.post(
            'http://localhost:5000/get_vdic_info',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ VDIC endpoint working")
            print(f"Food: {test_food}")
            print(f"VDIC status: {result.get('is_vdic', 'N/A')}")
            print(f"Synonyms: {result.get('synonyms', [])}")
            return True
        else:
            print(f"❌ VDIC endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing VDIC endpoint: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing NutriVision AI Web Interface")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Manual Food Analysis", test_manual_food_analysis),
        ("VDIC Information", test_vdic_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The web interface is working correctly.")
        print("\n🌐 Open your browser and go to: http://localhost:5000")
        print("📱 You can now:")
        print("   - Upload food images for analysis")
        print("   - Manually enter foods for nutrition analysis")
        print("   - View detailed nutrition breakdown with vitamins and minerals")
        print("   - Get personalized diet suggestions")
    else:
        print("❌ Some tests failed. Check the server logs for more details.")
    
    return passed == total

if __name__ == "__main__":
    main()



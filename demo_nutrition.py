#!/usr/bin/env python3
"""
Demo script to showcase the improved nutrition analysis system
"""

import requests
import json

def demo_nutrition_analysis():
    """Demonstrate the improved nutrition analysis with different foods"""
    
    print("🍎 NutriVision AI - Nutrition Analysis Demo")
    print("=" * 60)
    
    # Test different food combinations
    test_combinations = [
        {
            'name': 'Fruit Bowl',
            'foods': ['apple', 'banana', 'orange', 'strawberry']
        },
        {
            'name': 'Protein Power',
            'foods': ['chicken', 'eggs', 'salmon', 'tofu']
        },
        {
            'name': 'Vegetable Mix',
            'foods': ['broccoli', 'spinach', 'carrot', 'tomato']
        },
        {
            'name': 'Grain Bowl',
            'foods': ['rice', 'quinoa', 'bread', 'oatmeal']
        },
        {
            'name': 'Balanced Meal',
            'foods': ['chicken', 'rice', 'broccoli', 'milk']
        }
    ]
    
    for combo in test_combinations:
        print(f"\n🥗 {combo['name']}")
        print(f"Foods: {', '.join(combo['foods'])}")
        print("-" * 40)
        
        try:
            response = requests.post(
                'http://localhost:5000/analyze_foods',
                json={'foods': combo['foods'], 'user_preferences': {}},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                nutrition = result['total_nutrition']
                
                print(f"📊 Nutrition Summary:")
                print(f"   Calories: {nutrition['calories']} kcal")
                print(f"   Protein: {nutrition['protein']}g")
                print(f"   Carbs: {nutrition['carbs']}g")
                print(f"   Fat: {nutrition['fat']}g")
                print(f"   Fiber: {nutrition['fiber']}g")
                print(f"   Vitamin C: {nutrition['vitamin_c']}mg")
                print(f"   Calcium: {nutrition['calcium']}mg")
                print(f"   Iron: {nutrition['iron']}mg")
                print(f"   Health Score: {result['health_score']}/100")
                
                print(f"\n💡 Diet Suggestions ({len(result['suggestions'])}):")
                for i, suggestion in enumerate(result['suggestions'], 1):
                    if isinstance(suggestion, dict):
                        print(f"   {i}. {suggestion['title']} - {suggestion['message']}")
                    else:
                        print(f"   {i}. {suggestion}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)

def demo_vdic_detection():
    """Demonstrate VDIC detection for different foods"""
    
    print("\n🔍 VDIC (Visually Discernible and Instantaneously Consumable) Detection Demo")
    print("=" * 60)
    
    test_foods = ['apple', 'chicken', 'rice', 'broccoli', 'salad', 'soup', 'pizza']
    
    for food in test_foods:
        try:
            response = requests.post(
                'http://localhost:5000/get_vdic_info',
                json={'food_name': food},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                status = "✅ VDIC" if result['is_vdic'] else "❌ Not VDIC"
                print(f"{food.capitalize()}: {status}")
                if result['synonyms']:
                    print(f"   Synonyms: {', '.join(result['synonyms'])}")
            else:
                print(f"❌ Error analyzing {food}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    print("🚀 Starting NutriVision AI Demo...")
    print("Make sure the Flask server is running on http://localhost:5000")
    print()
    
    try:
        # Test server connection
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Server is running and ready!")
            print()
            
            # Run demos
            demo_nutrition_analysis()
            demo_vdic_detection()
            
            print("\n🎉 Demo completed successfully!")
            print("\n🌐 Open your browser and go to: http://localhost:5000")
            print("📱 Try different food combinations and see the varied nutrition data!")
            
        else:
            print("❌ Server is not responding properly")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the Flask app first:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

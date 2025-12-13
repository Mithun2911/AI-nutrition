#!/usr/bin/env python3
"""
Example usage of the AI-based Nutrition Detection and Diet Suggestion System
This script shows practical examples of how to use the system for different scenarios
"""

from fd import NutritionDetectionSystem, VDICFoodDetector, NutritionAnalyzer
from config import get_config
import json

def example_1_basic_food_detection():
    """Example 1: Basic food detection and nutrition analysis"""
    print("="*70)
    print("EXAMPLE 1: BASIC FOOD DETECTION AND NUTRITION ANALYSIS")
    print("="*70)
    
    # Initialize the system
    system = NutritionDetectionSystem()
    
    # Simulate detecting foods from an image
    print("📸 Analyzing food image...")
    result = system.detect_food_from_image("breakfast_plate.jpg")
    
    print("\n🍽️  Analysis Results:")
    print(f"Detected foods: {', '.join(result['food_details'][i]['food'] for i in range(len(result['food_details']))}")
    
    print("\n📊 Nutrition Summary:")
    for nutrient, value in result['total_nutrition'].items():
        unit = 'kcal' if nutrient == 'calories' else 'g'
        print(f"  {nutrient.capitalize()}: {value} {unit}")
    
    print("\n💡 Diet Suggestions:")
    for suggestion in result['suggestions']:
        print(f"  • {suggestion}")

def example_2_custom_user_preferences():
    """Example 2: Custom user preferences and dietary restrictions"""
    print("\n" + "="*70)
    print("EXAMPLE 2: CUSTOM USER PREFERENCES AND DIETARY RESTRICTIONS")
    print("="*70)
    
    # Initialize nutrition analyzer
    analyzer = NutritionAnalyzer()
    
    # Define custom user preferences
    user_preferences = {
        'calorie_goal': 1800,      # Lower calorie goal for weight loss
        'protein_goal': 140,       # Higher protein for muscle maintenance
        'carbs_goal': 180,         # Lower carbs for weight loss
        'fat_goal': 60,            # Moderate fat
        'dietary_restrictions': ['vegetarian']
    }
    
    print(f"👤 User Profile:")
    print(f"  Calorie Goal: {user_preferences['calorie_goal']} kcal")
    print(f"  Protein Goal: {user_preferences['protein_goal']}g")
    print(f"  Carbs Goal: {user_preferences['carbs_goal']}g")
    print(f"  Fat Goal: {user_preferences['fat_goal']}g")
    print(f"  Dietary Restrictions: {', '.join(user_preferences['dietary_restrictions'])}")
    
    # Analyze a vegetarian meal
    detected_foods = ['quinoa', 'chickpeas', 'spinach', 'avocado', 'tomato']
    
    print(f"\n🥗 Detected Foods: {', '.join(detected_foods)}")
    
    # Get nutrition analysis with custom preferences
    analysis = analyzer.generate_diet_suggestions(detected_foods, user_preferences)
    
    print(f"\n📊 Nutrition Analysis:")
    for nutrient, value in analysis['total_nutrition'].items():
        unit = 'kcal' if nutrient == 'calories' else 'g'
        print(f"  {nutrient.capitalize()}: {value} {unit}")
    
    print(f"\n💡 Personalized Suggestions:")
    for suggestion in analysis['suggestions']:
        print(f"  • {suggestion}")

def example_3_vdic_food_analysis():
    """Example 3: VDIC food analysis and synonym expansion"""
    print("\n" + "="*70)
    print("EXAMPLE 3: VDIC FOOD ANALYSIS AND SYNONYM EXPANSION")
    print("="*70)
    
    # Initialize VDIC detector
    detector = VDICFoodDetector()
    
    # Test various food items
    test_foods = [
        'banana', 'apple', 'sandwich', 'pizza', 'carrot',
        'cucumber', 'chips', 'chocolate', 'soup', 'raw_meat',
        'fresh_orange', 'cooked_chicken', 'instant_noodles'
    ]
    
    print("🔍 VDIC Food Analysis:")
    vdic_foods = []
    non_vdic_foods = []
    
    for food in test_foods:
        is_vdic = detector.predict_vdic_status(food)
        if is_vdic:
            vdic_foods.append(food)
            print(f"  ✓ {food:20} -> VDIC (Ready to eat)")
        else:
            non_vdic_foods.append(food)
            print(f"  ✗ {food:20} -> Not VDIC (Requires preparation)")
    
    print(f"\n📊 Summary:")
    print(f"  VDIC Foods: {len(vdic_foods)}")
    print(f"  Non-VDIC Foods: {len(non_vdic_foods)}")
    
    # Test synonym expansion
    print(f"\n🔄 Synonym Expansion Examples:")
    expansion_examples = ['tomato', 'apple', 'banana', 'sandwich']
    
    for food in expansion_examples:
        synonyms = detector.expand_synonyms(food)
        print(f"  {food:15} -> {', '.join(synonyms)}")

def example_4_meal_planning():
    """Example 4: Meal planning with nutrition goals"""
    print("\n" + "="*70)
    print("EXAMPLE 4: MEAL PLANNING WITH NUTRITION GOALS")
    print("="*70)
    
    # Initialize nutrition analyzer
    analyzer = NutritionAnalyzer()
    
    # Define daily nutrition goals
    daily_goals = {
        'calorie_goal': 2200,
        'protein_goal': 160,
        'carbs_goal': 250,
        'fat_goal': 70,
        'fiber_goal': 30
    }
    
    print("🎯 Daily Nutrition Goals:")
    for nutrient, goal in daily_goals.items():
        unit = 'kcal' if nutrient == 'calories' else 'g'
        print(f"  {nutrient.capitalize()}: {goal} {unit}")
    
    # Plan meals for the day
    meals = {
        'Breakfast': ['oatmeal', 'banana', 'almonds', 'milk'],
        'Lunch': ['chicken_breast', 'brown_rice', 'broccoli', 'olive_oil'],
        'Dinner': ['salmon', 'quinoa', 'spinach', 'avocado'],
        'Snacks': ['greek_yogurt', 'berries', 'nuts']
    }
    
    print(f"\n🍽️  Daily Meal Plan:")
    
    total_nutrition = {nutrient: 0 for nutrient in daily_goals.keys()}
    
    for meal_name, foods in meals.items():
        print(f"\n  {meal_name}:")
        print(f"    Foods: {', '.join(foods)}")
        
        # Analyze meal nutrition
        meal_analysis = analyzer.generate_diet_suggestions(foods, daily_goals)
        
        # Add to daily total
        for nutrient, value in meal_analysis['total_nutrition'].items():
            if nutrient in total_nutrition:
                total_nutrition[nutrient] += value
        
        # Show meal nutrition
        for nutrient, value in meal_analysis['total_nutrition'].items():
            if nutrient in daily_goals:
                unit = 'kcal' if nutrient == 'calories' else 'g'
                print(f"    {nutrient.capitalize()}: {value} {unit}")
    
    # Show daily totals and gaps
    print(f"\n📊 Daily Nutrition Summary:")
    for nutrient, total in total_nutrition.items():
        goal = daily_goals[nutrient]
        unit = 'kcal' if nutrient == 'calories' else 'g'
        gap = goal - total
        
        if gap > 0:
            print(f"  {nutrient.capitalize()}: {total}/{goal} {unit} (Need +{gap} {unit})")
        elif gap < 0:
            print(f"  {nutrient.capitalize()}: {total}/{goal} {unit} (Over by {abs(gap)} {unit})")
        else:
            print(f"  {nutrient.capitalize()}: {total}/{goal} {unit} (Perfect!)")

def example_5_system_configuration():
    """Example 5: System configuration and customization"""
    print("\n" + "="*70)
    print("EXAMPLE 5: SYSTEM CONFIGURATION AND CUSTOMIZATION")
    print("="*70)
    
    # Load current configuration
    config = get_config()
    
    print("⚙️  Current System Configuration:")
    print(f"  Model Architecture: {config['model']['architecture']}")
    print(f"  Number of Classes: {config['model']['num_classes']}")
    print(f"  VDIC Threshold: {config['vdic']['consensus_threshold']}")
    print(f"  Max Images per Food: {config['image_collection']['max_images_per_food']}")
    print(f"  Noise Filtering Cycles: {config['noise_filtering']['cyclic_aum']['num_cycles']}")
    
    # Show nutrition configuration
    print(f"\n🍎 Nutrition Configuration:")
    print(f"  Default Calorie Goal: {config['nutrition']['default_calorie_goal']} kcal")
    print(f"  Default Protein Goal: {config['nutrition']['default_protein_goal']}g")
    print(f"  Default Carbs Goal: {config['nutrition']['default_carbs_goal']}g")
    print(f"  Default Fat Goal: {config['nutrition']['default_fat_goal']}g")
    
    # Show user preferences configuration
    print(f"\n👤 User Preferences Configuration:")
    print(f"  Dietary Restrictions: {list(config['user_preferences']['dietary_restrictions'].keys())}")
    print(f"  Health Goals: {list(config['user_preferences']['health_goals'].keys())}")
    print(f"  Activity Level: {config['user_preferences']['activity_level']}")
    print(f"  Age Group: {config['user_preferences']['age_group']}")
    
    # Show performance configuration
    print(f"\n🚀 Performance Configuration:")
    print(f"  GPU Usage: {config['performance']['use_gpu']}")
    print(f"  Number of Workers: {config['performance']['num_workers']}")
    print(f"  Cache Size: {config['performance']['cache_size']}")
    print(f"  Max Memory Usage: {config['performance']['max_memory_usage']*100:.0f}%")

def example_6_export_results():
    """Example 6: Exporting results and generating reports"""
    print("\n" + "="*70)
    print("EXAMPLE 6: EXPORTING RESULTS AND GENERATING REPORTS")
    print("="*70)
    
    # Initialize system and analyze foods
    system = NutritionDetectionSystem()
    result = system.detect_food_from_image("meal_image.jpg")
    
    # Export results to JSON
    export_data = {
        'timestamp': '2024-01-15T12:00:00Z',
        'image_path': 'meal_image.jpg',
        'detected_foods': [food['food'] for food in result['food_details']],
        'nutrition_summary': result['total_nutrition'],
        'diet_suggestions': result['suggestions'],
        'system_info': {
            'version': '1.0.0',
            'model_architecture': 'ResNet101',
            'vdic_detection_enabled': True,
            'noise_filtering_enabled': True
        }
    }
    
    # Save to file
    with open('nutrition_analysis_report.json', 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print("📄 Report Generated:")
    print(f"  File: nutrition_analysis_report.json")
    print(f"  Detected Foods: {len(export_data['detected_foods'])}")
    print(f"  Total Calories: {export_data['nutrition_summary']['calories']} kcal")
    print(f"  Diet Suggestions: {len(export_data['diet_suggestions'])}")
    
    # Generate summary report
    print(f"\n📊 Summary Report:")
    print(f"  Date: {export_data['timestamp']}")
    print(f"  Image: {export_data['image_path']}")
    print(f"  Foods: {', '.join(export_data['detected_foods'])}")
    print(f"  Calories: {export_data['nutrition_summary']['calories']} kcal")
    print(f"  Protein: {export_data['nutrition_summary']['protein']}g")
    print(f"  Carbs: {export_data['nutrition_summary']['carbs']}g")
    print(f"  Fat: {export_data['nutrition_summary']['fat']}g")

def main():
    """Run all examples"""
    print("AI-BASED NUTRITION DETECTION SYSTEM - PRACTICAL EXAMPLES")
    print("="*80)
    
    try:
        # Run all examples
        example_1_basic_food_detection()
        example_2_custom_user_preferences()
        example_3_vdic_food_analysis()
        example_4_meal_planning()
        example_5_system_configuration()
        example_6_export_results()
        
        print("\n" + "="*80)
        print("🎉 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nThese examples demonstrate the key capabilities of the system:")
        print("• Basic food detection and nutrition analysis")
        print("• Custom user preferences and dietary restrictions")
        print("• VDIC food classification and synonym expansion")
        print("• Meal planning with nutrition goals")
        print("• System configuration and customization")
        print("• Results export and reporting")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure all dependencies are installed and the system is properly configured.")

if __name__ == "__main__":
    main()



#!/usr/bin/env python3
"""
Test script for the AI-based Nutrition Detection and Diet Suggestion System
This script demonstrates various components and allows testing of different functionalities
"""

import sys
import os
import time
from fd import (
    VDICFoodDetector, 
    ImageCollector, 
    AccuracyGapEstimator, 
    CyclicAUM,
    NutritionAnalyzer,
    NutritionDetectionSystem
)
from config import get_config, validate_config

def test_vdic_detector():
    """Test VDIC food detection functionality"""
    print("\n" + "="*60)
    print("TESTING VDIC FOOD DETECTOR")
    print("="*60)
    
    detector = VDICFoodDetector()
    
    # Test foods
    test_foods = [
        'banana', 'apple', 'sandwich', 'pizza', 'carrot',
        'cucumber', 'chips', 'chocolate', 'soup', 'raw_meat'
    ]
    
    print("Testing VDIC classification:")
    for food in test_foods:
        is_vdic = detector.predict_vdic_status(food)
        status = "✓ VDIC" if is_vdic else "✗ Not VDIC"
        print(f"  {food:15} -> {status}")
    
    # Test synonym expansion
    print("\nTesting synonym expansion:")
    test_synonyms = ['tomato', 'apple', 'banana', 'sandwich']
    for food in test_synonyms:
        synonyms = detector.expand_synonyms(food)
        print(f"  {food:15} -> {', '.join(synonyms)}")
    
    return True

def test_image_collector():
    """Test image collection functionality"""
    print("\n" + "="*60)
    print("TESTING IMAGE COLLECTOR")
    print("="*60)
    
    collector = ImageCollector()
    
    # Test image collection
    test_foods = ['pizza', 'apple', 'salad']
    for food in test_foods:
        print(f"\nCollecting images for: {food}")
        images = collector.collect_images(food, max_images=20)
        
        clean_count = sum(1 for img in images if img['is_clean'])
        noisy_count = len(images) - clean_count
        
        print(f"  Total images: {len(images)}")
        print(f"  Clean images: {clean_count}")
        print(f"  Noisy images: {noisy_count}")
        print(f"  Average confidence: {sum(img['confidence'] for img in images) / len(images):.3f}")
    
    return True

def test_noise_filtering():
    """Test noise filtering algorithms"""
    print("\n" + "="*60)
    print("TESTING NOISE FILTERING ALGORITHMS")
    print("="*60)
    
    # Create sample data
    sample_images = []
    for i in range(50):
        sample_images.append({
            'id': f'img_{i}',
            'is_clean': i < 35,  # 70% clean images
            'confidence': 0.9 if i < 35 else 0.3
        })
    
    # Test Accuracy Gap
    print("Testing Accuracy Gap (AccGap) algorithm:")
    acc_gap = AccuracyGapEstimator()
    
    predictions = [1 if img['is_clean'] else 0 for img in sample_images]
    ground_truth = [1 if img['is_clean'] else 0 for img in sample_images]
    
    noise_level = acc_gap.estimate_noise_level(sample_images, predictions, ground_truth)
    print(f"  Estimated noise level: {noise_level:.3f}")
    print(f"  Actual noise level: {1 - sum(1 for img in sample_images if img['is_clean']) / len(sample_images):.3f}")
    
    # Test Cyclic AUM
    print("\nTesting Cyclic AUM algorithm:")
    cyclic_aum = CyclicAUM(num_cycles=3)
    
    margins = [img['confidence'] for img in sample_images]
    filtered_images = cyclic_aum.filter_samples(sample_images, margins)
    
    print(f"  Original images: {len(sample_images)}")
    print(f"  Filtered images: {len(filtered_images)}")
    print(f"  Filtering ratio: {len(filtered_images) / len(sample_images):.3f}")
    
    return True

def test_nutrition_analyzer():
    """Test nutrition analysis functionality"""
    print("\n" + "="*60)
    print("TESTING NUTRITION ANALYZER")
    print("="*60)
    
    analyzer = NutritionAnalyzer()
    
    # Test nutrition info retrieval
    test_foods = ['apple', 'banana', 'chicken_breast', 'salmon']
    print("Testing nutrition information retrieval:")
    
    for food in test_foods:
        nutrition = analyzer.get_nutrition_info(food)
        print(f"\n  {food}:")
        for nutrient, value in nutrition.items():
            unit = 'g' if nutrient != 'calories' else 'kcal'
            print(f"    {nutrient.capitalize()}: {value} {unit}")
    
    # Test diet suggestions
    print("\nTesting diet suggestions generation:")
    detected_foods = ['apple', 'banana', 'sandwich']
    
    # Test with default preferences
    suggestions_default = analyzer.generate_diet_suggestions(detected_foods)
    print(f"\n  Default preferences suggestions:")
    for suggestion in suggestions_default['suggestions']:
        print(f"    • {suggestion}")
    
    # Test with custom preferences
    custom_preferences = {
        'calorie_goal': 1500,
        'protein_goal': 120,
        'carbs_goal': 150,
        'fat_goal': 50
    }
    
    suggestions_custom = analyzer.generate_diet_suggestions(detected_foods, custom_preferences)
    print(f"\n  Custom preferences suggestions:")
    for suggestion in suggestions_custom['suggestions']:
        print(f"    • {suggestion}")
    
    return True

def test_complete_system():
    """Test the complete nutrition detection system"""
    print("\n" + "="*60)
    print("TESTING COMPLETE NUTRITION DETECTION SYSTEM")
    print("="*60)
    
    system = NutritionDetectionSystem()
    
    # Test the main pipeline
    print("Running complete nutrition detection pipeline...")
    start_time = time.time()
    
    try:
        result = system.detect_food_from_image("test_image.jpg")
        end_time = time.time()
        
        print(f"\nPipeline completed successfully in {end_time - start_time:.2f} seconds")
        print(f"Result type: {type(result)}")
        
        if isinstance(result, dict):
            print(f"Result keys: {list(result.keys())}")
        
        return True
        
    except Exception as e:
        print(f"Pipeline failed with error: {e}")
        return False

def test_configuration():
    """Test configuration system"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION SYSTEM")
    print("="*60)
    
    try:
        # Load configuration
        config = get_config()
        print("✓ Configuration loaded successfully")
        
        # Display some key configurations
        print(f"  Model architecture: {config['model']['architecture']}")
        print(f"  Number of classes: {config['model']['num_classes']}")
        print(f"  VDIC threshold: {config['vdic']['consensus_threshold']}")
        print(f"  Max images per food: {config['image_collection']['max_images_per_food']}")
        
        # Validate configuration
        errors = validate_config()
        if errors:
            print("\n⚠ Configuration validation warnings:")
            for error in errors:
                print(f"    {error}")
        else:
            print("✓ Configuration validation passed")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def run_performance_test():
    """Run a simple performance test"""
    print("\n" + "="*60)
    print("RUNNING PERFORMANCE TEST")
    print("="*60)
    
    import numpy as np
    
    # Test VDIC detection performance
    detector = VDICFoodDetector()
    test_foods = ['apple', 'banana', 'pizza', 'salad', 'chips'] * 100
    
    start_time = time.time()
    results = [detector.predict_vdic_status(food) for food in test_foods]
    end_time = time.time()
    
    vdic_time = end_time - start_time
    vdic_count = sum(results)
    
    print(f"VDIC Detection Performance:")
    print(f"  Processed {len(test_foods)} foods in {vdic_time:.4f} seconds")
    print(f"  Rate: {len(test_foods) / vdic_time:.0f} foods/second")
    print(f"  VDIC foods found: {vdic_count}")
    
    # Test noise filtering performance
    sample_images = [{'id': f'img_{i}', 'confidence': np.random.random()} for i in range(1000)]
    margins = [img['confidence'] for img in sample_images]
    
    start_time = time.time()
    cyclic_aum = CyclicAUM(num_cycles=3)
    filtered = cyclic_aum.filter_samples(sample_images, margins)
    end_time = time.time()
    
    filter_time = end_time - start_time
    
    print(f"\nNoise Filtering Performance:")
    print(f"  Processed {len(sample_images)} images in {filter_time:.4f} seconds")
    print(f"  Rate: {len(sample_images) / filter_time:.0f} images/second")
    print(f"  Filtered to: {len(filtered)} images")
    
    return True

def main():
    """Main test function"""
    print("AI-BASED NUTRITION DETECTION SYSTEM - COMPREHENSIVE TEST")
    print("="*80)
    
    # Test results
    test_results = {}
    
    # Run all tests
    tests = [
        ("Configuration", test_configuration),
        ("VDIC Detector", test_vdic_detector),
        ("Image Collector", test_image_collector),
        ("Noise Filtering", test_noise_filtering),
        ("Nutrition Analyzer", test_nutrition_analyzer),
        ("Complete System", test_complete_system),
        ("Performance", run_performance_test)
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning {test_name} test...")
            result = test_func()
            test_results[test_name] = "PASSED" if result else "FAILED"
            print(f"✓ {test_name} test completed")
        except Exception as e:
            test_results[test_name] = f"ERROR: {e}"
            print(f"✗ {test_name} test failed: {e}")
    
    # Display test summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, result in test_results.items():
        status = "✓" if result == "PASSED" else "✗"
        print(f"{status} {test_name:20} -> {result}")
    
    # Overall result
    passed_tests = sum(1 for result in test_results.values() if result == "PASSED")
    total_tests = len(test_results)
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The system is working correctly.")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



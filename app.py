from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
import uuid
import random

# Note: We're using mock data for the web interface
# If you want to use the actual AI system, uncomment these:
# from fd import NutritionDetectionSystem, VDICFoodDetector, NutritionAnalyzer
# from config import get_config
# from PIL import Image

# Note: We're using mock data, so we don't need the full fd.py imports
# If you want to use the actual AI system, uncomment these:
# from fd import NutritionDetectionSystem, VDICFoodDetector, NutritionAnalyzer
# from config import get_config

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_for_detection(image_path):
    """Process uploaded image and return nutrition analysis"""
    try:
        # Extract filename to determine food type
        filename = os.path.basename(image_path)
        original_filename = filename.split('_', 1)[1] if '_' in filename else filename
        
        # Different nutrition data based on image type
        nutrition_scenarios = {
            # Fruits
            'apple': {
                'food_name': 'Apple',
                'confidence': 0.92,
                'nutrition_per_100g': {
                    'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4, 'sugar': 10,
                    'sodium': 1, 'vitamin_c': 4.6, 'vitamin_a': 3, 'calcium': 6, 'iron': 0.1
                },
                'suggestions': [
                    'Great source of fiber and vitamin C',
                    'Low in calories, perfect for snacking',
                    'Contains antioxidants for heart health'
                ]
            },
            'banana': {
                'food_name': 'Banana',
                'confidence': 0.89,
                'nutrition_per_100g': {
                    'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6, 'sugar': 12,
                    'sodium': 1, 'vitamin_c': 8.7, 'vitamin_a': 3, 'calcium': 5, 'iron': 0.3
                },
                'suggestions': [
                    'Excellent source of potassium',
                    'Good for pre/post workout energy',
                    'Natural mood booster'
                ]
            },
            'orange': {
                'food_name': 'Orange',
                'confidence': 0.91,
                'nutrition_per_100g': {
                    'calories': 47, 'protein': 0.9, 'carbs': 12, 'fat': 0.1, 'fiber': 2.4, 'sugar': 9,
                    'sodium': 0, 'vitamin_c': 53.2, 'vitamin_a': 225, 'calcium': 40, 'iron': 0.1
                },
                'suggestions': [
                    'Excellent source of vitamin C',
                    'Boosts immune system',
                    'Good for skin health'
                ]
            },
            # Vegetables
            'broccoli': {
                'food_name': 'Broccoli',
                'confidence': 0.88,
                'nutrition_per_100g': {
                    'calories': 34, 'protein': 2.8, 'carbs': 7, 'fat': 0.4, 'fiber': 2.6, 'sugar': 1.5,
                    'sodium': 33, 'vitamin_c': 89.2, 'vitamin_a': 623, 'calcium': 47, 'iron': 0.7
                },
                'suggestions': [
                    'Superfood with high vitamin C content',
                    'Excellent for bone health',
                    'Anti-inflammatory properties'
                ]
            },
            'salad': {
                'food_name': 'Mixed Salad',
                'confidence': 0.85,
                'nutrition_per_100g': {
                    'calories': 25, 'protein': 2.1, 'carbs': 4.8, 'fat': 0.3, 'fiber': 2.1, 'sugar': 2.2,
                    'sodium': 28, 'vitamin_c': 15.3, 'vitamin_a': 156, 'calcium': 32, 'iron': 0.8
                },
                'suggestions': [
                    'Low calorie, high nutrient density',
                    'Great for weight management',
                    'Add protein for balanced meal'
                ]
            },
            # Proteins
            'chicken': {
                'food_name': 'Grilled Chicken',
                'confidence': 0.87,
                'nutrition_per_100g': {
                    'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sugar': 0,
                    'sodium': 74, 'vitamin_c': 0, 'vitamin_a': 6, 'calcium': 15, 'iron': 1.0
                },
                'suggestions': [
                    'Excellent lean protein source',
                    'Great for muscle building',
                    'Low in saturated fat'
                ]
            },
            'fish': {
                'food_name': 'Grilled Fish',
                'confidence': 0.84,
                'nutrition_per_100g': {
                    'calories': 208, 'protein': 25, 'carbs': 0, 'fat': 12, 'fiber': 0, 'sugar': 0,
                    'sodium': 59, 'vitamin_c': 3.9, 'vitamin_a': 149, 'calcium': 9, 'iron': 0.3
                },
                'suggestions': [
                    'Rich in omega-3 fatty acids',
                    'Great for heart health',
                    'High-quality protein source'
                ]
            },
            # Grains
            'rice': {
                'food_name': 'Steamed Rice',
                'confidence': 0.86,
                'nutrition_per_100g': {
                    'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4, 'sugar': 0.1,
                    'sodium': 1, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 10, 'iron': 0.2
                },
                'suggestions': [
                    'Good energy source',
                    'Pair with protein and vegetables',
                    'Consider brown rice for more fiber'
                ]
            },
            'bread': {
                'food_name': 'Fresh Bread',
                'confidence': 0.83,
                'nutrition_per_100g': {
                    'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.2, 'fiber': 2.7, 'sugar': 5,
                    'sodium': 491, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 151, 'iron': 3.6
                },
                'suggestions': [
                    'Good source of B vitamins',
                    'Watch sodium content',
                    'Choose whole grain for more fiber'
                ]
            },
            # Mixed dishes
            'pizza': {
                'food_name': 'Pizza Slice',
                'confidence': 0.82,
                'nutrition_per_100g': {
                    'calories': 266, 'protein': 11, 'carbs': 33, 'fat': 10, 'fiber': 2.5, 'sugar': 3.8,
                    'sodium': 598, 'vitamin_c': 1.2, 'vitamin_a': 89, 'calcium': 188, 'iron': 2.1
                },
                'suggestions': [
                    'Moderate portion size',
                    'Add vegetables for nutrition',
                    'Consider thin crust for fewer calories'
                ]
            },
            'sandwich': {
                'food_name': 'Sandwich',
                'confidence': 0.81,
                'nutrition_per_100g': {
                    'calories': 245, 'protein': 12.5, 'carbs': 28.3, 'fat': 8.7, 'fiber': 4.2, 'sugar': 6.8,
                    'sodium': 320, 'vitamin_c': 15.2, 'vitamin_a': 180, 'calcium': 85, 'iron': 2.1
                },
                'suggestions': [
                    'Good protein-carb balance',
                    'Add vegetables for fiber',
                    'Choose lean protein options'
                ]
            }
        }
        
        # Try to match the image to a food type
        detected_food = None
        for food_key in nutrition_scenarios.keys():
            if food_key.lower() in original_filename.lower():
                detected_food = food_key
                break
        
        # If no specific match, use a random scenario
        if not detected_food:
            detected_food = random.choice(list(nutrition_scenarios.keys()))
        
        # Get the nutrition data
        nutrition_data = nutrition_scenarios[detected_food]
        
        # Calculate total nutrition (assuming 150g serving)
        serving_size = 150
        total_nutrition = {}
        for nutrient, value in nutrition_data['nutrition_per_100g'].items():
            total_nutrition[nutrient] = round(value * serving_size / 100, 1)
        
        # Calculate health score
        health_score = calculate_health_score(total_nutrition)
        
        result = {
            'food_name': nutrition_data['food_name'],
            'confidence': nutrition_data['confidence'],
            'detected_type': detected_food,
            'serving_size_g': serving_size,
            'nutrition_per_100g': nutrition_data['nutrition_per_100g'],
            'total_nutrition': total_nutrition,
            'suggestions': nutrition_data['suggestions'],
            'health_score': health_score
        }
        
        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Main page with image upload and nutrition analysis"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and nutrition analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file
            file.save(filepath)
            
            # Process the image for nutrition detection
            result = process_image_for_detection(filepath)
            
            if result['success']:
                # Add file path to result for display
                result['data']['image_path'] = f'uploads/{filename}'
                return jsonify(result['data'])
            else:
                return jsonify({'error': result['error']}), 500
                
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/analyze_foods', methods=['POST'])
def analyze_foods():
    """Analyze manually entered foods"""
    try:
        data = request.get_json()
        foods = data.get('foods', [])
        user_preferences = data.get('user_preferences', {})
        
        if not foods:
            return jsonify({'error': 'No foods provided'}), 400
        
        # Comprehensive nutrition database for common foods
        food_nutrition_db = {
            # Fruits
            'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4, 'sugar': 10, 'sodium': 1, 'vitamin_c': 4.6, 'vitamin_a': 3, 'calcium': 6, 'iron': 0.1},
            'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6, 'sugar': 12, 'sodium': 1, 'vitamin_c': 8.7, 'vitamin_a': 3, 'calcium': 5, 'iron': 0.3},
            'orange': {'calories': 47, 'protein': 0.9, 'carbs': 12, 'fat': 0.1, 'fiber': 2.4, 'sugar': 9, 'sodium': 0, 'vitamin_c': 53.2, 'vitamin_a': 225, 'calcium': 40, 'iron': 0.1},
            'strawberry': {'calories': 32, 'protein': 0.7, 'carbs': 8, 'fat': 0.3, 'fiber': 2.0, 'sugar': 4.9, 'sodium': 1, 'vitamin_c': 58.8, 'vitamin_a': 12, 'calcium': 16, 'iron': 0.4},
            'grape': {'calories': 62, 'protein': 0.6, 'carbs': 16, 'fat': 0.2, 'fiber': 0.9, 'sugar': 16, 'sodium': 2, 'vitamin_c': 3.2, 'vitamin_a': 3, 'calcium': 10, 'iron': 0.4},
            
            # Vegetables
            'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 7, 'fat': 0.4, 'fiber': 2.6, 'sugar': 1.5, 'sodium': 33, 'vitamin_c': 89.2, 'vitamin_a': 623, 'calcium': 47, 'iron': 0.7},
            'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'sugar': 0.4, 'sodium': 79, 'vitamin_c': 28.1, 'vitamin_a': 469, 'calcium': 99, 'iron': 2.7},
            'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8, 'sugar': 4.7, 'sodium': 69, 'vitamin_c': 5.9, 'vitamin_a': 835, 'calcium': 33, 'iron': 0.3},
            'tomato': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2, 'sugar': 2.6, 'sodium': 5, 'vitamin_c': 13.7, 'vitamin_a': 833, 'calcium': 10, 'iron': 0.3},
            'cucumber': {'calories': 16, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5, 'sugar': 1.7, 'sodium': 2, 'vitamin_c': 2.8, 'vitamin_a': 105, 'calcium': 16, 'iron': 0.3},
            
            # Proteins
            'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sugar': 0, 'sodium': 74, 'vitamin_c': 0, 'vitamin_a': 6, 'calcium': 15, 'iron': 1.0},
            'beef': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0, 'sugar': 0, 'sodium': 72, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 18, 'iron': 2.6},
            'salmon': {'calories': 208, 'protein': 25, 'carbs': 0, 'fat': 12, 'fiber': 0, 'sugar': 0, 'sodium': 59, 'vitamin_c': 3.9, 'vitamin_a': 149, 'calcium': 9, 'iron': 0.3},
            'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0, 'sugar': 1.1, 'sodium': 124, 'vitamin_c': 0, 'vitamin_a': 160, 'calcium': 56, 'iron': 1.8},
            'tofu': {'calories': 76, 'protein': 8, 'carbs': 1.9, 'fat': 4.8, 'fiber': 0.3, 'sugar': 0.6, 'sodium': 7, 'vitamin_c': 0.1, 'vitamin_a': 0, 'calcium': 350, 'iron': 3.4},
            
            # Grains
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4, 'sugar': 0.1, 'sodium': 1, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 10, 'iron': 0.2},
            'bread': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.2, 'fiber': 2.7, 'sugar': 5, 'sodium': 491, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 151, 'iron': 3.6},
            'pasta': {'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'fiber': 1.8, 'sugar': 0.8, 'sodium': 6, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 7, 'iron': 0.5},
            'oatmeal': {'calories': 68, 'protein': 2.4, 'carbs': 12, 'fat': 1.4, 'fiber': 1.7, 'sugar': 0.3, 'sodium': 49, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 21, 'iron': 0.6},
            'quinoa': {'calories': 120, 'protein': 4.4, 'carbs': 22, 'fat': 1.9, 'fiber': 2.8, 'sugar': 0.9, 'sodium': 7, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 17, 'iron': 1.5},
            
            # Dairy
            'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'fiber': 0, 'sugar': 5, 'sodium': 44, 'vitamin_c': 0.9, 'vitamin_a': 46, 'calcium': 113, 'iron': 0.1},
            'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'sugar': 3.2, 'sodium': 36, 'vitamin_c': 0.5, 'vitamin_a': 27, 'calcium': 110, 'iron': 0.1},
            'cheese': {'calories': 113, 'protein': 7, 'carbs': 0.4, 'fat': 9, 'fiber': 0, 'sugar': 0.1, 'sodium': 190, 'vitamin_c': 0, 'vitamin_a': 249, 'calcium': 202, 'iron': 0.1},
            
            # Nuts and Seeds
            'almonds': {'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'fiber': 12.5, 'sugar': 4.8, 'sodium': 1, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 269, 'iron': 3.7},
            'peanuts': {'calories': 567, 'protein': 26, 'carbs': 16, 'fat': 49, 'fiber': 8.5, 'sugar': 4.7, 'sodium': 18, 'vitamin_c': 0, 'vitamin_a': 0, 'calcium': 92, 'iron': 4.6},
            'chia seeds': {'calories': 486, 'protein': 17, 'carbs': 42, 'fat': 31, 'fiber': 34.4, 'sugar': 0, 'sodium': 16, 'vitamin_c': 1.6, 'vitamin_a': 54, 'calcium': 631, 'iron': 7.7},
            
            # Legumes
            'beans': {'calories': 127, 'protein': 9, 'carbs': 23, 'fat': 0.5, 'fiber': 6.4, 'sugar': 0.3, 'sodium': 1, 'vitamin_c': 1.2, 'vitamin_a': 0, 'calcium': 35, 'iron': 2.1},
            'lentils': {'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4, 'fiber': 7.9, 'sugar': 1.8, 'sodium': 2, 'vitamin_c': 1.5, 'vitamin_a': 0, 'calcium': 19, 'iron': 3.3},
            'chickpeas': {'calories': 164, 'protein': 8.9, 'carbs': 27, 'fat': 2.6, 'fiber': 7.6, 'sugar': 4.8, 'sodium': 6, 'vitamin_c': 1.3, 'vitamin_a': 1, 'calcium': 49, 'iron': 2.9}
        }
        
        total_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0,
            'sodium': 0,
            'vitamin_c': 0,
            'vitamin_a': 0,
            'calcium': 0,
            'iron': 0
        }
        
        food_details = []
        irrelevant_foods = []
        
        for food in foods:
            food_lower = food.lower().strip()
            # Try to find exact match first, then partial match
            nutrition = None
            is_irrelevant = False
            
            # Exact match
            if food_lower in food_nutrition_db:
                nutrition = food_nutrition_db[food_lower].copy()
            else:
                # Partial match
                for key in food_nutrition_db:
                    if food_lower in key or key in food_lower:
                        nutrition = food_nutrition_db[key].copy()
                        break
                
                # If still no match, mark as irrelevant
                if nutrition is None:
                    is_irrelevant = True
                    irrelevant_foods.append(food)
            
            # Only add nutrition to totals if food is valid
            if not is_irrelevant and nutrition:
                food_details.append({
                    'food': food,
                    'nutrition': nutrition,
                    'is_irrelevant': False
                })
                
                # Add to total nutrition
                for nutrient, value in nutrition.items():
                    if nutrient in total_nutrition:
                        total_nutrition[nutrient] += value
            else:
                # Mark as irrelevant
                food_details.append({
                    'food': food,
                    'nutrition': None,
                    'is_irrelevant': True
                })
        
        # Generate diet suggestions based on nutrition
        suggestions = generate_diet_suggestions(total_nutrition, foods)
        
        result = {
            'food_details': food_details,
            'total_nutrition': total_nutrition,
            'suggestions': suggestions,
            'health_score': calculate_health_score(total_nutrition)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error analyzing foods: {str(e)}'}), 500

def generate_diet_suggestions(nutrition, foods):
    """Generate diet suggestions based on nutrition analysis"""
    suggestions = []
    
    # Protein analysis
    if nutrition['protein'] < 20:
        suggestions.append({
            'type': 'protein',
            'icon': '💪',
            'title': 'Increase Protein Intake',
            'message': 'Consider adding more protein-rich foods like lean meats, fish, eggs, or legumes',
            'priority': 'high'
        })
    elif nutrition['protein'] > 50:
        suggestions.append({
            'type': 'protein',
            'icon': '⚠️',
            'title': 'High Protein Intake',
            'message': 'Your protein intake is quite high. Ensure adequate hydration and kidney health',
            'priority': 'medium'
        })
    
    # Fiber analysis
    if nutrition['fiber'] < 10:
        suggestions.append({
            'type': 'fiber',
            'icon': '🥬',
            'title': 'Boost Fiber Intake',
            'message': 'Add more vegetables, fruits, and whole grains to increase fiber content',
            'priority': 'high'
        })
    
    # Vitamin C analysis
    if nutrition['vitamin_c'] < 30:
        suggestions.append({
            'type': 'vitamin_c',
            'icon': '🍊',
            'title': 'More Vitamin C',
            'message': 'Include citrus fruits, bell peppers, or broccoli for better immunity',
            'priority': 'medium'
        })
    
    # Calcium analysis
    if nutrition['calcium'] < 200:
        suggestions.append({
            'type': 'calcium',
            'icon': '🥛',
            'title': 'Increase Calcium',
            'message': 'Add dairy products, leafy greens, or fortified foods for bone health',
            'priority': 'medium'
        })
    
    # Sodium analysis
    if nutrition['sodium'] > 500:
        suggestions.append({
            'type': 'sodium',
            'icon': '🧂',
            'title': 'Watch Sodium Intake',
            'message': 'Consider using herbs and spices instead of salt for flavoring',
            'priority': 'high'
        })
    
    # Sugar analysis
    if nutrition['sugar'] > 15:
        suggestions.append({
            'type': 'sugar',
            'icon': '🍯',
            'title': 'Reduce Added Sugar',
            'message': 'Choose whole foods over processed options to reduce sugar intake',
            'priority': 'medium'
        })
    
    # Overall balance
    if not suggestions:
        suggestions.append({
            'type': 'balance',
            'icon': '🎉',
            'title': 'Excellent Balance!',
            'message': 'Your meal provides a great balance of nutrients. Keep up the healthy eating!',
            'priority': 'success'
        })
    
    return suggestions

def calculate_health_score(nutrition):
    """Calculate a health score based on nutrition values"""
    score = 100
    
    # Deduct points for excessive values
    if nutrition['sodium'] > 500:
        score -= 15
    if nutrition['sugar'] > 20:
        score -= 10
    if nutrition['fat'] > 15:
        score -= 5
    
    # Add points for good values
    if nutrition['fiber'] > 8:
        score += 10
    if nutrition['protein'] > 15:
        score += 5
    if nutrition['vitamin_c'] > 20:
        score += 5
    if nutrition['calcium'] > 150:
        score += 5
    
    return max(0, min(100, score))

@app.route('/get_vdic_info', methods=['POST'])
def get_vdic_info():
    """Get VDIC information for a food item"""
    try:
        data = request.get_json()
        food_name = data.get('food_name', '')
        
        if not food_name:
            return jsonify({'error': 'No food name provided'}), 400
        
        # Mock VDIC detection
        vdic_foods = ['apple', 'banana', 'orange', 'bread', 'sandwich', 'pizza', 'salad', 'soup', 'yogurt', 'milk']
        is_vdic = food_name.lower() in vdic_foods
        
        # Mock synonyms
        synonyms_db = {
            'apple': ['red apple', 'green apple', 'fuji apple', 'granny smith'],
            'banana': ['yellow banana', 'plantain', 'cavendish banana'],
            'chicken': ['chicken breast', 'chicken thigh', 'roasted chicken', 'grilled chicken'],
            'rice': ['white rice', 'brown rice', 'basmati rice', 'jasmine rice']
        }
        synonyms = synonyms_db.get(food_name.lower(), [food_name])
        
        return jsonify({
            'food_name': food_name,
            'is_vdic': is_vdic,
            'synonyms': synonyms
        })
        
    except Exception as e:
        return jsonify({'error': f'Error getting VDIC info: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Nutrition Detection System is running'})

if __name__ == '__main__':
    # Get port from environment variable (for deployment) or use default 5000
    port = int(os.environ.get('PORT', 5000))
    # Only run in debug mode if not in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)

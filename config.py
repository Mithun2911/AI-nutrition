"""
Configuration file for the AI-based Nutrition Detection and Diet Suggestion System
Modify these parameters to customize the system behavior
"""

# API Configuration
SPOONACULAR_API_KEY = "your_spoonacular_api_key_here"
SPOONACULAR_BASE_URL = "https://api.spoonacular.com/food"

# Model Configuration
MODEL_CONFIG = {
    'architecture': 'resnet101',
    'pretrained': True,
    'num_classes': 100,  # Adjust based on your food categories
    'input_size': (224, 224),
    'dropout_rate': 0.5,
    'learning_rate': 0.001,
    'batch_size': 32,
    'num_epochs': 20
}

# VDIC Detection Configuration
VDIC_CONFIG = {
    'consensus_threshold': 2,  # Minimum score for VDIC classification
    'categories': {
        'fruits': ['banana', 'apple', 'orange', 'grape', 'strawberry', 'blueberry', 
                  'mango', 'pineapple', 'kiwi', 'peach', 'plum', 'cherry'],
        'vegetables': ['carrot', 'cucumber', 'tomato', 'lettuce', 'spinach', 
                      'broccoli', 'cauliflower', 'bell_pepper', 'onion', 'garlic'],
        'ready_foods': ['sandwich', 'pizza', 'burger', 'sushi', 'salad', 
                       'pasta', 'rice', 'noodles', 'soup', 'stew'],
        'snacks': ['chips', 'nuts', 'chocolate', 'cookies', 'popcorn', 
                  'crackers', 'pretzels', 'trail_mix', 'granola_bar']
    }
}

# Image Collection Configuration
IMAGE_COLLECTION_CONFIG = {
    'max_images_per_food': 100,
    'search_engines': ['google', 'bing', 'baidu'],
    'image_formats': ['.jpg', '.jpeg', '.png', '.webp'],
    'min_image_size': (100, 100),
    'max_image_size': (2000, 2000)
}

# Noise Filtering Configuration
NOISE_FILTERING_CONFIG = {
    'acc_gap': {
        'accuracy_threshold': 0.8,
        'noise_estimation_method': 'gap_based'
    },
    'cyclic_aum': {
        'num_cycles': 3,
        'aum_threshold_factor': 0.5,
        'cycle_adjustment_factor': 0.1
    }
}

# Training Configuration
TRAINING_CONFIG = {
    'optimizer': 'adam',
    'scheduler': 'step',
    'scheduler_step_size': 7,
    'scheduler_gamma': 0.1,
    'weight_decay': 1e-4,
    'gradient_clipping': 1.0,
    'early_stopping_patience': 10,
    'validation_split': 0.2
}

# Data Augmentation Configuration
AUGMENTATION_CONFIG = {
    'enabled': True,
    'transforms': {
        'random_horizontal_flip': 0.5,
        'random_rotation': 15,
        'random_brightness': 0.2,
        'random_contrast': 0.2,
        'random_saturation': 0.2,
        'random_hue': 0.1,
        'color_jitter': True
    }
}

# Nutrition Analysis Configuration
NUTRITION_CONFIG = {
    'default_calorie_goal': 2000,
    'default_protein_goal': 150,  # grams
    'default_carbs_goal': 250,    # grams
    'default_fat_goal': 65,       # grams
    'default_fiber_goal': 25,     # grams
    'default_sugar_limit': 50,    # grams
    'nutrients_to_track': ['calories', 'protein', 'carbs', 'fat', 'fiber', 'sugar', 
                          'sodium', 'vitamin_c', 'vitamin_d', 'calcium', 'iron']
}

# User Preferences Configuration
USER_PREFERENCES_CONFIG = {
    'dietary_restrictions': {
        'vegetarian': False,
        'vegan': False,
        'gluten_free': False,
        'dairy_free': False,
        'nut_free': False
    },
    'health_goals': {
        'weight_loss': False,
        'muscle_gain': False,
        'maintenance': False,
        'diabetes_management': False,
        'heart_health': False
    },
    'activity_level': 'moderate',  # sedentary, light, moderate, active, very_active
    'age_group': 'adult',          # child, teen, adult, senior
    'gender': 'not_specified'      # male, female, not_specified
}

# System Performance Configuration
PERFORMANCE_CONFIG = {
    'use_gpu': True,
    'num_workers': 4,
    'pin_memory': True,
    'prefetch_factor': 2,
    'cache_size': 1000,
    'max_memory_usage': 0.8  # 80% of available memory
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'nutrition_system.log',
    'console_output': True
}

# File Paths Configuration
FILE_PATHS = {
    'models_dir': './models/',
    'data_dir': './data/',
    'logs_dir': './logs/',
    'temp_dir': './temp/',
    'output_dir': './output/'
}

# Web Interface Configuration (if implementing web UI)
WEB_CONFIG = {
    'host': 'localhost',
    'port': 5000,
    'debug': False,
    'secret_key': 'your_secret_key_here',
    'max_file_size': 16 * 1024 * 1024,  # 16MB
    'allowed_extensions': ['.jpg', '.jpeg', '.png', '.webp']
}

# Database Configuration (if implementing database storage)
DATABASE_CONFIG = {
    'type': 'sqlite',  # sqlite, postgresql, mysql
    'host': 'localhost',
    'port': 5432,
    'database': 'nutrition_db',
    'username': 'username',
    'password': 'password'
}

# External API Configuration
EXTERNAL_APIS = {
    'spoonacular': {
        'enabled': True,
        'api_key': SPOONACULAR_API_KEY,
        'base_url': SPOONACULAR_BASE_URL,
        'rate_limit': 150,  # requests per day
        'timeout': 30
    },
    'usda': {
        'enabled': False,
        'api_key': 'your_usda_api_key_here',
        'base_url': 'https://api.nal.usda.gov/fdc/v1/',
        'rate_limit': 1000,
        'timeout': 30
    },
    'openfoodfacts': {
        'enabled': False,
        'base_url': 'https://world.openfoodfacts.org/api/v0/product/',
        'timeout': 30
    }
}

# Model Evaluation Configuration
EVALUATION_CONFIG = {
    'metrics': ['accuracy', 'precision', 'recall', 'f1_score', 'confusion_matrix'],
    'cross_validation_folds': 5,
    'test_size': 0.2,
    'random_state': 42,
    'save_predictions': True,
    'save_confusion_matrix': True
}

# Deployment Configuration
DEPLOYMENT_CONFIG = {
    'environment': 'development',  # development, staging, production
    'version': '1.0.0',
    'auto_update': False,
    'health_check_interval': 300,  # seconds
    'backup_enabled': True,
    'backup_interval': 86400  # 24 hours in seconds
}

def get_config():
    """
    Return the complete configuration dictionary
    """
    return {
        'model': MODEL_CONFIG,
        'vdic': VDIC_CONFIG,
        'image_collection': IMAGE_COLLECTION_CONFIG,
        'noise_filtering': NOISE_FILTERING_CONFIG,
        'training': TRAINING_CONFIG,
        'augmentation': AUGMENTATION_CONFIG,
        'nutrition': NUTRITION_CONFIG,
        'user_preferences': USER_PREFERENCES_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'logging': LOGGING_CONFIG,
        'file_paths': FILE_PATHS,
        'web': WEB_CONFIG,
        'database': DATABASE_CONFIG,
        'external_apis': EXTERNAL_APIS,
        'evaluation': EVALUATION_CONFIG,
        'deployment': DEPLOYMENT_CONFIG
    }

def update_config(new_config):
    """
    Update configuration with new values
    """
    global MODEL_CONFIG, VDIC_CONFIG, IMAGE_COLLECTION_CONFIG, NOISE_FILTERING_CONFIG
    global TRAINING_CONFIG, AUGMENTATION_CONFIG, NUTRITION_CONFIG, USER_PREFERENCES_CONFIG
    global PERFORMANCE_CONFIG, LOGGING_CONFIG, FILE_PATHS, WEB_CONFIG
    global DATABASE_CONFIG, EXTERNAL_APIS, EVALUATION_CONFIG, DEPLOYMENT_CONFIG
    
    # Update each configuration section
    if 'model' in new_config:
        MODEL_CONFIG.update(new_config['model'])
    if 'vdic' in new_config:
        VDIC_CONFIG.update(new_config['vdic'])
    if 'image_collection' in new_config:
        IMAGE_COLLECTION_CONFIG.update(new_config['image_collection'])
    if 'noise_filtering' in new_config:
        NOISE_FILTERING_CONFIG.update(new_config['noise_filtering'])
    if 'training' in new_config:
        TRAINING_CONFIG.update(new_config['training'])
    if 'augmentation' in new_config:
        AUGMENTATION_CONFIG.update(new_config['augmentation'])
    if 'nutrition' in new_config:
        NUTRITION_CONFIG.update(new_config['nutrition'])
    if 'user_preferences' in new_config:
        USER_PREFERENCES_CONFIG.update(new_config['user_preferences'])
    if 'performance' in new_config:
        PERFORMANCE_CONFIG.update(new_config['performance'])
    if 'logging' in new_config:
        LOGGING_CONFIG.update(new_config['logging'])
    if 'file_paths' in new_config:
        FILE_PATHS.update(new_config['file_paths'])
    if 'web' in new_config:
        WEB_CONFIG.update(new_config['web'])
    if 'database' in new_config:
        DATABASE_CONFIG.update(new_config['database'])
    if 'external_apis' in new_config:
        EXTERNAL_APIS.update(new_config['external_apis'])
    if 'evaluation' in new_config:
        EVALUATION_CONFIG.update(new_config['evaluation'])
    if 'deployment' in new_config:
        DEPLOYMENT_CONFIG.update(new_config['deployment'])

def validate_config():
    """
    Validate configuration parameters
    """
    errors = []
    
    # Check required API keys
    if EXTERNAL_APIS['spoonacular']['enabled'] and EXTERNAL_APIS['spoonacular']['api_key'] == "your_spoonacular_api_key_here":
        errors.append("Spoonacular API key not configured")
    
    # Check file paths exist
    for path_name, path in FILE_PATHS.items():
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create directory {path}: {e}")
    
    # Check model parameters
    if MODEL_CONFIG['num_classes'] <= 0:
        errors.append("Number of classes must be positive")
    
    if MODEL_CONFIG['input_size'][0] <= 0 or MODEL_CONFIG['input_size'][1] <= 0:
        errors.append("Input size dimensions must be positive")
    
    return errors

# Import os for directory creation
import os

if __name__ == "__main__":
    # Test configuration
    config = get_config()
    print("Configuration loaded successfully!")
    
    # Validate configuration
    errors = validate_config()
    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration validation passed!")



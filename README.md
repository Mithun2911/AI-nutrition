# AI-based Nutrition Detection and Diet Suggestion System

## Overview

This system transforms traditional text-based nutrition queries into an intuitive, image-driven approach for food recognition and nutrition tracking. It builds upon the Food Nutrition Knowledge Base (FoodnKB) and incorporates advanced AI techniques for robust visual food recognition.

## Key Features

- **VDIC Food Detection**: Identifies "Visually Discernible and Instantaneously Consumable" foods using LLM consensus
- **Advanced Noise Filtering**: Implements AccGap and Cyclic AUM algorithms for high-quality image datasets
- **Deep Learning Classification**: Uses ResNet101 pre-trained on ImageNet for accurate food recognition
- **Nutrition Analysis**: Integrates with Spoonacular API for comprehensive nutritional information
- **Personalized Diet Suggestions**: Provides tailored recommendations based on detected foods and user preferences

## System Architecture

### 1. VDIC Food Detector
- Uses consensus-based approach with multiple LLM predictions
- Categorizes foods into fruits, vegetables, ready foods, and snacks
- Expands food synonyms for comprehensive coverage

### 2. Image Collection & Noise Filtering
- Collects images from multiple search engines (Google, Bing, Baidu)
- Implements **Accuracy Gap (AccGap)** algorithm to estimate noise levels
- Uses **Cyclic AUM (cAUM)** for distinguishing clean, hard, and noisy samples

### 3. Deep Learning Model
- **ResNet101** architecture pre-trained on ImageNet
- Custom classification head for food categories
- Dropout layers for regularization
- Transfer learning approach for optimal performance

### 4. Nutrition Analyzer
- Integration with Spoonacular API
- Comprehensive nutritional analysis (calories, protein, carbs, fat, fiber, sugar)
- Personalized diet suggestions based on user goals

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nutrition-detection-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Spoonacular API key (optional):
```python
# In your code, replace with your actual API key
nutrition_analyzer = NutritionAnalyzer(api_key="your_spoonacular_api_key")
```

## Usage

### Basic Usage

```python
from fd import NutritionDetectionSystem

# Initialize the system
system = NutritionDetectionSystem()

# Detect food from image and get nutrition analysis
result = system.detect_food_from_image("path/to/food/image.jpg")

# Train the model
system.train_model(train_data, train_labels, num_epochs=10)

# Save the trained model
system.save_model("food_classifier_model.pth")
```

### Running the Demo

```bash
python fd.py
```

This will run a complete demonstration of the system including:
- VDIC food detection
- Image collection simulation
- Noise filtering algorithms
- Model training demonstration
- Nutrition analysis and diet suggestions

## Components in Detail

### VDICFoodDetector
```python
detector = VDICFoodDetector()
is_vdic = detector.predict_vdic_status("banana")  # Returns True
synonyms = detector.expand_synonyms("apple")      # Returns expanded list
```

### ImageCollector
```python
collector = ImageCollector()
images = collector.collect_images("pizza", max_images=100)
```

### AccuracyGapEstimator
```python
estimator = AccuracyGapEstimator()
noise_level = estimator.estimate_noise_level(images, predictions, ground_truth)
```

### CyclicAUM
```python
cyclic_aum = CyclicAUM(num_cycles=3)
filtered_images = cyclic_aum.filter_samples(images, margins)
```

### FoodClassifier
```python
model = FoodClassifier(num_classes=10, pretrained=True)
# Model uses ResNet101 with custom classification head
```

### NutritionAnalyzer
```python
analyzer = NutritionAnalyzer(api_key="your_key")
nutrition = analyzer.get_nutrition_info("apple")
suggestions = analyzer.generate_diet_suggestions(["apple", "banana"])
```

## API Integration

### Spoonacular API
The system integrates with the Spoonacular API for nutritional data. To use this feature:

1. Sign up at [Spoonacular](https://spoonacular.com/food-api)
2. Get your API key
3. Replace the placeholder in the code:
```python
nutrition_analyzer = NutritionAnalyzer(api_key="your_actual_api_key")
```

## Model Training

### Data Preparation
```python
# Prepare your food image dataset
train_data = your_image_data      # Shape: (N, 3, 224, 224)
train_labels = your_labels        # Shape: (N,)

# Train the model
system.train_model(train_data, train_labels, num_epochs=20)
```

### Custom Classes
```python
# Modify the FoodClassifier for your specific food categories
class CustomFoodClassifier(FoodClassifier):
    def __init__(self, num_classes, pretrained=True):
        super().__init__(num_classes, pretrained)
        # Add custom layers or modifications
```

## Performance Optimization

### GPU Acceleration
```python
# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
```

### Batch Processing
```python
# Use DataLoader for efficient batch processing
dataset = FoodDataset(image_paths, labels)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

## Extending the System

### Adding New Food Categories
```python
# Extend VDIC foods dictionary
detector.vdic_foods['new_category'] = ['food1', 'food2', 'food3']
```

### Custom Noise Filtering
```python
# Implement your own noise filtering algorithm
class CustomNoiseFilter:
    def filter_images(self, images):
        # Your custom logic here
        return filtered_images
```

### Additional APIs
```python
# Add support for other nutrition APIs
class ExtendedNutritionAnalyzer(NutritionAnalyzer):
    def get_nutrition_from_usda(self, food_name):
        # USDA API integration
        pass
```

## Research Background

This system is inspired by the research paper "Robust Visual Food Recognition for Enriching Nutrition Knowledge Bases" and builds upon:

- **FoodnKB**: Food Nutrition Knowledge Base
- **VDIC Classification**: Visually Discernible and Instantaneously Consumable foods
- **AccGap Algorithm**: Accuracy Gap estimation for noise assessment
- **Cyclic AUM**: Enhanced Area Under the Margin with cyclical training

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this system in your research, please cite:

```bibtex
@article{nutrition_detection_2024,
  title={AI-based Nutrition Detection and Diet Suggestion System},
  author={Your Name},
  journal={Journal Name},
  year={2024}
}
```

## Support

For questions and support:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## 🚀 Free Deployment (Share with Friends!)

Want to deploy this as a free website to share with friends? We've got you covered!

### Quick Deploy Options:

1. **Render** (Recommended - Easiest)
   - Free tier: 750 hours/month
   - Auto-deploy from GitHub
   - See `DEPLOYMENT_GUIDE.md` for step-by-step instructions

2. **Railway** (Best Free Tier)
   - $5 credit/month
   - Great for small apps
   - Auto-detects Python apps

3. **PythonAnywhere** (Simple)
   - Free tier available
   - Easy setup for beginners

4. **Replit** (Easiest for Beginners)
   - One-click deployment
   - Share instantly

### Before Deploying:

Run the preparation script:
```bash
python prepare_deploy.py
```

This will check all required files and prepare your project for deployment.

### Deployment Files:

- `requirements_deploy.txt` - Lightweight dependencies (no heavy ML libs)
- `Procfile` - For Render/Railway deployment
- `runtime.txt` - Python version specification
- `.gitignore` - Git ignore rules

### Full Guide:

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed instructions on deploying to any platform!

---

## Future Enhancements

- Real-time image processing
- Mobile app integration
- Multi-language support
- Advanced dietary restrictions handling
- Integration with wearable devices
- Community-driven food database



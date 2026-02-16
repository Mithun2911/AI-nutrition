// Global variables
let selectedFile = null;
let foodList = [];

// DOM elements
let uploadArea, uploadContent, uploadPreview, previewImage, imageInput, analyzeBtn;
let foodInput, foodListContainer, analyzeFoodsBtn, resultsSection, resultImage;
let nutritionGrid, suggestionsList, loadingOverlay, foodDetailsSection, foodDetailsList;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing NutriVision AI...');
    
    // Get DOM elements
    initializeDOMElements();
    
    // Debug: Check if elements are found
    console.log('📋 DOM Elements Check:');
    console.log('  - Food input element:', foodInput);
    console.log('  - Analyze foods button:', analyzeFoodsBtn);
    console.log('  - Food list container:', foodListContainer);
    console.log('  - Results section:', resultsSection);
    console.log('  - Nutrition grid:', nutritionGrid);
    console.log('  - Suggestions list:', suggestionsList);
    
    initializeEventListeners();
    initializeNavigation();
    
    // Test button functionality
    testButtonFunctionality();
});

// Initialize DOM elements
function initializeDOMElements() {
    uploadArea = document.getElementById('uploadArea');
    uploadContent = document.getElementById('uploadContent');
    uploadPreview = document.getElementById('uploadPreview');
    previewImage = document.getElementById('previewImage');
    imageInput = document.getElementById('imageInput');
    analyzeBtn = document.getElementById('analyzeBtn');
    foodInput = document.getElementById('foodInput');
    foodListContainer = document.getElementById('foodList');
    analyzeFoodsBtn = document.getElementById('analyzeFoodsBtn');
    resultsSection = document.getElementById('results');
    resultImage = document.getElementById('resultImage');
    nutritionGrid = document.getElementById('nutritionGrid');
    suggestionsList = document.getElementById('suggestionsList');
    loadingOverlay = document.getElementById('loadingOverlay');
    foodDetailsSection = document.getElementById('foodDetailsSection');
    foodDetailsList = document.getElementById('foodDetailsList');
}

// Test button functionality
function testButtonFunctionality() {
    console.log('🧪 Testing button functionality...');
    
    if (analyzeFoodsBtn) {
        console.log('✅ Analyze foods button found');
        console.log('  - Button text:', analyzeFoodsBtn.textContent);
        console.log('  - Button disabled:', analyzeFoodsBtn.disabled);
        
        // Test click event
        analyzeFoodsBtn.addEventListener('click', function(e) {
            console.log('🎯 Analyze foods button clicked!');
            e.preventDefault();
            analyzeFoods();
        });
        
        console.log('✅ Click event listener added to analyze foods button');
    } else {
        console.error('❌ Analyze foods button NOT FOUND!');
    }
}

// Initialize all event listeners
function initializeEventListeners() {
    console.log('🔧 Setting up event listeners...');
    
    // Image upload events
    if (uploadArea) {
        uploadArea.addEventListener('click', () => imageInput.click());
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('drop', handleDrop);
        console.log('✅ Image upload event listeners added');
    } else {
        console.error('❌ Upload area not found');
    }
    
    if (imageInput) {
        imageInput.addEventListener('change', handleFileSelect);
        console.log('✅ Image input event listener added');
    } else {
        console.error('❌ Image input not found');
    }
    
    // Food input events
    if (foodInput) {
        foodInput.addEventListener('keypress', handleFoodInputKeypress);
        foodInput.addEventListener('input', handleFoodInputChange);
        console.log('✅ Food input event listeners added');
    } else {
        console.error('❌ Food input not found');
    }
    
    // Add food button
    const addFoodBtn = document.querySelector('.food-input-group .btn');
    if (addFoodBtn) {
        addFoodBtn.addEventListener('click', function(e) {
            console.log('➕ Add food button clicked');
            e.preventDefault();
            addFood();
        });
        console.log('✅ Add food button event listener added');
    } else {
        console.error('❌ Add food button not found');
    }
    
    // Reset upload button
    const resetUploadBtn = document.querySelector('.upload-preview .btn');
    if (resetUploadBtn) {
        resetUploadBtn.addEventListener('click', function(e) {
            console.log('🔄 Reset upload button clicked');
            e.preventDefault();
            resetUpload();
        });
        console.log('✅ Reset upload button event listener added');
    } else {
        console.error('❌ Reset upload button not found');
    }
    
    // Analyze foods button
    if (analyzeFoodsBtn) {
        // Remove any existing onclick to avoid conflicts
        analyzeFoodsBtn.removeAttribute('onclick');
        
        // Add event listener
        analyzeFoodsBtn.addEventListener('click', function(e) {
            console.log('🎯 Analyze foods button clicked via event listener');
            e.preventDefault();
            analyzeFoods();
        });
        
        console.log('✅ Analyze foods button event listener added');
    } else {
        console.error('❌ Analyze foods button not found');
    }
    
    // Analyze image button
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', function(e) {
            console.log('🎯 Analyze image button clicked');
            e.preventDefault();
            analyzeImage();
        });
        console.log('✅ Analyze image button event listener added');
    } else {
        console.error('❌ Analyze image button not found');
    }
    
    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Handle food input changes
function handleFoodInputChange(e) {
    const value = e.target.value.trim();
    console.log('📝 Food input changed:', value);
    
    // Enable/disable analyze button based on food list
    if (analyzeFoodsBtn) {
        analyzeFoodsBtn.disabled = foodList.length === 0;
        console.log('🔘 Analyze button disabled:', analyzeFoodsBtn.disabled);
    }
}

// Initialize navigation
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Handle drag and drop events
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Process selected file
function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showNotification('Please select an image file', 'error');
        return;
    }
    
    selectedFile = file;
    displayImagePreview(file);
    if (analyzeBtn) {
        analyzeBtn.disabled = false;
    }
}

// Display image preview
function displayImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        if (previewImage) {
            previewImage.src = e.target.result;
        }
        if (uploadContent) {
            uploadContent.style.display = 'none';
        }
        if (uploadPreview) {
            uploadPreview.style.display = 'block';
        }
    };
    reader.readAsDataURL(file);
}

// Reset upload
function resetUpload() {
    selectedFile = null;
    if (uploadContent) {
        uploadContent.style.display = 'block';
    }
    if (uploadPreview) {
        uploadPreview.style.display = 'none';
    }
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
    }
    if (imageInput) {
        imageInput.value = '';
    }
}

// Analyze uploaded image
async function analyzeImage() {
    if (!selectedFile) {
        showNotification('Please select an image first', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
            scrollToResults();
        } else {
            throw new Error(result.error || 'Failed to analyze image');
        }
    } catch (error) {
        console.error('Error analyzing image:', error);
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Handle food input
function handleFoodInputKeypress(e) {
    if (e.key === 'Enter') {
        addFood();
    }
}

// Add food to list
function addFood() {
    console.log('➕ Adding food...');
    
    if (!foodInput) {
        console.error('❌ Food input element not found');
        showNotification('Food input not found', 'error');
        return;
    }
    
    const foodName = foodInput.value.trim();
    console.log('🍎 Food name:', foodName);
    
    if (!foodName) {
        showNotification('Please enter a food name', 'error');
        return;
    }
    
    if (foodList.includes(foodName)) {
        showNotification('This food is already in the list', 'warning');
        return;
    }
    
    foodList.push(foodName);
    console.log('📋 Food list updated:', foodList);
    
    updateFoodList();
    foodInput.value = '';
    
    if (analyzeFoodsBtn) {
        analyzeFoodsBtn.disabled = false;
        console.log('🔘 Analyze button enabled');
    }
    
    showNotification(`Added ${foodName} to the list`, 'success');
}

// Update food list display
function updateFoodList() {
    if (!foodListContainer) {
        console.error('❌ Food list container not found');
        return;
    }
    
    foodListContainer.innerHTML = '';
    
    foodList.forEach((food, index) => {
        const foodTag = document.createElement('div');
        foodTag.className = 'food-tag';
        foodTag.innerHTML = `
            ${food}
            <button class="remove-btn" onclick="removeFood(${index})">
                <i class="fas fa-times"></i>
            </button>
        `;
        foodListContainer.appendChild(foodTag);
    });
    
    console.log('📋 Food list display updated');
}

// Remove food from list
function removeFood(index) {
    const removedFood = foodList[index];
    foodList.splice(index, 1);
    updateFoodList();
    
    if (foodList.length === 0 && analyzeFoodsBtn) {
        analyzeFoodsBtn.disabled = true;
        console.log('🔘 Analyze button disabled (no foods)');
    }
    
    showNotification(`Removed ${removedFood} from the list`, 'info');
}

// Analyze manually entered foods
async function analyzeFoods() {
    console.log('🔍 Analyzing foods:', foodList);
    
    if (foodList.length === 0) {
        showNotification('Please add foods to analyze', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        console.log('📡 Sending request to /analyze_foods...');
        
        const response = await fetch('/analyze_foods', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                foods: foodList,
                user_preferences: {}
            })
        });
        
        console.log('📥 Response received:', response.status);
        
        const result = await response.json();
        console.log('📊 Analysis result:', result);
        
        if (response.ok) {
            // Create a mock result structure for manual entry
            const mockResult = {
                ...result,
                image_path: null,
                food_details: result.food_details || foodList.map(food => ({ food }))
            };
            
            displayResults(mockResult);
            scrollToResults();
            showNotification(`Analyzed ${foodList.length} food(s) successfully!`, 'success');
        } else {
            throw new Error(result.error || 'Failed to analyze foods');
        }
    } catch (error) {
        console.error('❌ Error analyzing foods:', error);
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Display analysis results
function displayResults(result) {
    console.log('📊 Displaying results:', result);
    
    // Display image if available
    if (resultImage && result.image_path) {
        resultImage.src = `/static/${result.image_path}`;
        resultImage.style.display = 'block';
    } else if (resultImage) {
        resultImage.style.display = 'none';
    }
    
    // Display individual food details if available
    if (result.food_details && result.food_details.length > 0) {
        displayFoodDetails(result.food_details);
    }
    
    // Display nutrition summary
    if (result.total_nutrition) {
        displayNutritionSummary(result.total_nutrition);
    }
    
    // Display diet suggestions
    if (result.suggestions) {
        displayDietSuggestions(result.suggestions);
    }
    
    // Show results section
    if (resultsSection) {
        resultsSection.style.display = 'block';
        console.log('📋 Results section displayed');
    }
}

// Display individual food details
function displayFoodDetails(foodDetails) {
    if (!foodDetailsList || !foodDetailsSection) {
        console.error('❌ Food details elements not found');
        return;
    }
    
    foodDetailsList.innerHTML = '';
    
    foodDetails.forEach((item, index) => {
        const foodCard = document.createElement('div');
        foodCard.className = 'food-detail-card';
        
        if (item.is_irrelevant) {
            // Show irrelevant food message
            foodCard.className += ' irrelevant-food';
            foodCard.innerHTML = `
                <div class="food-name irrelevant">
                    <span class="food-icon">❌</span>
                    <span class="food-text">${item.food}</span>
                </div>
                <div class="irrelevant-message">
                    <strong>Irrelevant food items</strong>
                    <p>This food item is not recognized in our database.</p>
                </div>
            `;
        } else if (item.nutrition) {
            // Show nutrition for valid food
            const nutrition = item.nutrition;
            foodCard.innerHTML = `
                <div class="food-name">
                    <span class="food-icon">✅</span>
                    <span class="food-text">${item.food}</span>
                </div>
                <div class="food-nutrition-grid">
                    <div class="food-nutrient">
                        <span class="nutrient-label">Calories:</span>
                        <span class="nutrient-value">${nutrition.calories || 0} kcal</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Protein:</span>
                        <span class="nutrient-value">${nutrition.protein || 0} g</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Carbs:</span>
                        <span class="nutrient-value">${nutrition.carbs || 0} g</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Fat:</span>
                        <span class="nutrient-value">${nutrition.fat || 0} g</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Fiber:</span>
                        <span class="nutrient-value">${nutrition.fiber || 0} g</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Sugar:</span>
                        <span class="nutrient-value">${nutrition.sugar || 0} g</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Sodium:</span>
                        <span class="nutrient-value">${nutrition.sodium || 0} mg</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Vitamin C:</span>
                        <span class="nutrient-value">${nutrition.vitamin_c || 0} mg</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Vitamin A:</span>
                        <span class="nutrient-value">${nutrition.vitamin_a || 0} IU</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Calcium:</span>
                        <span class="nutrient-value">${nutrition.calcium || 0} mg</span>
                    </div>
                    <div class="food-nutrient">
                        <span class="nutrient-label">Iron:</span>
                        <span class="nutrient-value">${nutrition.iron || 0} mg</span>
                    </div>
                </div>
            `;
        }
        
        foodDetailsList.appendChild(foodCard);
    });
    
    // Show the food details section
    foodDetailsSection.style.display = 'block';
}

// Display nutrition summary
function displayNutritionSummary(nutrition) {
    if (!nutritionGrid) {
        console.error('❌ Nutrition grid not found');
        return;
    }
    
    nutritionGrid.innerHTML = '';
    
    const nutrients = [
        { key: 'calories', label: 'Calories', unit: 'kcal', icon: '🔥' },
        { key: 'protein', label: 'Protein', unit: 'g', icon: '💪' },
        { key: 'carbs', label: 'Carbohydrates', unit: 'g', icon: '🌾' },
        { key: 'fat', label: 'Fat', unit: 'g', icon: '🥑' },
        { key: 'fiber', label: 'Fiber', unit: 'g', icon: '🥬' },
        { key: 'sugar', label: 'Sugar', unit: 'g', icon: '🍯' },
        { key: 'sodium', label: 'Sodium', unit: 'mg', icon: '🧂' },
        { key: 'vitamin_c', label: 'Vitamin C', unit: 'mg', icon: '🍊' },
        { key: 'vitamin_a', label: 'Vitamin A', unit: 'IU', icon: '🥕' },
        { key: 'calcium', label: 'Calcium', unit: 'mg', icon: '🥛' },
        { key: 'iron', label: 'Iron', unit: 'mg', icon: '🩸' }
    ];
    
    nutrients.forEach(nutrient => {
        const value = nutrition[nutrient.key] || 0;
        const nutritionItem = document.createElement('div');
        nutritionItem.className = 'nutrition-item';
        nutritionItem.innerHTML = `
            <div class="nutrition-icon">${nutrient.icon}</div>
            <div class="nutrition-value">${value}</div>
            <div class="nutrition-label">${nutrient.label} (${nutrient.unit})</div>
        `;
        nutritionGrid.appendChild(nutritionItem);
    });
}

// Display diet suggestions
function displayDietSuggestions(suggestions) {
    if (!suggestionsList) {
        console.error('❌ Suggestions list not found');
        return;
    }
    
    suggestionsList.innerHTML = '';
    
    if (suggestions && suggestions.length > 0) {
        suggestions.forEach(suggestion => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = `suggestion-item suggestion-${suggestion.priority || 'medium'}`;
            
            // Handle both old string format and new object format
            if (typeof suggestion === 'string') {
                suggestionItem.innerHTML = `
                    <div class="suggestion-icon">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                    <div class="suggestion-content">
                        <div class="suggestion-title">Diet Suggestion</div>
                        <div class="suggestion-message">${suggestion}</div>
                    </div>
                `;
            } else {
                // New structured format
                const priorityClass = suggestion.priority || 'medium';
                const icon = suggestion.icon || '💡';
                
                suggestionItem.innerHTML = `
                    <div class="suggestion-icon">
                        <span class="suggestion-emoji">${icon}</span>
                    </div>
                    <div class="suggestion-content">
                        <div class="suggestion-title">${suggestion.title}</div>
                        <div class="suggestion-message">${suggestion.message}</div>
                    </div>
                    <div class="suggestion-priority priority-${priorityClass}">
                        ${getPriorityLabel(priorityClass)}
                    </div>
                `;
            }
            
            suggestionsList.appendChild(suggestionItem);
        });
    } else {
        suggestionsList.innerHTML = `
            <div class="suggestion-item suggestion-success">
                <div class="suggestion-icon">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="suggestion-content">
                    <div class="suggestion-title">No Specific Suggestions</div>
                    <div class="suggestion-message">Keep up the healthy eating!</div>
                </div>
            </div>
        `;
    }
}

// Get priority label
function getPriorityLabel(priority) {
    const labels = {
        'high': 'High Priority',
        'medium': 'Medium Priority',
        'low': 'Low Priority',
        'success': 'Great Job!'
    };
    return labels[priority] || 'Medium Priority';
}

// Show/hide loading overlay
function showLoading(show) {
    if (loadingOverlay) {
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }
}

// Show notification
function showNotification(message, type = 'info') {
    console.log(`📢 Notification [${type}]:`, message);
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Get notification icon
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Get notification color
function getNotificationColor(type) {
    const colors = {
        success: '#27ae60',
        error: '#e74c3c',
        warning: '#f39c12',
        info: '#3498db'
    };
    return colors[type] || '#3498db';
}

// Scroll to upload section
function scrollToUpload() {
    const uploadSection = document.getElementById('upload');
    if (uploadSection) {
        uploadSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Scroll to features section
function scrollToFeatures() {
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
        featuresSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Scroll to results section
function scrollToResults() {
    const resultsSection = document.getElementById('results');
    if (resultsSection) {
        resultsSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .drag-over {
        border-color: #ff6b6b !important;
        background: rgba(255, 107, 107, 0.1) !important;
        transform: scale(1.02);
    }
    
    .notification button {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
    
    .notification button:hover {
        opacity: 0.8;
    }
    
    .nutrition-icon {
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
    }
    
    .suggestion-item {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border-left: 5px solid;
        position: relative;
        overflow: hidden;
    }
    
    .suggestion-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .suggestion-high {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        border-left-color: #c0392b;
    }
    
    .suggestion-medium {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        border-left-color: #d68910;
    }
    
    .suggestion-low {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border-left-color: #21618c;
    }
    
    .suggestion-success {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        border-left-color: #1e8449;
    }
    
    .suggestion-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .suggestion-emoji {
        font-size: 2.5rem;
        display: block;
    }
    
    .suggestion-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    
    .suggestion-message {
        font-size: 1rem;
        line-height: 1.6;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .suggestion-priority {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }
    
    .priority-high {
        background: rgba(231, 76, 60, 0.9);
    }
    
    .priority-medium {
        background: rgba(243, 156, 18, 0.9);
    }
    
    .priority-low {
        background: rgba(52, 152, 219, 0.9);
    }
    
    .priority-success {
        background: rgba(39, 174, 96, 0.9);
    }
`;
document.head.appendChild(style);

// Add drag and drop visual feedback
if (uploadArea) {
    uploadArea.addEventListener('dragenter', () => {
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        if (!uploadArea.contains(e.relatedTarget)) {
            uploadArea.classList.remove('drag-over');
        }
    });
}

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Escape key to close loading overlay
    if (e.key === 'Escape' && loadingOverlay && loadingOverlay.style.display === 'flex') {
        showLoading(false);
    }
    
    // Enter key in food input
    if (e.key === 'Enter' && document.activeElement === foodInput) {
        addFood();
    }
});

// Add touch support for mobile devices
if ('ontouchstart' in window) {
    if (uploadArea) {
        uploadArea.addEventListener('touchstart', () => {
            uploadArea.classList.add('touch-active');
        });
        
        uploadArea.addEventListener('touchend', () => {
            uploadArea.classList.remove('touch-active');
        });
    }
}

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll performance
const optimizedScrollHandler = debounce(() => {
    // Navigation highlighting logic here
}, 100);

window.addEventListener('scroll', optimizedScrollHandler);

// Add accessibility improvements
document.addEventListener('DOMContentLoaded', () => {
    // Add ARIA labels
    if (uploadArea) {
        uploadArea.setAttribute('aria-label', 'Image upload area. Click or drag and drop an image here.');
    }
    if (foodInput) {
        foodInput.setAttribute('aria-label', 'Enter food name');
    }
    
    // Add focus indicators
    const focusableElements = document.querySelectorAll('button, input, a');
    focusableElements.forEach(element => {
        element.addEventListener('focus', () => {
            element.style.outline = '2px solid #ff6b6b';
            element.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', () => {
            element.style.outline = '';
            element.style.outlineOffset = '';
        });
    });
});

// Add error boundary for better user experience
window.addEventListener('error', (e) => {
    console.error('Application error:', e.error);
    showNotification('An unexpected error occurred. Please try again.', 'error');
});

// Add unhandled promise rejection handler
window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    showNotification('An error occurred while processing your request. Please try again.', 'error');
    e.preventDefault();
});

// Debug: Log when script is fully loaded
console.log('🎉 NutriVision AI JavaScript loaded successfully');

// Global function for onclick handlers (fallback)
window.analyzeFoods = analyzeFoods;
window.addFood = addFood;
window.removeFood = removeFood;
window.resetUpload = resetUpload;
window.analyzeImage = analyzeImage;

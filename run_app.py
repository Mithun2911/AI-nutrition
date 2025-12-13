#!/usr/bin/env python3
"""
Startup script for the AI-based Nutrition Detection System Web Interface
"""

import os
import sys

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import flask
        print("✓ Flask is available")
        
        # Check for optional dependencies
        try:
            import torch
            print("✓ PyTorch is available (optional)")
        except ImportError:
            print("⚠ PyTorch not available (optional - using mock data)")
        
        try:
            import numpy
            print("✓ NumPy is available (optional)")
        except ImportError:
            print("⚠ NumPy not available (optional - using mock data)")
        
        return True
    except ImportError as e:
        print(f"✗ Missing required dependency: {e}")
        print("Please install Flask using: pip install Flask")
        return False

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'static/uploads',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")

def main():
    """Main startup function"""
    print("="*60)
    print("AI-BASED NUTRITION DETECTION SYSTEM")
    print("Web Interface Startup")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Import app after checking dependencies
    try:
        from app import app
        print("✓ App imported successfully")
    except ImportError as e:
        print(f"✗ Error importing app: {e}")
        print("Please check that app.py exists and all required dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading app: {e}")
        print("Please check app.py for any syntax errors")
        sys.exit(1)
    
    print("\n🚀 Starting web application...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("="*60)
    
    try:
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

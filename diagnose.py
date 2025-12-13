#!/usr/bin/env python3
"""
Diagnostic script to check if the NutriVision AI app can run
"""

import sys
import os

print("NutriVision AI - Diagnostic Check")
print("=" * 60)

# Check Python version
print(f"\nPython Version: {sys.version}")

# Check current directory
print(f"Current Directory: {os.getcwd()}")

# Check if app.py exists
if os.path.exists('app.py'):
    print("[OK] app.py exists")
else:
    print("[ERROR] app.py NOT FOUND!")
    sys.exit(1)

# Check if Flask is installed
print("\nChecking Dependencies:")
try:
    import flask
    print(f"[OK] Flask {flask.__version__} is installed")
except ImportError:
    print("[ERROR] Flask is NOT installed")
    print("   Install with: pip install Flask")
    sys.exit(1)

# Try to import app
print("\nTesting App Import:")
try:
    from app import app
    print("[OK] App imported successfully!")
    print(f"[OK] Flask app object: {type(app)}")
except ImportError as e:
    print(f"[ERROR] Import Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check if app has required routes
print("\nChecking App Routes:")
try:
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(rule.rule)
    print(f"[OK] Found {len(routes)} routes:")
    for route in routes[:5]:  # Show first 5
        print(f"   - {route}")
    if len(routes) > 5:
        print(f"   ... and {len(routes) - 5} more")
except Exception as e:
    print(f"[WARNING] Could not check routes: {e}")

# Check static files
print("\nChecking Static Files:")
static_files = {
    'static/js/app.js': 'JavaScript',
    'static/css/style.css': 'CSS',
    'templates/index.html': 'HTML Template'
}

for file, file_type in static_files.items():
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"[OK] {file_type}: {file} ({size} bytes)")
    else:
        print(f"[ERROR] {file_type}: {file} NOT FOUND")

print("\n" + "=" * 60)
print("Diagnostic Complete!")
print("\nTo start the server:")
print("   python run_app.py")
print("\nOr directly:")
print("   python app.py")
print("\nThen open: http://localhost:5000")


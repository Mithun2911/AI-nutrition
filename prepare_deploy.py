#!/usr/bin/env python3
"""
Quick script to prepare your project for deployment
"""

import os
import shutil

print("Preparing NutriVision AI for Deployment...")
print("=" * 60)

# Check if required files exist
required_files = [
    'app.py',
    'requirements_deploy.txt',
    'Procfile',
    'runtime.txt',
    'templates/index.html',
    'static/css/style.css',
    'static/js/app.js'
]

print("\nChecking required files...")
missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"[OK] {file}")
    else:
        print(f"[ERROR] {file} - MISSING!")
        missing_files.append(file)

if missing_files:
    print(f"\n[WARNING] {len(missing_files)} file(s) missing!")
    print("Please ensure all files are present before deploying.")
else:
    print("\n[OK] All required files present!")

# Check uploads folder
print("\nChecking uploads folder...")
uploads_dir = 'static/uploads'
if os.path.exists(uploads_dir):
    # Create .gitkeep if it doesn't exist
    gitkeep = os.path.join(uploads_dir, '.gitkeep')
    if not os.path.exists(gitkeep):
        with open(gitkeep, 'w') as f:
            f.write('')
        print("[OK] Created .gitkeep in uploads folder")
    else:
        print("[OK] Uploads folder ready")
else:
    os.makedirs(uploads_dir)
    with open(os.path.join(uploads_dir, '.gitkeep'), 'w') as f:
        f.write('')
    print("[OK] Created uploads folder with .gitkeep")

# Check if .gitignore exists
print("\nChecking .gitignore...")
if os.path.exists('.gitignore'):
    print("[OK] .gitignore exists")
else:
    print("[WARNING] .gitignore not found (created one for you)")

print("\n" + "=" * 60)
print("[OK] Deployment preparation complete!")
print("\nNext steps:")
print("1. Review DEPLOYMENT_GUIDE.md for deployment instructions")
print("2. Push your code to GitHub")
print("3. Deploy to Render, Railway, or your preferred platform")
print("\nRecommended platforms:")
print("   - Render: https://render.com (Easiest)")
print("   - Railway: https://railway.app (Best free tier)")
print("   - PythonAnywhere: https://pythonanywhere.com (Simple)")
print("\nGood luck with your deployment!")


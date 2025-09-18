#!/usr/bin/env python3
"""
Setup script for AI Shopping Assistant
This script helps install dependencies and set up the environment
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with error: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 7):
        print(f"❌ Python 3.7 or higher is required. Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    return run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def check_webscraper():
    """Check if webscraper.py exists and is importable"""
    print("🔍 Checking webscraper.py...")
    if not os.path.exists('webscraper.py'):
        print("❌ webscraper.py not found in current directory")
        print("💡 Please make sure your webscraper.py file is in the same directory")
        return False
    
    try:
        # Try to import the functions
        sys.path.append('.')
        from webscraper import scrape_amazon_in, premiummax, budgetbalance, persona_debate
        print("✅ webscraper.py functions imported successfully")
        return True
    except ImportError as e:
        print(f"⚠️ Could not import webscraper functions: {e}")
        print("💡 The frontend will use mock data instead of real Amazon scraping")
        return False

def main():
    """Main setup function"""
    print("🤖 AI Shopping Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check webscraper
    webscraper_available = check_webscraper()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Run the backend server: python app.py")
    print("2. Open your browser and go to: http://localhost:5000")
    print("3. Start searching for products on Amazon India!")
    
    if not webscraper_available:
        print("\n⚠️  Note: webscraper.py not fully functional")
        print("   The app will use mock data for demonstration")
        print("   Make sure your webscraper.py has the correct functions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



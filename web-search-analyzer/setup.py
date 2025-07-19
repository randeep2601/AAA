#!/usr/bin/env python3
"""
Web Search Analyzer Setup Script
This script helps with the initial setup and configuration of the application.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.8 or higher")
        return False

def install_dependencies():
    """Install Python dependencies."""
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def setup_nltk_data():
    """Download required NLTK data."""
    nltk_downloads = [
        "punkt",
        "stopwords", 
        "averaged_perceptron_tagger",
        "vader_lexicon"
    ]
    
    for data in nltk_downloads:
        success = run_command(
            f"{sys.executable} -c \"import nltk; nltk.download('{data}', quiet=True)\"",
            f"Downloading NLTK {data} data"
        )
        if not success:
            return False
    return True

def check_chrome():
    """Check if Chrome is installed."""
    system = platform.system()
    if system == "Windows":
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    elif system == "Darwin":  # macOS
        chrome_paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    else:  # Linux
        chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✅ Chrome browser found")
            return True
    
    print("⚠️  Chrome browser not found. Please install Google Chrome for web scraping functionality.")
    return False

def create_directories():
    """Create necessary directories."""
    directories = [
        "logs",
        "cache",
        "downloads"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def test_installation():
    """Test if the installation works."""
    print("\n🧪 Testing installation...")
    
    # Test imports
    test_imports = [
        "flask",
        "requests",
        "beautifulsoup4",
        "selenium",
        "nltk",
        "transformers",
        "matplotlib",
        "plotly",
        "wordcloud",
        "textstat",
        "langdetect",
        "newspaper3k"
    ]
    
    failed_imports = []
    for module in test_imports:
        try:
            __import__(module.replace("-", "_"))
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Try running: pip install -r requirements.txt")
        return False
    
    print("\n✅ All imports successful!")
    return True

def main():
    """Main setup function."""
    print("🚀 Web Search Analyzer Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Chrome
    check_chrome()
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Setup NLTK data
    if not setup_nltk_data():
        print("\n❌ Failed to download NLTK data. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed. Please check the error messages above.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the application:")
    print("1. cd backend")
    print("2. python app.py")
    print("3. Open http://localhost:5000 in your browser")
    
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
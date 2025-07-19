#!/usr/bin/env python3
"""
Web Search Analyzer - Quick Start Script
Simple script to launch the application with proper configuration.
"""

import os
import sys
import subprocess
import signal
import webbrowser
import time

def check_dependencies():
    """Check if required dependencies are installed."""
    required_modules = ['flask', 'requests', 'beautifulsoup4', 'selenium']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Run 'python setup.py' to install dependencies")
        return False
    
    return True

def start_server():
    """Start the Flask server."""
    print("🚀 Starting Web Search Analyzer...")
    print("Press Ctrl+C to stop the server")
    
    # Change to backend directory
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    
    try:
        # Start the Flask application
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd=backend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Server started successfully!")
            print("🌐 Opening browser...")
            
            # Open browser
            try:
                webbrowser.open('http://localhost:5000')
            except:
                print("Could not open browser automatically.")
                print("Please open http://localhost:5000 manually")
            
            print("\n📖 Usage:")
            print("1. Enter a search query in the search bar")
            print("2. Select up to 10 results to analyze") 
            print("3. Click 'Extract Content' to process the selected links")
            print("4. Choose a summary type to generate analysis")
            print("\nPress Ctrl+C to stop the server")
            
            # Wait for the process
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped")
        else:
            # Server failed to start
            stdout, stderr = process.communicate()
            print("❌ Failed to start server")
            print(f"Error: {stderr}")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping server...")
        if 'process' in locals():
            process.terminate()
            process.wait()
        print("✅ Server stopped")
    
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function."""
    print("🔍 Web Search Analyzer - Quick Start")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('backend/app.py'):
        print("❌ Please run this script from the web-search-analyzer directory")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
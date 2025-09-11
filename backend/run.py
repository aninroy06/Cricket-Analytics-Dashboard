#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def start_app():
    """Start the Flask application"""
    try:
        print("🏏 Starting Cricket Analytics Dashboard...")
        print(f"📁 Directory: {os.getcwd()}")
        print("🚀 Server will be available at: http://127.0.0.1:8000")
        
        # Import and run the app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=8000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Installing dependencies and retrying...")
        install_requirements()
        from app import app
        app.run(debug=True, host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_app()

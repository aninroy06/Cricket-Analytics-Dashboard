#!/usr/bin/env python3
"""
Simple startup script for Cricket Analytics Dashboard
"""
import os
import sys

def start_server():
    """Start the Flask server with minimal configuration"""
    try:
        print("🏏 Cricket Analytics Dashboard")
        print("=" * 50)
        print("🚀 Starting server...")
        print("📍 URL: http://127.0.0.1:8000")
        print("=" * 50)
        
        # Import and run the Flask app
        from app import app
        
        # Simple run configuration without network IP detection
        app.run(
            debug=True,
            host='127.0.0.1',  # Only bind to localhost to avoid network issues
            port=8000,
            use_reloader=False  # Disable reloader to avoid duplicate startup
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the backend directory with app.py")
        sys.exit(1)
    except OSError as e:
        if "Address already in use" in str(e):
            print("❌ Port 8000 is already in use!")
            print("💡 Try killing the process or use a different port")
            print("   To kill: lsof -ti:8000 | xargs kill -9")
        else:
            print(f"❌ Network error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()

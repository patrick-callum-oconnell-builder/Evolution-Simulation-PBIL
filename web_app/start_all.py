#!/usr/bin/env python3
"""
Master startup script for PBIL Real-time Visualization

This script can:
1. Start both backend and frontend together
2. Start only backend or frontend
3. Automatically handle port conflicts
4. Test the API connection
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="PBIL Visualization Startup Script")
    parser.add_argument(
        "mode", 
        choices=["all", "backend", "frontend", "test"], 
        nargs="?", 
        default="all",
        help="What to start: 'all' (default), 'backend', 'frontend', or 'test'"
    )
    
    args = parser.parse_args()
    
    print("🧬 PBIL Real-time Visualization Startup")
    print("=" * 45)
    
    # Ensure we're in the project root
    script_dir = Path(__file__).parent.parent
    if (script_dir / "c_src").exists() and (script_dir / "evolution_simulation").exists():
        os.chdir(script_dir)
        print(f"✅ Working from project root: {script_dir}")
    else:
        print("❌ Could not find project root directory")
        sys.exit(1)
    
    if args.mode == "backend":
        print("\n🚀 Starting Backend Only...")
        subprocess.run([sys.executable, "web_app/start_backend.py"])
    
    elif args.mode == "frontend":
        print("\n⚛️  Starting Frontend Only...")
        subprocess.run([sys.executable, "web_app/start_frontend.py"])
    
    elif args.mode == "test":
        print("\n🧪 Testing Backend API...")
        subprocess.run([sys.executable, "web_app/test_backend.py"])
    
    elif args.mode == "all":
        print("\n🚀 Starting Full Application...")
        print("\n1. Starting Backend Server...")
        
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "web_app/start_backend.py"
        ])
        
        # Wait for backend to start
        print("⏱️  Waiting for backend to start...")
        time.sleep(5)
        
        # Test backend
        print("🧪 Testing backend connection...")
        test_result = subprocess.run([
            sys.executable, "web_app/test_backend.py"
        ], capture_output=True, text=True)
        
        if "All tests passed" in test_result.stdout:
            print("✅ Backend is running successfully!")
            print("\n2. Starting Frontend Server...")
            
            try:
                # Start frontend (this will block)
                subprocess.run([sys.executable, "web_app/start_frontend.py"])
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
            finally:
                # Clean up backend process
                print("🧹 Cleaning up backend process...")
                backend_process.terminate()
                try:
                    backend_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    backend_process.kill()
        else:
            print("❌ Backend failed to start properly")
            print(test_result.stdout)
            backend_process.terminate()
            sys.exit(1)
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main() 
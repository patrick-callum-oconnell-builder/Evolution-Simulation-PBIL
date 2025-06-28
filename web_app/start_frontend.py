#!/usr/bin/env python3
"""
Frontend startup script for PBIL Real-time Visualization

This script:
1. Kills any existing process using port 3000
2. Ensures npm dependencies are installed
3. Starts the React development server
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def kill_port_3000():
    """Kill any process using port 3000."""
    print("🔍 Checking for processes using port 3000...")
    
    try:
        # Find process using port 3000
        result = subprocess.run(
            ["lsof", "-ti:3000"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"💀 Killing process {pid} on port 3000...")
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        time.sleep(1)
                        # Force kill if still running
                        try:
                            os.kill(int(pid), signal.SIGKILL)
                        except ProcessLookupError:
                            pass  # Process already dead
                    except (ProcessLookupError, ValueError):
                        pass  # Process not found or invalid PID
            
            print("✅ Port 3000 cleared")
        else:
            print("✅ Port 3000 is free")
            
    except FileNotFoundError:
        # lsof not available, try alternative method
        print("⚠️  lsof not found, trying alternative method...")
        try:
            subprocess.run(["pkill", "-f", "react-scripts"], check=False)
            subprocess.run(["pkill", "-f", "npm start"], check=False)
            print("✅ Killed any running React processes")
        except FileNotFoundError:
            print("⚠️  Could not kill processes automatically")

def ensure_frontend_directory():
    """Ensure we're in the frontend directory."""
    current_dir = Path.cwd()
    frontend_dir = None
    
    # Check if we're already in frontend directory
    if (current_dir / "package.json").exists() and "pbil-visualization-frontend" in (current_dir / "package.json").read_text():
        frontend_dir = current_dir
    
    # Check if we're in web_app directory
    elif (current_dir / "frontend" / "package.json").exists():
        frontend_dir = current_dir / "frontend"
    
    # Check if we're in project root
    elif (current_dir / "web_app" / "frontend" / "package.json").exists():
        frontend_dir = current_dir / "web_app" / "frontend"
    
    if frontend_dir:
        os.chdir(frontend_dir)
        print(f"✅ Changed to frontend directory: {frontend_dir}")
        return frontend_dir
    
    print("❌ Could not find frontend directory")
    sys.exit(1)

def install_dependencies():
    """Install npm dependencies if needed."""
    if not (Path.cwd() / "node_modules").exists():
        print("📦 Installing npm dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)
    else:
        print("✅ Dependencies already installed")

def start_frontend():
    """Start the React development server."""
    print("⚛️  Starting React Development Server...")
    print("📍 Frontend will be available at: http://localhost:3000")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Set environment to automatically open browser
        env = os.environ.copy()
        env["BROWSER"] = "none"  # Don't auto-open browser
        
        subprocess.run(["npm", "start"], env=env, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server failed to start: {e}")
        sys.exit(1)

def main():
    """Main startup sequence."""
    print("⚛️  PBIL Frontend Startup Script")
    print("=" * 40)
    
    # Step 1: Kill any existing processes on port 3000
    kill_port_3000()
    
    # Step 2: Ensure we're in the frontend directory
    ensure_frontend_directory()
    
    # Step 3: Install dependencies if needed
    install_dependencies()
    
    # Step 4: Start the frontend
    start_frontend()

if __name__ == "__main__":
    main() 
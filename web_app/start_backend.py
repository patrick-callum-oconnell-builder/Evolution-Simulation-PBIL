#!/usr/bin/env python3
"""
Backend startup script for PBIL Real-time Visualization

This script:
1. Kills any existing process using port 8000
2. Ensures we're in the correct directory
3. Starts the FastAPI backend server
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def kill_port_8000():
    """Kill any process using port 8000."""
    print("🔍 Checking for processes using port 8000...")
    
    try:
        # Find process using port 8000
        result = subprocess.run(
            ["lsof", "-ti:8000"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"💀 Killing process {pid} on port 8000...")
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
            
            print("✅ Port 8000 cleared")
        else:
            print("✅ Port 8000 is free")
            
    except FileNotFoundError:
        # lsof not available, try alternative method
        print("⚠️  lsof not found, trying alternative method...")
        try:
            subprocess.run(["pkill", "-f", "main.py"], check=False)
            subprocess.run(["pkill", "-f", "uvicorn"], check=False)
            print("✅ Killed any running backend processes")
        except FileNotFoundError:
            print("⚠️  Could not kill processes automatically")

def ensure_project_root():
    """Ensure we're running from the project root directory."""
    current_dir = Path.cwd()
    
    # Check if we're in the project root (should have c_src and evolution_simulation)
    if (current_dir / "c_src").exists() and (current_dir / "evolution_simulation").exists():
        print(f"✅ Running from project root: {current_dir}")
        return current_dir
    
    # Try to find project root
    script_dir = Path(__file__).parent.parent  # web_app/.. = project root
    if (script_dir / "c_src").exists() and (script_dir / "evolution_simulation").exists():
        os.chdir(script_dir)
        print(f"✅ Changed to project root: {script_dir}")
        return script_dir
    
    print("❌ Could not find project root directory")
    sys.exit(1)

def start_backend():
    """Start the FastAPI backend server."""
    backend_script = Path("web_app/backend/main.py")
    
    if not backend_script.exists():
        print(f"❌ Backend script not found: {backend_script}")
        sys.exit(1)
    
    print("🚀 Starting PBIL Backend Server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws/pbil")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Use python -m uvicorn to ensure consistent environment
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "web_app.backend.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--log-level", "info"
        ], env=env, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

def main():
    """Main startup sequence."""
    print("🧬 PBIL Backend Startup Script")
    print("=" * 40)
    
    # Step 1: Kill any existing processes on port 8000
    kill_port_8000()
    
    # Step 2: Ensure we're in the right directory
    ensure_project_root()
    
    # Step 3: Start the backend
    start_backend()

if __name__ == "__main__":
    main() 
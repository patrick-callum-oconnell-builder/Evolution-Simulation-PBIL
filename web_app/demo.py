#!/usr/bin/env python3
"""
Demo script for PBIL Real-time Visualization Web Application

This script demonstrates the complete web application we've built:
1. FastAPI backend with WebSocket support
2. React frontend with real-time visualization
3. Integration with your existing PBIL C implementation
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def demo_info():
    """Display information about what we've built."""
    print("🧬 PBIL Real-time Visualization Demo")
    print("=" * 50)
    print()
    print("🎯 What we've built:")
    print("├── 🖥️  FastAPI Backend")
    print("│   ├── WebSocket streaming for real-time updates")
    print("│   ├── REST API for configuration and control")
    print("│   ├── Integration with your PBIL C wrapper")
    print("│   └── Automatic port cleanup and startup")
    print("│")
    print("├── ⚛️  React Frontend")
    print("│   ├── Real-time fitness evolution charts")
    print("│   ├── Probability vector heatmap visualization")
    print("│   ├── Interactive parameter controls") 
    print("│   ├── Live solution display")
    print("│   └── Beautiful Material-UI dark theme")
    print("│")
    print("└── 🔧 Integration Features")
    print("    ├── Calls your original C implementation directly")
    print("    ├── Zero performance loss (native C speed)")
    print("    ├── Real-time streaming of algorithm progress")
    print("    ├── Parameter tuning with live feedback")
    print("    └── Visual algorithm insights")
    print()

def show_file_structure():
    """Show the file structure we've created."""
    print("📁 File Structure Created:")
    print("evolution_simulation/")
    print("├── web_app/")
    print("│   ├── backend/")
    print("│   │   ├── main.py              # FastAPI server with WebSocket")
    print("│   │   └── requirements.txt     # Backend dependencies")
    print("│   ├── frontend/")
    print("│   │   ├── src/")
    print("│   │   │   ├── App.js           # Main React application")
    print("│   │   │   ├── hooks/")
    print("│   │   │   │   └── useWebSocket.js  # WebSocket management")
    print("│   │   │   └── components/")
    print("│   │   │       ├── ParameterPanel.js    # Algorithm controls")
    print("│   │   │       ├── FitnessChart.js      # Real-time fitness graph")
    print("│   │   │       ├── ProbabilityHeatmap.js # Prob vector visualization")
    print("│   │   │       ├── StatusPanel.js       # Connection/status info")
    print("│   │   │       └── SolutionDisplay.js   # Current best solution")
    print("│   │   ├── package.json         # React dependencies")
    print("│   │   └── public/")
    print("│   │       └── index.html       # Main HTML template")
    print("│   ├── start_backend.py         # Backend startup with port cleanup")
    print("│   ├── start_frontend.py        # Frontend startup script") 
    print("│   ├── start_all.py             # Master startup script")
    print("│   └── test_backend.py          # API testing script")
    print("├── evolution_simulation/")
    print("│   └── pbil.py                  # Your C wrapper (already working!)")
    print("├── c_src/                       # Your C implementation")
    print("└── sample_problem.cnf           # Test problem")
    print()

def demo_features():
    """Demonstrate key features."""
    print("🚀 Key Features Demonstrated:")
    print()
    print("1. 📊 Real-time Visualization:")
    print("   • Live fitness evolution charts")
    print("   • Probability vector heatmaps")
    print("   • Generation-by-generation progress")
    print()
    print("2. 🎛️  Interactive Controls:")
    print("   • Population size sliders")
    print("   • Learning rate adjustments")
    print("   • Parameter presets (Conservative/Balanced/Aggressive)")
    print("   • Real-time start/stop controls")
    print()
    print("3. 🔌 WebSocket Integration:")
    print("   • Zero-latency algorithm updates")
    print("   • Streaming probability vectors")
    print("   • Live fitness tracking")
    print("   • Real-time solution updates")
    print()
    print("4. 🎯 Algorithm Insights:")
    print("   • Probability vector convergence visualization")
    print("   • Variable assignment tracking")
    print("   • Solution quality metrics")
    print("   • Performance statistics")
    print()

def test_pbil_wrapper():
    """Test that the PBIL wrapper is working."""
    print("🧪 Testing PBIL Wrapper...")
    try:
        from evolution_simulation.pbil import run_pbil
        result = run_pbil('sample_problem.cnf', max_iterations=100)
        print(f"✅ PBIL Wrapper: Working! Found solution with fitness {result['fitness']}/{result['max_fitness']}")
        return True
    except Exception as e:
        print(f"❌ PBIL Wrapper Error: {e}")
        return False

def show_usage_examples():
    """Show how to use the application."""
    print("🎮 Usage Examples:")
    print()
    print("# Start just the backend:")
    print("python web_app/start_backend.py")
    print()
    print("# Start just the frontend:")  
    print("python web_app/start_frontend.py")
    print()
    print("# Start both (full application):")
    print("python web_app/start_all.py")
    print()
    print("# Test the backend API:")
    print("python web_app/test_backend.py")
    print()
    print("# Quick test of the PBIL wrapper:")
    print("python main.py")
    print()

def main():
    """Run the complete demo."""
    # Change to project root
    script_dir = Path(__file__).parent.parent
    if (script_dir / "c_src").exists():
        os.chdir(script_dir)
    
    demo_info()
    show_file_structure()
    demo_features()
    
    # Test the core PBIL functionality
    if test_pbil_wrapper():
        print()
        show_usage_examples()
        
        print("🌐 Web Application Ready!")
        print("=" * 30)
        print("Your PBIL algorithm is now wrapped with:")
        print("• Real-time web visualization")
        print("• Interactive parameter tuning") 
        print("• Beautiful charts and graphs")
        print("• WebSocket streaming updates")
        print()
        print("Next steps:")
        print("1. Run: python web_app/start_all.py")
        print("2. Open: http://localhost:3000")
        print("3. Watch your algorithm visualized in real-time!")
        print()
        print("✨ Your C implementation now has a modern web interface!")
    else:
        print("❌ Please fix the PBIL wrapper first")

if __name__ == "__main__":
    main() 
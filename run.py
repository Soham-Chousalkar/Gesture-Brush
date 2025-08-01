#!/usr/bin/env python3
"""
Gesture Brush - Runner Script
This script launches the main application from the project root.
"""

import os
import sys
import subprocess

def main():
    """Main function to run the gesture brush application"""
    print("🎨 Gesture Brush - Virtual Painter")
    print("=" * 40)
    
    # Check if we're in the right directory
    project_dir = "GestureBrush/Project"
    if not os.path.exists(project_dir):
        print("❌ Error: Project directory not found!")
        print("Please run this script from the project root directory.")
        return 1
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Check if gesture_brush.py exists
    if not os.path.exists("gesture_brush.py"):
        print("❌ Error: gesture_brush.py not found!")
        print("Please ensure all files are properly installed.")
        return 1
    
    print("🚀 Starting Gesture Brush...")
    print("📋 Controls:")
    print("   - Show your hand to the camera")
    print("   - Point with index finger to draw")
    print("   - Point to top area to select tools")
    print("   - Point to left area to select colors")
    print("   - Press ESC to exit")
    print("=" * 40)
    
    try:
        # Run the main application
        subprocess.run([sys.executable, "gesture_brush.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        return 1
    except FileNotFoundError:
        print("❌ Error: Python executable not found!")
        print("Please ensure Python is properly installed and in your PATH.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
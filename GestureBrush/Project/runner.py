#!/usr/bin/env python3
"""
Gesture Brush Launcher
Choose which version to run
"""

import os
import sys

def print_banner():
    print("🎨" + "="*50 + "🎨")
    print("           GESTURE BRUSH LAUNCHER")
    print("🎨" + "="*50 + "🎨")
    print()

def print_menu():
    print("Choose which version to run:")
    print("1. Demo Version (Mouse Control)")
    print("2. Alternative Version (Basic Hand Detection)")
    print("3. Full Version (MediaPipe - requires Python 3.11/3.12)")
    print("4. Test Imports")
    print("5. Exit")
    print()

def run_demo():
    print("Starting Demo Version (Mouse Control)...")
    print("Controls: Click and drag to draw, click on tools/colors to select")
    print("Press ESC to exit")
    print("-" * 50)
    os.system("python demo_painter.py")

def run_alternative():
    print("Starting Alternative Version (Basic Hand Detection)...")
    print("Controls: Show hand to camera, move hand to draw")
    print("Press ESC to exit")
    print("-" * 50)
    os.system("python alternative_painter.py")

def run_full():
    print("Starting Full Version (MediaPipe)...")
    print("Note: This requires MediaPipe which is not available for Python 3.13")
    print("If you have Python 3.11 or 3.12, install MediaPipe first:")
    print("pip install mediapipe")
    print("-" * 50)
    try:
        import mediapipe
        os.system("python virtual_painter.py")
    except ImportError:
        print("❌ MediaPipe not available. Please install it or use option 1 or 2.")

def test_imports():
    print("Testing imports...")
    print("-" * 50)
    os.system("python test_imports.py")

def main():
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                run_demo()
            elif choice == "2":
                run_alternative()
            elif choice == "3":
                run_full()
            elif choice == "4":
                test_imports()
            elif choice == "5":
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 
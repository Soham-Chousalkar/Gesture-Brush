#!/usr/bin/env python3
"""
Gesture Brush - Installation Script
This script helps set up the project environment.
"""

import os
import sys
import subprocess
import venv

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Error: Python 3.11+ is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = ".venv"
    if os.path.exists(venv_path):
        print("✅ Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the correct pip command
    if os.name == 'nt':  # Windows
        pip_cmd = os.path.join(".venv", "Scripts", "pip")
    else:  # Unix/Linux/Mac
        pip_cmd = os.path.join(".venv", "bin", "pip")
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def main():
    """Main installation function"""
    print("🎨 Gesture Brush - Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create virtual environment
    if not create_virtual_environment():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   .venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source .venv/bin/activate")
    print("2. Run the application:")
    print("   python run.py")
    print("\n🚀 Happy drawing!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
#!/usr/bin/env python3
"""
GitHub Setup Script for Gesture Brush
This script helps initialize and push the project to GitHub.
"""

import os
import subprocess
import sys

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed or not in PATH")
        return False

def initialize_git_repo():
    """Initialize git repository"""
    if os.path.exists(".git"):
        print("✅ Git repository already exists")
        return True
    
    print("🔧 Initializing git repository...")
    try:
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing git: {e}")
        return False

def add_files_to_git():
    """Add all files to git"""
    print("📁 Adding files to git...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Files added to git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error adding files: {e}")
        return False

def make_initial_commit():
    """Make initial commit"""
    print("💾 Making initial commit...")
    try:
        subprocess.run(["git", "commit", "-m", "Initial commit: Gesture Brush project"], check=True)
        print("✅ Initial commit created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error making commit: {e}")
        return False

def setup_remote_repo():
    """Guide user to set up remote repository"""
    print("\n🌐 GitHub Repository Setup")
    print("=" * 40)
    print("To push to GitHub, follow these steps:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'gesture-brush'")
    print("3. Don't initialize with README (we already have one)")
    print("4. Copy the repository URL")
    print("5. Run the following commands:")
    print()
    print("git remote add origin https://github.com/YOUR_USERNAME/gesture-brush.git")
    print("git branch -M main")
    print("git push -u origin main")
    print()

def main():
    """Main function"""
    print("🎨 Gesture Brush - GitHub Setup")
    print("=" * 40)
    
    # Check if git is installed
    if not check_git_installed():
        print("Please install Git first: https://git-scm.com/")
        return 1
    
    # Initialize git repository
    if not initialize_git_repo():
        return 1
    
    # Add files to git
    if not add_files_to_git():
        return 1
    
    # Make initial commit
    if not make_initial_commit():
        return 1
    
    # Guide user to set up remote
    setup_remote_repo()
    
    print("✅ Local git repository is ready!")
    print("Follow the steps above to push to GitHub.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
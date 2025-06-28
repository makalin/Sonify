#!/usr/bin/env python3
"""
Sonify Quickstart Script
Helps users set up the Sonify project quickly
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print the Sonify banner"""
    print("🎶" * 20)
    print("🎶 Sonify - Spotify Data Visualizer 🎶")
    print("🎶" * 20)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ Error: pip is not available")
        sys.exit(1)

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to create virtual environment")
        sys.exit(1)

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Set up environment file"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ Environment file already exists")
        return
    
    if env_example.exists():
        print("📝 Creating environment file...")
        shutil.copy(env_example, env_file)
        print("✅ Environment file created from template")
        print("⚠️  Please edit .env with your Spotify API credentials")
    else:
        print("❌ Error: env.example not found")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = ["static/exports", "flask_session"]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*50)
    print("🎉 Setup Complete!")
    print("="*50)
    print()
    print("Next steps:")
    print("1. 📝 Edit .env file with your Spotify API credentials:")
    print("   - Get credentials from: https://developer.spotify.com/dashboard")
    print("   - Add http://localhost:5000/callback to Redirect URIs")
    print()
    print("2. 🚀 Activate virtual environment and run the app:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("   python run.py")
    print()
    print("3. 🌐 Open your browser and go to: http://localhost:5000")
    print()
    print("📚 For more information, see README.md")
    print("🐛 For help, see CONTRIBUTING.md")
    print()
    print("Happy visualizing! 🎶")

def main():
    """Main function"""
    print_banner()
    
    print("🔍 Checking prerequisites...")
    check_python_version()
    check_pip()
    print()
    
    print("🚀 Setting up Sonify...")
    create_virtual_environment()
    install_dependencies()
    setup_environment()
    create_directories()
    print()
    
    print_next_steps()

if __name__ == "__main__":
    main() 
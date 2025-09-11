#!/usr/bin/env python3
"""
Build script to create executable for Noteted using PyInstaller.
"""

import os
import subprocess
import sys

def build_executable():
    """Build the Noteted as an executable"""
    print("Building Noteted executable...")
    
    # PyInstaller command with options
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single executable file
        '--windowed',                   # Hide console window (GUI app)
        '--name=Noteted',               # Name of the executable
        '--icon="assets/NTD.ico"',        # Use icon file if it exists
        'main.py'                       # Main script to build
    ]
    
    # Check if icon files exist and adjust command accordingly
    if not os.path.exists('icon.ico'):
        print("Warning: icon.ico not found, executable will use default icon")
        cmd = [arg for arg in cmd if not arg.startswith('--icon=')]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created: dist/Noteted.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Please install it first:")
        print("pip install pyinstaller")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()

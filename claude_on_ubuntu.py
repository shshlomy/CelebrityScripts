#!/usr/bin/env python3
"""
Script to install Claude CLI on Ubuntu 22.04 with Python
"""

import subprocess
import sys
import os
import urllib.request
import shutil
import tempfile

def run_command(command, check=True, shell=False):
    """Run a shell command and return the result"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command) if isinstance(command, list) else command}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_root():
    """Check if running as root or with sudo privileges"""
    if os.geteuid() != 0:
        print("This script requires root privileges. Please run with sudo:")
        print(f"sudo python3 {sys.argv[0]}")
        sys.exit(1)

def update_system():
    """Update the package manager and install basic dependencies"""
    print("Updating system packages...")
    run_command(["apt", "update"])
    run_command(["apt", "install", "-y", "curl", "wget", "gnupg", "lsb-release", "ca-certificates"])

def install_python():
    """Install Python 3 and pip if not already installed"""
    print("Installing Python 3 and pip...")
    run_command(["apt", "install", "-y", "python3", "python3-pip", "python3-venv"])

def install_node():
    """Install Node.js (required for Claude CLI)"""
    print("Installing Node.js...")
    
    # Add NodeSource repository
    run_command("curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -", shell=True)
    run_command(["apt", "install", "-y", "nodejs"])
    
    # Verify installation
    result = run_command(["node", "--version"], check=False)
    if result.returncode == 0:
        print(f"Node.js installed successfully: {result.stdout.strip()}")
    else:
        print("Failed to install Node.js")
        sys.exit(1)

def install_claude():
    """Install Claude CLI"""
    print("Installing Claude CLI...")
    
    # Install Claude CLI globally using npm
    run_command(["npm", "install", "-g", "@anthropic/claude"])
    
    # Verify installation
    result = run_command(["claude", "--version"], check=False)
    if result.returncode == 0:
        print(f"Claude CLI installed successfully: {result.stdout.strip()}")
    else:
        print("Failed to install Claude CLI")
        sys.exit(1)

def setup_claude():
    """Provide setup instructions for Claude"""
    print("\n" + "="*50)
    print("Claude CLI Installation Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Run 'claude auth' to authenticate with your Anthropic account")
    print("2. Get your API key from: https://console.anthropic.com/")
    print("3. Run 'claude --help' to see available commands")
    print("\nUsage examples:")
    print("  claude chat                 # Start an interactive chat")
    print("  claude complete 'prompt'    # Get a completion")
    print("  claude --help              # Show help")

def main():
    """Main installation function"""
    print("Starting Claude CLI installation on Ubuntu 22.04...")
    
    # Check if running as root
    check_root()
    
    try:
        # Update system
        update_system()
        
        # Install Python
        install_python()
        
        # Install Node.js
        install_node()
        
        # Install Claude CLI
        install_claude()
        
        # Show setup instructions
        setup_claude()
        
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
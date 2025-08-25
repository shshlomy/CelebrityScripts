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
            raise
        return e
    return result

def check_command_exists(command):
    """Check if a command exists in PATH"""
    return shutil.which(command) is not None

def install_python_and_pip():
    """Install Python 3 and pip if not already installed"""
    print("Installing Python 3 and pip...")
    
    # Check if Python 3 is already installed
    if check_command_exists("python3"):
        print("Python 3 is already installed")
    else:
        print("Installing Python 3...")
        run_command(["apt", "update"], shell=True)
        run_command(["apt", "install", "-y", "python3", "python3-pip"], shell=True)
    
    # Check if pip is installed
    if check_command_exists("pip3"):
        print("pip3 is already installed")
    else:
        print("Installing pip3...")
        run_command(["apt", "install", "-y", "python3-pip"], shell=True)
    
    # Upgrade pip to latest version
    print("Upgrading pip...")
    run_command(["python3", "-m", "pip", "install", "--upgrade", "pip"], shell=True)

def install_claude():
    """Install Claude CLI using the current method"""
    print("Installing Claude CLI...")
    
    # Method 1: Try installing anthropic package (includes CLI)
    print("Trying to install anthropic package...")
    try:
        result = run_command(["python3", "-m", "pip", "install", "anthropic"], shell=True)
        if result.returncode == 0:
            print("✅ Successfully installed anthropic package")
            
            # Check if claude command is available
            if check_command_exists("claude"):
                print("✅ Claude CLI is now available as 'claude'")
                return True
            else:
                print("⚠️  anthropic package installed but 'claude' command not found")
                print("   This package provides Python API access to Claude")
        else:
            print("❌ Failed to install anthropic package")
    except Exception as e:
        print(f"❌ Error installing anthropic package: {e}")
    
    # Method 2: Try installing claude-cli package
    print("Trying to install claude-cli package...")
    try:
        result = run_command(["python3", "-m", "pip", "install", "claude-cli"], shell=True)
        if result.returncode == 0:
            print("✅ Successfully installed claude-cli package")
            
            # Check if claude command is available
            if check_command_exists("claude"):
                print("✅ Claude CLI is now available as 'claude'")
                return True
            else:
                print("⚠️  claude-cli package installed but 'claude' command not found")
        else:
            print("❌ Failed to install claude-cli package")
    except Exception as e:
        print(f"❌ Error installing claude-cli package: {e}")
    
    # Method 3: Try installing claude package
    print("Trying to install claude package...")
    try:
        result = run_command(["python3", "-m", "pip", "install", "claude"], shell=True)
        if result.returncode == 0:
            print("✅ Successfully installed claude package")
            
            # Check if claude command is available
            if check_command_exists("claude"):
                print("✅ Claude CLI is now available as 'claude'")
                return True
            else:
                print("⚠️  claude package installed but 'claude' command not found")
        else:
            print("❌ Failed to install claude package")
    except Exception as e:
        print(f"❌ Error installing claude package: {e}")
    
    # Method 4: Manual installation from GitHub releases
    print("Trying manual installation from GitHub...")
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            # Try to find the correct repository and binary
            print("Searching for Claude CLI releases...")
            
            # Try different possible repository names
            repos_to_try = [
                "anthropics/anthropic-cli",
                "anthropics/claude-cli", 
                "anthropics/claude",
                "claude-ai/claude-cli"
            ]
            
            for repo in repos_to_try:
                try:
                    print(f"Trying repository: {repo}")
                    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
                    response = urllib.request.urlopen(api_url)
                    data = response.read().decode('utf-8')
                    
                    # Look for Linux binary
                    if "linux" in data.lower() and "x86_64" in data.lower():
                        print(f"✅ Found working repository: {repo}")
                        
                        # Download the binary
                        download_url = f"https://github.com/{repo}/releases/latest/download/claude-linux-x86_64"
                        print(f"Downloading from: {download_url}")
                        
                        urllib.request.urlretrieve(download_url, "claude")
                        os.chmod("claude", 0o755)
                        
                        # Move to system PATH
                        shutil.move("claude", "/usr/local/bin/claude")
                        print("✅ Claude CLI installed successfully!")
                        return True
                        
                except Exception as e:
                    print(f"Repository {repo} failed: {e}")
                    continue
            
            print("❌ Could not find working repository")
            
    except Exception as e:
        print(f"❌ Manual installation failed: {e}")
    
    return False

def main():
    """Main installation function"""
    print("Starting Claude CLI installation on Ubuntu 22.04...")
    
    # Check if running as root
    if os.geteuid() != 0:
        print("❌ This script must be run as root (use sudo)")
        sys.exit(1)
    
    try:
        # Install Python and pip
        install_python_and_pip()
        
        # Install Claude CLI
        if install_claude():
            print("\n🎉 Claude CLI installation completed successfully!")
            print("\nNext steps:")
            print("1. Set your Anthropic API key:")
            print("   export ANTHROPIC_API_KEY='your-api-key-here'")
            print("2. Test the installation:")
            print("   claude --help")
            print("3. Start chatting:")
            print("   claude")
        else:
            print("\n❌ Claude CLI installation failed")
            print("\nManual installation options:")
            print("1. Use Python API directly:")
            print("   pip install anthropic")
            print("   python3 -c \"import anthropic; print('Anthropic package available')\"")
            print("2. Check for updates:")
            print("   pip install --upgrade anthropic")
            print("3. Visit Anthropic documentation:")
            print("   https://docs.anthropic.com/")
            
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
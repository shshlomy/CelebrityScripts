#!/usr/bin/env python3
"""
Script to install Gemini CLI on Ubuntu 22.04 with Python
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
    run_command(["apt", "install", "-y", "curl", "wget", "gnupg", "lsb-release", "ca-certificates", "software-properties-common"])

def install_python():
    """Install Python 3 and pip if not already installed"""
    print("Installing Python 3 and pip...")
    run_command(["apt", "install", "-y", "python3", "python3-pip", "python3-venv"])

def install_google_cloud_cli():
    """Install Google Cloud CLI (required for Gemini API access)"""
    print("Installing Google Cloud CLI...")
    
    # Add Google Cloud SDK repository
    run_command("curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg", shell=True)
    run_command("echo 'deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main' | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list", shell=True)
    
    # Update and install
    run_command(["apt", "update"])
    run_command(["apt", "install", "-y", "google-cloud-cli"])
    
    # Verify installation
    result = run_command(["gcloud", "--version"], check=False)
    if result.returncode == 0:
        print(f"Google Cloud CLI installed successfully")
    else:
        print("Failed to install Google Cloud CLI")
        sys.exit(1)

def install_gemini_python_sdk():
    """Install Google Generative AI Python SDK"""
    print("Installing Google Generative AI Python SDK...")
    run_command(["pip3", "install", "google-generativeai"])
    
    # Verify installation
    result = run_command(["python3", "-c", "import google.generativeai; print('Google Generative AI SDK installed successfully')"], check=False)
    if result.returncode != 0:
        print("Failed to install Google Generative AI SDK")
        sys.exit(1)

def create_gemini_cli():
    """Create a simple Gemini CLI wrapper script"""
    print("Creating Gemini CLI wrapper...")
    
    cli_script = """#!/usr/bin/env python3
\"\"\"
Simple Gemini CLI wrapper
\"\"\"

import argparse
import os
import sys
import google.generativeai as genai

def main():
    parser = argparse.ArgumentParser(description='Gemini CLI')
    parser.add_argument('--api-key', help='Gemini API key (or set GEMINI_API_KEY env var)')
    parser.add_argument('--model', default='gemini-pro', help='Model to use (default: gemini-pro)')
    parser.add_argument('prompt', nargs='*', help='Prompt text')
    parser.add_argument('--chat', action='store_true', help='Start interactive chat mode')
    parser.add_argument('--version', action='version', version='Gemini CLI 1.0')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: Please provide API key via --api-key or GEMINI_API_KEY environment variable")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(args.model)
    
    if args.chat:
        print("Starting Gemini chat (type 'quit' or 'exit' to stop)")
        print("=" * 50)
        chat = model.start_chat()
        while True:
            try:
                prompt = input("You: ")
                if prompt.lower() in ['quit', 'exit', 'q']:
                    break
                response = chat.send_message(prompt)
                print(f"Gemini: {response.text}")
                print()
            except KeyboardInterrupt:
                print("\\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    else:
        if not args.prompt:
            print("Error: Please provide a prompt or use --chat for interactive mode")
            sys.exit(1)
        
        prompt_text = ' '.join(args.prompt)
        try:
            response = model.generate_content(prompt_text)
            print(response.text)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
"""
    
    # Write the CLI script
    with open('/usr/local/bin/gemini', 'w') as f:
        f.write(cli_script)
    
    # Make it executable
    os.chmod('/usr/local/bin/gemini', 0o755)
    
    print("Gemini CLI wrapper created at /usr/local/bin/gemini")

def setup_gemini():
    """Provide setup instructions for Gemini"""
    print("\n" + "="*50)
    print("Gemini CLI Installation Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Set your API key as an environment variable:")
    print("   export GEMINI_API_KEY='your-api-key-here'")
    print("3. Add the above line to your ~/.bashrc or ~/.profile for persistence")
    print("\nUsage examples:")
    print("  gemini 'Hello, how are you?'           # Single prompt")
    print("  gemini --chat                          # Interactive chat mode")
    print("  gemini --model gemini-pro 'prompt'     # Specify model")
    print("  gemini --api-key YOUR_KEY 'prompt'     # Specify API key")
    print("  gemini --help                          # Show help")
    print("\nAvailable models:")
    print("  - gemini-pro (default)")
    print("  - gemini-pro-vision")

def main():
    """Main installation function"""
    print("Starting Gemini CLI installation on Ubuntu 22.04...")
    
    # Check if running as root
    check_root()
    
    try:
        # Update system
        update_system()
        
        # Install Python
        install_python()
        
        # Install Google Cloud CLI
        install_google_cloud_cli()
        
        # Install Gemini Python SDK
        install_gemini_python_sdk()
        
        # Create Gemini CLI wrapper
        create_gemini_cli()
        
        # Show setup instructions
        setup_gemini()
        
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
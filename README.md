# Scripts Collection

A collection of utility scripts for various system administration and setup tasks.

## Scripts

### claude_on_ubuntu.py

An automated installation script for Claude CLI on Ubuntu 22.04 systems.

**Features:**
- Installs Python 3 and pip
- Installs Node.js LTS
- Installs Claude CLI via npm
- Provides post-installation setup instructions

**Usage:**
```bash
sudo python3 claude_on_ubuntu.py
```

**Requirements:**
- Ubuntu 22.04 (or compatible)
- Root/sudo privileges
- Internet connection

**What it installs:**
- Python 3 and pip
- Node.js (LTS version)
- Claude CLI (@anthropic/claude)

**Post-installation:**
After running the script, you'll need to:
1. Run `claude auth` to authenticate
2. Get your API key from https://console.anthropic.com/
3. Use `claude --help` to explore available commands

## Installation

1. Clone or download the scripts
2. Make scripts executable: `chmod +x script_name.py`
3. Run with appropriate permissions

## Contributing

Feel free to add more utility scripts to this collection.
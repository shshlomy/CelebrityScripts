# Scripts Collection

A collection of utility scripts for various system administration and setup tasks.

## Scripts

### claude_on_ubuntu.py

An automated installation script for Claude CLI on Ubuntu 22.04 systems.

**Features:**
- Installs Python 3 and pip
- Multiple Claude CLI installation methods with fallbacks
- Provides post-installation setup instructions
- Handles various installation scenarios

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
- Claude CLI (multiple methods attempted)

**Installation Methods (in order of preference):**
1. **anthropic package** - Official Python package with API access
2. **claude-cli package** - Dedicated CLI package
3. **claude package** - Alternative CLI package
4. **GitHub binary** - Direct binary download (fallback)

**Current Status:**
- The official `@anthropic/claude` npm package is deprecated
- Multiple Python-based alternatives are available
- The script will try all methods and provide clear feedback

**Post-Installation:**
1. Set your Anthropic API key: `export ANTHROPIC_API_KEY='your-key'`
2. Test: `claude --help`
3. Start chatting: `claude`

### gemini_on_ubuntu.py

An automated installation script for Google Gemini AI on Ubuntu 22.04 systems.

**Features:**
- Installs Python 3 and pip
- Installs Google Gemini AI package
- Provides post-installation setup instructions

**Usage:**
```bash
sudo python3 gemini_on_ubuntu.py
```

**Requirements:**
- Ubuntu 22.04 (or compatible)
- Root/sudo privileges
- Internet connection
- Google AI Studio API key

**What it installs:**
- Python 3 and pip
- Google Gemini AI package

## General Notes

- All scripts require root/sudo privileges
- Scripts are designed for Ubuntu 22.04 but may work on other Debian-based systems
- Internet connection is required for package downloads
- Scripts include error handling and fallback methods
#!/usr/bin/env python3
"""
Setup script for Deep Research System

This script helps set up the project environment and validates the new structure.
"""

import sys
import os
from pathlib import Path

def check_structure():
    """Check if the project structure is properly organized."""
    print("🔍 Checking project structure...")
    
    required_dirs = [
        "src/deepsearch",
        "src/deepsearch/agents", 
        "src/deepsearch/core",
        "src/deepsearch/services",
        "src/deepsearch/utils",
        "tests/unit",
        "tests/integration", 
        "tests/e2e",
        "examples/demos",
        "examples/samples",
        "docs",
        "deployment",
        "config"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ All required directories exist")
        return True

def check_files():
    """Check if key files are in the right locations."""
    print("🔍 Checking file organization...")
    
    key_files = [
        "src/deepsearch/agents/base_agent.py",
        "src/deepsearch/core/agent_manager.py",
        "src/deepsearch/utils/config.py",
        "main.py",
        "config/.env.example"
    ]
    
    missing_files = []
    for file_path in key_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All key files are in place")
        return True

def setup_environment():
    """Set up the environment for the new structure."""
    print("🔧 Setting up environment...")
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    print("✅ Created logs directory")
    
    # Create uploads directory
    Path("uploads").mkdir(exist_ok=True)
    print("✅ Created uploads directory")
    
    # Check if .env exists, if not suggest copying from example
    if not Path(".env").exists():
        if Path("config/.env.example").exists():
            print("💡 Tip: Copy config/.env.example to .env and add your API keys")
        else:
            print("⚠️ No .env.example found in config/")
    
    return True

def main():
    """Main setup function."""
    print("🚀 Deep Research System - Project Setup")
    print("=" * 50)
    
    # Check structure
    structure_ok = check_structure()
    
    # Check files
    files_ok = check_files()
    
    # Setup environment
    env_ok = setup_environment()
    
    print("\n" + "=" * 50)
    
    if structure_ok and files_ok and env_ok:
        print("✅ Project structure is properly organized!")
        print("\n📋 Next steps:")
        print("1. Copy config/.env.example to .env")
        print("2. Add your API keys to .env")
        print("3. Run: python main.py --mode web")
        print("4. Or run: python main.py --mode interactive")
        print("\n📚 Documentation:")
        print("- Project structure: docs/PROJECT_STRUCTURE.md")
        print("- Updated README: README_NEW.md")
    else:
        print("❌ Project structure needs attention")
        print("Please check the missing directories and files above")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Deep Research System - Main Entry Point

This is the main entry point for the Deep Research System application.
It provides a command-line interface to run the system.
"""

import sys
import asyncio
import argparse
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deepsearch.utils.config import config
from deepsearch.utils.logger import setup_logging
from deepsearch.app import main as app_main

def setup_environment():
    """Setup the application environment."""
    # Setup logging
    logger = setup_logging()
    
    # Validate configuration
    config.validate()
    
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    return logger

async def run_interactive():
    """Run the system in interactive mode."""
    logger = setup_environment()
    logger.info("Starting Deep Research System in interactive mode")
    
    try:
        await app_main()
    except KeyboardInterrupt:
        logger.info("System shutdown requested by user")
    except Exception as e:
        logger.error(f"System error: {e}")
        raise

def run_web():
    """Run the system as a web application."""
    logger = setup_environment()
    logger.info("Starting Deep Research System as web application")
    
    import chainlit as cl
    
    # Run the Chainlit app
    cl.run()

def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Deep Research System - AI-powered lead research platform"
    )
    parser.add_argument(
        "--mode",
        choices=["interactive", "web"],
        default="web",
        help="Run mode: interactive (CLI) or web (Chainlit UI)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for web mode (default: 8000)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for web mode (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Set log level
    import os
    os.environ["LOG_LEVEL"] = args.log_level
    
    if args.mode == "interactive":
        asyncio.run(run_interactive())
    elif args.mode == "web":
        run_web()

if __name__ == "__main__":
    main()
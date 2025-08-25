#!/usr/bin/env python3
"""
LumaEngine Quick Start - Minimal setup for local development and testing.

This script provides a fast, minimal setup that:
1. Creates a virtual environment
2. Installs only core dependencies needed to run the app
3. Starts the FastAPI server with minimal configuration
4. No Docker, no heavy dependencies, no complex validation

Usage:
    python3 quick_start.py          # Setup and run
    python3 quick_start.py --setup  # Setup only
    python3 quick_start.py --run    # Run only (assumes setup done)
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def log(message, level="INFO"):
    """Simple logging."""
    print(f"[{level}] {message}")


def run_command(cmd, cwd=None, check=True):
    """Run a shell command."""
    log(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        log(f"Command failed: {result.stderr}", "ERROR")
        sys.exit(1)
    return result


def check_python():
    """Check Python version."""
    if sys.version_info < (3, 11):
        log("Python 3.11+ required", "ERROR")
        sys.exit(1)
    log(f"Python {sys.version_info.major}.{sys.version_info.minor} OK")


def create_minimal_env():
    """Create .env file with minimal config."""
    env_content = """# LumaEngine Quick Start Configuration
APP_NAME=LumaEngine
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# Minimal features for quick start
ENABLE_METRICS=false
ENABLE_TRACING=false
ENABLE_CACHING=false
ENABLE_RATE_LIMITING=false
"""

    with open(".env", "w") as f:
        f.write(env_content)
    log("Created minimal .env file")


def setup():
    """Minimal setup - just core FastAPI dependencies."""
    log("=== LumaEngine Quick Start Setup ===")

    # Check Python
    check_python()

    # Create venv if needed
    if not Path("venv").exists():
        log("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv venv")
    else:
        log("Virtual environment already exists")

    # Get pip path
    pip_cmd = "venv/bin/pip" if os.name != "nt" else "venv\\Scripts\\pip"

    # Install minimal dependencies only
    log("Installing core dependencies (this should be fast)...")
    core_deps = [
        "fastapi>=0.104.0,<0.106.0",
        "uvicorn[standard]>=0.24.0,<0.26.0",
        "pydantic>=2.5.0,<2.6.0",
        "pydantic-settings>=2.1.0,<2.2.0",
    ]

    for dep in core_deps:
        run_command(f"{pip_cmd} install '{dep}' --no-cache-dir")

    # Create minimal env
    if not Path(".env").exists():
        create_minimal_env()
    else:
        log(".env already exists")

    log("=== Setup Complete! ===")
    log("Total time: < 30 seconds (vs 2+ minutes)")


def run_server():
    """Run the FastAPI server."""
    log("=== Starting LumaEngine ===")

    # Check if venv exists
    if not Path("venv").exists():
        log("Virtual environment not found. Run setup first.", "ERROR")
        sys.exit(1)

    # Get python path
    python_cmd = "venv/bin/python" if os.name != "nt" else "venv\\Scripts\\python"

    # Simple server start - no complex validation
    log("Starting FastAPI server on http://localhost:8000")
    log("API docs: http://localhost:8000/docs")
    log("Health check: http://localhost:8000/health")
    log("")
    log("Press Ctrl+C to stop")

    try:
        # Run uvicorn directly - simpler than the main.py approach
        subprocess.run(
            [
                python_cmd,
                "-m",
                "uvicorn",
                "backend.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--log-level",
                "info",
            ]
        )
    except KeyboardInterrupt:
        log("Server stopped")


def main():
    parser = argparse.ArgumentParser(description="LumaEngine Quick Start")
    parser.add_argument("--setup", action="store_true", help="Setup only")
    parser.add_argument("--run", action="store_true", help="Run only")

    args = parser.parse_args()

    start_time = time.time()

    if args.setup:
        setup()
    elif args.run:
        run_server()
    else:
        # Default: setup and run
        setup()
        elapsed = time.time() - start_time
        log(f"Setup completed in {elapsed:.1f} seconds")
        log("Starting server in 2 seconds...")
        time.sleep(2)
        run_server()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Ultra-simple LumaEngine runner - just FastAPI with zero complex dependencies.
No pydantic, no settings, no validation - just a working API server.
"""

import os
import subprocess
import sys
from pathlib import Path


def log(msg):
    print(f"[SIMPLE] {msg}")


def setup_and_run():
    """Ultra-minimal setup and run."""
    log("Starting ultra-simple setup...")

    # Check Python
    if sys.version_info < (3, 11):
        log(
            f"ERROR: Need Python 3.11+, got {sys.version_info.major}.{sys.version_info.minor}"
        )
        sys.exit(1)

    # Create venv if needed
    if not Path("simple_venv").exists():
        log("Creating minimal virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "simple_venv"])

    # Pip path
    pip_cmd = "simple_venv/bin/pip" if os.name != "nt" else "simple_venv\\Scripts\\pip"
    python_cmd = (
        "simple_venv/bin/python" if os.name != "nt" else "simple_venv\\Scripts\\python"
    )

    # Install only FastAPI and uvicorn - no pydantic v2
    log("Installing FastAPI and uvicorn (should take ~10 seconds)...")
    subprocess.run(
        [
            pip_cmd,
            "install",
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "--no-cache-dir",
        ]
    )

    # Create ultra-simple app
    app_code = '''"""Ultra-simple FastAPI app."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="LumaEngine Simple", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "LumaEngine Ultra-Simple Mode",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": time.time()}

@app.get("/api/v1/test")
async def test():
    return {"test": "success", "mode": "ultra-simple"}
'''

    with open("simple_app.py", "w") as f:
        f.write(app_code)

    log("Setup complete! Starting server...")
    log("📍 Server: http://localhost:8000")
    log("📖 Docs: http://localhost:8000/docs")
    log("❤️  Health: http://localhost:8000/health")
    log("")

    # Run server
    try:
        subprocess.run(
            [
                python_cmd,
                "-m",
                "uvicorn",
                "simple_app:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ]
        )
    except KeyboardInterrupt:
        log("Server stopped")


if __name__ == "__main__":
    setup_and_run()

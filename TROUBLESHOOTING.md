# LumaEngine Development Environment Troubleshooting

This guide helps resolve common Python environment and dependency issues.

## Quick Fix - Start Fresh

If you're experiencing persistent issues, try the fresh setup:

```bash
# 1. Clean start
./setup_env.sh

# 2. Activate environment
source ./activate_luma.sh

# 3. Test the setup
make run
```

## Common Issues

### 1. Virtual Environment Issues

#### Problem: "Virtual environment not activated"
```
❌ Virtual environment not activated or incorrect environment
Run: source ./activate_luma.sh
```

**Solution:**
```bash
# Check current environment
echo $VIRTUAL_ENV

# If not activated or wrong environment
source ./activate_luma.sh

# Verify activation
python --version
which python
```

#### Problem: Virtual environment creation fails
```
ERROR: Failed to create virtual environment
```

**Solutions:**
```bash
# Option 1: Check Python installation
python3 --version  # Should be 3.11+

# Option 2: Install Python 3.11+ if needed (macOS with Homebrew)
brew install python@3.11
brew link python@3.11

# Option 3: Force recreate venv
rm -rf venv
python3.11 -m venv venv --prompt luma-engine
```

### 2. Dependency Installation Issues

#### Problem: Package installation fails
```
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output to see the issue
pip install -e ".[dev]" -v

# Try installing problematic packages individually
pip install "package_name>=version"
```

#### Problem: Conflicting dependencies
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solutions:**
```bash
# Fresh environment setup
./setup_env.sh

# Or manual cleanup
pip freeze > requirements_backup.txt
pip uninstall -r requirements_backup.txt -y
pip install -e ".[dev]"
```

### 3. Import Issues

#### Problem: "ModuleNotFoundError: No module named 'backend'"
**Solution:**
```bash
# Ensure you're in the project root
pwd  # Should show /path/to/luma-engine

# Reinstall in development mode
pip install -e .

# Check if backend is in sys.path
python -c "import sys; print('\\n'.join(sys.path))"
```

#### Problem: Pydantic warnings about model fields
```
UserWarning: Field "model_used" in LLMResponse has conflict with protected namespace "model_".
```

**Solution:** This is a non-critical warning. To fix:
```python
# In your Pydantic models, add:
class MyModel(BaseModel):
    model_config = {'protected_namespaces': ()}
```

### 4. Development Tool Issues

#### Problem: "pre-commit: command not found"
**Solution:**
```bash
# Check if pre-commit is installed
which pre-commit

# If not installed
pip install pre-commit
pre-commit install
```

#### Problem: Black/isort/mypy not found
**Solution:**
```bash
# Ensure development dependencies are installed
pip install -e ".[dev]"

# Or install individually
pip install black isort mypy flake8
```

### 5. Docker Issues

#### Problem: Docker services won't start
```
ERROR: Couldn't connect to Docker daemon
```

**Solutions:**
```bash
# Check Docker is running
docker --version
docker ps

# Start Docker services
make docker-run

# If ports are in use
make docker-stop
make docker-run

# Check what's using the ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432
```

### 6. Web Interface Issues

#### Problem: "npm: command not found"
**Solution:**
```bash
# Install Node.js (macOS with Homebrew)
brew install node

# Verify installation
node --version
npm --version

# Install web dependencies
make web-install
```

#### Problem: Web interface fails to start
```
Error: Cannot resolve module
```

**Solution:**
```bash
# Clean and reinstall
make web-clean
make web-install
make web-dev
```

## Environment Validation

### Check Python Setup
```bash
# Python version (should be 3.11+)
python --version

# Virtual environment
echo $VIRTUAL_ENV  # Should contain "luma-engine"

# Package installation
pip list | grep fastapi
pip list | grep pydantic

# Import test
python -c "import backend.main; print('✅ Backend OK')"
```

### Check Project Structure
```bash
# Verify project files
ls -la
# Should see: backend/, cli/, web/, pyproject.toml, Makefile

# Check backend structure
ls -la backend/
# Should see: main.py, api/, core/, models/
```

### Check Services
```bash
# Docker services
docker-compose ps

# API health check
curl http://localhost:8000/health

# API docs
curl http://localhost:8000/docs
```

## Reset Everything

If nothing else works, complete reset:

```bash
# 1. Stop all services
make docker-stop

# 2. Clean Python environment
rm -rf venv
find . -type d -name "__pycache__" -delete
find . -name "*.pyc" -delete

# 3. Clean Docker
docker-compose down -v
docker system prune -f

# 4. Clean web
cd web && rm -rf node_modules dist .vite && cd ..

# 5. Fresh setup
./setup_env.sh

# 6. Start fresh
source ./activate_luma.sh
make setup
```

## Getting Help

### Environment Information
```bash
# Gather environment info
echo "=== Python Environment ==="
python --version
which python
echo $VIRTUAL_ENV

echo "=== Project Structure ==="
ls -la

echo "=== Installed Packages ==="
pip list | head -20

echo "=== Docker Status ==="
docker ps

echo "=== Port Usage ==="
netstat -tulpn | grep -E ":(8000|5432|6379|3000)"
```

### Common Commands
```bash
# Environment management
source ./activate_luma.sh    # Activate environment
make check-venv              # Check environment status
make setup-env               # Fresh environment setup

# Development
make run                     # Start backend
make web-dev                 # Start frontend
make dev-stack              # Start both
make test                   # Run tests
make lint                   # Check code quality

# Troubleshooting
make clean                  # Clean Python artifacts
make docker-stop            # Stop Docker services
make docker-logs            # View Docker logs
```

### Still Having Issues?

1. Check the [GitHub Issues](https://github.com/edwardhallam/luma-engine/issues) for similar problems
2. Run `./setup_env.sh` to ensure clean environment
3. Verify you're using Python 3.11+
4. Ensure all required tools are installed (Docker, Node.js)
5. Check firewall/antivirus isn't blocking ports 8000, 3000, 5432, 6379

If you continue having issues, please create a GitHub issue with:
- Your operating system
- Python version (`python --version`)
- Error messages (full output)
- Steps you tried from this guide

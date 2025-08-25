#!/bin/bash
# LumaEngine Environment Diagnostics Script
# This script diagnoses common environment issues

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check system requirements
check_system() {
    echo "============================================"
    log_info "System Information"
    echo "============================================"

    echo "OS: $(uname -s) $(uname -r)"
    echo "Architecture: $(uname -m)"

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
        echo "Python: $PYTHON_VERSION ($(which python3))"

        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
            log_success "Python version is compatible (≥3.11)"
        else
            log_error "Python version is too old (need ≥3.11)"
        fi
    else
        log_error "Python 3 not found"
    fi

    # Check pip
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        echo "Pip: $PIP_VERSION"
        log_success "pip is available"
    else
        log_error "pip3 not found"
    fi

    # Check Docker
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        echo "Docker: $DOCKER_VERSION"
        log_success "Docker is available"
    else
        log_warning "Docker not found (optional for development)"
    fi

    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo "Node.js: $NODE_VERSION"
        log_success "Node.js is available"
    else
        log_warning "Node.js not found (needed for web interface)"
    fi
}

# Check project structure
check_project() {
    echo ""
    echo "============================================"
    log_info "Project Structure"
    echo "============================================"

    if [ -f "pyproject.toml" ]; then
        log_success "pyproject.toml found"
    else
        log_error "pyproject.toml not found - are you in the right directory?"
        return 1
    fi

    if [ -d "backend" ]; then
        log_success "backend/ directory found"
    else
        log_error "backend/ directory not found"
    fi

    if [ -f "backend/main.py" ]; then
        log_success "backend/main.py found"
    else
        log_error "backend/main.py not found"
    fi

    if [ -f "Makefile" ]; then
        log_success "Makefile found"
    else
        log_warning "Makefile not found"
    fi

    if [ -f ".env" ]; then
        log_success ".env file found"
    else
        log_warning ".env file not found (will be created by setup)"
    fi
}

# Check virtual environment
check_venv() {
    echo ""
    echo "============================================"
    log_info "Virtual Environment"
    echo "============================================"

    if [ -d "venv" ]; then
        log_success "Virtual environment directory exists"

        if [ -f "venv/bin/activate" ]; then
            log_success "Activation script exists"
        else
            log_error "Activation script missing"
        fi

        if [ -f "venv/pyvenv.cfg" ]; then
            echo "Configuration:"
            cat venv/pyvenv.cfg | head -5
        fi
    else
        log_warning "Virtual environment not found (run ./setup_env.sh to create)"
    fi

    if [ -n "${VIRTUAL_ENV:-}" ]; then
        if [[ "$VIRTUAL_ENV" == *"luma-engine"* ]]; then
            log_success "LumaEngine virtual environment is active"
            echo "Environment: $VIRTUAL_ENV"
        else
            log_warning "Different virtual environment is active: $VIRTUAL_ENV"
        fi
    else
        log_warning "No virtual environment is currently active"
    fi
}

# Check Python packages
check_packages() {
    echo ""
    echo "============================================"
    log_info "Python Packages"
    echo "============================================"

    if [ -n "${VIRTUAL_ENV:-}" ]; then
        echo "Checking packages in virtual environment..."

        # Check key packages
        local packages=("fastapi" "pydantic" "uvicorn" "langchain" "openai" "anthropic")

        for pkg in "${packages[@]}"; do
            if python -c "import $pkg" 2>/dev/null; then
                VERSION=$(python -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))" 2>/dev/null)
                log_success "$pkg ($VERSION)"
            else
                log_error "$pkg not found or broken"
            fi
        done

        # Check development tools
        local dev_tools=("black" "isort" "flake8" "mypy" "pytest")
        echo ""
        echo "Development tools:"
        for tool in "${dev_tools[@]}"; do
            if command -v $tool &> /dev/null; then
                log_success "$tool available"
            else
                log_warning "$tool not found"
            fi
        done
    else
        log_warning "Virtual environment not active, skipping package check"
    fi
}

# Check imports
check_imports() {
    echo ""
    echo "============================================"
    log_info "Import Tests"
    echo "============================================"

    if [ -n "${VIRTUAL_ENV:-}" ]; then
        # Test backend import
        if python -c "import backend" 2>/dev/null; then
            log_success "Backend package imports successfully"
        else
            log_error "Backend package import failed"
            echo "Error details:"
            python -c "import backend" 2>&1 || true
        fi

        # Test main module
        if python -c "import backend.main" 2>/dev/null; then
            log_success "Backend main module imports successfully"
        else
            log_error "Backend main module import failed"
            echo "Error details:"
            python -c "import backend.main" 2>&1 || true
        fi

        # Test FastAPI app
        if python -c "from backend.main import app; print('FastAPI app loaded')" 2>/dev/null; then
            log_success "FastAPI application loads successfully"
        else
            log_warning "FastAPI application failed to load"
        fi

        # Test CLI (optional)
        if python -c "import cli" 2>/dev/null; then
            log_success "CLI package imports successfully"
        else
            log_info "CLI package import failed (may be expected)"
        fi
    else
        log_warning "Virtual environment not active, skipping import tests"
    fi
}

# Check services
check_services() {
    echo ""
    echo "============================================"
    log_info "Services Status"
    echo "============================================"

    # Check if Docker services are running
    if command -v docker &> /dev/null; then
        if docker ps &> /dev/null; then
            log_success "Docker is running"

            # Check specific services
            if docker-compose ps | grep -q "Up"; then
                log_success "Docker Compose services are running"
                echo "Active services:"
                docker-compose ps --services --filter status=running | while read service; do
                    echo "  - $service"
                done
            else
                log_info "No Docker Compose services currently running"
            fi
        else
            log_warning "Docker daemon is not running"
        fi
    fi

    # Check ports
    echo ""
    echo "Port usage:"
    local ports=(8000 3000 5432 6379)
    for port in "${ports[@]}"; do
        if lsof -i :$port &> /dev/null; then
            local process=$(lsof -i :$port | tail -n 1 | awk '{print $1, $2}')
            log_warning "Port $port in use by: $process"
        else
            log_success "Port $port available"
        fi
    done
}

# Check web interface
check_web() {
    echo ""
    echo "============================================"
    log_info "Web Interface"
    echo "============================================"

    if [ -d "web" ]; then
        log_success "Web directory exists"

        if [ -f "web/package.json" ]; then
            log_success "package.json found"
        else
            log_error "package.json not found in web/"
        fi

        if [ -d "web/node_modules" ]; then
            log_success "node_modules directory exists"
        else
            log_warning "node_modules not found (run: make web-install)"
        fi

        if command -v npm &> /dev/null; then
            log_success "npm is available"
        else
            log_error "npm not found - install Node.js"
        fi
    else
        log_warning "Web directory not found"
    fi
}

# Provide recommendations
provide_recommendations() {
    echo ""
    echo "============================================"
    log_info "Recommendations"
    echo "============================================"

    # Check if fresh setup is needed
    local needs_setup=false

    if [ ! -d "venv" ]; then
        needs_setup=true
        echo "🔧 Virtual environment missing"
    fi

    if [ -z "${VIRTUAL_ENV:-}" ]; then
        echo "🔧 Virtual environment not active"
        echo "   Run: source ./activate_luma.sh"
    fi

    if ! python -c "import backend.main" 2>/dev/null && [ -n "${VIRTUAL_ENV:-}" ]; then
        needs_setup=true
        echo "🔧 Backend imports failing"
    fi

    if [ "$needs_setup" = true ]; then
        echo ""
        echo "💡 Recommended action: Fresh environment setup"
        echo "   Run: ./setup_env.sh"
        echo ""
    fi

    # Check for Docker setup
    if ! docker ps &> /dev/null; then
        echo "🔧 Docker services not running"
        echo "   Run: make docker-run"
    fi

    # Check for web setup
    if [ -d "web" ] && [ ! -d "web/node_modules" ]; then
        echo "🔧 Web dependencies not installed"
        echo "   Run: make web-install"
    fi

    echo ""
    echo "📋 Quick commands:"
    echo "   ./setup_env.sh          - Fresh Python environment"
    echo "   source ./activate_luma.sh - Activate environment"
    echo "   make setup              - Full development setup"
    echo "   make run                - Start backend server"
    echo "   make web-dev            - Start web interface"
    echo "   make dev-stack          - Start full stack"
}

# Main function
main() {
    echo "LumaEngine Environment Diagnostics"
    echo "Generated: $(date)"

    check_system
    check_project || exit 1
    check_venv
    check_packages
    check_imports
    check_services
    check_web
    provide_recommendations

    echo ""
    echo "============================================"
    log_info "Diagnostics completed"
    echo "============================================"
    echo ""
    echo "If you need help, check TROUBLESHOOTING.md or create a GitHub issue"
    echo "with the output of this diagnostic script."
}

# Run diagnostics
main "$@"

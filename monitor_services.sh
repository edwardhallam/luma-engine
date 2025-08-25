#!/bin/bash
# LumaEngine Service Monitor Script
# This script checks the health of backend and frontend services

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Service URLs
BACKEND_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
HEALTH_ENDPOINT="${BACKEND_URL}/health"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_backend() {
    log_info "Checking backend service at ${BACKEND_URL}..."

    if curl -s --max-time 5 "${HEALTH_ENDPOINT}" > /dev/null; then
        HEALTH_RESPONSE=$(curl -s --max-time 5 "${HEALTH_ENDPOINT}")
        log_success "Backend is healthy"
        echo "  Response: ${HEALTH_RESPONSE}"
        return 0
    else
        log_error "Backend is not responding"
        return 1
    fi
}

check_frontend() {
    log_info "Checking frontend service at ${FRONTEND_URL}..."

    if curl -s --max-time 5 -I "${FRONTEND_URL}" | grep -q "200 OK"; then
        log_success "Frontend is accessible"
        return 0
    else
        log_error "Frontend is not responding"
        return 1
    fi
}

check_processes() {
    log_info "Checking running processes..."

    # Check for uvicorn (backend)
    if pgrep -f "uvicorn.*backend.main" > /dev/null; then
        BACKEND_PID=$(pgrep -f "uvicorn.*backend.main")
        log_success "Backend process running (PID: ${BACKEND_PID})"
    else
        log_warning "Backend process not found"
    fi

    # Check for node/vite (frontend)
    if pgrep -f "vite" > /dev/null; then
        FRONTEND_PID=$(pgrep -f "vite")
        log_success "Frontend process running (PID: ${FRONTEND_PID})"
    else
        log_warning "Frontend process not found"
    fi
}

show_usage() {
    echo "LumaEngine Service Monitor"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --watch, -w     Monitor continuously (every 10 seconds)"
    echo "  --auto, -a      Auto-restart services if they fail"
    echo "  --restart, -r   Restart all services"
    echo "  --stop, -s      Stop all services"
    echo "  --help, -h      Show this help message"
    echo ""
    echo "Services:"
    echo "  Backend:  ${BACKEND_URL}"
    echo "  Frontend: ${FRONTEND_URL}"
    echo "  Health:   ${HEALTH_ENDPOINT}"
}

monitor_once() {
    echo "============================================"
    echo "LumaEngine Service Health Check"
    echo "Timestamp: $(date)"
    echo "============================================"

    BACKEND_OK=0
    FRONTEND_OK=0

    check_backend && BACKEND_OK=1
    check_frontend && FRONTEND_OK=1
    check_processes

    echo ""
    if [ $BACKEND_OK -eq 1 ] && [ $FRONTEND_OK -eq 1 ]; then
        log_success "All services are healthy!"
        echo "  🌐 Frontend: ${FRONTEND_URL}"
        echo "  🔧 API: ${BACKEND_URL}"
        echo "  📚 Docs: ${BACKEND_URL}/docs"
    else
        log_warning "Some services may not be running properly"
        echo ""
        echo "To start services:"
        echo "  Backend:  source ./activate_luma.sh && make run"
        echo "  Frontend: make web-dev"
        echo "  Both:     make dev-stack"
    fi

    echo "============================================"
}

monitor_continuous() {
    log_info "Starting continuous monitoring (Press Ctrl+C to stop)..."
    echo ""

    while true; do
        monitor_once
        echo ""
        log_info "Next check in 10 seconds..."
        sleep 10
        clear
    done
}

start_backend() {
    log_info "Starting backend service..."

    # Activate virtual environment and start backend
    export VIRTUAL_ENV="/Users/edwardhallam/Code/claude-code/luma-engine/venv"
    export PATH="$VIRTUAL_ENV/bin:$PATH"

    cd /Users/edwardhallam/Code/claude-code/luma-engine
    nohup uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &

    sleep 3
    if check_backend; then
        log_success "Backend started successfully"
        return 0
    else
        log_error "Failed to start backend"
        return 1
    fi
}

start_frontend() {
    log_info "Starting frontend service..."

    cd /Users/edwardhallam/Code/claude-code/luma-engine/web
    nohup npm run dev > ../logs/frontend.log 2>&1 &

    sleep 5
    if check_frontend; then
        log_success "Frontend started successfully"
        return 0
    else
        log_error "Failed to start frontend"
        return 1
    fi
}

stop_services() {
    log_info "Stopping all services..."

    # Stop backend
    if pgrep -f "uvicorn.*backend.main" > /dev/null; then
        pkill -f "uvicorn.*backend.main" && log_success "Backend stopped"
    fi

    # Stop frontend
    if pgrep -f "vite" > /dev/null; then
        pkill -f "vite" && log_success "Frontend stopped"
    fi

    sleep 2
}

restart_services() {
    log_info "Restarting all services..."
    stop_services
    sleep 2

    # Ensure logs directory exists
    mkdir -p logs

    start_backend
    start_frontend

    log_success "Services restarted"
}

monitor_with_auto_restart() {
    log_info "Starting continuous monitoring with auto-restart (Press Ctrl+C to stop)..."
    echo ""

    # Ensure logs directory exists
    mkdir -p logs

    while true; do
        NEED_RESTART=0

        # Check backend
        if ! check_backend > /dev/null 2>&1; then
            if ! pgrep -f "uvicorn.*backend.main" > /dev/null; then
                log_warning "Backend is down, restarting..."
                start_backend
                NEED_RESTART=1
            fi
        fi

        # Check frontend
        if ! check_frontend > /dev/null 2>&1; then
            if ! pgrep -f "vite" > /dev/null; then
                log_warning "Frontend is down, restarting..."
                start_frontend
                NEED_RESTART=1
            fi
        fi

        if [ $NEED_RESTART -eq 0 ]; then
            echo -n "."  # Show that monitoring is active
        else
            echo ""
        fi

        sleep 10
    done
}

# Parse command line arguments
case "${1:-}" in
    --watch|-w)
        monitor_continuous
        ;;
    --auto|-a)
        monitor_with_auto_restart
        ;;
    --restart|-r)
        restart_services
        ;;
    --stop|-s)
        stop_services
        ;;
    --help|-h)
        show_usage
        ;;
    "")
        monitor_once
        ;;
    *)
        echo "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac

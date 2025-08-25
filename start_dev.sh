#!/bin/bash
# LumaEngine Development Server Startup Script

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting LumaEngine Development Servers...${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the LumaEngine root directory"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ] || [[ "$VIRTUAL_ENV" != *"luma-engine"* ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated. Activating...${NC}"
    source venv/bin/activate || {
        echo "❌ Failed to activate virtual environment. Run: ./setup_env.sh"
        exit 1
    }
fi

# Install web dependencies if needed
if [ ! -d "web/node_modules" ]; then
    echo -e "${BLUE}📦 Installing web dependencies...${NC}"
    cd web && npm install && cd ..
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}🔧 Starting backend server (http://localhost:8000)...${NC}"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo -e "${GREEN}📱 Starting frontend server (http://localhost:3000)...${NC}"
cd web && npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "============================================"
echo -e "${GREEN}✅ LumaEngine is running!${NC}"
echo ""
echo -e "📱 Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "🔧 Backend API: ${BLUE}http://localhost:8000${NC}"
echo -e "📚 API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "❤️  Health Check: ${BLUE}http://localhost:8000/health${NC}"
echo "============================================"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID

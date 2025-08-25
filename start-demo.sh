#!/bin/bash

# LumaEngine Quick Start Demo Script
set -e

echo "🚀 LumaEngine Quick Start Demo"
echo "================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
    echo "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo "✅ Prerequisites satisfied"

# Navigate to web directory
cd web

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🎉 Starting LumaEngine Web Interface..."
echo ""
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "📊 All features available with mock data"
echo "🔧 No backend required for demo"
echo ""
echo "Press Ctrl+C to stop the demo"
echo ""

# Start the development server
npm run dev

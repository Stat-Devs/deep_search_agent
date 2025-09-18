#!/bin/bash

echo "🐳 StatDevs Sales Intelligence System - Docker Deployment"
echo "========================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose first."
    exit 1
fi

# Check if .env file exists, create from example if not
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from .env.example"
        echo "⚠️  Please edit .env with your actual API keys for local development"
        echo "   nano .env"
        echo ""
        echo "For production deployment, the GitHub Actions workflow will automatically"
        echo "use the secrets configured in your repository settings."
        echo ""
        read -p "Press Enter to continue with placeholder values (for testing) or Ctrl+C to edit .env first..."
    else
        echo "❌ No .env.example file found. Please create .env file manually:"
        echo "   OPENAI_API_KEY=your_actual_openai_api_key"
        echo "   GEMINI_API_KEY=your_actual_gemini_api_key"
        echo "   TAVILY_API_KEY=your_actual_tavily_api_key"
        echo "   OPENAI_TRACE=1"
        exit 1
    fi
fi

# Load environment variables
source .env

# Check if API keys are set (allow placeholder values for testing)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not found in .env file"
    exit 1
fi

echo "ℹ️  Using API keys from .env file for local development"

echo "✅ Environment variables loaded"
echo "✅ Docker is running"
echo "✅ docker-compose is available"

# Build and start the containers
echo ""
echo "🚀 Building and starting StatDevs Sales Intelligence System..."
docker-compose up --build -d

# Wait for the service to be ready
echo ""
echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if the service is running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "🎉 StatDevs Sales Intelligence System is now running!"
    echo ""
    echo "🌐 Access your application at: http://localhost:8000"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop service: docker-compose down"
    echo "   Restart service: docker-compose restart"
    echo "   Update and restart: docker-compose up --build -d"
    echo ""
    echo "🔍 Check service status:"
    docker-compose ps
else
    echo ""
    echo "❌ Service failed to start. Check logs with:"
    echo "   docker-compose logs"
    exit 1
fi

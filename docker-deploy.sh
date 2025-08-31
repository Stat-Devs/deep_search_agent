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

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file. Please edit it with your actual API keys."
        echo "   nano .env"
        exit 1
    else
        echo "❌ No .env.example file found. Please create .env file manually:"
        echo "   OPENAI_API_KEY=your_actual_openai_api_key"
        echo "   OPENAI_TRACE=1"
        exit 1
    fi
fi

# Load environment variables
source .env

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ Please set your actual OPENAI_API_KEY in the .env file"
    exit 1
fi

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

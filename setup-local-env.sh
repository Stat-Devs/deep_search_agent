#!/bin/bash

echo "🔧 StatDevs Sales Intelligence - Local Environment Setup"
echo "======================================================="

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from .env.example"
    else
        echo "❌ .env.example file not found!"
        exit 1
    fi
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your actual API keys:"
echo "   nano .env"
echo ""
echo "2. Or run the deployment script:"
echo "   ./deployment/docker-deploy.sh"
echo ""
echo "ℹ️  For production deployment:"
echo "   - Push to GitHub main branch"
echo "   - GitHub Actions will automatically deploy using repository secrets"
echo "   - No need to set local API keys for production"
echo ""
echo "🔑 Required API keys for local development:"
echo "   - OPENAI_API_KEY"
echo "   - GEMINI_API_KEY" 
echo "   - TAVILY_API_KEY"

#!/bin/bash

echo "🚀 StatDevs Sales Intelligence System - Deployment Script"
echo "========================================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please run 'git init' first."
    exit 1
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    exit 1
fi

echo "✅ Git repository found"

# Add all files
echo "📁 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy StatDevs Sales Intelligence System v1.0"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "🎉 Deployment to GitHub completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Install Railway CLI: npm install -g @railway/cli"
echo "2. Login to Railway: railway login"
echo "3. Create project: railway init"
echo "4. Set environment variables:"
echo "   - OPENAI_API_KEY: Your OpenAI API key"
echo "   - OPENAI_TRACE: Set to 1"
echo "5. Deploy: railway up"
echo ""
echo "🌐 Your app will be available at Railway's provided URL"
echo ""
echo "💡 For custom domain, use Railway's custom domain feature"
echo "   Example: sales.statdevs.com"
echo ""
echo "📞 Need help? Contact StatDevs team at info@statdevs.com"

#!/bin/bash

echo "🚀 StatDevs Sales Intelligence System - GitHub CI/CD Deployment"
echo "==============================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_error "Git repository not found. Please run 'git init' first."
    exit 1
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    print_error "No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    exit 1
fi

print_success "Git repository found"

# Check if GitHub Actions workflow exists
if [ ! -f ".github/workflows/deploy.yml" ]; then
    print_warning "GitHub Actions workflow not found. Creating it..."
    mkdir -p .github/workflows
    # The workflow file should already be created by the setup process
fi

# Add all files
print_status "Adding files to git..."
git add .

# Commit changes
print_status "Committing changes..."
git commit -m "Deploy StatDevs Sales Intelligence System v1.0 - Digital Ocean CI/CD"

# Push to GitHub
print_status "Pushing to GitHub..."
git push origin main

print_success "Deployment to GitHub completed!"
echo ""
echo "🎉 GitHub CI/CD Pipeline Activated!"
echo ""
echo "📋 What happens next:"
echo "1. ✅ GitHub Actions will automatically build and test your app"
echo "2. 🚀 If tests pass, it will deploy to Digital Ocean server"
echo "3. 🌐 Your app will be available at: http://143.110.183.47:8000"
echo ""
echo "📊 Monitor deployment:"
echo "   - GitHub Actions: https://github.com/YOUR_USERNAME/YOUR_REPO/actions"
echo "   - Server logs: ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose logs -f'"
echo ""
echo "🔧 Required GitHub Secrets (set in repository settings):"
echo "   - DO_HOST: 143.110.183.47"
echo "   - DO_USERNAME: root"
echo "   - DO_SSH_KEY: Your private SSH key"
echo "   - OPENAI_API_KEY: Your OpenAI API key"
echo "   - GEMINI_API_KEY: Your Gemini API key"
echo "   - TAVILY_API_KEY: Your Tavily API key"
echo ""
echo "💡 For custom domain setup:"
echo "   - Update nginx configuration on the server"
echo "   - Setup SSL with Let's Encrypt"
echo "   - Example: sales.statdevs.com"
echo ""
echo "📞 Need help? Contact StatDevs team at info@statdevs.com"

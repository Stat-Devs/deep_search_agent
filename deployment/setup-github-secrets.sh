#!/bin/bash

echo "🔐 GitHub Secrets Setup Helper"
echo "=============================="

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

# Check if GitHub CLI is installed
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI (gh) is not installed."
        echo "Install it from: https://cli.github.com/"
        echo "Or use the manual method below."
        return 1
    fi
    return 0
}

# Setup secrets using GitHub CLI
setup_secrets_gh_cli() {
    print_status "Setting up GitHub secrets using GitHub CLI..."
    
    # Check if user is logged in
    if ! gh auth status &> /dev/null; then
        print_error "Not logged in to GitHub CLI. Please run: gh auth login"
        exit 1
    fi
    
    # Get repository name
    REPO_NAME=$(gh repo view --json name -q .name)
    if [ -z "$REPO_NAME" ]; then
        print_error "Could not determine repository name. Make sure you're in a Git repository."
        exit 1
    fi
    
    print_success "Repository: $REPO_NAME"
    
    # Set Digital Ocean secrets
    print_status "Setting Digital Ocean secrets..."
    gh secret set DO_HOST --body "143.110.183.47"
    gh secret set DO_USERNAME --body "root"
    
    # Get SSH key
    if [ -f ~/.ssh/id_rsa ]; then
        SSH_KEY=$(cat ~/.ssh/id_rsa)
        gh secret set DO_SSH_KEY --body "$SSH_KEY"
        print_success "SSH key secret set"
    else
        print_warning "SSH key not found at ~/.ssh/id_rsa"
        echo "Please generate an SSH key first:"
        echo "  ssh-keygen -t rsa -b 4096 -C \"your_email@example.com\""
    fi
    
    # Get API keys from user
    echo ""
    print_status "Please provide your API keys:"
    
    read -p "OpenAI API Key: " OPENAI_KEY
    if [ -n "$OPENAI_KEY" ]; then
        gh secret set OPENAI_API_KEY --body "$OPENAI_KEY"
        print_success "OpenAI API key secret set"
    fi
    
    read -p "Gemini API Key: " GEMINI_KEY
    if [ -n "$GEMINI_KEY" ]; then
        gh secret set GEMINI_API_KEY --body "$GEMINI_KEY"
        print_success "Gemini API key secret set"
    fi
    
    read -p "Tavily API Key: " TAVILY_KEY
    if [ -n "$TAVILY_KEY" ]; then
        gh secret set TAVILY_API_KEY --body "$TAVILY_KEY"
        print_success "Tavily API key secret set"
    fi
    
    print_success "All secrets have been set!"
}

# Manual setup instructions
show_manual_setup() {
    print_status "Manual GitHub Secrets Setup Instructions:"
    echo ""
    echo "1. Go to your GitHub repository"
    echo "2. Click on 'Settings' tab"
    echo "3. Click on 'Secrets and variables' → 'Actions'"
    echo "4. Click 'New repository secret' for each secret below:"
    echo ""
    echo "Required Secrets:"
    echo "┌─────────────────┬─────────────────────┬─────────────────────────────────┐"
    echo "│ Secret Name     │ Value               │ Description                     │"
    echo "├─────────────────┼─────────────────────┼─────────────────────────────────┤"
    echo "│ DO_HOST         │ 143.110.183.47      │ Digital Ocean server IP         │"
    echo "│ DO_USERNAME     │ root                │ Server username                 │"
    echo "│ DO_SSH_KEY      │ [Your private key]  │ Private SSH key for server      │"
    echo "│ OPENAI_API_KEY  │ [Your OpenAI key]   │ OpenAI API key                  │"
    echo "│ GEMINI_API_KEY  │ [Your Gemini key]   │ Google Gemini API key           │"
    echo "│ TAVILY_API_KEY  │ [Your Tavily key]   │ Tavily API key                  │"
    echo "└─────────────────┴─────────────────────┴─────────────────────────────────┘"
    echo ""
    echo "To get your SSH private key:"
    echo "  cat ~/.ssh/id_rsa"
    echo ""
    echo "To add your public key to the server:"
    echo "  ssh-copy-id root@143.110.183.47"
    echo ""
}

# Generate SSH key if needed
generate_ssh_key() {
    if [ ! -f ~/.ssh/id_rsa ]; then
        print_status "Generating SSH key pair..."
        read -p "Enter your email address: " EMAIL
        ssh-keygen -t rsa -b 4096 -C "$EMAIL" -f ~/.ssh/id_rsa -N ""
        print_success "SSH key generated at ~/.ssh/id_rsa"
        
        # Add to SSH agent
        eval "$(ssh-agent -s)"
        ssh-add ~/.ssh/id_rsa
        
        print_status "Adding public key to Digital Ocean server..."
        ssh-copy-id root@143.110.183.47
        print_success "SSH key added to server"
    else
        print_success "SSH key already exists at ~/.ssh/id_rsa"
    fi
}

# Main function
main() {
    print_status "GitHub Secrets Setup Helper"
    echo ""
    
    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        print_error "Not in a Git repository. Please run this script from your project directory."
        exit 1
    fi
    
    # Generate SSH key if needed
    generate_ssh_key
    
    # Try to use GitHub CLI
    if check_gh_cli; then
        echo ""
        read -p "Use GitHub CLI to set secrets automatically? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            setup_secrets_gh_cli
        else
            show_manual_setup
        fi
    else
        show_manual_setup
    fi
    
    echo ""
    print_success "GitHub secrets setup completed!"
    echo ""
    echo "🎉 Next steps:"
    echo "1. Push your code to trigger deployment:"
    echo "   git add ."
    echo "   git commit -m 'Setup CI/CD deployment'"
    echo "   git push origin main"
    echo ""
    echo "2. Monitor deployment at:"
    echo "   https://github.com/YOUR_USERNAME/YOUR_REPO/actions"
    echo ""
    echo "3. Your app will be available at:"
    echo "   http://143.110.183.47:8000"
    echo ""
}

# Run main function
main "$@"


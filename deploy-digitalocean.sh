#!/bin/bash

echo "🚀 StatDevs Sales Intelligence System - Digital Ocean Deployment"
echo "==============================================================="

# Configuration
DO_HOST="143.110.183.47"
DO_USER="root"
APP_NAME="statdevs-sales-intelligence"
APP_DIR="/opt/$APP_NAME"
APP_PORT="8000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if required environment variables are set
check_env_vars() {
    print_status "Checking environment variables..."
    
    if [ -z "$OPENAI_API_KEY" ]; then
        print_error "OPENAI_API_KEY is not set"
        exit 1
    fi
    
    if [ -z "$GEMINI_API_KEY" ]; then
        print_error "GEMINI_API_KEY is not set"
        exit 1
    fi
    
    if [ -z "$TAVILY_API_KEY" ]; then
        print_error "TAVILY_API_KEY is not set"
        exit 1
    fi
    
    print_success "All required environment variables are set"
}

# Install Docker and Docker Compose on Digital Ocean server
install_docker() {
    print_status "Installing Docker and Docker Compose on Digital Ocean server..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << 'EOF'
        # Update system
        apt-get update
        
        # Install Docker
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        
        # Install Docker Compose
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        
        # Start and enable Docker
        systemctl start docker
        systemctl enable docker
        
        # Add user to docker group
        usermod -aG docker $USER
        
        echo "Docker and Docker Compose installed successfully"
EOF
    
    print_success "Docker installation completed"
}

# Deploy application to Digital Ocean
deploy_app() {
    print_status "Deploying application to Digital Ocean..."
    
    # Create deployment package
    print_status "Creating deployment package..."
    tar -czf deployment.tar.gz \
        --exclude='.git' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env' \
        --exclude='logs/*' \
        --exclude='uploads/*' \
        --exclude='deployment.tar.gz' \
        .
    
    # Copy files to server
    print_status "Copying files to Digital Ocean server..."
    scp -o StrictHostKeyChecking=no deployment.tar.gz $DO_USER@$DO_HOST:/tmp/
    
    # Deploy on server
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << EOF
        # Create application directory
        mkdir -p $APP_DIR
        cd $APP_DIR
        
        # Extract application files
        tar -xzf /tmp/deployment.tar.gz -C $APP_DIR
        
        # Create environment file
        cat > .env << 'ENVEOF'
OPENAI_API_KEY=$OPENAI_API_KEY
GEMINI_API_KEY=$GEMINI_API_KEY
TAVILY_API_KEY=$TAVILY_API_KEY
OPENAI_TRACE=1
PYTHONPATH=/app
ENVEOF
        
        # Create logs and uploads directories
        mkdir -p logs uploads
        
        # Stop existing containers
        docker-compose down || true
        
        # Remove old images to free up space
        docker image prune -f
        
        # Build and start the application
        docker-compose up -d --build
        
        # Wait for application to be ready
        echo "Waiting for application to start..."
        sleep 30
        
        # Check if application is running
        if curl -f http://localhost:$APP_PORT/health; then
            echo "✅ Application deployed successfully!"
            echo "🌐 Application is running at: http://$DO_HOST:$APP_PORT"
        else
            echo "❌ Application deployment failed!"
            docker-compose logs
            exit 1
        fi
        
        # Setup nginx reverse proxy (optional)
        if command -v nginx >/dev/null 2>&1; then
            cat > /etc/nginx/sites-available/$APP_NAME << 'NGINXEOF'
server {
    listen 80;
    server_name $DO_HOST;
    
    location / {
        proxy_pass http://localhost:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support for Chainlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
NGINXEOF
            
            # Enable the site
            ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
            nginx -t && systemctl reload nginx || echo "Nginx configuration failed, but app is running on port $APP_PORT"
        fi
        
        # Clean up
        rm -f /tmp/deployment.tar.gz
EOF
    
    # Clean up local deployment package
    rm -f deployment.tar.gz
    
    print_success "Application deployed successfully!"
}

# Setup SSL with Let's Encrypt (optional)
setup_ssl() {
    print_status "Setting up SSL with Let's Encrypt..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << 'EOF'
        # Install certbot
        apt-get install -y certbot python3-certbot-nginx
        
        # Get SSL certificate
        certbot --nginx -d 143.110.183.47 --non-interactive --agree-tos --email admin@statdevs.com
        
        # Setup auto-renewal
        echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
        
        echo "SSL setup completed"
EOF
    
    print_success "SSL setup completed"
}

# Monitor application
monitor_app() {
    print_status "Monitoring application status..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << EOF
        cd $APP_DIR
        
        echo "=== Docker Containers ==="
        docker ps
        
        echo "=== Application Logs ==="
        docker-compose logs --tail=50
        
        echo "=== System Resources ==="
        df -h
        free -h
        
        echo "=== Application Health ==="
        curl -f http://localhost:$APP_PORT/health || echo "Health check failed"
EOF
}

# Main deployment function
main() {
    print_status "Starting Digital Ocean deployment..."
    
    # Check environment variables
    check_env_vars
    
    # Install Docker if needed
    print_status "Checking Docker installation..."
    if ! ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST "command -v docker >/dev/null 2>&1"; then
        install_docker
    else
        print_success "Docker is already installed"
    fi
    
    # Deploy application
    deploy_app
    
    # Setup SSL (optional)
    read -p "Do you want to setup SSL with Let's Encrypt? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_ssl
    fi
    
    # Monitor application
    monitor_app
    
    print_success "Deployment completed successfully!"
    echo ""
    echo "🎉 StatDevs Sales Intelligence System is now running!"
    echo "🌐 Access your application at: http://$DO_HOST:$APP_PORT"
    echo "📊 Monitor logs with: ssh $DO_USER@$DO_HOST 'cd $APP_DIR && docker-compose logs -f'"
    echo ""
    echo "📋 Useful commands:"
    echo "  - View logs: ssh $DO_USER@$DO_HOST 'cd $APP_DIR && docker-compose logs -f'"
    echo "  - Restart app: ssh $DO_USER@$DO_HOST 'cd $APP_DIR && docker-compose restart'"
    echo "  - Update app: Run this script again"
    echo "  - Stop app: ssh $DO_USER@$DO_HOST 'cd $APP_DIR && docker-compose down'"
}

# Run main function
main "$@"



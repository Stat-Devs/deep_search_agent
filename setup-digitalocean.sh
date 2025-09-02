#!/bin/bash

echo "🔧 Digital Ocean Server Setup for StatDevs Sales Intelligence"
echo "============================================================="

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

# Setup server environment
setup_server() {
    print_status "Setting up Digital Ocean server environment..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << 'EOF'
        # Update system
        apt-get update && apt-get upgrade -y
        
        # Install essential packages
        apt-get install -y \
            curl \
            wget \
            git \
            unzip \
            htop \
            nginx \
            ufw \
            fail2ban \
            certbot \
            python3-certbot-nginx
        
        # Install Docker
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        rm get-docker.sh
        
        # Install Docker Compose
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        
        # Start and enable services
        systemctl start docker
        systemctl enable docker
        systemctl start nginx
        systemctl enable nginx
        systemctl start fail2ban
        systemctl enable fail2ban
        
        # Configure firewall
        ufw allow ssh
        ufw allow 80
        ufw allow 443
        ufw allow 8000
        ufw --force enable
        
        # Create application directory
        mkdir -p /opt/$APP_NAME
        mkdir -p /opt/$APP_NAME/logs
        mkdir -p /opt/$APP_NAME/uploads
        
        # Set proper permissions
        chown -R $DO_USER:$DO_USER /opt/$APP_NAME
        
        echo "Server setup completed successfully"
EOF
    
    print_success "Server environment setup completed"
}

# Create systemd service for the application
create_systemd_service() {
    print_status "Creating systemd service for the application..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << EOF
        cat > /etc/systemd/system/$APP_NAME.service << 'SERVICEEOF'
[Unit]
Description=StatDevs Sales Intelligence System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
SERVICEEOF
        
        # Reload systemd and enable service
        systemctl daemon-reload
        systemctl enable $APP_NAME.service
        
        echo "Systemd service created and enabled"
EOF
    
    print_success "Systemd service created"
}

# Setup monitoring and logging
setup_monitoring() {
    print_status "Setting up monitoring and logging..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << 'EOF'
        # Create log rotation configuration
        cat > /etc/logrotate.d/statdevs-sales << 'LOGROTATEEOF'
/opt/statdevs-sales-intelligence/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
LOGROTATEEOF
        
        # Create monitoring script
        cat > /opt/statdevs-sales-intelligence/monitor.sh << 'MONITOREOF'
#!/bin/bash

# Monitor application health
APP_DIR="/opt/statdevs-sales-intelligence"
LOG_FILE="$APP_DIR/logs/monitor.log"

# Function to log with timestamp
log_with_timestamp() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

# Check if application is running
if ! curl -f http://localhost:8000/health >/dev/null 2>&1; then
    log_with_timestamp "Application health check failed, restarting..."
    cd $APP_DIR
    docker-compose restart
    log_with_timestamp "Application restarted"
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    log_with_timestamp "Disk usage is high: ${DISK_USAGE}%"
    # Clean up old Docker images
    docker image prune -f
    log_with_timestamp "Cleaned up old Docker images"
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $MEMORY_USAGE -gt 80 ]; then
    log_with_timestamp "Memory usage is high: ${MEMORY_USAGE}%"
fi
MONITOREOF
        
        chmod +x /opt/statdevs-sales-intelligence/monitor.sh
        
        # Add monitoring to crontab
        (crontab -l 2>/dev/null; echo "*/5 * * * * /opt/statdevs-sales-intelligence/monitor.sh") | crontab -
        
        echo "Monitoring setup completed"
EOF
    
    print_success "Monitoring and logging setup completed"
}

# Setup backup script
setup_backup() {
    print_status "Setting up backup system..."
    
    ssh -o StrictHostKeyChecking=no $DO_USER@$DO_HOST << 'EOF'
        # Create backup script
        cat > /opt/statdevs-sales-intelligence/backup.sh << 'BACKUPEOF'
#!/bin/bash

# Backup configuration
BACKUP_DIR="/opt/backups"
APP_DIR="/opt/statdevs-sales-intelligence"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="statdevs-sales-backup-$DATE.tar.gz"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
tar -czf $BACKUP_DIR/$BACKUP_FILE \
    --exclude='logs/*' \
    --exclude='uploads/*' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    $APP_DIR

# Keep only last 7 days of backups
find $BACKUP_DIR -name "statdevs-sales-backup-*.tar.gz" -mtime +7 -delete

echo "Backup created: $BACKUP_FILE"
BACKUPEOF
        
        chmod +x /opt/statdevs-sales-intelligence/backup.sh
        
        # Add backup to crontab (daily at 2 AM)
        (crontab -l 2>/dev/null; echo "0 2 * * * /opt/statdevs-sales-intelligence/backup.sh") | crontab -
        
        echo "Backup system setup completed"
EOF
    
    print_success "Backup system setup completed"
}

# Main setup function
main() {
    print_status "Starting Digital Ocean server setup..."
    
    # Setup server environment
    setup_server
    
    # Create systemd service
    create_systemd_service
    
    # Setup monitoring
    setup_monitoring
    
    # Setup backup
    setup_backup
    
    print_success "Digital Ocean server setup completed!"
    echo ""
    echo "🎉 Server is ready for deployment!"
    echo "📋 Next steps:"
    echo "  1. Set up your environment variables"
    echo "  2. Run the deployment script: ./deploy-digitalocean.sh"
    echo "  3. Or use GitHub Actions for automated deployment"
    echo ""
    echo "🔧 Server features configured:"
    echo "  - Docker and Docker Compose"
    echo "  - Nginx reverse proxy"
    echo "  - SSL support with Let's Encrypt"
    echo "  - Firewall configuration"
    echo "  - Monitoring and health checks"
    echo "  - Automated backups"
    echo "  - Log rotation"
    echo ""
    echo "🌐 Your server is ready at: $DO_HOST"
}

# Run main function
main "$@"



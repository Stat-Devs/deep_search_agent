# StatDevs Sales Intelligence System - Digital Ocean Deployment Guide

This guide will help you deploy your StatDevs Sales Intelligence System to Digital Ocean using GitHub CI/CD pipeline.

## 🚀 Quick Start

1. **Setup Digital Ocean Server** (One-time setup)
2. **Configure GitHub Secrets** (One-time setup)
3. **Deploy via GitHub Actions** (Automatic on every commit)

## 📋 Prerequisites

- Digital Ocean server with root access
- GitHub repository
- Required API keys (OpenAI, Gemini, Tavily)

## 🔧 Step 1: Digital Ocean Server Setup

### Option A: Automated Setup (Recommended)
```bash
# Run the automated setup script
./setup-digitalocean.sh
```

### Option B: Manual Setup
```bash
# SSH into your Digital Ocean server
ssh root@143.110.183.47

# Update system
apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Nginx
apt-get install -y nginx

# Configure firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw allow 8000
ufw --force enable

# Create application directory
mkdir -p /opt/statdevs-sales-intelligence
```

## 🔐 Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

### Required Secrets

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `DO_HOST` | `143.110.183.47` | Digital Ocean server IP |
| `DO_USERNAME` | `root` | Server username |
| `DO_SSH_KEY` | `[Your private SSH key]` | Private SSH key for server access |
| `OPENAI_API_KEY` | `[Your OpenAI API key]` | OpenAI API key |
| `GEMINI_API_KEY` | `[Your Gemini API key]` | Google Gemini API key |
| `TAVILY_API_KEY` | `[Your Tavily API key]` | Tavily API key |

### How to get your SSH key:

1. **Generate SSH key pair** (if you don't have one):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

2. **Copy your private key**:
   ```bash
   cat ~/.ssh/id_rsa
   ```
   Copy the entire output and paste it as the `DO_SSH_KEY` secret.

3. **Add public key to Digital Ocean server**:
   ```bash
   ssh-copy-id root@143.110.183.47
   ```
   Or manually add it:
   ```bash
   ssh root@143.110.183.47
   echo "your_public_key_here" >> ~/.ssh/authorized_keys
   ```

## 🚀 Step 3: Deploy via GitHub Actions

### Automatic Deployment
Every time you push to the `main` branch, GitHub Actions will:
1. Run tests
2. Build Docker image
3. Deploy to Digital Ocean server
4. Start the application

### Manual Deployment
```bash
# Push your changes to trigger deployment
git add .
git commit -m "Deploy to Digital Ocean"
git push origin main
```

### Monitor Deployment
- **GitHub Actions**: Go to your repository → Actions tab
- **Server Logs**: `ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose logs -f'`

## 🌐 Step 4: Access Your Application

After successful deployment, your application will be available at:
- **Direct access**: http://143.110.183.47:8000
- **Via Nginx** (if configured): http://143.110.183.47

## 🔧 Step 5: Optional Configurations

### Custom Domain Setup
1. **Point your domain to the server IP**:
   ```
   A record: your-domain.com → 143.110.183.47
   ```

2. **Setup SSL with Let's Encrypt**:
   ```bash
   ssh root@143.110.183.47
   certbot --nginx -d your-domain.com
   ```

3. **Update Nginx configuration**:
   ```bash
   # Edit nginx config
   nano /etc/nginx/sites-available/statdevs-sales
   
   # Update server_name
   server_name your-domain.com;
   ```

### Environment Variables
The following environment variables are automatically set:
- `OPENAI_API_KEY`: Your OpenAI API key
- `GEMINI_API_KEY`: Your Gemini API key
- `TAVILY_API_KEY`: Your Tavily API key
- `OPENAI_TRACE`: Set to 1 for tracing
- `PYTHONPATH`: Set to /app

## 📊 Monitoring and Maintenance

### Health Checks
The application includes automatic health checks:
- **Docker health check**: Every 30 seconds
- **Application monitoring**: Every 5 minutes
- **Log rotation**: Daily

### Useful Commands

```bash
# View application logs
ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose logs -f'

# Restart application
ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose restart'

# Check application status
ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose ps'

# Update application
# Just push to GitHub - deployment is automatic!

# Stop application
ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose down'

# View system resources
ssh root@143.110.183.47 'htop'
```

### Backup System
Automatic backups are configured:
- **Daily backups** at 2 AM
- **7-day retention** policy
- **Backup location**: `/opt/backups/`

## 🚨 Troubleshooting

### Common Issues

1. **Deployment fails with SSH error**:
   - Check if SSH key is correctly set in GitHub secrets
   - Verify server is accessible: `ssh root@143.110.183.47`

2. **Application not starting**:
   - Check logs: `docker-compose logs`
   - Verify environment variables are set
   - Check if port 8000 is available

3. **Health check failing**:
   - Application might be starting slowly
   - Check if all dependencies are installed
   - Verify API keys are valid

4. **Out of disk space**:
   - Clean up old Docker images: `docker image prune -f`
   - Check backup retention policy

### Debug Commands

```bash
# Check Docker status
ssh root@143.110.183.47 'systemctl status docker'

# Check application logs
ssh root@143.110.183.47 'cd /opt/statdevs-sales-intelligence && docker-compose logs --tail=100'

# Check system resources
ssh root@143.110.183.47 'df -h && free -h'

# Test application health
ssh root@143.110.183.47 'curl -f http://localhost:8000/health'
```

## 📞 Support

If you encounter any issues:
1. Check the GitHub Actions logs
2. Review server logs
3. Contact StatDevs team at info@statdevs.com

## 🎉 Success!

Once deployed, your StatDevs Sales Intelligence System will be:
- ✅ Automatically deployed on every commit
- ✅ Monitored with health checks
- ✅ Backed up daily
- ✅ Accessible at http://143.110.183.47:8000
- ✅ Ready for production use

---

**Note**: This deployment guide is integrated into the existing documentation as per your preferences. The system is now ready for automated deployment to Digital Ocean via GitHub CI/CD pipeline.



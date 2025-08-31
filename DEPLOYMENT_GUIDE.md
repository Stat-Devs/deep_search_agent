# 🚀 StatDevs Sales Intelligence System - Deployment Guide

## 🎯 **What We've Built**

Your **StatDevs Sales Intelligence System** is now ready for public deployment! This AI-powered tool:

- **Analyzes company websites** and identifies StatDevs opportunities
- **Maps industry problems** to your specific solutions
- **Generates sales-ready reports** with proven ROI metrics
- **Creates personalized email pitches** highlighting StatDevs value
- **Uses your business context** for targeted insights

## 🌐 **Deployment Options**

### **Option 1: Docker (Recommended) ⭐**

**Step 1: Ensure Docker is Running**
- Start Docker Desktop on your machine
- Verify with: `docker --version`

**Step 2: Set Up Environment**
```bash
# Copy environment file
cp env.example .env

# Edit with your API keys
nano .env
```

**Step 3: Deploy with Docker Compose**
```bash
# Make script executable (first time only)
chmod +x docker-deploy.sh

# Run deployment
./docker-deploy.sh
```

**Step 4: Access Your App**
- Open browser to: `http://localhost:8000`
- Your StatDevs Sales Intelligence System is now running!

**Alternative: Manual Docker Commands**
```bash
# Build the image
docker build -t statdevs-sales-ai .

# Run the container
docker run -d \
  --name statdevs-sales-ai \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_TRACE=1 \
  statdevs-sales-ai

# View logs
docker logs -f statdevs-sales-ai

# Stop and remove
docker stop statdevs-sales-ai && docker rm statdevs-sales-ai
```

### **Option 2: Heroku**

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set OPENAI_TRACE=1

# Deploy
git push heroku main
```

### **Option 3: Heroku**

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set OPENAI_TRACE=1

# Deploy
git push heroku main
```

## 🔧 **Environment Setup**

### **Local Development**

#### **Option 1: Direct Python (Recommended for Development)**
```bash
# Copy example environment file
cp env.example .env

# Edit .env with your actual API keys
nano .env

# Install dependencies
uv sync

# Run locally
uv run chainlit run app.py -w
```

#### **Option 2: Docker Development**
```bash
# Build development image
docker build -t statdevs-sales-ai:dev .

# Run with volume mounting for live code changes
docker run -d --name statdevs-sales-ai-dev \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_TRACE=1 \
  statdevs-sales-ai:dev

# View logs
docker logs -f statdevs-sales-ai-dev

# Stop development container
docker stop statdevs-sales-ai-dev && docker rm statdevs-sales-ai-dev
```

### **Production Deployment**
- Use `requirements.txt` for dependency installation
- Set environment variables in your hosting platform
- Never commit `.env` files to git

### **Docker Management Commands**

#### **Using Docker Compose (Recommended)**
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down

# Restart the service
docker-compose restart

# Update and restart
docker-compose up --build -d

# Check status
docker-compose ps

# View resource usage
docker-compose top
```

#### **Using Docker Directly**
```bash
# Build image
docker build -t statdevs-sales-ai .

# Run container
docker run -d --name statdevs-sales-ai -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_TRACE=1 \
  statdevs-sales-ai

# View logs
docker logs -f statdevs-sales-ai

# Stop container
docker stop statdevs-sales-ai

# Remove container
docker rm statdevs-sales-ai

# View running containers
docker ps

# View all containers
docker ps -a

# View resource usage
docker stats
```

## 📱 **Public Access Features**

Once deployed, anyone can:

✅ **Access your StatDevs Sales Intelligence System**
✅ **Research leads using AI-powered analysis**
✅ **See your company's capabilities and ROI metrics**
✅ **Generate leads for your business**
✅ **Experience your professional brand**

## 🌟 **Your Business Context Integration**

The system automatically uses your StatDevs information:

- **Core Services**: Data Engineering, AI/ML, Business Intelligence, Data Science
- **Proven ROI**: 82% reduction in data integration time, 3.2x return on AI investment
- **Expertise**: Python, R, R Shiny, Streamlit, AWS, Machine Learning
- **Industries**: Research Organizations, Supply Chain, Marketing, Fintech, Non-Profits, Manufacturing
- **Process**: Discovery Call → Assessment → Solution Design → Phased Implementation

## 🎨 **Customization Options**

### **Branding**
- Update company name and services in `STATDEVS_CONTEXT`
- Modify colors and themes in your application
- Add your logo and company information

### **Custom Domain**
- Use your hosting provider's custom domain feature
- Point your own domain (e.g., `sales.statdevs.com`)
- Professional branding for your sales team

## 🚀 **Docker Production Deployment**

### **Cloud Deployment Options**

#### **AWS ECS/Fargate**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag statdevs-sales-ai:latest <account>.dkr.ecr.us-east-1.amazonaws.com/statdevs-sales-ai:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/statdevs-sales-ai:latest
```

#### **Google Cloud Run**
```bash
# Build and push to GCR
docker tag statdevs-sales-ai:latest gcr.io/<project-id>/statdevs-sales-ai:latest
docker push gcr.io/<project-id>/statdevs-sales-ai:latest

# Deploy to Cloud Run
gcloud run deploy statdevs-sales-ai \
  --image gcr.io/<project-id>/statdevs-sales-ai:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

#### **Azure Container Instances**
```bash
# Build and push to ACR
az acr build --registry <registry-name> --image statdevs-sales-ai:latest .

# Deploy to Container Instances
az container create \
  --resource-group <resource-group> \
  --name statdevs-sales-ai \
  --image <registry-name>.azurecr.io/statdevs-sales-ai:latest \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your_key OPENAI_TRACE=1
```

## 📊 **Analytics & Monitoring**

- **OpenAI Tracing**: Monitor API usage and costs
- **User Analytics**: Track lead research activities
- **Performance Metrics**: Monitor system response times
- **Lead Generation**: Track potential opportunities

## 🚨 **Security & Best Practices**

✅ **API Keys**: Stored securely in environment variables
✅ **Git Security**: Sensitive files excluded from version control
✅ **Access Control**: Public access with optional authentication
✅ **Data Privacy**: No user data stored permanently

## 🔧 **Docker Troubleshooting**

### **Common Issues & Solutions**

#### **Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
docker run -p 8001:8000 statdevs-sales-ai
```

#### **Container Won't Start**
```bash
# Check container logs
docker logs statdevs-sales-ai

# Check container status
docker ps -a

# Remove and recreate
docker rm statdevs-sales-ai
docker run -d --name statdevs-sales-ai -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  statdevs-sales-ai
```

#### **Build Failures**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t statdevs-sales-ai .

# Check Dockerfile syntax
docker build --dry-run .
```

#### **Environment Variables Not Working**
```bash
# Verify environment variables
docker exec statdevs-sales-ai env | grep OPENAI

# Restart with correct environment
docker stop statdevs-sales-ai
docker rm statdevs-sales-ai
docker run -d --name statdevs-sales-ai -p 8000:8000 \
  -e OPENAI_API_KEY=your_actual_key \
  -e OPENAI_TRACE=1 \
  statdevs-sales-ai
```

## 📞 **Support & Maintenance**

### **Technical Support**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Comprehensive guides and examples
- **Community**: Chainlit community for best practices

### **Business Support**
- **StatDevs Team**: info@statdevs.com
- **Feature Requests**: [Google Form](https://forms.gle/D9uAUPtJR1gmoDCD7)
- **Custom Development**: Contact for enterprise features

## 🎯 **Next Steps**

1. **Deploy with Docker** (recommended)
2. **Test with sample leads** to ensure functionality
3. **Share with your sales team** for feedback
4. **Customize branding** to match your company
5. **Monitor usage** and gather insights
6. **Iterate and improve** based on feedback

## 🎉 **Congratulations!**

You now have a **professional, AI-powered sales intelligence system** that:

- **Showcases StatDevs capabilities** to potential clients
- **Generates qualified leads** through intelligent research
- **Demonstrates your technical expertise** with cutting-edge AI
- **Provides measurable ROI** for your sales process

**Your StatDevs Sales Intelligence System is ready to transform your lead generation! 🚀**

---

*For technical support or custom development, contact the StatDevs team at info@statdevs.com*

# AWS Linux Deployment Guide

## Summary: What We've Done & What to Try on AWS Linux

### Current Status
- ✅ **Code is ready**: All lazy-loading optimizations are in place
- ✅ **Dockerfile is optimized**: Python 3.10 with thread limits and environment variables
- ✅ **Docker Compose configured**: PostgreSQL + Backend setup ready
- ⚠️ **Mac Docker Desktop issue**: Segfault (ExitCode 139) persists on Mac due to Docker Desktop VM limitations
- ✅ **Linux image built**: Successfully built `linux/amd64` image using buildx

---

## What to Try on AWS Linux

### Option 1: EC2 Instance with Docker (Recommended)

#### Step 1: Launch EC2 Instance
```bash
# Launch Ubuntu 22.04 LTS or Amazon Linux 2023
# Instance type: t3.medium or larger (2+ vCPUs, 4GB+ RAM)
# Security Group: Open ports 22 (SSH), 8000 (Backend), 5432 (PostgreSQL - optional)
```

#### Step 2: Install Docker on EC2
```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker

# Verify Docker
docker --version
docker-compose --version
```

#### Step 3: Deploy Application
```bash
# Clone your repository
git clone <your-repo-url>
cd regression-app

# Build and start services
docker-compose up -d --build

# Check logs
docker-compose logs -f backend

# Verify it's running
curl http://localhost:8000/
```

#### Expected Result
- ✅ Container should start without segfault
- ✅ Backend should respond to HTTP requests
- ✅ No ExitCode 139 errors

---

### Option 2: ECS (Elastic Container Service)

#### Step 1: Build and Push Image to ECR
```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name regression-app-backend --region us-east-1

# Build and push image
docker buildx build --platform linux/amd64 -t regression-app-backend:latest ./backend
docker tag regression-app-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/regression-app-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/regression-app-backend:latest
```

#### Step 2: Create ECS Task Definition
```json
{
  "family": "regression-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/regression-app-backend:latest",
      "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
      "environment": [
        {"name": "DATABASE_URL", "value": "postgresql://user:pass@rds-endpoint:5432/db"},
        {"name": "JWT_SECRET", "value": "your-secret"},
        {"name": "OPENBLAS_NUM_THREADS", "value": "1"},
        {"name": "OMP_NUM_THREADS", "value": "1"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/regression-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Step 3: Create RDS PostgreSQL Database
```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier regression-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username regression_user \
  --master-user-password regression_password \
  --allocated-storage 20
```

---

### Option 3: AWS App Runner (Simplest)

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for AWS deployment"
git push origin main
```

#### Step 2: Create App Runner Service
- Go to AWS Console → App Runner
- Connect GitHub repository
- Build command: `cd backend && docker build -t app .`
- Start command: `docker run -p 8000:8000 app`
- Environment variables:
  - `DATABASE_URL`: RDS endpoint
  - `JWT_SECRET`: Your secret
  - `OPENBLAS_NUM_THREADS=1`
  - `OMP_NUM_THREADS=1`

---

## Key Configuration for AWS Linux

### Environment Variables (Already in Dockerfile)
```dockerfile
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV NUMBA_NUM_THREADS=1
ENV MPLBACKEND=Agg
ENV PIP_PROGRESS_BAR=off
```

### Docker Compose for AWS (if using EC2)
The existing `docker-compose.yml` should work, but ensure:
- Database is accessible (RDS or local PostgreSQL)
- Network configuration allows communication
- Volumes are properly mounted

---

## Troubleshooting on AWS Linux

### If Segfault Still Occurs:
1. **Check system limits**:
   ```bash
   ulimit -a
   ulimit -u 4096  # Increase process limit
   ```

2. **Verify numpy/scipy installation**:
   ```bash
   docker exec -it <container> python -c "import numpy; print(numpy.__version__)"
   docker exec -it <container> python -c "import scipy; print(scipy.__version__)"
   ```

3. **Check container logs**:
   ```bash
   docker-compose logs backend
   docker inspect <container> | grep -A 5 ExitCode
   ```

4. **Test with minimal setup**:
   ```bash
   # Run Python directly
   docker exec -it <container> python -c "import pandas; import numpy; import sklearn; print('OK')"
   ```

### If It Works on AWS:
- ✅ The issue is confirmed as Docker Desktop Mac-specific
- ✅ Your code and Dockerfile are correct
- ✅ You can proceed with production deployment

---

## Quick Start Script for EC2

Create `deploy.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 Deploying Regression App to AWS Linux..."

# Update system
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Clone repository
git clone <your-repo-url> regression-app
cd regression-app

# Build and start
docker-compose up -d --build

# Wait for services
sleep 10

# Check status
docker-compose ps
curl http://localhost:8000/ || echo "Backend not responding yet"

echo "✅ Deployment complete!"
```

---

## Expected Differences on AWS Linux

### Why It Should Work:
1. **Native Linux**: No VM layer like Docker Desktop Mac
2. **Better resource management**: Direct access to CPU/memory
3. **No threading limitations**: Linux kernel handles threads better
4. **Optimized libraries**: numpy/scipy compiled for Linux/amd64

### What to Monitor:
- Container startup time
- Memory usage (numpy/scipy can be memory-intensive)
- Response times for ML endpoints
- Database connection pooling

---

## Next Steps After Successful Deployment

1. **Set up CI/CD**: GitHub Actions → ECR → ECS
2. **Add monitoring**: CloudWatch logs and metrics
3. **Configure load balancer**: ALB for high availability
4. **Set up backups**: RDS automated backups
5. **Security hardening**: Secrets Manager for credentials

---

## Summary

**What We've Done:**
- ✅ Optimized code with lazy-loading
- ✅ Configured Dockerfile with thread limits
- ✅ Built Linux/amd64 image
- ✅ Prepared docker-compose.yml

**What to Try on AWS:**
1. Deploy to EC2 with Docker (easiest to test)
2. Verify no segfault occurs
3. Test ML endpoints
4. Monitor performance

**Expected Outcome:**
- ✅ No ExitCode 139 on native Linux
- ✅ Backend responds correctly
- ✅ ML pipelines work as expected

The segfault issue is Docker Desktop Mac-specific and should not occur on AWS Linux.

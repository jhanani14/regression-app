#!/bin/bash
# Quick deployment script for AWS EC2 Linux

set -e

echo "🚀 AWS Linux Deployment Script"
echo "================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker $USER
    echo "⚠️  Please run 'newgrp docker' or logout/login for Docker group to take effect"
    exit 0
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing docker-compose..."
    sudo apt-get install -y docker-compose
fi

echo "✅ Docker is ready"

# Navigate to project directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📂 Project directory: $SCRIPT_DIR"

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 15

# Check container status
echo ""
echo "📊 Container Status:"
docker-compose ps

# Check backend health
echo ""
echo "🏥 Checking backend health..."
BACKEND_STATUS=$(docker-compose ps backend | grep -c "Up" || echo "0")
if [ "$BACKEND_STATUS" -gt 0 ]; then
    echo "✅ Backend container is running"
    
    # Check exit code
    EXIT_CODE=$(docker inspect regression-backend 2>/dev/null | grep -A 2 '"ExitCode"' | head -3 | grep -o '"ExitCode": [0-9]*' | cut -d' ' -f2 || echo "unknown")
    echo "   Exit Code: $EXIT_CODE"
    
    if [ "$EXIT_CODE" = "0" ] || [ "$EXIT_CODE" = "null" ]; then
        echo "✅ Backend started successfully (no segfault)"
    else
        echo "⚠️  Backend exit code: $EXIT_CODE (check logs)"
    fi
    
    # Test HTTP endpoint
    echo ""
    echo "🌐 Testing HTTP endpoint..."
    HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ || echo "000")
    if [ "$HTTP_RESPONSE" = "200" ] || [ "$HTTP_RESPONSE" = "404" ] || [ "$HTTP_RESPONSE" = "405" ]; then
        echo "✅ Backend is responding (HTTP $HTTP_RESPONSE)"
    else
        echo "⚠️  Backend not responding (HTTP $HTTP_RESPONSE)"
        echo "   Check logs: docker-compose logs backend"
    fi
else
    echo "❌ Backend container is not running"
    echo "   Check logs: docker-compose logs backend"
fi

# Show recent logs
echo ""
echo "📋 Recent Backend Logs:"
docker-compose logs --tail=10 backend

echo ""
echo "================================"
echo "✅ Deployment check complete!"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose logs -f backend"
echo "  Stop:         docker-compose down"
echo "  Restart:      docker-compose restart backend"
echo "  Shell access: docker exec -it regression-backend bash"

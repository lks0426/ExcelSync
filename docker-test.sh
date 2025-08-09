#!/bin/bash

# ExcelSync Docker Test Script
echo "🚀 Starting ExcelSync Docker Test..."

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v --remove-orphans

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Test backend health
echo "🏥 Testing backend health..."
backend_health=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health)
if [ "$backend_health" = "200" ]; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed (HTTP $backend_health)"
fi

# Test frontend 
echo "🌐 Testing frontend..."
frontend_health=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$frontend_health" = "200" ]; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed (HTTP $frontend_health)"
fi

# Show container status
echo "📊 Container Status:"
docker-compose ps

# Show logs if there are any errors
if [ "$backend_health" != "200" ] || [ "$frontend_health" != "200" ]; then
    echo "📋 Recent logs:"
    docker-compose logs --tail=10
fi

echo "🎉 Docker test completed!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000/api/health"
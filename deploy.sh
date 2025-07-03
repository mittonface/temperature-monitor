#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with the following variables:"
    echo "  FLASK_SECRET_KEY=your-secret-key"
    echo "  NEST_CLIENT_ID=your-nest-client-id"
    echo "  NEST_CLIENT_SECRET=your-nest-client-secret"
    echo "  NEST_REFRESH_TOKEN=your-nest-refresh-token"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Validate required environment variables
required_vars=("FLASK_SECRET_KEY" "NEST_CLIENT_ID" "NEST_CLIENT_SECRET" "NEST_REFRESH_TOKEN")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var is not set in .env file!"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --timeout 30

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo "✅ Deployment completed!"
echo ""
echo "🌐 Your application should be accessible at:"
echo "   Local: http://localhost:5001"
echo "   Health check: http://localhost:5001/health"
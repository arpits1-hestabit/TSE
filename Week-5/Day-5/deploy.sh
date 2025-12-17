#!/bin/bash

echo "Stopping old containers..."
docker compose -f docker-compose.prod.yml down

echo "Building new images..."
docker compose -f docker-compose.prod.yml build --no-cache

echo "Starting containers..."
docker compose -f docker-compose.prod.yml up -d

echo "Deployment complete!"
docker ps
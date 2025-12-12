#!/bin/bash
# Helper script for running Playwright ScriptForge in Docker

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose is not installed${NC}"
    echo "Please install docker-compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Build image if it doesn't exist
if [[ "$(docker images -q playwright-scriptforge:latest 2> /dev/null)" == "" ]]; then
    echo -e "${BLUE}Building Playwright ScriptForge Docker image...${NC}"
    docker-compose build
fi

# Run command
echo -e "${GREEN}Running: scriptforge $@${NC}"
docker-compose run --rm scriptforge "$@"

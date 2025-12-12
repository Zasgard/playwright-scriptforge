#!/bin/bash
# Quick start script for Playwright ScriptForge

set -e

echo "🚀 Playwright ScriptForge Quick Start"
echo "======================================"
echo ""

# Check if Docker is available
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose found"
    USE_DOCKER=true
else
    echo "⚠️  Docker Compose not found, using local installation"
    USE_DOCKER=false
fi

# Function to run commands
run_cmd() {
    if [ "$USE_DOCKER" = true ]; then
        docker-compose run --rm scriptforge "$@"
    else
        python scriptforge.py "$@"
    fi
}

echo ""
echo "Step 1: Building/Installing..."
if [ "$USE_DOCKER" = true ]; then
    docker-compose build
else
    pip install -r requirements.txt
    playwright install --with-deps chromium
fi

echo ""
echo "Step 2: Validating example scripts..."
run_cmd validate examples/example_script.yaml

echo ""
echo "Step 3: Compiling example script..."
run_cmd compile examples/example_script.yaml --output /tmp/quickstart_example.py

echo ""
echo "Step 4: Converting Python example..."
run_cmd convert examples/example_codegen.py --output /tmp/quickstart_converted.yaml

echo ""
echo "✅ Quick start complete!"
echo ""
echo "📚 Next steps:"
echo "   - Check the compiled script: /tmp/quickstart_example.py"
echo "   - Check the converted YAML: /tmp/quickstart_converted.yaml"
echo "   - Read USAGE.md for more examples"
echo "   - Run 'make help' to see all available commands"
echo ""
echo "🎯 Try recording your own session:"
if [ "$USE_DOCKER" = true ]; then
    echo "   docker-compose run scriptforge record --url https://example.com --output scripts/my_recording.py"
else
    echo "   python scriptforge.py record --url https://example.com --output scripts/my_recording.py"
fi

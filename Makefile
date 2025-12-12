.PHONY: help build run test clean install validate example

help:
	@echo "Playwright ScriptForge - Makefile Commands"
	@echo ""
	@echo "  make build        Build Docker image"
	@echo "  make test         Run tests"
	@echo "  make validate     Validate example scripts"
	@echo "  make example      Run example workflow"
	@echo "  make install      Install dependencies locally"
	@echo "  make clean        Clean generated files"
	@echo "  make help         Show this help message"

build:
	docker-compose build

run:
	docker-compose run scriptforge $(ARGS)

test:
	python test_scriptforge.py

test-docker:
	docker-compose run scriptforge python test_scriptforge.py

validate:
	python scriptforge.py validate examples/example_script.yaml
	python scriptforge.py validate examples/login_flow.yaml

example:
	@echo "Running example workflow..."
	python scriptforge.py convert examples/example_codegen.py --output /tmp/example.yaml
	python scriptforge.py compile /tmp/example.yaml --output /tmp/example_compiled.py
	@echo "Example workflow complete! Check /tmp/example_compiled.py"

install:
	pip install -r requirements.txt
	playwright install --with-deps chromium firefox webkit

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf *.pyc
	rm -rf output/*.png
	rm -rf /tmp/test_*.py /tmp/test_*.yaml

docker-clean:
	docker-compose down
	docker system prune -f

# Makefile for Bewerbung Generator

.PHONY: test_1 test_2 test_3 test_4 test install clean venv generate

# Create virtual environment if it doesn't exist
venv:
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		python3.12 -m venv .venv; \
		. .venv/bin/activate && pip install --upgrade pip; \
	fi

# Test Step 1: Profile reading functionality
test_1: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python -m pytest tests/test_step1.py -v; \
	else \
		python -m pytest tests/test_step1.py -v; \
	fi

# Test Step 2: Job description reading functionality
test_2: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python -m pytest tests/test_step2.py -v; \
	else \
		python -m pytest tests/test_step2.py -v; \
	fi

# Test Step 3: Output directory creation functionality
test_3: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python -m pytest tests/test_step3.py -v; \
	else \
		python -m pytest tests/test_step3.py -v; \
	fi

# Test Step 4: Template system and PDF generation
test_4: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python -m pytest tests/test_template_system.py -v; \
	else \
		python -m pytest tests/test_template_system.py -v; \
	fi

# Run all tests
test: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python -m pytest tests/ -v; \
	else \
		python -m pytest tests/ -v; \
	fi

# Install dependencies
install: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and installing dependencies..."; \
		. .venv/bin/activate && pip install -r requirements.txt; \
	else \
		pip install -r requirements.txt; \
	fi

# Generate application documents using the complete workflow
generate: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python src/bewerbung_generator.py; \
	else \
		python src/bewerbung_generator.py; \
	fi

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

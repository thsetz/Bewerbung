# Makefile for Bewerbung Generator

.PHONY: test_1 test_2 test_3 test_4 test test_memory test-coverage coverage-report coverage-xml coverage-clean install clean venv generate variants variants-detailed docs docs-pdf docs-clean docs-serve docs-check docs-all clear-cache generate-fresh generate-cached cache-status test-documentation-generator test-version-management release-major release-minor release-patch test-make-release test-links analyze-links

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

# Test memory usage stability
test_memory: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && python -m pytest tests/test_performance_requirements.py::TestPerformanceRequirements::test_memory_usage_stability -v; \
	else \
		python -m pytest tests/test_performance_requirements.py::TestPerformanceRequirements::test_memory_usage_stability -v; \
	fi

# Run performance tests separately
test-performance: venv
	@echo "⚡ Running performance tests..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/ -v -m "performance"; \
	else \
		python -m pytest tests/ -v -m "performance"; \
	fi

# Test content variants analyzer
test-variants: venv
	@echo "🔍 Running content variants analyzer tests..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/test_content_variants_analyzer.py -v; \
	else \
		python -m pytest tests/test_content_variants_analyzer.py -v; \
	fi

# Test documentation generator
test-documentation-generator: venv
	@echo "📚 Running documentation generator tests..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/test_documentation_generator.py -v; \
	else \
		python -m pytest tests/test_documentation_generator.py -v; \
	fi

# Test version management strategy
test-version-management: venv
	@echo "🏷️  Running version management tests..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/test_version_management.py -v; \
	else \
		python -m pytest tests/test_version_management.py -v; \
	fi

# Release management targets
release-major: venv
	@echo "🚀 Creating major release (X.0.0)..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python src/make_release.py major; \
	else \
		python src/make_release.py major; \
	fi

release-minor: venv
	@echo "🚀 Creating minor release (x.X.0)..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python src/make_release.py minor; \
	else \
		python src/make_release.py minor; \
	fi

release-patch: venv
	@echo "🚀 Creating patch release (x.x.X)..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python src/make_release.py patch; \
	else \
		python src/make_release.py patch; \
	fi

# Test release management script
test-make-release: venv
	@echo "🚀 Running release management tests..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/test_make_release.py -v; \
	else \
		python -m pytest tests/test_make_release.py -v; \
	fi

# Test documentation links validation
test-links: venv
	@echo "🔗 Running documentation link validation tests..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/test_links_in_documentation.py -v; \
	else \
		python -m pytest tests/test_links_in_documentation.py -v; \
	fi

# Generate link analysis files (persistent output)
analyze-links: venv
	@echo "🔍 Generating persistent link analysis files..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python tests/test_links_in_documentation.py --phase both --output-dir .; \
	else \
		python tests/test_links_in_documentation.py --phase both --output-dir .; \
	fi
	@echo "📁 Generated files:"
	@echo "  - index.links (discovered links)"
	@echo "  - link_test_report.json (validation results)"

# Run tests with coverage collection (excluding performance tests)
test-coverage: venv
	@echo "🧪 Running tests with coverage collection..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml -v -m "not performance"; \
	else \
		python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml -v -m "not performance"; \
	fi
	@echo "📊 Coverage reports generated:"
	@echo "  - HTML: docs/_static/coverage/index.html"
	@echo "  - XML: coverage.xml"

# Generate HTML coverage report only
coverage-report: venv
	@echo "📊 Generating HTML coverage report..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && coverage html; \
	else \
		coverage html; \
	fi
	@echo "✅ HTML coverage report: docs/_static/coverage/index.html"

# Generate XML coverage report for CI/CD
coverage-xml: venv
	@echo "📄 Generating XML coverage report..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && coverage xml; \
	else \
		coverage xml; \
	fi
	@echo "✅ XML coverage report: coverage.xml"

# Clean coverage data files
coverage-clean:
	@echo "🗑️ Cleaning coverage data files..."
	@rm -f .coverage coverage.xml
	@rm -rf docs/_static/coverage/
	@echo "✅ Coverage files cleaned"

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

# AI Provider Management
test-providers: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and testing AI providers..."; \
		. .venv/bin/activate && cd src && python -c "import sys; sys.path.append('.'); from ai_client_factory import AIClientFactory; f = AIClientFactory(); print('Available providers:', f.get_available_providers()); results = f.test_all_providers(); [print(f'{'✅' if r[\"available\"] else '❌'} {p}: available={r[\"available\"]}, test_passed={r[\"test_passed\"]}') for p, r in results.items()]"; \
	else \
		cd src && python -c "import sys; sys.path.append('.'); from ai_client_factory import AIClientFactory; f = AIClientFactory(); print('Available providers:', f.get_available_providers()); results = f.test_all_providers(); [print(f'{'✅' if r[\"available\"] else '❌'} {p}: available={r[\"available\"]}, test_passed={r[\"test_passed\"]}') for p, r in results.items()]"; \
	fi

# Ollama setup and management
check-ollama:
	@echo "Checking Ollama installation..."
	@if command -v ollama >/dev/null 2>&1; then \
		echo "✅ Ollama is installed"; \
		if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then \
			echo "✅ Ollama is running"; \
		else \
			echo "❌ Ollama is not running. Start with: ollama serve"; \
		fi \
	else \
		echo "❌ Ollama not found. Install from: https://ollama.ai/"; \
	fi

install-llama-model:
	@echo "Installing recommended Llama model..."
	@if command -v ollama >/dev/null 2>&1; then \
		ollama pull llama3.2:3b; \
	else \
		echo "❌ Ollama not found. Please install Ollama first."; \
	fi

setup-ollama: check-ollama install-llama-model
	@echo "Ollama setup complete!"

# Test regeneration scripts
test-regeneration: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and testing regeneration scripts..."; \
		. .venv/bin/activate && python tests/test_regeneration.py --mode=content; \
	else \
		python tests/test_regeneration.py --mode=content; \
	fi

# Test regeneration with all AI providers
test-regeneration-all: venv
	@echo "🧪 Testing regeneration across all AI providers..."
	@for provider in claude llama sample; do \
		echo "Testing $$provider provider..."; \
		if [ -z "$$VIRTUAL_ENV" ]; then \
			. .venv/bin/activate && AI_PROVIDER=$$provider OUTPUT_STRUCTURE=by_model GENERATE_DOCUMENTATION=true make generate && python tests/test_regeneration.py --mode=content; \
		else \
			AI_PROVIDER=$$provider OUTPUT_STRUCTURE=by_model GENERATE_DOCUMENTATION=true make generate && python tests/test_regeneration.py --mode=content; \
		fi; \
	done

# Quick regeneration test (structure only)
test-regeneration-quick: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Running quick regeneration test..."; \
		. .venv/bin/activate && python tests/test_regeneration.py --mode=structure --timeout=60; \
	else \
		python tests/test_regeneration.py --mode=structure --timeout=60; \
	fi

# Generate with documentation and test regeneration
generate-and-test: venv
	@echo "🚀 Generating application with documentation and testing regeneration..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && OUTPUT_STRUCTURE=by_model GENERATE_DOCUMENTATION=true INCLUDE_GENERATION_METADATA=true make generate && python tests/test_regeneration.py --mode=content; \
	else \
		OUTPUT_STRUCTURE=by_model GENERATE_DOCUMENTATION=true INCLUDE_GENERATION_METADATA=true make generate && python tests/test_regeneration.py --mode=content; \
	fi

# Analyze content variants across different AI client/model combinations
variants: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and analyzing content variants..."; \
		. .venv/bin/activate && python src/content_variants_analyzer.py; \
	else \
		python src/content_variants_analyzer.py; \
	fi

# Analyze content variants with detailed content comparison
variants-detailed: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and analyzing content variants (detailed)..."; \
		. .venv/bin/activate && python src/content_variants_analyzer.py --content; \
	else \
		python src/content_variants_analyzer.py --content; \
	fi

# Build Sphinx documentation
docs: venv
	@echo "📚 Building documentation with version verification..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and building documentation..."; \
		. .venv/bin/activate && python -c "from src import get_version; print(f'📋 Building docs for version: {get_version()}')" && cd docs && make html; \
	else \
		python -c "from src import get_version; print(f'📋 Building docs for version: {get_version()}')" && cd docs && make html; \
	fi
	@echo "📚 Documentation built successfully!"
	@echo "📁 Open: docs/_build/html/index.html"

# Build PDF documentation
docs-pdf: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment and building PDF documentation..."; \
		. .venv/bin/activate && cd docs && make latexpdf; \
	else \
		cd docs && make latexpdf; \
	fi

# Clean documentation build files
docs-clean:
	@echo "Cleaning documentation build files..."
	@cd docs && make clean

# Serve documentation locally
docs-serve: docs
	@echo "🌐 Starting documentation server..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. .venv/bin/activate && python -m http.server 8000 --directory docs/_build/html; \
	else \
		python -m http.server 8000 --directory docs/_build/html; \
	fi

# Check documentation for broken links and issues
docs-check: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Checking documentation for issues..."; \
		. .venv/bin/activate && cd docs && make linkcheck; \
	else \
		cd docs && make linkcheck; \
	fi

# Build all documentation formats
docs-all: docs docs-pdf
	@echo "📚 All documentation formats built successfully!"

# Clear AI content cache manually
clear-cache:
	@echo "🗑️ Clearing AI content cache..."
	@rm -f .cache/ai_content_cache.json
	@echo "✅ AI content cache cleared"

# Generate application with fresh content (no cache)
generate-fresh: clear-cache generate
	@echo "✅ Fresh application generation completed!"

# Generate application preserving existing cache
generate-cached: 
	@echo "🚀 Generating application with cache preservation..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Activating virtual environment..."; \
		. .venv/bin/activate && CLEAR_CACHE_ON_START=false python src/bewerbung_generator.py; \
	else \
		CLEAR_CACHE_ON_START=false python src/bewerbung_generator.py; \
	fi

# Show cache status and statistics
cache-status:
	@echo "📊 AI Content Cache Status:"
	@if [ -f ".cache/ai_content_cache.json" ]; then \
		echo "✅ Cache file exists: .cache/ai_content_cache.json"; \
		echo "📏 Cache file size: $$(du -h .cache/ai_content_cache.json | cut -f1)"; \
		echo "📅 Last modified: $$(date -r .cache/ai_content_cache.json)"; \
		echo "🔢 Cache entries: $$(python -c "import json; print(len(json.load(open('.cache/ai_content_cache.json'))))" 2>/dev/null || echo "Error reading cache")"; \
	else \
		echo "❌ No cache file found"; \
	fi

# Clean up temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

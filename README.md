# Bewerbung Generator

**Professional Application Document Generator with AI Support**

An intelligent system for generating customized job application documents (cover letters, CVs, and attachments) using AI providers with automatic fallback mechanisms.


## 🚀 Quick Start

```bash
# Install dependencies
make install

# Generate application documents
make generate

# View documentation
make docs && make docs-serve
```

## 📋 Application Components

A complete application (Bewerbung) consists of:

- **Anschreiben** (Cover Letter) - AI-generated, personalized content
- **Lebenslauf** (CV/Resume) - Professional formatted resume
- **Anlagen** (Attachments) - Supporting documents
  - Certificates (Zeugnisse)
  - References (Referenzen) 
  - Additional documents


## 🔄 Generation Workflow

The application generation follows a structured 7-step process:

📊 **[🔗 View Interactive System Workflow Diagram →](docs/diagrams/system-workflow.html)**

### Detailed Steps

0. **🗑️ AI Cache Clearing** - Clears existing AI content cache (`.cache/ai_content_cache.json`) to ensure fresh content generation
1. **📁 Profile Reading** - Discovers and reads the newest profile file (pattern: `YYYYMMDD.*`) from `profil/` directory
2. **📄 Job Description Reading** - Reads the newest job description (pattern: `YYYYMMDD.*`) from `Stellenbeschreibung/` directory  
3. **📂 Output Directory Creation** - Creates structured output directory: `Ausgabe/{job_date}_{job_name}-{profile_date}_{profile_name}/`
4. **🤖 AI Content Generation** - Generates personalized content using AI provider chain (Llama → Claude → Sample fallback) with fresh, non-cached content
5. **📁 PDF Directory Setup** - Creates `/pdf` subdirectory for converted documents
6. **📄 PDF Conversion** - Converts all markdown documents to professional PDF format




## 🤖 AI Provider Support

📊 **[🔗 View AI Provider Selection Diagram →](docs/diagrams/ai-provider-selection.html)**

## 🏗️ Directory-Only Output Structure

The generator uses a **clean directory-only structure** for organized output:

📊 **[🔗 View Directory Structure Diagram →](docs/diagrams/directory-structure.html)**

**Key Features:**
- **No Root Files**: All documents are contained within AI provider subdirectories
- **Clean Organization**: Each AI provider gets its own folder (e.g., `sample_content/`, `claude_sonnet_3_5/`)
- **Easy Comparison**: Compare outputs from different AI providers side-by-side
- **Self-Contained**: Each folder includes provider-specific documentation and PDFs

## 🛠️ System Requirements

### Dependencies
```bash
# macOS
brew install cffi fonttools pango pillow six

# Install ripgrep for fast code searching
brew install ripgrep

# Install Python dependencies
make install
```

### AI Provider Setup

**Option 1: Llama/Ollama (Recommended - Local & Private)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Setup Llama model
make setup-ollama
```

**Option 2: Claude API**
```bash
# Set API key
export ANTHROPIC_API_KEY="your-api-key"
```

## 🗑️ Cache Management

The system automatically clears AI content cache before each generation to ensure fresh content. You can control this behavior:

### Automatic Cache Clearing (Default)
```bash
# Normal generation - cache cleared automatically
make generate

# Explicitly generate with fresh content
make generate-fresh
```

### Cache Control Options
```bash
# Generate while preserving existing cache
make generate-cached

# Manually clear cache only
make clear-cache

# Check cache status and statistics
make cache-status

# Disable automatic cache clearing via environment variable
export CLEAR_CACHE_ON_START=false
make generate
```

### Cache File Location
- **Cache file**: `.cache/ai_content_cache.json`
- **Content**: Stores AI-generated text sections by content type
- **Behavior**: Automatically cleared on each generation for fresh content

## 📖 Documentation

### User Documentation
- **[📚 Full Documentation](docs/_build/html/index.html)** - Complete user guide and API reference
- **[🚀 Quick Start Guide](docs/user_guide/quickstart.rst)** - Get started in minutes  
- **[⚙️ Configuration](docs/user_guide/configuration.rst)** - Customize your setup
- **[🏗️ Architecture](docs/development/architecture.rst)** - System design and components

### Project Requirements
- **[📋 Project Requirements](project_requirements/project_requirements.md)** - Complete formal requirements specification
  - 25 Functional Requirements (FR-1.x through FR-5.x)
  - 20+ Non-Functional Requirements (Performance, Security, Usability, etc.)
  - Acceptance criteria and test specifications
  - Stakeholder definitions and success metrics

## 🧪 Testing & Validation

### Comprehensive Test Suite
The project includes extensive testing aligned with formal requirements:

```bash
# Run all tests
make test

# Run specific test categories
pytest tests/test_workflow_requirements.py          # FR-1.1, FR-1.2 (7-step workflow)
pytest tests/test_multi_provider_integration.py     # FR-2.1, FR-2.2 (AI providers)
pytest tests/test_directory_structure_requirements.py # FR-3.1 (directory structure)
pytest tests/test_performance_requirements.py -m performance # NFR-Perf-1 to NFR-Perf-4

# Test AI providers
make test-providers

# Test regeneration
make test-regeneration

# Analyze content variants
make variants
```

### Test Coverage

Run tests with coverage reporting:

```bash
# Run all tests with coverage collection
make test-coverage

# Generate HTML coverage report only
make coverage-report

# Generate XML coverage for CI/CD
make coverage-xml

# Clean coverage data
make coverage-clean
```

**Coverage Overview:**
- **Current Coverage**: 41% (target: 75%)
- **HTML Reports**: `docs/_static/coverage/index.html`
- **Documentation**: [Coverage Reports](docs/_build/html/testing/coverage.html)

**Test Categories:**
- **Functional Requirements**: Complete 7-step workflow, multi-provider AI support, directory structure
- **Performance Requirements**: <30s generation, 100+ apps/day, <10s AI generation, <5s PDF conversion
- **Reliability Requirements**: Graceful provider failure handling and fallback mechanisms
- **Integration Tests**: End-to-end workflow validation with real and mocked providers

### Performance Targets
- **Generation Time**: Complete application generation in <30 seconds (NFR-Perf-1)
- **Throughput**: Support 100+ applications per day (NFR-Perf-2) 
- **AI Generation**: AI content generation in <10 seconds (NFR-Perf-3)
- **PDF Conversion**: PDF conversion in <5 seconds (NFR-Perf-4)


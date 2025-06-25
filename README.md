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

The application generation follows a structured 6-step process:

```mermaid
flowchart TD
    A[📁 Step 1: Read Profile] --> B[📄 Step 2: Read Job Description]
    B --> C[📂 Step 3: Create Output Directory]
    C --> D[🤖 Step 4: Generate AI Content]
    D --> E[📁 Step 5: Create PDF Directory]
    E --> F[📄 Step 6: Convert to PDF]
    
    A1[profil/YYYYMMDD_*.pdf<br/>→ Newest file] --> A
    B1[Stellenbeschreibung/YYYYMMDD_*.txt<br/>→ Newest file] --> B
    C1[Ausgabe/DATE_job-DATE_profile/] --> C
    D1[AI Provider Chain:<br/>Llama → Claude → Sample] --> D
    E1[Create /pdf subdirectory] --> E
    F1[Markdown → HTML → PDF] --> F
    
    F --> G[✅ Complete Application Package]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#e0f2f1
    style G fill:#e8f5e8,stroke:#4caf50,stroke-width:3px
```

### Detailed Steps

1. **📁 Profile Reading** - Discovers and reads the newest profile file (pattern: `YYYYMMDD.*`) from `profil/` directory
2. **📄 Job Description Reading** - Reads the newest job description (pattern: `YYYYMMDD.*`) from `Stellenbeschreibung/` directory  
3. **📂 Output Directory Creation** - Creates structured output directory: `Ausgabe/{job_date}_{job_name}-{profile_date}_{profile_name}/`
4. **🤖 AI Content Generation** - Generates personalized content using AI provider chain (Llama → Claude → Sample fallback)
5. **📁 PDF Directory Setup** - Creates `/pdf` subdirectory for converted documents
6. **📄 PDF Conversion** - Converts all markdown documents to professional PDF format




## 🤖 AI Provider Support

```mermaid
flowchart LR
    Start([Content Request]) --> Check1{Llama/Ollama<br/>Available?}
    Check1 -->|✅ Yes| Llama[🦙 Llama/Ollama<br/>Local & Private]
    Check1 -->|❌ No| Check2{Claude API<br/>Available?}
    Check2 -->|✅ Yes| Claude[🧠 Claude API<br/>High Quality]
    Check2 -->|❌ No| Sample[📝 Sample Content<br/>Always Available]
    
    Llama --> Success[✅ Generated Content]
    Claude --> Success
    Sample --> Success
    
    style Llama fill:#e3f2fd
    style Claude fill:#f3e5f5
    style Sample fill:#fff3e0
    style Success fill:#e8f5e8
```

## 📊 Output Structure Options

```mermaid
flowchart TD
    Config[OUTPUT_STRUCTURE] --> Decision{Structure Type}
    
    Decision -->|legacy| Legacy[📁 Legacy Structure<br/>Single output directory]
    Decision -->|by_model| ByModel[📂 By-Model Structure<br/>Separate AI provider dirs]
    Decision -->|both| Both[📁📂 Both Structures<br/>Legacy + By-Model]
    
    Legacy --> LegacyOut[Ausgabe/job-profile/<br/>├── anschreiben.md<br/>├── lebenslauf.md<br/>├── anlagen.md<br/>└── pdf/]
    
    ByModel --> ModelOut[Ausgabe/job-profile/<br/>├── claude_sonnet-3-5/<br/>├── llama_3-2-latest/<br/>└── sample_content/]
    
    Both --> LegacyOut
    Both --> ModelOut
    
    style Legacy fill:#e1f5fe
    style ByModel fill:#f3e5f5
    style Both fill:#e8f5e8
```

## 🛠️ System Requirements

### Dependencies
```bash
# macOS
brew install cffi fonttools pango pillow six

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

## 📖 Documentation

- **[📚 Full Documentation](docs/_build/html/index.html)** - Complete user guide and API reference
- **[🚀 Quick Start Guide](docs/user_guide/quickstart.rst)** - Get started in minutes  
- **[⚙️ Configuration](docs/user_guide/configuration.rst)** - Customize your setup
- **[🏗️ Architecture](docs/development/architecture.rst)** - System design and components

## 🧪 Testing & Validation

```bash
# Run all tests
make test

# Test AI providers
make test-providers

# Test regeneration
make test-regeneration

# Analyze content variants
make variants
```


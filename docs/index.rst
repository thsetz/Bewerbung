Bewerbung Generator Documentation
==================================

Welcome to the Bewerbung Generator documentation! This tool generates professional German job applications using AI-powered content generation with multiple provider support.

System Workflow
---------------

.. mermaid::

   flowchart TD
       A0[🗑️ Step 0: Clear AI Cache] --> A[📁 Step 1: Read Profile]
       A --> B[📄 Step 2: Read Job Description]
       B --> C[📂 Step 3: Create Output Directory]
       C --> D[🤖 Step 4: Generate AI Content]
       D --> E[📁 Step 5: Create PDF Directory]
       E --> F[📄 Step 6: Convert to PDF]
       
       A01[.cache/ai_content_cache.json<br/>→ Clear for fresh content] --> A0
       A1[profil/YYYYMMDD_*.pdf<br/>→ Newest file] --> A
       B1[Stellenbeschreibung/YYYYMMDD_*.txt<br/>→ Newest file] --> B
       C1[Ausgabe/DATE_job-DATE_profile/] --> C
       D1[AI Provider Chain:<br/>Llama → Claude → Sample<br/>(Fresh content, no cache)] --> D
       E1[Create /pdf subdirectory] --> E
       F1[Markdown → HTML → PDF] --> F
       
       F --> G[✅ Complete Application Package]
       
       style A0 fill:#ffebee
       style A fill:#e1f5fe
       style B fill:#e8f5e8
       style C fill:#fff3e0
       style D fill:#fce4ec
       style E fill:#f3e5f5
       style F fill:#e0f2f1
       style G fill:#e8f5e8,stroke:#4caf50,stroke-width:3px

AI Provider Selection
---------------------

.. mermaid::

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

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   user_guide/installation
   user_guide/quickstart
   user_guide/configuration
   user_guide/tutorials

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api/modules

.. toctree::
   :maxdepth: 2
   :caption: Development
   
   development/architecture
   development/testing
   development/contributing

.. toctree::
   :maxdepth: 2
   :caption: Testing & Quality
   
   testing/coverage.md

Features
--------

✨ **Multi-Provider AI Support**
   Support for Claude API, Ollama/Llama, and sample content fallback

🏗️ **Directory-Only Organization** 
   Clean structure with AI provider subdirectories, no root files

📚 **Comprehensive Documentation**
   Auto-generated README files and regeneration scripts for each output

🔄 **Regeneration Testing**
   Automated validation that regeneration scripts work correctly

📊 **Content Variants Analysis**
   Compare AI-generated content across different providers

🧪 **Comprehensive Test Coverage**
   `View Coverage Reports <_static/coverage/index.html>`_ - Track code quality with detailed test coverage analysis

🗃️ **Structured Logging**
   Detailed logs for each generation process

Quick Start
-----------

1. **Installation**:

   .. code-block:: bash

      git clone https://github.com/thsetz/Bewerbung.git
      cd Bewerbung
      make install

2. **Configuration**:

   .. code-block:: bash

      cp .env.example .env
      # Edit .env with your AI provider API keys

3. **Generate Application**:

   .. code-block:: bash

      make generate

4. **View Results**:

   .. code-block:: bash

      ls Ausgabe/

Architecture Overview
--------------------

The Bewerbung Generator follows a modular architecture:

- **AI Client Factory**: Manages multiple AI providers with fallback support
- **Template Manager**: Handles Jinja2 templates for document generation  
- **Content Variants Analyzer**: Compares content across providers
- **Documentation Generator**: Creates comprehensive documentation
- **Regeneration Tester**: Validates script reproducibility

Supported AI Providers
----------------------

- **Claude API**: Professional-grade content generation
- **Ollama/Llama**: Local AI models for privacy-focused generation
- **Sample Content**: Built-in fallback for reliable operation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
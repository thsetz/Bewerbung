Bewerbung Generator Documentation
==================================

.. raw:: html

   <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; 
              padding: 20px; 
              border-radius: 10px; 
              margin: 20px 0; 
              text-align: center;">
      <h2 style="color: white; margin-top: 0;">🚀 Bewerbung Generator v1.0.3</h2>
      <p style="margin-bottom: 0; font-size: 1.1em;">
         Professional German Job Application Generator with AI Support
      </p>
   </div>

Welcome to the **Bewerbung Generator v|version|** documentation! This tool generates professional German job applications using AI-powered content generation with multiple provider support.

.. note::
   **Current Version:** |version| | **Release:** |release|
   
   📋 View the `changelog <https://github.com/thsetz/Bewerbung/blob/main/CHANGELOG.md>`_ for recent updates and improvements.

System Workflow
---------------

📊 **Interactive Diagram:** `View System Workflow <_static/system-workflow.html>`_

The application generation follows a structured 7-step process from cache clearing through PDF conversion.

AI Provider Selection
---------------------

📊 **Interactive Diagram:** `View AI Provider Selection <_static/ai-provider-selection.html>`_

The system uses intelligent multi-provider fallback with automatic provider switching for reliable content generation.

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
   
   testing/coverage

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
Installation
============

This guide will help you install and set up the Bewerbung Generator on your system.

Requirements
------------

- Python 3.8 or higher
- Git
- Virtual environment support

System Dependencies
------------------

For PDF generation (optional):

**macOS**:

.. code-block:: bash

   brew install pango

**Ubuntu/Debian**:

.. code-block:: bash

   sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

**Windows**:

PDF dependencies are included with WeasyPrint on Windows.

Installation Steps
------------------

1. **Clone the Repository**:

   .. code-block:: bash

      git clone https://github.com/thsetz/Bewerbung.git
      cd Bewerbung

2. **Set up Virtual Environment**:

   .. code-block:: bash

      make venv

3. **Install Dependencies**:

   .. code-block:: bash

      make install

4. **Configure Environment Variables**:

   .. code-block:: bash

      cp .env.example .env

   Edit the ``.env`` file with your configuration:

   .. code-block:: bash

      # AI Provider Configuration
      AI_PROVIDER=auto  # auto, claude, llama, sample
      
      # Claude API (optional)
      ANTHROPIC_API_KEY=your_claude_api_key_here
      
      # Llama/Ollama Configuration (optional)
      LLAMA_MODEL=llama3.2:latest
      OLLAMA_BASE_URL=http://localhost:11434
      
      # Output Configuration
      OUTPUT_STRUCTURE=by_model  # legacy, by_model, both
      INCLUDE_GENERATION_METADATA=true
      GENERATE_DOCUMENTATION=true

5. **Verify Installation**:

   .. code-block:: bash

      make test-providers

AI Provider Setup
-----------------

Claude API Setup
~~~~~~~~~~~~~~~~

1. Get an API key from `Anthropic <https://console.anthropic.com/>`_
2. Add your key to the ``.env`` file:

   .. code-block:: bash

      ANTHROPIC_API_KEY=your_api_key_here

3. Test the connection:

   .. code-block:: bash

      make test-providers

Ollama/Llama Setup
~~~~~~~~~~~~~~~~~~

1. **Install Ollama**:

   Visit `Ollama.ai <https://ollama.ai/>`_ and follow the installation instructions.

2. **Start Ollama Server**:

   .. code-block:: bash

      ollama serve

3. **Install Llama Model**:

   .. code-block:: bash

      make install-llama-model

4. **Verify Setup**:

   .. code-block:: bash

      make check-ollama

Quick Setup Script
------------------

For automated setup, you can use:

.. code-block:: bash

   # Complete setup with Ollama
   make setup-ollama
   
   # Test everything
   make test

Troubleshooting
---------------

**Virtual Environment Issues**:

.. code-block:: bash

   # Remove and recreate virtual environment
   rm -rf .venv
   make venv
   make install

**Permission Issues on macOS/Linux**:

.. code-block:: bash

   # Make scripts executable
   chmod +x scripts/*.sh

**Missing Dependencies**:

.. code-block:: bash

   # Force reinstall dependencies
   pip install -r requirements.txt --force-reinstall

**PDF Generation Issues**:

If PDF generation fails, check that system dependencies are installed:

.. code-block:: bash

   # Test PDF generation
   python -c "import weasyprint; print('WeasyPrint OK')"

Next Steps
----------

After installation, see:

- :doc:`quickstart` - Generate your first application
- :doc:`configuration` - Detailed configuration options
- :doc:`tutorials` - Step-by-step tutorials
Configuration
=============

This guide covers all configuration options for the Bewerbung Generator.

Environment Variables
---------------------

The application is configured through environment variables in the ``.env`` file.

AI Provider Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

**AI_PROVIDER**
   Selects which AI provider to use.
   
   - **auto** (default): Try Llama → Claude → Sample content
   - **claude**: Use Claude API only
   - **llama**: Use Ollama/Llama only  
   - **sample**: Use built-in sample content only

**ANTHROPIC_API_KEY**
   Your Claude API key from Anthropic Console.
   
   .. code-block:: bash
   
      ANTHROPIC_API_KEY=sk-ant-api03-...

**LLAMA_MODEL**
   Specific Llama model to use with Ollama.
   
   .. code-block:: bash
   
      LLAMA_MODEL=llama3.2:latest
      LLAMA_MODEL=llama3.2:3b

**OLLAMA_BASE_URL**
   Base URL for Ollama API server.
   
   .. code-block:: bash
   
      OLLAMA_BASE_URL=http://localhost:11434

Output Configuration
~~~~~~~~~~~~~~~~~~~

**OUTPUT_STRUCTURE**
   How to organize generated files.
   
   - **legacy**: Single directory structure (backward compatible)
   - **by_model**: Separate subdirectories for each AI client/model
   - **both**: Generate both legacy and by-model structures

**INCLUDE_GENERATION_METADATA**
   Whether to generate ``generation_info.json`` with technical details.
   
   - **true**: Include detailed metadata
   - **false**: Skip metadata generation

**GENERATE_DOCUMENTATION**
   Whether to create README files and regeneration scripts.
   
   - **true** (default): Generate comprehensive documentation
   - **false**: Skip documentation generation

Testing Configuration
~~~~~~~~~~~~~~~~~~~~~

**REGENERATION_TEST_MODE**
   How strictly to compare regenerated content.
   
   - **content**: Compare actual content (handles AI variations)
   - **structure**: Compare only file structure
   - **strict**: Exact byte-for-byte comparison

**REGENERATION_TEST_TIMEOUT**
   Maximum time (seconds) for regeneration tests.
   
   .. code-block:: bash
   
      REGENERATION_TEST_TIMEOUT=120

File Organization Patterns
---------------------------

Input File Naming
~~~~~~~~~~~~~~~~~

**Profile Files** (``profil/`` directory):
   
   Pattern: ``YYYYMMDD_identifier.pdf``
   
   Examples:
   
   .. code-block:: bash
   
      profil/20250604_dr_setz.pdf
      profil/20250101_max_mustermann.pdf

**Job Description Files** (``Stellenbeschreibung/`` directory):
   
   Pattern: ``YYYYMMDD_jobid_title.txt``
   
   Examples:
   
   .. code-block:: bash
   
      Stellenbeschreibung/20250624_61383_SeniorDevOpsEngineer.txt
      Stellenbeschreibung/20250615_12345_PythonDeveloper.txt

Output Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Legacy Structure**:

.. code-block::

   Ausgabe/YYYYMMDD_jobid_title-YYYYMMDD_profile/
   ├── anschreiben.md
   ├── lebenslauf.md  
   ├── anlagen.md
   ├── pdf/
   │   ├── anschreiben.pdf
   │   ├── lebenslauf.pdf
   │   └── anlagen.pdf
   ├── README.md
   ├── regenerate.sh
   └── regenerate.bat

**By-Model Structure**:

.. code-block::

   Ausgabe/YYYYMMDD_jobid_title-YYYYMMDD_profile/
   ├── claude_sonnet-3-5/
   │   ├── anschreiben.md
   │   ├── lebenslauf.md
   │   ├── anlagen.md
   │   ├── generation.log
   │   ├── generation_info.json
   │   ├── README.md
   │   └── regenerate.sh
   └── llama_3-2-latest/
       ├── anschreiben.md
       ├── lebenslauf.md
       ├── anlagen.md
       └── README.md

Template Configuration
----------------------

The application uses Jinja2 templates located in the ``templates/`` directory.

Template Variables
~~~~~~~~~~~~~~~~~

**Environment Variables** (UPPERCASE):
   Available in all templates from ``.env`` file or environment.
   
   .. code-block:: jinja
   
      {{ BEWERBUNG_ADRESSAT_FIRMA }}
      {{ BEWERBUNG_STELLE }}

**Dynamic Variables** (lowercase):
   Generated at runtime by AI or extracted from input.
   
   .. code-block:: jinja
   
      {{ einstiegstext }}
      {{ fachliche_passung }}
      {{ motivationstext }}

**Profile Variables** (mixed case):
   Extracted from profile files.
   
   .. code-block:: jinja
   
      {{ vollstaendiger_name }}
      {{ telefon }}
      {{ email }}

Custom Templates
~~~~~~~~~~~~~~~

You can customize templates by editing files in ``templates/``:

- ``anschreiben.md.j2`` - Cover letter template
- ``lebenslauf.md.j2`` - CV/Resume template  
- ``anlagen.md.j2`` - Attachments template

Example template customization:

.. code-block:: jinja

   # Custom cover letter section
   {% if custom_section %}
   ## {{ custom_section_title }}
   
   {{ custom_section_content }}
   {% endif %}

AI Provider Settings
--------------------

Claude API Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

**Model Selection**:
   The application automatically uses the latest Claude model. You can specify a different model by modifying the client code.

**API Limits**:
   Respects Claude API rate limits and includes retry logic.

**Caching**:
   Generated content is cached to avoid redundant API calls.

Ollama/Llama Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

**Model Management**:

.. code-block:: bash

   # List available models
   ollama list
   
   # Pull a specific model
   ollama pull llama3.2:3b
   
   # Remove a model
   ollama rm llama3.2:3b

**Performance Tuning**:

.. code-block:: bash

   # Set custom Ollama options
   OLLAMA_NUM_PARALLEL=4
   OLLAMA_MAX_LOADED_MODELS=2

**Custom Model Settings**:

You can modify the Llama client to use custom parameters:

.. code-block:: python

   # In llama_api_client.py
   generation_params = {
       "temperature": 0.7,
       "max_tokens": 2000,
       "top_p": 0.9
   }

Logging Configuration
--------------------

**Log Levels**:
   
   - INFO: General operation information
   - WARNING: Non-critical issues
   - ERROR: Critical problems

**Log Files**:
   
   - ``generation.log``: Detailed generation process log
   - Console output: Important messages and errors

**Log Format**:

.. code-block::

   2025-06-25 02:00:18 | INFO     | === Bewerbung Generation Started ===
   2025-06-25 02:00:18 | INFO     | AI client: ClaudeAPIClient
   2025-06-25 02:00:18 | INFO     | AI model: sonnet-3-5

Advanced Configuration
---------------------

Fallback Chain Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default AI provider fallback chain is:

1. Llama (if available and configured)
2. Claude (if API key provided)  
3. Sample content (always available)

You can modify this in ``ai_client_factory.py``.

Content Caching
~~~~~~~~~~~~~~

**Cache Location**: ``.cache/ai_content_cache.json``

**Cache Behavior**:
   - Caches AI-generated content by input hash
   - Survives between runs
   - Can be cleared manually

**Disable Caching**:

.. code-block:: python

   # In AI client initialization
   use_cache = False

PDF Generation Settings
~~~~~~~~~~~~~~~~~~~~~~

**WeasyPrint Configuration**:
   
   Modify CSS styles in templates or add custom CSS files.

**PDF Output Quality**:

.. code-block:: python

   # Custom PDF settings
   pdf_options = {
       'page-size': 'A4',
       'margin-top': '1in',
       'margin-bottom': '1in',
       'encoding': 'UTF-8'
   }

Configuration Validation
------------------------

**Test Configuration**:

.. code-block:: bash

   # Validate all settings
   make test-providers
   
   # Test specific provider
   AI_PROVIDER=claude make test-providers

**Debug Configuration**:

.. code-block:: bash

   # Show current configuration
   python -c "
   import os
   from src.ai_client_factory import AIClientFactory
   f = AIClientFactory()
   print('Current config:', f.get_config_summary())
   "

Environment File Examples
-------------------------

**Minimal Configuration** (``.env``):

.. code-block:: bash

   AI_PROVIDER=sample
   OUTPUT_STRUCTURE=legacy

**Full Configuration** (``.env``):

.. code-block:: bash

   # AI Provider Configuration
   AI_PROVIDER=auto
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   LLAMA_MODEL=llama3.2:latest
   OLLAMA_BASE_URL=http://localhost:11434
   
   # Output Configuration
   OUTPUT_STRUCTURE=by_model
   INCLUDE_GENERATION_METADATA=true
   GENERATE_DOCUMENTATION=true
   
   # Testing Configuration  
   REGENERATION_TEST_MODE=content
   REGENERATION_TEST_TIMEOUT=120

**Development Configuration** (``.env.development``):

.. code-block:: bash

   AI_PROVIDER=sample  # Fast for development
   OUTPUT_STRUCTURE=both  # Test both structures
   INCLUDE_GENERATION_METADATA=true
   GENERATE_DOCUMENTATION=true
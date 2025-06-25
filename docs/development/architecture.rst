Architecture
============

This document describes the system architecture and design principles of the Bewerbung Generator.

System Overview
---------------

The Bewerbung Generator follows a modular, extensible architecture designed for:

- **Multi-provider AI support** with fallback mechanisms
- **Flexible output organization** (legacy, by-model, both)
- **Comprehensive testing and validation**
- **Professional documentation generation**

High-Level Architecture
-----------------------

📊 **Interactive Diagram:** See ../diagrams/system-architecture.html

The Bewerbung Generator follows a modular, extensible architecture with clear separation of concerns.

Core Components
---------------

BewerbungGenerator (Main Controller)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Responsibilities**:
- Orchestrate the 6-step generation workflow
- Manage file I/O and directory structure
- Coordinate between components
- Handle logging and error reporting

**Key Methods**:
- ``run()``: Execute complete workflow
- ``read_newest_profile()``: Step 1 - Profile discovery
- ``read_newest_job_description()``: Step 2 - Job description discovery
- ``create_output_directory()``: Step 3 - Directory creation
- ``generate_application_documents()``: Step 4 - AI content generation
- ``create_pdf_directory()``: Step 5 - PDF directory setup
- ``convert_to_pdf()``: Step 6 - Document conversion

AIClientFactory (Provider Management)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Responsibilities**:
- Abstract AI provider selection
- Implement fallback chain logic
- Manage provider configuration
- Handle provider availability testing

**Fallback Chain**:
1. Llama/Ollama (local, privacy-focused)
2. Claude API (cloud-based, high-quality)
3. Sample Content (built-in, always available)

**Key Methods**:
- ``create_client()``: Factory method for client creation
- ``get_available_providers()``: Discover available providers
- ``test_all_providers()``: Validate provider configurations

BaseAIClient (Provider Interface)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Responsibilities**:
- Define standard interface for all AI providers
- Implement content caching mechanism
- Provide helper methods for content generation
- Ensure consistent API across providers

**Content Generation Methods**:
- ``generate_einstiegstext()``: Opening paragraph
- ``generate_fachliche_passung()``: Technical qualifications
- ``generate_motivationstext()``: Motivation section
- ``generate_mehrwert()``: Value proposition
- ``generate_abschlusstext()``: Professional closing

TemplateManager (Document Generation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Responsibilities**:
- Manage Jinja2 template rendering
- Handle variable substitution
- Generate structured markdown documents
- Support custom template extensions

**Template Variables**:
- **UPPERCASE**: Environment/configuration variables
- **lowercase**: AI-generated dynamic content
- **Mixed case**: Profile-extracted information

Data Flow
---------

Input Processing
~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TB
       subgraph "📁 Input Files"
           PF[profil/YYYYMMDD_*.pdf]
           JF[Stellenbeschreibung/YYYYMMDD_*.txt]
       end
       
       subgraph "🔍 Discovery Process"
           PD[Profile Discovery<br/>→ Newest by date]
           JD[Job Description Discovery<br/>→ Newest by date]
       end
       
       subgraph "📝 Content Processing"
           PE[Profile Extraction<br/>→ Variable population]
           JP[Job Parsing<br/>→ Company/position extraction]
       end
       
       PF --> PD --> PE
       JF --> JD --> JP
       
       PE --> Merge[🔗 Merge Data]
       JP --> Merge
       
       style PF fill:#e1f5fe
       style JF fill:#e8f5e8
       style Merge fill:#fff3e0

AI Content Generation
~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TD
       Input[📊 Job Description + Profile] --> Factory[🏭 AI Client Factory]
       Factory --> Selection{🎯 Provider Selection}
       
       Selection -->|1st Choice| Claude[🧠 Claude API]
       Selection -->|2nd Choice| Llama[🦙 Llama/Ollama]
       Selection -->|Fallback| Sample[📝 Sample Content]
       
       Claude --> Cache[💾 Content Caching]
       Llama --> Cache
       Sample --> Cache
       
       Cache --> Sections[📋 5 Content Sections]
       Sections --> Render[🎨 Template Rendering]
       
       subgraph "📋 Content Sections"
           E[Einstiegstext]
           F[Fachliche Passung]
           M[Motivationstext]
           W[Mehrwert]
           A[Abschlusstext]
       end
       
       style Input fill:#e1f5fe
       style Factory fill:#e8f5e8
       style Cache fill:#fff3e0
       style Render fill:#f3e5f5

Output Structure Decision
~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TD
       Content[📝 Rendered Content] --> Decision{⚙️ OUTPUT_STRUCTURE}
       
       Decision -->|legacy| Legacy[📁 Legacy Structure]
       Decision -->|by_model| ByModel[📂 By-Model Structure] 
       Decision -->|both| Both[📁📂 Both Structures]
       
       Legacy --> LDir[📁 Single Directory<br/>Ausgabe/job-profile/]
       ByModel --> MDir[📂 Model Directories<br/>Ausgabe/job-profile/model_name/]
       Both --> LDir
       Both --> MDir
       
       LDir --> Generation[📄 Document Generation]
       MDir --> Generation
       
       Generation --> Markdown[📝 Markdown Files]
       Generation --> PDF[📄 PDF Files]
       Generation --> Docs[📚 Documentation]
       Generation --> Scripts[🔄 Regeneration Scripts]
       
       style Decision fill:#fff3e0
       style Legacy fill:#e1f5fe
       style ByModel fill:#f3e5f5
       style Both fill:#e8f5e8

Design Patterns
---------------

Factory Pattern (AI Client Creation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``AIClientFactory`` implements the Factory pattern to:
- Abstract provider instantiation
- Enable runtime provider selection  
- Support configuration-driven behavior
- Facilitate testing and mocking

.. code-block:: python

   # Factory creates appropriate client based on configuration
   factory = AIClientFactory()
   client = factory.create_client()  # Returns Claude, Llama, or Sample client

Strategy Pattern (Provider Selection)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Different AI providers implement the same interface:
- Enables runtime algorithm selection
- Supports fallback strategies
- Facilitates A/B testing
- Allows transparent provider switching

Observer Pattern (Logging)
~~~~~~~~~~~~~~~~~~~~~~~~~

Structured logging throughout the system:
- Centralized logging configuration
- Component-specific loggers
- Hierarchical log levels
- Persistent log files

Module Dependencies
-------------------

Core Dependencies
~~~~~~~~~~~~~~~~

.. code-block::

   bewerbung_generator
   ├── ai_client_factory
   │   ├── base_ai_client
   │   ├── claude_api_client
   │   ├── llama_api_client
   │   └── ai_content_generator (sample)
   ├── template_manager
   └── documentation_generator

Analysis Dependencies
~~~~~~~~~~~~~~~~~~~

.. code-block::

   content_variants_analyzer
   ├── (independent module)
   └── uses output from bewerbung_generator

Testing Dependencies
~~~~~~~~~~~~~~~~~~~

.. code-block::

   tests/
   ├── test_regeneration
   │   └── uses regeneration scripts
   └── individual module tests

Configuration Management
------------------------

Environment-Based Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All configuration through environment variables:
- **AI_PROVIDER**: Provider selection
- **OUTPUT_STRUCTURE**: Output organization
- **API Keys**: Provider authentication
- **Feature Flags**: Optional functionality

File-Based Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Templates and static configuration:
- **templates/**: Jinja2 templates
- **profil/** and **Stellenbeschreibung/**: Input directories
- **.env**: Environment variable definitions

Error Handling Strategy
----------------------

Layered Error Handling
~~~~~~~~~~~~~~~~~~~~~

1. **Provider Level**: ``AIProviderError`` for AI-specific issues
2. **Application Level**: Graceful degradation with fallbacks
3. **User Level**: Clear error messages and recovery suggestions

Fallback Mechanisms
~~~~~~~~~~~~~~~~~~

- **AI Provider Fallback**: Automatic provider switching
- **Content Fallback**: Sample content when AI unavailable
- **PDF Fallback**: Continue without PDF if conversion fails

Testing Strategy
---------------

Unit Testing
~~~~~~~~~~~~

- Individual component testing
- Mock external dependencies
- Validate core functionality

Integration Testing
~~~~~~~~~~~~~~~~~~

- End-to-end workflow testing
- AI provider integration
- File I/O validation

Regeneration Testing
~~~~~~~~~~~~~~~~~~~

- Validate regeneration script accuracy
- Test content reproducibility
- Verify environment consistency

Content Analysis Testing
~~~~~~~~~~~~~~~~~~~~~~~

- Compare AI provider outputs
- Validate content quality metrics
- Test variant analysis functionality

Performance Considerations
-------------------------

Caching Strategy
~~~~~~~~~~~~~~~

- **AI Content Caching**: Avoid redundant API calls
- **Template Caching**: Reuse compiled templates
- **File System Caching**: Minimize disk I/O

Resource Management
~~~~~~~~~~~~~~~~~~

- **Memory**: Lazy loading of large files
- **Network**: Efficient API usage with retries
- **Storage**: Organized output structure

Scalability
~~~~~~~~~~

- **Horizontal**: Multiple AI providers
- **Vertical**: Batch processing support
- **Extensibility**: Plugin architecture for new providers

Security Considerations
----------------------

API Key Management
~~~~~~~~~~~~~~~~~

- Environment variable storage
- No hardcoded credentials
- Support for external secret management

Data Privacy
~~~~~~~~~~~~

- Local processing with Ollama option
- No data persistence in AI providers
- Configurable caching policies

File Security
~~~~~~~~~~~~

- Input validation for file paths
- Sandboxed template rendering
- Secure PDF generation

Future Architecture Enhancements
--------------------------------

Planned Improvements
~~~~~~~~~~~~~~~~~~~

1. **Plugin System**: Dynamic provider loading
2. **API Service**: REST API for remote usage
3. **Web Interface**: Browser-based UI
4. **Database Integration**: Structured data storage
5. **Cloud Deployment**: Container orchestration support
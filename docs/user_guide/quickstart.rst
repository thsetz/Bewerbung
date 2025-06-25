Quick Start
===========

This guide will get you up and running with the Bewerbung Generator in just a few minutes.

Prerequisites
-------------

Before starting, make sure you have:

- Completed the :doc:`installation` steps
- Prepared your profile and job description files
- Configured at least one AI provider (or use sample content)

Your First Application
----------------------

1. **Prepare Input Files**

   Place your files in the appropriate directories:

   - **Profile**: ``profil/YYYYMMDD_your_name.pdf``
   - **Job Description**: ``Stellenbeschreibung/YYYYMMDD_job_title.txt``

   Example:

   .. code-block:: bash

      # Profile file
      profil/20250604_dr_setz.pdf
      
      # Job description file  
      Stellenbeschreibung/20250624_61383_SeniorDevOpsEngineer.txt

2. **Generate Application**

   .. code-block:: bash

      make generate

   This will:
   
   - Find the newest profile and job description files
   - Create an output directory
   - Generate personalized application documents
   - Create PDF versions
   - Generate documentation and regeneration scripts

3. **Review Output**

   Your generated application will be in:

   .. code-block:: bash

      Ausgabe/YYYYMMDD_jobid_JobTitle-YYYYMMDD_profile_name/

   The output includes:

   - ``anschreiben.md`` - Cover letter
   - ``lebenslauf.md`` - CV/Resume  
   - ``anlagen.md`` - Attachments list
   - ``pdf/`` - PDF versions
   - ``README.md`` - Generation documentation
   - ``regenerate.sh`` / ``regenerate.bat`` - Regeneration scripts

Understanding the Output Structure
----------------------------------

Depending on your ``OUTPUT_STRUCTURE`` setting:

**Legacy Structure** (``legacy``):

.. code-block::

   Ausgabe/20250624_job-20250604_profile/
   ├── anschreiben.md
   ├── lebenslauf.md
   ├── anlagen.md
   └── pdf/

**By Model Structure** (``by_model``):

.. code-block::

   Ausgabe/20250624_job-20250604_profile/
   ├── claude_sonnet-3-5/
   │   ├── anschreiben.md
   │   ├── lebenslauf.md
   │   ├── generation.log
   │   └── README.md
   └── llama_3-2-latest/
       ├── anschreiben.md
       ├── lebenslauf.md
       └── README.md

**Both Structures** (``both``):

Combines both legacy and by-model organization.

Using Different AI Providers
-----------------------------

**Automatic Provider Selection**:

.. code-block:: bash

   make generate

**Force Specific Provider**:

.. code-block:: bash

   # Use Claude only
   AI_PROVIDER=claude make generate
   
   # Use Llama only  
   AI_PROVIDER=llama make generate
   
   # Use sample content only
   AI_PROVIDER=sample make generate

Advanced Generation Options
---------------------------

**Generate with Metadata**:

.. code-block:: bash

   INCLUDE_GENERATION_METADATA=true make generate

**Generate without Documentation**:

.. code-block:: bash

   GENERATE_DOCUMENTATION=false make generate

**Organize by Model**:

.. code-block:: bash

   OUTPUT_STRUCTURE=by_model make generate

Testing Your Setup
------------------

**Test AI Providers**:

.. code-block:: bash

   make test-providers

**Generate and Test Regeneration**:

.. code-block:: bash

   make generate-and-test

**Analyze Content Variants**:

.. code-block:: bash

   make variants

Understanding Generated Content
-------------------------------

The AI generates content for these sections:

- **Einstiegstext**: Opening paragraph expressing interest
- **Fachliche Passung**: Technical qualifications and experience
- **Motivationstext**: Motivation and enthusiasm for the role
- **Mehrwert**: Value proposition and achievements  
- **Abschlusstext**: Professional closing and call to action

Each section is personalized based on:

- Your profile information
- The job description requirements
- The specific AI provider's capabilities

Regeneration Scripts
--------------------

Each generated application includes scripts to reproduce the exact same output:

**Unix/Linux/macOS**:

.. code-block:: bash

   cd Ausgabe/your_application_folder/
   ./regenerate.sh

**Windows**:

.. code-block:: bash

   cd Ausgabe\your_application_folder\
   regenerate.bat

These scripts:

- Set the exact AI provider and model used
- Reproduce the same generation environment
- Generate identical content (for deterministic providers)

Next Steps
----------

Now that you have generated your first application:

- :doc:`configuration` - Learn about detailed configuration options
- :doc:`tutorials` - Explore advanced usage scenarios
- :doc:`../development/testing` - Learn about testing and validation

Common Issues
-------------

**No AI Provider Available**:

If you see "Using sample content", either:

- Configure an AI provider in ``.env``
- Install and start Ollama for local generation
- Continue with sample content for testing

**PDF Generation Failed**:

Install system dependencies:

.. code-block:: bash

   # macOS
   brew install pango
   
   # Ubuntu/Debian  
   sudo apt-get install libpango-1.0-0

**Empty Generated Content**:

Check your input files:

- Profile file exists and is readable
- Job description file contains text content
- File naming follows the YYYYMMDD pattern
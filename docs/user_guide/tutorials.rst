Tutorials
=========

This section provides step-by-step tutorials for common use cases and advanced scenarios.

Tutorial 1: Basic Application Generation
-----------------------------------------

This tutorial walks through generating your first job application from start to finish.

**Prerequisites**: Completed installation and basic configuration.

**Step 1: Prepare Your Profile**

Create a PDF file with your professional information:

.. code-block:: bash

   # Example filename (replace with your details)
   profil/20250604_max_mustermann.pdf

The file should contain:
- Personal information (name, contact details)
- Professional experience
- Education and qualifications
- Skills and certifications

**Step 2: Prepare Job Description**

Save the job posting as a text file:

.. code-block:: bash

   # Example filename
   Stellenbeschreibung/20250625_12345_SoftwareDeveloper.txt

Include:
- Company name and details
- Job title and reference number
- Required qualifications
- Job responsibilities
- Company culture information

**Step 3: Configure AI Provider**

Choose your preferred AI provider in ``.env``:

.. code-block:: bash

   # For high-quality content
   AI_PROVIDER=claude
   ANTHROPIC_API_KEY=your_key_here
   
   # For local/private generation
   AI_PROVIDER=llama
   LLAMA_MODEL=llama3.2:latest
   
   # For testing/demo
   AI_PROVIDER=sample

**Step 4: Generate Application**

.. code-block:: bash

   make generate

**Step 5: Review Output**

Check the generated files:

.. code-block:: bash

   # Navigate to output directory
   cd Ausgabe/20250625_12345_SoftwareDeveloper-20250604_max_mustermann/
   
   # Review generated content
   cat anschreiben.md
   cat lebenslauf.md
   
   # Check PDF versions
   ls pdf/

**Step 6: Test Regeneration**

Verify the regeneration script works:

.. code-block:: bash

   ./regenerate.sh

Tutorial 2: Comparing AI Providers
----------------------------------

This tutorial shows how to generate applications with different AI providers and compare the results.

**Step 1: Generate with Multiple Providers**

.. code-block:: bash

   # Generate with Claude
   AI_PROVIDER=claude OUTPUT_STRUCTURE=by_model make generate
   
   # Generate with Llama  
   AI_PROVIDER=llama OUTPUT_STRUCTURE=by_model make generate
   
   # Generate sample content
   AI_PROVIDER=sample OUTPUT_STRUCTURE=by_model make generate

**Step 2: Analyze Variants**

.. code-block:: bash

   # Quick comparison
   make variants
   
   # Detailed content comparison
   make variants-detailed

**Step 3: Compare Quality**

Review the generated content for:
- **Tone and style**: Professional vs. casual
- **Technical detail**: Specific vs. general
- **Length**: Concise vs. detailed
- **Personalization**: Generic vs. tailored

**Step 4: Choose Best Provider**

Based on your analysis, set your preferred provider:

.. code-block:: bash

   # Update .env with your choice
   AI_PROVIDER=claude  # or llama, or auto

Tutorial 3: Advanced Output Organization
-----------------------------------------

Learn how to organize outputs for different scenarios.

**Scenario 1: Multiple Applications per Day**

For high-volume application generation:

.. code-block:: bash

   # Use by-model structure for organization
   OUTPUT_STRUCTURE=by_model
   INCLUDE_GENERATION_METADATA=true

**Scenario 2: A/B Testing Content**

Compare different AI providers for the same job:

.. code-block:: bash

   # Generate with all providers
   OUTPUT_STRUCTURE=by_model
   
   # Script to generate with all providers
   for provider in claude llama sample; do
     AI_PROVIDER=$provider make generate
   done
   
   # Analyze results
   make variants-detailed

**Scenario 3: Client/Agency Use**

For professional services generating applications for multiple clients:

.. code-block:: bash

   # Organize by client and preserve full documentation
   OUTPUT_STRUCTURE=both
   INCLUDE_GENERATION_METADATA=true
   GENERATE_DOCUMENTATION=true

Tutorial 4: Custom Template Development
---------------------------------------

Create custom templates for specialized applications.

**Step 1: Understand Template Structure**

Examine existing templates:

.. code-block:: bash

   ls templates/
   cat templates/anschreiben.md.j2

**Step 2: Create Custom Template**

.. code-block:: bash

   # Copy existing template as starting point
   cp templates/anschreiben.md.j2 templates/anschreiben_tech.md.j2

**Step 3: Modify Template**

Add custom sections for technical roles:

.. code-block:: jinja

   ## Technical Skills
   
   {{ technical_skills }}
   
   ## Project Portfolio
   
   {{ project_portfolio }}
   
   ## Open Source Contributions
   
   {{ open_source_contributions }}

**Step 4: Test Custom Template**

Modify the template manager to use your custom template and test.

Tutorial 5: Automated Testing Workflow
--------------------------------------

Set up comprehensive testing for your application generation.

**Step 1: Basic Validation**

.. code-block:: bash

   # Test all components
   make test
   
   # Test AI providers
   make test-providers
   
   # Test regeneration
   make test-regeneration

**Step 2: Content Quality Testing**

.. code-block:: bash

   # Generate test applications
   make generate-and-test
   
   # Analyze content quality
   make variants

**Step 3: Automated Testing Script**

Create a comprehensive test script:

.. code-block:: bash

   #!/bin/bash
   # test_all.sh
   
   echo "🧪 Running comprehensive tests..."
   
   # Test each provider
   for provider in claude llama sample; do
     echo "Testing $provider..."
     AI_PROVIDER=$provider OUTPUT_STRUCTURE=by_model make generate
   done
   
   # Test regeneration
   make test-regeneration
   
   # Analyze variants
   make variants
   
   echo "✅ All tests completed"

**Step 4: Continuous Integration**

For automated testing in CI/CD:

.. code-block:: yaml

   # .github/workflows/test.yml
   name: Test Bewerbung Generator
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.9'
         - run: make install
         - run: AI_PROVIDER=sample make test

Tutorial 6: Performance Optimization
------------------------------------

Optimize the application for faster generation and better resource usage.

**Step 1: Cache Management**

.. code-block:: bash

   # Check cache status
   ls -la .cache/
   
   # Clear cache if needed
   rm -f .cache/ai_content_cache.json
   
   # Generate with fresh cache
   make generate

**Step 2: Provider Selection Optimization**

.. code-block:: bash

   # Test provider performance
   time AI_PROVIDER=claude make generate
   time AI_PROVIDER=llama make generate
   time AI_PROVIDER=sample make generate

**Step 3: Batch Processing**

For multiple applications:

.. code-block:: bash

   #!/bin/bash
   # batch_generate.sh
   
   # List of job descriptions
   jobs=(
     "20250625_001_DevOps.txt"
     "20250625_002_Frontend.txt"
     "20250625_003_Backend.txt"
   )
   
   for job in "${jobs[@]}"; do
     echo "Processing $job..."
     # Copy to standard location
     cp "batch_jobs/$job" "Stellenbeschreibung/"
     make generate
   done

**Step 4: Resource Monitoring**

Monitor resource usage during generation:

.. code-block:: bash

   # Monitor CPU and memory
   top -p $(pgrep -f "python.*bewerbung")
   
   # Check disk usage
   du -sh Ausgabe/

Tutorial 7: Troubleshooting Common Issues
-----------------------------------------

Solutions for common problems and error scenarios.

**Issue 1: AI Provider Not Available**

**Problem**: "AI provider not available" errors.

**Solution**:

.. code-block:: bash

   # Check provider status
   make test-providers
   
   # For Claude issues
   echo $ANTHROPIC_API_KEY  # Should not be empty
   
   # For Ollama issues
   curl http://localhost:11434/api/tags
   ollama list

**Issue 2: PDF Generation Fails**

**Problem**: PDF files not generated.

**Solution**:

.. code-block:: bash

   # Install system dependencies
   # macOS:
   brew install pango
   
   # Ubuntu:
   sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
   
   # Test WeasyPrint
   python -c "import weasyprint; print('WeasyPrint OK')"

**Issue 3: Empty Generated Content**

**Problem**: Generated files contain template placeholders.

**Solution**:

.. code-block:: bash

   # Check input files
   ls -la profil/
   ls -la Stellenbeschreibung/
   
   # Verify file content
   file profil/*.pdf
   head Stellenbeschreibung/*.txt
   
   # Check AI provider status
   make test-providers

**Issue 4: Regeneration Script Fails**

**Problem**: Regeneration scripts don't work.

**Solution**:

.. code-block:: bash

   # Make script executable
   chmod +x regenerate.sh
   
   # Check script content
   head regenerate.sh
   
   # Run with debug
   bash -x regenerate.sh

**Issue 5: Template Errors**

**Problem**: Jinja2 template rendering errors.

**Solution**:

.. code-block:: bash

   # Check template syntax
   python -c "
   from jinja2 import Template
   with open('templates/anschreiben.md.j2') as f:
       Template(f.read())
   print('Template syntax OK')
   "
   
   # Check available variables
   make generate 2>&1 | grep -i "undefined"

Next Steps
----------

After completing these tutorials:

- Explore the :doc:`../api/modules` for advanced customization
- Check :doc:`../development/architecture` to understand the system design
- Contribute improvements following :doc:`../development/contributing`
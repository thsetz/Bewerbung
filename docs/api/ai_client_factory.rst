ai_client_factory module
========================

.. automodule:: ai_client_factory
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

.. autoclass:: AIClientFactory
   :members:
   :special-members: __init__
   :exclude-members: __weakref__

Factory Methods
---------------

.. automethod:: AIClientFactory.create_client
.. automethod:: AIClientFactory.get_available_providers
.. automethod:: AIClientFactory.test_all_providers

Provider Selection
------------------

The factory implements an intelligent fallback chain:

1. **Llama/Ollama** - Local AI models (privacy-focused)
2. **Claude API** - Cloud-based AI (high quality) 
3. **Sample Content** - Built-in fallback (always available)

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from ai_client_factory import AIClientFactory
   
   # Create factory with auto-selection
   factory = AIClientFactory()
   client = factory.create_client()
   
   # Generate content
   content = client.generate_einstiegstext(
       job_description="...",
       profile_content="...",
       company_name="Example Corp",
       position_title="Software Engineer"
   )

Provider Testing
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Test all available providers
   factory = AIClientFactory()
   results = factory.test_all_providers()
   
   for provider, result in results.items():
       status = "✅" if result["available"] else "❌"
       print(f"{status} {provider}: {result}")

Forced Provider Selection
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   
   # Force specific provider
   os.environ["AI_PROVIDER"] = "claude"
   factory = AIClientFactory()
   client = factory.create_client()  # Will use Claude only

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

- **AI_PROVIDER**: ``auto``, ``claude``, ``llama``, ``sample``
- **AI_ENABLE_FALLBACK**: ``true``/``false`` (enable fallback chain)
- **ANTHROPIC_API_KEY**: Claude API key
- **LLAMA_MODEL**: Specific Llama model to use
- **OLLAMA_BASE_URL**: Ollama server URL
base_ai_client module
====================

.. automodule:: base_ai_client
   :members:
   :undoc-members:
   :show-inheritance:

Abstract Base Class
-------------------

.. autoclass:: BaseAIClient
   :members:
   :special-members: __init__
   :exclude-members: __weakref__

Abstract Methods
~~~~~~~~~~~~~~~~

All AI client implementations must provide these methods:

.. automethod:: BaseAIClient.generate_einstiegstext
.. automethod:: BaseAIClient.generate_fachliche_passung
.. automethod:: BaseAIClient.generate_motivationstext
.. automethod:: BaseAIClient.generate_mehrwert
.. automethod:: BaseAIClient.generate_abschlusstext

Utility Methods
~~~~~~~~~~~~~~~

.. automethod:: BaseAIClient.extract_company_and_position
.. automethod:: BaseAIClient.generate_all_cover_letter_content
.. automethod:: BaseAIClient.is_available
.. automethod:: BaseAIClient.get_model_name
.. automethod:: BaseAIClient.get_client_model_folder

Exception Classes
-----------------

.. autoexception:: AIProviderError

Implementation Guide
--------------------

To create a new AI provider, inherit from ``BaseAIClient`` and implement all abstract methods:

.. code-block:: python

   from base_ai_client import BaseAIClient, AIProviderError
   
   class CustomAIClient(BaseAIClient):
       def __init__(self, base_dir: str = ".", use_cache: bool = True):
           super().__init__(base_dir, use_cache)
           # Initialize your AI provider
   
       def is_available(self) -> bool:
           # Check if your AI provider is accessible
           return True
   
       def get_model_name(self) -> str:
           return "custom-model-v1"
   
       def generate_einstiegstext(self, job_description: str, 
                                profile_content: str, company_name: str,
                                position_title: str) -> str:
           # Implement content generation
           return "Generated introduction text..."
   
       # Implement other required methods...

Content Generation Methods
--------------------------

Each content generation method follows the same pattern:

Parameters
~~~~~~~~~~

- **job_description** (str): Full text of the job posting
- **profile_content** (str): Applicant's profile information  
- **company_name** (str): Name of the hiring company
- **position_title** (str): Title of the position being applied for

Returns
~~~~~~~

- **str**: Generated German text content for the specific section

Content Sections
~~~~~~~~~~~~~~~~

- **einstiegstext**: Opening paragraph expressing interest
- **fachliche_passung**: Technical qualifications and experience match
- **motivationstext**: Personal motivation and enthusiasm  
- **mehrwert**: Value proposition and unique contributions
- **abschlusstext**: Professional closing and call to action

Caching Behavior
----------------

The base client provides automatic caching:

- Content is cached by hash of input parameters
- Cache survives between application runs
- Cache can be disabled by setting ``use_cache=False``
- Cache location: ``.cache/ai_content_cache.json``

Error Handling
--------------

All methods should raise ``AIProviderError`` for provider-specific issues:

.. code-block:: python

   from base_ai_client import AIProviderError
   
   def generate_content(self, ...):
       try:
           # AI provider call
           response = self.ai_api.generate(...)
           return response.text
       except Exception as e:
           raise AIProviderError(f"Failed to generate content: {e}")
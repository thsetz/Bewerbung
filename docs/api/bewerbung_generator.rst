bewerbung_generator module
==========================

.. automodule:: bewerbung_generator
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

.. autoclass:: BewerbungGenerator
   :members:
   :special-members: __init__
   :exclude-members: __weakref__

Methods
-------

Core Workflow Methods
~~~~~~~~~~~~~~~~~~~~~

.. automethod:: BewerbungGenerator.read_newest_profile
.. automethod:: BewerbungGenerator.read_newest_job_description
.. automethod:: BewerbungGenerator.create_output_directory
.. automethod:: BewerbungGenerator.generate_application_documents
.. automethod:: BewerbungGenerator.create_pdf_directory
.. automethod:: BewerbungGenerator.convert_to_pdf

Utility Methods
~~~~~~~~~~~~~~~

.. automethod:: BewerbungGenerator.get_newest_file_by_date_pattern
.. automethod:: BewerbungGenerator.run

Usage Example
-------------

.. code-block:: python

   from bewerbung_generator import BewerbungGenerator
   
   # Initialize generator
   generator = BewerbungGenerator(base_dir=".")
   
   # Run complete workflow
   result = generator.run()
   
   if result:
       print("✅ Application generated successfully")
   else:
       print("❌ Generation failed")
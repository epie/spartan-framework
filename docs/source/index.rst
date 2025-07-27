.. Spartan Framework documentation master file

Welcome to Spartan Framework's documentation!
=============================================

Spartan Framework is an infrastructure framework for serverless development in AWS.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/modules
   contributing
   changelog

Features
--------

* Serverless development framework for AWS
* FastAPI integration with AWS Lambda
* Database management with SQLAlchemy and Alembic
* Comprehensive logging and tracing
* Request/Response validation with Pydantic
* Middleware support
* Testing utilities

Installation
============

You can install the Spartan Framework using pip:

.. code-block:: bash

   pip install spartan-framework

Quick Start
===========

Here's a simple example of how to use the Spartan Framework:

.. code-block:: python

   from app.models.base import BaseModel
   from app.services.logging import LoggingService

   # Create a logging service
   logger = LoggingService()
   logger.info("Starting application")

API Documentation
=================

For detailed API documentation, see the :doc:`api/modules` section.

Contributing
============

Please read our :doc:`contributing` guide for details on our code of conduct and the process for submitting pull requests.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

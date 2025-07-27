Quick Start
===========

This guide will help you get started with the Spartan Framework quickly.

Basic Usage
-----------

Setting up a Basic Model
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from app.models.base import BaseModel
   from sqlalchemy import Column, String, Integer

   class User(BaseModel):
       __tablename__ = 'users'

       id = Column(Integer, primary_key=True)
       name = Column(String(100), nullable=False)
       email = Column(String(255), unique=True, nullable=False)

Using the Logging Service
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from app.services.logging import LoggingService

   # Initialize the logging service
   logger = LoggingService()

   # Log messages
   logger.info("Application started")
   logger.error("An error occurred", extra={"user_id": 123})

Database Operations
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from app.helpers.database import DatabaseHelper
   from app.models.user import User

   # Initialize database helper
   db = DatabaseHelper()

   # Create a new user
   user = User(name="John Doe", email="john@example.com")
   db.session.add(user)
   db.session.commit()

   # Query users
   users = db.session.query(User).all()

Request/Response Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from app.requests.user import UserCreateRequest
   from app.responses.user import UserResponse

   # Validate incoming request
   request_data = {"name": "John Doe", "email": "john@example.com"}
   user_request = UserCreateRequest(**request_data)

   # Create response
   response = UserResponse(
       id=1,
       name=user_request.name,
       email=user_request.email
   )

AWS Lambda Handler
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from handlers.inference import lambda_handler
   from mangum import Mangum
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/health")
   def health_check():
       return {"status": "healthy"}

   # Wrap FastAPI app for Lambda
   handler = Mangum(app)

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The framework uses environment variables for configuration:

.. code-block:: bash

   # .env file
   DATABASE_URL=postgresql://user:password@localhost/dbname
   LOG_LEVEL=INFO
   AWS_REGION=us-east-1

Database Migrations
~~~~~~~~~~~~~~~~~~~

Use Alembic for database migrations:

.. code-block:: bash

   # Create a new migration
   alembic revision --autogenerate -m "Add user table"

   # Apply migrations
   alembic upgrade head

Testing
-------

Run tests using pytest:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=app

   # Run specific test file
   pytest tests/unit/test_user_model.py

Next Steps
----------

* Explore the :doc:`api/modules` for detailed API documentation
* Check out the example handlers in the `handlers/` directory
* Read about :doc:`contributing` to the project

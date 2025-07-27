Installation
============

Requirements
------------

* Python 3.11 or higher
* Poetry (recommended) or pip

Using Poetry (Recommended)
---------------------------

If you're developing with the Spartan Framework or want to install it from source:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/nerdmonkey/spartan-framework.git
   cd spartan-framework

   # Install dependencies with Poetry
   poetry install

Using pip
---------

For production use or if you prefer pip:

.. code-block:: bash

   pip install spartan-framework

Development Installation
-------------------------

For development, you'll want to install the development dependencies as well:

.. code-block:: bash

   # With Poetry
   poetry install --with dev

   # Or with pip (after cloning the repo)
   pip install -r requirements.txt
   pip install -e .

Environment Setup
-----------------

The Spartan Framework uses environment variables for configuration. Create a `.env` file in your project root:

.. code-block:: bash

   # Database configuration
   DATABASE_URL=postgresql://user:password@localhost/dbname

   # AWS configuration
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key

   # Logging configuration
   LOG_LEVEL=INFO

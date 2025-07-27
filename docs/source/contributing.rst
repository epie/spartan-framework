Contributing
============

We welcome contributions to the Spartan Framework! This document outlines the process for contributing to the project.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Write or update tests as necessary
6. Ensure all tests pass
7. Submit a pull request

Development Setup
-----------------

.. code-block:: bash

   # Clone your fork
   git clone https://github.com/yourusername/spartan-framework.git
   cd spartan-framework

   # Install dependencies
   poetry install --with dev

   # Install pre-commit hooks (optional but recommended)
   pre-commit install

Code Style
----------

We use several tools to maintain code quality:

* **Black**: Code formatting
* **isort**: Import sorting
* **flake8**: Linting
* **bandit**: Security checks

Run these tools before submitting:

.. code-block:: bash

   # Format code
   black .

   # Sort imports
   isort .

   # Check linting
   flake8

   # Security check
   bandit -r app/

Testing
-------

All contributions should include tests. We use pytest for testing:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=app --cov-report=html

   # Run specific test categories
   pytest tests/unit/
   pytest tests/integration/
   pytest tests/e2e/

Documentation
-------------

When adding new features, please update the documentation:

* Add docstrings to your code
* Update relevant .rst files in `docs/source/`
* Build docs locally to verify: `make html` in the `docs/` directory

Pull Request Guidelines
-----------------------

1. **Clear Description**: Provide a clear description of what your PR does
2. **Tests**: Include tests for new functionality
3. **Documentation**: Update documentation as needed
4. **Changelog**: Add an entry to CHANGELOG.md
5. **Small PRs**: Keep PRs focused and reasonably sized

Commit Messages
---------------

Use clear, descriptive commit messages:

.. code-block:: text

   feat: add user authentication middleware
   fix: resolve database connection timeout
   docs: update installation instructions
   test: add unit tests for logging service

Issue Reporting
---------------

When reporting issues:

1. Use the issue template
2. Provide a clear description
3. Include steps to reproduce
4. Add relevant logs or error messages
5. Specify your environment (Python version, OS, etc.)

Code of Conduct
---------------

Please note that this project is released with a Code of Conduct. By participating in this project, you agree to abide by its terms.

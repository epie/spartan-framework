# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build
POETRY        = poetry
PROJECT_ROOT  = .

# Detect if we're using Poetry
HAS_POETRY := $(shell command -v poetry 2> /dev/null)

# Set the command prefix based on Poetry availability
ifdef HAS_POETRY
	CMD_PREFIX = $(POETRY) run
else
	CMD_PREFIX =
endif

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Spartan Framework Documentation Build"
	@echo "====================================="
	@echo ""
	@echo "Available targets:"
	@echo "  help       Show this help message"
	@echo "  setup      Quick setup for development (install deps + pre-commit)"
	@echo "  install    Install documentation dependencies"
	@echo "  clean      Remove built documentation"
	@echo "  html       Build HTML documentation"
	@echo "  build      Clean and build HTML documentation"
	@echo "  serve      Build and serve documentation locally"
	@echo "  open       Open documentation in browser (macOS)"
	@echo "  apidoc     Generate API documentation from source code"
	@echo "  linkcheck  Check for broken external links"
	@echo "  livehtml   Build and auto-reload documentation on changes"
	@echo ""
	@echo "Development targets:"
	@echo "  setup-precommit  Install and setup pre-commit hooks"
	@echo "  precommit        Run pre-commit on all files"
	@echo "  precommit-fix    Run pre-commit and auto-fix issues"
	@echo "  format           Format code with black and isort"
	@echo "  lint             Run linting checks"
	@echo "  test             Run tests"
	@echo "  test-cov         Run tests with coverage report"
	@echo "  quality          Run all quality checks (format, lint, test)"
	@echo "  clean-cache      Clean Python cache files"
	@echo "  update-hooks     Update pre-commit hooks to latest versions"
	@echo ""
	@echo "Environment:"
ifdef HAS_POETRY
	@echo "  Using Poetry: Yes"
else
	@echo "  Using Poetry: No"
endif

.PHONY: help Makefile setup install clean html build serve open apidoc linkcheck livehtml setup-precommit precommit precommit-fix format lint test test-cov quality clean-cache update-hooks

# Catch-all target: route all unknown targets to Sphinx-Build using the -M option.
%: Makefile
	@$(CMD_PREFIX) $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Quick setup target for new developers
setup: setup-precommit
	@echo ""
	@echo "🎉 Development environment setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Make some changes to your code"
	@echo "  2. Run 'make quality' to check everything"
	@echo "  3. Commit your changes (pre-commit will run automatically)"

# Installation target
install:
ifdef HAS_POETRY
	@echo "Installing documentation dependencies with Poetry..."
	$(POETRY) install --with dev
else
	@echo "Poetry not found. Please install dependencies manually:"
	@echo "  pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints"
endif

# Custom targets for convenience
clean:
	@echo "Cleaning documentation build directory..."
	@$(CMD_PREFIX) $(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Documentation cleaned."

html:
	@echo "Building HTML documentation..."
	@$(CMD_PREFIX) $(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo "Documentation built successfully!"
	@echo "Open: file://$(shell pwd)/$(BUILDDIR)/html/index.html"

# Build target: clean and build
build: clean html

# Serve documentation locally
serve: html
	@echo "Starting local documentation server..."
	@echo "Documentation will be available at: http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	cd $(BUILDDIR)/html && python -m http.server 8000

# Open documentation in browser (macOS only)
open: html
ifeq ($(shell uname),Darwin)
	@echo "Opening documentation in browser..."
	open "file://$(shell pwd)/$(BUILDDIR)/html/index.html"
else
	@echo "Open target only available on macOS"
	@echo "Documentation location: file://$(shell pwd)/$(BUILDDIR)/html/index.html"
endif

# Generate API documentation
apidoc:
	@echo "Generating API documentation..."
	@$(CMD_PREFIX) sphinx-apidoc -o "$(SOURCEDIR)/api" $(PROJECT_ROOT)/app $(PROJECT_ROOT)/config $(PROJECT_ROOT)/handlers --force --module-first
	@echo "API documentation generated."

# Live reload documentation
livehtml:
ifdef HAS_POETRY
	@echo "Starting live documentation server..."
	@echo "Documentation will be available at: http://localhost:8000"
	@echo "Changes will auto-reload. Press Ctrl+C to stop."
	@$(CMD_PREFIX) sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
else
	@echo "Live reload requires sphinx-autobuild. Install with:"
	@echo "  pip install sphinx-autobuild"
endif

# Check for broken links
linkcheck:
	@echo "Checking for broken external links..."
	@$(CMD_PREFIX) $(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS) $(O)
	@echo "Link check complete. See $(BUILDDIR)/linkcheck/output.txt for results."

# Development targets
setup-precommit:
	@echo "🚀 Setting up Pre-commit for Spartan Framework"
	@echo "=============================================="
ifdef HAS_POETRY
	@echo "✅ Poetry found"
	@echo "📦 Installing development dependencies..."
	@$(POETRY) install --with dev
	@echo "🔗 Installing pre-commit hooks..."
	@$(POETRY) run pre-commit install
	@echo "🔍 Running initial pre-commit check..."
	@$(POETRY) run pre-commit run --all-files || { \
		echo "⚠️  Some pre-commit checks failed. This is normal for the first run."; \
		echo "   The issues should be auto-fixed. Try running 'make precommit' again."; \
	}
	@echo ""
	@echo "✅ Pre-commit setup complete!"
	@echo ""
	@echo "📋 Available commands:"
	@echo "   make setup-precommit  - Setup pre-commit hooks"
	@echo "   make precommit        - Run pre-commit on all files"
	@echo "   make format           - Format code with black and isort"
	@echo "   make lint             - Run linting checks"
	@echo "   make test             - Run tests"
	@echo "   make quality          - Run all quality checks"
	@echo ""
	@echo "🔧 Pre-commit will now run automatically on every commit!"
	@echo "   To skip pre-commit for a commit, use: git commit --no-verify"
else
	@echo "❌ Poetry is not installed. Please install Poetry first:"
	@echo "   curl -sSL https://install.python-poetry.org | python3 -"
	@echo "   Then run 'make setup-precommit' again"
	@exit 1
endif

precommit:
	@echo "Running pre-commit on all files..."
	@$(CMD_PREFIX) pre-commit run --all-files

precommit-fix:
	@echo "Running pre-commit on all files with auto-fix..."
	@$(CMD_PREFIX) pre-commit run --all-files || { \
		echo "Pre-commit found issues. Auto-fixing and running again..."; \
		$(CMD_PREFIX) pre-commit run --all-files; \
	}

format:
	@echo "Formatting code with black and isort..."
	@$(CMD_PREFIX) black .
	@$(CMD_PREFIX) isort .
	@$(CMD_PREFIX) autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables .
	@echo "Code formatting completed!"

# Lint code
lint:
	@echo "Running linting checks..."
	@./.venv/bin/flake8 . --max-line-length=88 --extend-ignore=E203,W503,E501,D,E402,E251 --exclude=.venv,docs,database/migrations,storage,tinker.py

test:
	@echo "Running tests..."
	@$(CMD_PREFIX) pytest

test-cov:
	@echo "Running tests with coverage report..."
	@$(CMD_PREFIX) pytest --cov=app --cov=config --cov=handlers --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

clean-cache:
	@echo "Cleaning Python cache files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/ .coverage
	@echo "Cache files cleaned!"

update-hooks:
ifdef HAS_POETRY
	@echo "Updating pre-commit hooks to latest versions..."
	@$(POETRY) run pre-commit autoupdate
	@echo "Pre-commit hooks updated!"
else
	@echo "Poetry not found. Cannot update hooks."
	@exit 1
endif

quality: clean-cache format lint test
	@echo ""
	@echo "✅ All quality checks completed successfully!"
	@echo "🎉 Your code is ready for commit!"

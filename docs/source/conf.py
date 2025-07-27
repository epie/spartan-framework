# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

# Mock modules that have complex dependencies for documentation building
from unittest.mock import MagicMock


class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = [
    "boto3",
    "botocore",
    "botocore.exceptions",
    "pymysql",
    "pg8000",
    "sqlalchemy",
    "sqlalchemy.engine",
    "sqlalchemy.engine.result",
    "sqlalchemy.orm",
    "sqlalchemy.ext",
    "sqlalchemy.ext.declarative",
    "aws_lambda_powertools",
    "aws_lambda_powertools.logging",
    "aws_lambda_powertools.tracing",
    "aws_xray_sdk",
    "aws_xray_sdk.core",
    "mangum",
    "alembic",
]

sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# Set mock environment variables for documentation
os.environ.setdefault("APP_NAME", "spartan-framework-docs")
os.environ.setdefault("APP_ENVIRONMENT", "development")
os.environ.setdefault("APP_DEBUG", "true")
os.environ.setdefault("ALLOWED_ORIGINS", "*")
os.environ.setdefault("LOG_LEVEL", "INFO")
os.environ.setdefault("LOG_CHANNEL", "file")
os.environ.setdefault("LOG_DIR", "/tmp/logs")
os.environ.setdefault("DB_TYPE", "mysql")
os.environ.setdefault("DB_DRIVER", "pg8000")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_NAME", "spartan_db")
os.environ.setdefault("DB_USERNAME", "user")
os.environ.setdefault("DB_PASSWORD", "password")

project = "Spartan Framework"
copyright = "2025, Sydel Palinlin"
author = "Sydel Palinlin"
release = "0.1.8"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
]

# Support for RST files only for now
# source_suffix = {
#     '.rst': None,
#     '.md': 'myst_parser',
# }

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# HTML theme options
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Type hints settings
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "boto3": ("https://boto3.amazonaws.com/v1/documentation/api/latest/", None),
    "fastapi": ("https://fastapi.tiangolo.com/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/20/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Create _static directory if it doesn't exist
import os

if not os.path.exists("_static"):
    os.makedirs("_static")

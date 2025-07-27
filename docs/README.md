# Spartan Framework Documentation

This directory contains the Sphinx documentation for the Spartan Framework.

## Building the Documentation

### Prerequisites

Make sure you have the documentation dependencies installed:

```bash
# With Poetry
poetry install --with dev

# Or with pip
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser
```

### Building HTML Documentation

To build the HTML documentation:

```bash
cd docs
make html
```

The generated documentation will be available in `build/html/index.html`.

### Auto-rebuilding Documentation

For development, you can use the live reload feature:

```bash
cd docs
make livehtml
```

This will start a local server and automatically rebuild the documentation when files change.

### Other Build Formats

```bash
# PDF (requires LaTeX)
make latexpdf

# ePub
make epub

# Check for broken links
make linkcheck

# Clean build directory
make clean
```

### Regenerating API Documentation

If you add new modules, you can regenerate the API documentation:

```bash
cd docs
make apidoc
```

This will update the RST files in `source/api/` to include any new modules.

## Documentation Structure

```
docs/
├── source/                 # Source files
│   ├── _static/           # Static files (CSS, images, etc.)
│   ├── _templates/        # Custom templates
│   ├── api/               # Auto-generated API documentation
│   ├── conf.py            # Sphinx configuration
│   ├── index.rst          # Main documentation page
│   ├── installation.rst   # Installation guide
│   ├── quickstart.rst     # Quick start guide
│   ├── contributing.rst   # Contributing guide
│   └── changelog.md       # Symlink to CHANGELOG.md
├── build/                 # Generated documentation
├── Makefile              # Build commands (Unix/macOS)
├── make.bat              # Build commands (Windows)
└── README.md             # This file
```

## Writing Documentation

### Adding New Pages

1. Create a new `.rst` or `.md` file in `source/`
2. Add it to the table of contents in `index.rst` or the appropriate parent page
3. Build the documentation to verify

### Documenting Code

Use standard Python docstrings in your code. Sphinx will automatically extract and format them:

```python
def my_function(param1: str, param2: int) -> bool:
    """Short description of the function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something goes wrong
    """
    pass
```

### Cross-referencing

Use Sphinx cross-references to link to other parts of the documentation:

```rst
See :doc:`installation` for setup instructions.
See :class:`app.models.base.BaseModel` for the base model class.
See :func:`app.helpers.database.get_session` for database sessions.
```

## Configuration

The Sphinx configuration is in `source/conf.py`. Key settings include:

- **Extensions**: Enabled Sphinx extensions
- **Theme**: Using the Read the Docs theme
- **API Documentation**: Auto-documentation settings
- **Cross-references**: Intersphinx mappings to external documentation

## Publishing

The documentation can be published to various platforms:

- **GitHub Pages**: Use the `gh-pages` branch
- **Read the Docs**: Connect your repository to readthedocs.org
- **Netlify/Vercel**: Deploy the `build/html` directory

For GitHub Pages, you can use the `sphinx.ext.githubpages` extension (already enabled) to generate the necessary files.

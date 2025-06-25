===========
Developing
===========

Developer Guide for |project| v|version|
==========================================

This guide provides information for developers working on the |project| project, including development setup, coding standards, testing procedures, and release management.

.. note::
   **Current Version:** |version| | **Release:** |release|
   
   This documentation corresponds to |project| version |version|. For the latest updates, check the `changelog <https://github.com/thsetz/Bewerbung/blob/main/CHANGELOG.md>`_.

Development Setup
=================

Prerequisites
-------------

- Python 3.12 or higher
- Git
- Virtual environment support
- Make (for using Makefile targets)

Getting Started
---------------

1. Clone the repository::

    git clone <repository-url>
    cd Bewerbung

2. Create and activate virtual environment::

    make venv

3. Install dependencies::

    make install

4. Run tests to verify setup::

    make test

Project Structure
=================

The project follows a standard Python package structure:

.. code-block:: text

    Bewerbung/
    ├── src/                    # Source code
    │   ├── __init__.py        # Package initialization and version
    │   ├── bewerbung_generator.py
    │   ├── make_release.py    # Release management script
    │   └── ...
    ├── tests/                 # Test suite
    ├── docs/                  # Documentation
    ├── templates/             # Jinja2 templates
    ├── profil/               # Profile documents
    ├── Stellenbeschreibung/  # Job descriptions
    ├── Ausgabe/              # Generated outputs
    └── Makefile              # Build automation

Testing
=======

The project includes comprehensive test coverage with multiple test categories:

Running Tests
-------------

Run all tests::

    make test

Run specific test categories::

    make test-documentation-generator
    make test-version-management
    make test-make-release
    make test-variants

Run tests with coverage::

    make test-coverage

Performance tests (separate execution)::

    make test-performance

Test Coverage
-------------

View coverage reports:

- **HTML Report**: ``docs/_static/coverage/index.html``
- **XML Report**: ``coverage.xml``

Current coverage target: **> 60%**

Documentation
=============

Building Documentation
-----------------------

Build HTML documentation::

    make docs

Build PDF documentation::

    make docs-pdf

Serve documentation locally::

    make docs-serve

The documentation is built using Sphinx and includes:

- API documentation
- User guides
- Developer documentation
- Mermaid diagrams and workflows

Release Management
==================

The project uses semantic versioning and automated changelog generation for releases.

Version Format
--------------

Versions follow `Semantic Versioning <https://semver.org/>`_:

- **MAJOR.MINOR.PATCH** (e.g., 1.0.1)
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

Release Process
---------------

The release process is automated using the ``make_release.py`` script and Makefile targets.

Prerequisites
~~~~~~~~~~~~~

Before creating a release, ensure:

1. Working directory is clean (no uncommitted changes)
2. You are in a git repository
3. All tests pass
4. Version file exists (``src/__init__.py``)

Creating Releases
~~~~~~~~~~~~~~~~~

Use the appropriate Makefile target based on the type of release:

**Patch Release** (1.0.0 → 1.0.1)::

    make release-patch

**Minor Release** (1.0.0 → 1.1.0)::

    make release-minor

**Major Release** (1.0.0 → 2.0.0)::

    make release-major

What Happens During Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you run a release target, the system automatically:

1. **Validates prerequisites**:
   - Checks for clean working directory
   - Verifies git repository status
   - Ensures version file exists

2. **Analyzes git history**:
   - Gets commits since last version tag
   - Categorizes commits by type (added, fixed, changed, etc.)

3. **Updates version**:
   - Bumps version in ``src/__init__.py``
   - Follows semantic versioning rules

4. **Generates changelog**:
   - Creates or updates ``CHANGELOG.md``
   - Uses `Keep a Changelog <https://keepachangelog.com/>`_ format
   - Categorizes changes automatically

5. **Creates git tag**:
   - Commits version and changelog changes
   - Creates annotated git tag (e.g., ``v1.0.1``)

Dry Run Mode
~~~~~~~~~~~~

Test the release process without making changes::

    python src/make_release.py --dry-run patch

This will show what changes would be made without actually modifying files.

Changelog Format
~~~~~~~~~~~~~~~~

The generated changelog follows Keep a Changelog format with these sections:

- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

Example changelog entry:

.. code-block:: markdown

    ## [1.0.1] - 2025-06-25

    ### Added
    - Add comprehensive release management system
    - Add new user authentication feature

    ### Fixed
    - Fix template rendering bug
    - Fix performance issues in test suite

Commit Message Conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~

For optimal changelog generation, use conventional commit messages:

.. code-block:: text

    feat: add new feature
    fix: resolve bug in template
    docs: update API documentation
    test: add unit tests
    refactor: improve code structure
    style: fix formatting
    chore: update dependencies

These patterns are automatically categorized in the changelog.

Testing Releases
~~~~~~~~~~~~~~~~

Test the release management system::

    make test-make-release

This runs comprehensive tests covering:

- Version parsing and bumping
- Git operations (mocked)
- Commit categorization
- Changelog generation
- Prerequisites validation
- Error handling

Manual Release Process
~~~~~~~~~~~~~~~~~~~~~~

If you need to create a release manually:

1. Update version in ``src/__init__.py``
2. Update ``CHANGELOG.md`` with new version entry
3. Commit changes::

    git add src/__init__.py CHANGELOG.md
    git commit -m "Release X.Y.Z"

4. Create and push tag::

    git tag -a vX.Y.Z -m "Version X.Y.Z"
    git push origin master --tags

Release Validation
~~~~~~~~~~~~~~~~~~

After creating a release:

1. Verify version was updated::

    python -c "from src import get_version; print(get_version())"

2. Check git tag was created::

    git tag --list

3. Review generated changelog::

    cat CHANGELOG.md

4. Verify tests still pass::

    make test

Troubleshooting
~~~~~~~~~~~~~~~

Common release issues and solutions:

**"Working directory is not clean"**
    Commit or stash your changes before releasing::

        git add .
        git commit -m "Prepare for release"

**"Not in a git repository"**
    Ensure you're in the project root directory with git initialized.

**"Version file not found"**
    Verify ``src/__init__.py`` exists and contains ``__version__`` variable.

**"No commits found"**
    This happens when there are no commits since the last tag. The release will proceed with version-only updates.

Coding Standards
================

Code Style
----------

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write comprehensive docstrings
- Maintain test coverage above 60%

Git Workflow
------------

1. Create feature branches from master
2. Make atomic commits with clear messages
3. Ensure tests pass before committing
4. Use conventional commit messages for better changelog generation
5. Create pull requests for review

Testing Standards
-----------------

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies appropriately

Documentation Standards
-----------------------

- Update documentation for new features
- Include examples in docstrings
- Keep README.md up to date
- Update this developer guide as needed

Contributing
============

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

For questions or support, please refer to the project documentation or create an issue in the repository.
# Migration from pip-tools to Poetry

## Overview

This project has been migrated from using pip-tools for dependency management to using Poetry. This document explains the migration process, benefits, and how to use Poetry for managing dependencies.

## Why Poetry?

Poetry offers several advantages over pip-tools:

1. **Unified dependency management**: Poetry handles both application dependencies and development dependencies in a single `pyproject.toml` file.

2. **Simplified workflow**: Poetry combines dependency resolution, virtual environment management, and package building in a single tool.

3. **Better dependency resolution**: Poetry has a more robust dependency resolver that can handle complex dependency graphs.

4. **Standardized configuration**: Poetry uses the PEP 518 standard `pyproject.toml` file for configuration.

5. **Improved reproducibility**: Poetry's lock file ensures that the same dependencies are installed across different environments.

## Files Affected by Migration

### Obsolete Files

The following files are no longer needed after migrating to Poetry:

- `requirements.in`: Replaced by dependencies in `pyproject.toml`
- `requirements.txt`: Replaced by `poetry.lock`
- `dev-requirements.in`: Replaced by dev-dependencies in `pyproject.toml`
- `dev-requirements.txt`: Replaced by `poetry.lock`
- `compile_requirements.py`: No longer needed as Poetry handles dependency compilation

### New Files

- `pyproject.toml`: Contains project metadata and dependencies
- `poetry.lock`: Contains locked dependencies with exact versions
- `setup_poetry.py`: Script to set up Poetry and install dependencies
- `setup_and_run_poetry.bat`/`setup_and_run_poetry.sh`: Scripts to set up Poetry and run the application

## Migration Steps

1. **Install Poetry**: Poetry has been installed in the virtual environment.

2. **Convert dependencies**: Dependencies from `requirements.in` and `dev-requirements.in` have been converted to the Poetry format in `pyproject.toml`.

3. **Install dependencies**: Dependencies have been installed using Poetry.

4. **Cleanup**: Obsolete files can be removed using the `cleanup_after_poetry.py` script.

## How to Use Poetry

### Installing Dependencies

```bash
# Install all dependencies
poetry install

# Install only production dependencies
poetry install --no-dev
```

### Adding Dependencies

```bash
# Add a production dependency
poetry add package-name

# Add a development dependency
poetry add --dev package-name

# Add a dependency with a specific version
poetry add package-name@^1.0.0
```

### Updating Dependencies

```bash
# Update all dependencies
poetry update

# Update a specific dependency
poetry update package-name
```

### Running Scripts

```bash
# Run a script in the virtual environment
poetry run python main.py

# Activate the virtual environment
poetry shell
```

## Cleanup

To clean up obsolete files after migrating to Poetry, run:

```bash
# List obsolete files
python cleanup_after_poetry.py

# Remove obsolete files
python cleanup_after_poetry.py --remove
```

## Troubleshooting

### Common Issues

1. **Dependency conflicts**: If you encounter dependency conflicts, try updating the problematic dependencies or adjusting their version constraints in `pyproject.toml`.

2. **Python version compatibility**: Ensure that your Python version is compatible with the requirements specified in `pyproject.toml`. The project requires Python 3.8.1 or higher.

3. **Missing dependencies**: If you're missing dependencies, make sure you've run `poetry install` and that the dependencies are correctly specified in `pyproject.toml`.

### Getting Help

For more information on using Poetry, refer to the [official Poetry documentation](https://python-poetry.org/docs/).
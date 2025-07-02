#!/usr/bin/env python
"""
Setup Script for Poetry-based Dependency Management

This script handles Python version checks, Poetry installation, and project setup
using Poetry for dependency management. It also integrates with dependency_resolver.py
and compatibility_checker.py for robust dependency conflict resolution.
"""

import os
import sys
import subprocess
import platform
import importlib.util
from pathlib import Path

# Minimum required Python version
MIN_PYTHON_VERSION = (3, 8, 1)

# Critical dependencies to verify
CRITICAL_DEPENDENCIES = [
    "uvicorn",
    "fastapi",
    "nicegui",
    "pydantic"
]

# Known dependency compatibility requirements
DEPENDENCY_COMPATIBILITY = {
    "nicegui": {
        "version_range": "1.4.21-1.4.24",
        "requires": {
            "fastapi": ">=0.109.1,<0.110.0"
        }
    }
}

def check_python_version():
    """Check if the current Python version meets the minimum requirement."""
    current_version = sys.version_info[:2]
    if current_version < MIN_PYTHON_VERSION:
        print(f"Error: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    return True

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("Virtual environment already exists.")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def get_python_executable():
    """Get the appropriate Python executable path based on the platform and environment."""
    if platform.system() == "Windows":
        return str(Path("venv") / "Scripts" / "python.exe")
    else:
        return str(Path("venv") / "bin" / "python")

def install_poetry():
    """Install Poetry in the virtual environment if not already installed."""
    python_path = get_python_executable()
    
    # Check if Poetry is already installed
    try:
        result = subprocess.run(
            [python_path, "-m", "pip", "show", "poetry"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Poetry is already installed.")
            return True
    except Exception:
        pass
    
    print("Installing Poetry...")
    try:
        # Install Poetry using pip
        subprocess.run(
            [python_path, "-m", "pip", "install", "poetry"],
            check=True
        )
        print("Poetry installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Poetry: {e}")
        return False

def setup_poetry_project():
    """Set up the project using Poetry."""
    python_path = get_python_executable()
    
    print("Setting up project with Poetry...")
    try:
        # Install dependencies using Poetry
        if platform.system() == "Windows":
            poetry_path = str(Path("venv") / "Scripts" / "poetry")
        else:
            poetry_path = str(Path("venv") / "bin" / "poetry")
        
        # Install dependencies
        subprocess.run(
            [python_path, "-m", "poetry", "install"],
            check=True
        )
        print("Project dependencies installed successfully.")
        
        # Run dependency resolver if available
        if os.path.exists("dependency_resolver.py"):
            print("\nRunning dependency resolver to check for conflicts...")
            try:
                subprocess.run(
                    [python_path, "dependency_resolver.py", "--check"],
                    check=True
                )
                print("✓ Dependency resolver check completed")
            except subprocess.CalledProcessError:
                print("⚠️ Dependency conflicts detected. Attempting to resolve...")
                try:
                    subprocess.run(
                        [python_path, "dependency_resolver.py", "--update"],
                        check=True
                    )
                    print("✓ Dependencies updated successfully")
                except subprocess.CalledProcessError as e:
                    print(f"✗ Failed to resolve dependency conflicts: {e}")
                    print("Please run 'python dependency_resolver.py --diagnose' for more information.")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting up project with Poetry: {e}")
        
        # Suggest using dependency resolver for diagnosis
        if os.path.exists("dependency_resolver.py"):
            print("\nTry running 'python dependency_resolver.py --diagnose' to diagnose dependency issues.")
        
        return False

def verify_critical_dependencies():
    """Verify that critical dependencies are installed."""
    print("Verifying critical dependencies...")
    
    python_path = get_python_executable()
    
    missing_deps = []
    installed_versions = {}
    
    for dep in CRITICAL_DEPENDENCIES:
        try:
            # Use the virtual environment's Python to check for the dependency and its version
            result = subprocess.run(
                [python_path, "-c", f"import {dep}; print('{dep}:' + getattr({dep}, '__version__', 'unknown'))"],
                capture_output=True,
                text=True,
                check=True
            )
            version_output = result.stdout.strip()
            if ':' in version_output:
                dep_name, version = version_output.split(':', 1)
                installed_versions[dep_name] = version
                print(f"✓ {dep} is installed (version {version})")
            else:
                print(f"✓ {dep} is installed (version unknown)")
        except subprocess.CalledProcessError:
            missing_deps.append(dep)
            print(f"✗ {dep} is missing")
    
    if missing_deps:
        print("\nWarning: Some critical dependencies are missing:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease try running the setup again or install them manually.")
        return False
    
    # Check for dependency compatibility issues
    compatibility_issues = check_dependency_compatibility(installed_versions)
    if compatibility_issues:
        print("\nWarning: Dependency compatibility issues detected:")
        for issue in compatibility_issues:
            print(f"  - {issue}")
        print("\nThe application may not function correctly due to these compatibility issues.")
        print("Poetry should have resolved these issues. Please check your pyproject.toml file.")
        return False
    
    # Run compatibility checker if available
    if os.path.exists("compatibility_checker.py"):
        print("\nRunning compatibility checker...")
        try:
            subprocess.run(
                [python_path, "compatibility_checker.py"],
                check=True
            )
        except subprocess.CalledProcessError:
            print("⚠️ Compatibility issues detected. Please review the output above.")
            return False
    
    print("All critical dependencies are installed and compatible.")
    return True

def check_dependency_compatibility(installed_versions):
    """Check for known dependency compatibility issues."""
    issues = []
    
    # Check NiceGUI and FastAPI compatibility
    if 'nicegui' in installed_versions and 'fastapi' in installed_versions:
        nicegui_version = installed_versions['nicegui']
        fastapi_version = installed_versions['fastapi']
        
        # NiceGUI 1.4.21-1.4.24 requires FastAPI <0.110.0, >=0.109.1
        if nicegui_version.startswith('1.4.2'):
            try:
                from packaging import version
                if version.parse(fastapi_version) >= version.parse('0.110.0'):
                    issues.append(f"NiceGUI {nicegui_version} requires FastAPI <0.110.0, but {fastapi_version} is installed")
            except ImportError:
                # Simple string comparison if packaging is not available
                major, minor, patch = fastapi_version.split(".", 2)
                if int(major) > 0 or int(minor) >= 110:
                    issues.append(f"NiceGUI {nicegui_version} requires FastAPI <0.110.0, but {fastapi_version} is installed")
    
    return issues

def print_activation_instructions():
    """Print instructions for activating the virtual environment."""
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    
    print("\nAfter activation, you can run the application with:")
    print("  python main.py")
    
    print("\nTo manage dependencies with Poetry:")
    print("  poetry add <package>      # Add a new dependency")
    print("  poetry remove <package>   # Remove a dependency")
    print("  poetry update            # Update all dependencies")
    print("  poetry show              # List all dependencies")

def main():
    """Main setup function."""
    print("=== Project Setup with Poetry ===")
    
    if not check_python_version():
        return False
    
    if not create_venv():
        return False
    
    if not install_poetry():
        print("Warning: Failed to install Poetry. Will try to continue with pip.")
        return False
    
    if not setup_poetry_project():
        print("Warning: Failed to set up project with Poetry.")
        return False
    
    if not verify_critical_dependencies():
        print("Setup completed with warnings.")
    else:
        print("\nSetup completed successfully!")
    
    print_activation_instructions()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""Build and publish tiktok-live-api to PyPI.

Usage:
    # First time: set your PyPI token
    # Linux/macOS:  export PYPI_TOKEN=pypi-...
    # Windows CMD:  set PYPI_TOKEN=pypi-...
    # PowerShell:   $env:PYPI_TOKEN="pypi-..."

    python deploy.py          # Build and upload
    python deploy.py --test   # Upload to TestPyPI instead
"""

import os
import shutil
import subprocess
import sys


def main():
    use_test = "--test" in sys.argv

    token = os.environ.get("PYPI_TOKEN", "")
    if not token:
        print("Error: PYPI_TOKEN environment variable is not set.")
        print()
        print("Get your token from:")
        if use_test:
            print("  https://test.pypi.org/manage/account/#api-tokens")
        else:
            print("  https://pypi.org/manage/account/#api-tokens")
        print()
        print("Then set it:")
        print('  PowerShell:   $env:PYPI_TOKEN="pypi-..."')
        print("  CMD:          set PYPI_TOKEN=pypi-...")
        print("  Linux/macOS:  export PYPI_TOKEN=pypi-...")
        sys.exit(1)

    # Clean previous builds
    for path in ("dist", "build"):
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Cleaned {path}/")

    # Build
    print("\nBuilding package...")
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        check=False,
    )
    if result.returncode != 0:
        print("Build failed.")
        sys.exit(1)

    # Upload
    repo_url = (
        "https://test.pypi.org/legacy/"
        if use_test
        else "https://upload.pypi.org/legacy/"
    )
    target = "TestPyPI" if use_test else "PyPI"
    print(f"\nUploading to {target}...")

    result = subprocess.run(
        [
            sys.executable, "-m", "twine", "upload",
            "--repository-url", repo_url,
            "--username", "__token__",
            "--password", token,
            "--non-interactive",
            "dist/*",
        ],
        check=False,
    )
    if result.returncode != 0:
        print(f"\nUpload to {target} failed.")
        print("Common issues:")
        print("  - Version already exists: bump version in pyproject.toml")
        print("  - Invalid token: check PYPI_TOKEN value")
        sys.exit(1)

    print(f"\nPublished to {target}!")
    if use_test:
        print("  https://test.pypi.org/project/tiktok-live-api/")
        print("  pip install -i https://test.pypi.org/simple/ tiktok-live-api")
    else:
        print("  https://pypi.org/project/tiktok-live-api/")
        print("  pip install tiktok-live-api")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
MyPy runner script for CI/CD pipeline.
This ensures mypy runs correctly regardless of PATH configuration.
"""
import subprocess
import sys


def main():
    """Run mypy with the provided arguments."""
    # Get all command line arguments except the script name
    args = sys.argv[1:]

    # Run mypy with python -m to ensure it works in any environment
    cmd = [sys.executable, "-m", "mypy"] + args

    # Execute and return the exit code
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

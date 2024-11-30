#!/usr/bin/env python3
"""
Run the test suite with coverage reporting.
"""
import subprocess
import sys

def run_tests():
    """Run pytest with coverage"""
    try:
        # Run pytest with coverage
        cmd = [
            "pytest",
            "-v",
            "--cov=please",
            "--cov-report=term-missing",
            "tests/"
        ]
        subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(run_tests())

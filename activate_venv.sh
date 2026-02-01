#!/bin/bash
# Activate the py-ta virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"
echo "Python: $(python --version)"
echo "py-ta version: $(python -c 'import py_ta; print(py_ta.__version__)')"

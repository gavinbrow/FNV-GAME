@echo off
python -I "%~dp0verify_contrib.py" 12 && python -I "%~dp0assemble_contrib.py"

@echo off
REM Set up a virtual environment if not already present
if not exist venv (
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Run your main script (replace 'main.py' with your script name)
python main.py

REM Deactivate the virtual environment
call venv\Scripts\deactivate

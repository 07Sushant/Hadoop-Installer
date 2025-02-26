@echo off
echo Checking required Python packages...

:: Define the list of required packages
set PACKAGES=pillow gdown

:: Check and install missing packages
for %%p in (%PACKAGES%) do (
    python -c "import %%p" 2>nul
    if errorlevel 1 (
        echo Installing %%p...
        pip install %%p
    )
)

echo All dependencies are installed.
echo Running Hadoop_Installer.py...

:: Run the Python script
python Hadoop_Installer.py

exit

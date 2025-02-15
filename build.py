
import PyInstaller.__main__
import os
import shutil

# Clean previous builds
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Build main.py
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--name=felix',
    '--icon=felix_logo.ico',
])

# Build ide.py
PyInstaller.__main__.run([
    'ide.py',
    '--onefile',
    '--name=felix-ide',
    '--icon=felix_logo.ico',
])

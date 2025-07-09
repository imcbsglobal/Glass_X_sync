import os
import shutil
import subprocess
import zipfile

# Configuration
PYTHON_EXECUTABLE = "python"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
SPEC_FILE = "sync.spec"

# Install PyInstaller if needed
subprocess.run([PYTHON_EXECUTABLE, "-m", "pip",
               "install", "pyinstaller"], check=True)

# Clean previous builds
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
if os.path.exists(SPEC_FILE):
    os.remove(SPEC_FILE)

# Build EXE
subprocess.run([
    PYTHON_EXECUTABLE, "-m", "PyInstaller",
    "--onefile", "--noconsole",
    "--add-data", "config.json;.",
    "--add-data", "table_mapping.py;.",
    "sync.py"
], check=True)

# Prepare folder
if os.path.exists("sync_tool"):
    shutil.rmtree("sync_tool")
os.makedirs("sync_tool", exist_ok=True)

# Copy files
shutil.copy(os.path.join(OUTPUT_DIR, "sync.exe"), "sync_tool")
shutil.copy("config.json", "sync_tool")
shutil.copy("table_mapping.py", "sync_tool")
shutil.copy("sync.bat", "sync_tool")
shutil.copy("sync_silent.vbs", "sync_tool")

# # Create log and readme
# open(os.path.join("sync_tool", "sync.log"), "w").close()

with open(os.path.join("sync_tool", "README.txt"), "w") as f:
    f.write("""DATABASE SYNC TOOL
=================

1. Edit config.json with DB and API details.
2. Run sync.bat to start sync.
3. Logs saved in sync.log.
4. For silent run, double-click sync_silent.vbs.
""")

# Create ZIP
# with zipfile.ZipFile("sync_tool.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
#     for root, dirs, files in os.walk("sync_tool"):
#         for file in files:
#             file_path = os.path.join(root, file)
#             arcname = os.path.relpath(file_path, "sync_tool")
#             zipf.write(file_path, arcname)

# print("✅ Build complete. Zip created: sync_tool.zip")

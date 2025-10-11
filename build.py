import os
import shutil
import subprocess
import zipfile

# Configuration
PYTHON_EXECUTABLE = "python"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
SPEC_FILE = "sync.spec"

print("🔧 Installing PyInstaller...")
subprocess.run([PYTHON_EXECUTABLE, "-m", "pip", "install", "pyinstaller"], check=True)

# Clean previous builds
print("🧹 Cleaning previous builds...")
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
if os.path.exists(SPEC_FILE):
    os.remove(SPEC_FILE)

# Create a wrapper script that keeps terminal open
print("📝 Creating sync wrapper...")
with open("sync_wrapper.py", "w", encoding="utf-8") as f:
    f.write("""import json
from fetch_data import fetch_all_tables
from api_client import push_bulk_data
from utils import log, setup_logging

def run_sync():
    setup_logging()
    log("🚀 Starting Bulk Sync Process (Single Request for All Tables)")

    try:
        with open("config.json") as f:
            config = json.load(f)
    except Exception as e:
        log(f"❌ Error loading config.json: {e}")
        input("\\nPress Enter to exit...")
        return

    dsn = config.get("dsn")
    api_url = config.get("api_url")
    client_id = config.get("client_id")

    if not all([dsn, api_url, client_id]):
        log("❌ Missing required config values (dsn, api_url, client_id)")
        input("\\nPress Enter to exit...")
        return

    try:
        # Fetch all table data from DSN
        all_data = fetch_all_tables(dsn)

        if not all_data:
            log("❌ No data fetched. Exiting.")
            input("\\nPress Enter to exit...")
            return

        log(f"📦 Tables fetched: {list(all_data.keys())}")

        # Push all table data in one call
        success = push_bulk_data(api_url, client_id, all_data)

        if success:
            log("✅ Bulk sync completed successfully!")
        else:
            log("❌ Bulk sync failed.")

    except Exception as e:
        log(f"🔥 Unexpected error during sync: {e}")
    
    # Keep terminal open
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    run_sync()
""")

# Build EXE with console enabled
print("🔨 Building executable...")
subprocess.run([
    PYTHON_EXECUTABLE, "-m", "PyInstaller",
    "--onefile",
    "--console",  # Changed to --console to show terminal
    "--add-data", "config.json;.",
    "--add-data", "table_mapping.py;.",
    "--name", "GlassXSync",
    "--icon", "NONE",
    "sync_wrapper.py"
], check=True)

# Clean up wrapper
if os.path.exists("sync_wrapper.py"):
    os.remove("sync_wrapper.py")

# Prepare folder
print("📁 Creating sync_tool folder...")
if os.path.exists("sync_tool"):
    shutil.rmtree("sync_tool")
os.makedirs("sync_tool", exist_ok=True)

# Copy files
print("📋 Copying files...")
shutil.copy(os.path.join(OUTPUT_DIR, "GlassXSync.exe"), "sync_tool")
shutil.copy("config.json", "sync_tool")
shutil.copy("table_mapping.py", "sync_tool")

# Create an enhanced batch file
print("📝 Creating batch files...")
with open(os.path.join("sync_tool", "sync.bat"), "w", encoding="utf-8") as f:
    f.write("""@echo off
title Glass X Database Sync Tool
color 0A
echo ========================================
echo   GLASS X DATABASE SYNC TOOL
echo ========================================
echo.
GlassXSync.exe
echo.
echo ========================================
echo   Sync Process Completed
echo ========================================
echo.
pause
""")

# Create README
print("📄 Creating README...")
with open(os.path.join("sync_tool", "README.txt"), "w", encoding="utf-8") as f:
    f.write("""GLASS X DATABASE SYNC TOOL
===========================

SETUP:
------
1. Edit config.json with your database DSN, API URL, and Client ID
2. Ensure table_mapping.py contains correct table definitions

USAGE:
------
Option 1: Double-click GlassXSync.exe
         - Opens terminal window
         - Shows real-time sync progress
         - Terminal stays open until you press a key

Option 2: Run sync.bat
         - Same as Option 1 but with formatted header/footer
         - Recommended for better visibility

CONFIGURATION:
--------------
config.json structure:
{
  "dsn": "YOUR_DSN_NAME",
  "api_url": "https://your-api-url.com/",
  "client_id": "YOUR_CLIENT_ID"
}

LOGS:
-----
- All operations are logged to sync.log
- Check this file for detailed execution history

TROUBLESHOOTING:
----------------
- Ensure database DSN is configured in ODBC Data Sources
- Verify API URL is accessible
- Check sync.log for error details
- Ensure all required Python dependencies are included

For support, contact your system administrator.
""")

# Create a startup info file
with open(os.path.join("sync_tool", "HOW_TO_RUN.txt"), "w", encoding="utf-8") as f:
    f.write("""QUICK START GUIDE
=================

To run the sync:
1. Double-click "GlassXSync.exe"
   OR
2. Double-click "sync.bat"

The terminal will show:
- Starting message
- Tables being fetched
- Upload progress
- Success/failure status
- Completion message

The terminal will wait for you to press a key before closing.
""")

print("✅ Build complete!")
print(f"📦 Output folder: sync_tool/")
print(f"🚀 To run: Double-click sync_tool/GlassXSync.exe")
print()
print("Files created:")
print("  - GlassXSync.exe (main executable)")
print("  - config.json (configuration)")
print("  - table_mapping.py (table definitions)")
print("  - sync.bat (batch launcher)")
print("  - README.txt (documentation)")
print("  - HOW_TO_RUN.txt (quick guide)")
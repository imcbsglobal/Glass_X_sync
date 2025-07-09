import os
import datetime
import sys

# ✅ Set UTF-8 encoding for stdout (safe for modern terminals)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # For Python versions < 3.7 or environments without reconfigure
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)

# ✅ Go one level up to make sure logs go into project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "sync.log")

os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")  # Clear the log file

def log(message, icon="ℹ️"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"{icon} [{timestamp}] {message}"

    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode('ascii', 'replace').decode())

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except UnicodeEncodeError:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line.encode('ascii', 'replace').decode() + "\n")

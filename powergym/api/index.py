import os
import sys

# Get the absolute path to the directory containing this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# The project root is one level up
project_root = os.path.join(current_dir, '..')
# Add to sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# Debug: Print sys.path to logs
print(f"Current Dir: {current_dir}")
print(f"Project Root: {project_root}")
print(f"Sys Path: {sys.path}")

try:
    from powergym_project.wsgi import app
    # Vercel looks for the 'app' variable in the root of the file
    handler = app
except ImportError as e:
    print(f"Import Error: {e}")
    # List files in project root to debug
    try:
        print(f"Files in {project_root}: {os.listdir(project_root)}")
    except Exception as list_err:
        print(f"Could not list dir: {list_err}")
    raise e

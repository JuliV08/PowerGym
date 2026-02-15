import os
import sys

# Add the project directory to the sys.path so Django can find its modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from powergym_project.wsgi import app

# Vercel looks for the 'app' variable in the root of the file
handler = app

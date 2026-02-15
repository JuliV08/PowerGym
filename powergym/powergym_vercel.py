import os
import sys

# Add the project directory to the sys.path so Django can find its modules
sys.path.append(os.path.dirname(__file__))

# Import the WSGI app from the project folder
from powergym_project.wsgi import app

# Vercel looks for 'app' or 'application'
application = app

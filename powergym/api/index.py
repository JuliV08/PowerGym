import os
import sys
from django.core.wsgi import get_wsgi_application

# Set up paths explicitly
current_dir = os.path.dirname(os.path.abspath(__file__)) # powergym/api
project_root = os.path.dirname(current_dir) # powergym
sys.path.append(project_root)

# Force settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'powergym_project.settings.production')

# Load the application directly
try:
    app = get_wsgi_application()
    print("WSGI Application loaded successfully.")
except Exception as e:
    print(f"Failed to load WSGI application: {e}")
    # Create a dummy app to prevent 500 crash effectively, allowing logs to show
    def fallback_app(environ, start_response):
        status = '500 Internal Server Error'
        output = f"Critical Error loading Django: {e}".encode('utf-8')
        response_headers = [('Content-type', 'text/plain'),
                            ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return [output]
    app = fallback_app

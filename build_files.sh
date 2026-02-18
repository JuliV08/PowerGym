# build_files.sh
# Ensure we are in the project directory
# build_files.sh
# Ensure we are in the project directory
# cd powergym || echo "Already in root or powergym dir"


# Create and activate a virtual environment
python3.12 -m venv build_venv
source build_venv/bin/activate

# Install dependencies into the virtual environment
pip install -r requirements.txt

# Run collectstatic using the virtual environment's python
python3 manage.py collectstatic --noinput --clear --verbosity 2



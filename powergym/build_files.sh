# build_files.sh
# Ensure we are in the project directory
cd powergym || echo "Already in root or powergym dir"

pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear --verbosity 2



# build_files.sh
pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
mkdir -p staticfiles_build/static
cp -r static/* staticfiles_build/static/ 2>/dev/null || :


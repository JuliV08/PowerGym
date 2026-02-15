# build_files.sh
pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/ 2>/dev/null || :
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || :


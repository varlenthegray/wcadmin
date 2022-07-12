find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*.sqlite3"  -delete
pip install --upgrade --force-reinstall  Django~=4.0.6
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
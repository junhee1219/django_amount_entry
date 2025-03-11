# django_amount_entry

#run database
docker-compose up -d

#make venv
python -m venv amount

#activate venv
  linux:
    source amount/bin/activate
  windows:
    amount/Scripts/activate 

#install
pip intall -r requirements

#confirm
django-admin --version

#run(dev)
python manage.py runserver

#run(prd)
gunicorn entry_project.wsgi:application --bind 0.0.0.0:8000 --workers 3

#migrate
python manage.py makemigrations (options) module
python manage.py migrate
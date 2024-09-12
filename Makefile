migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

user:
	python3 manage.py createsuperuser --username omonjon

sort:
	black .
	isort .

req:
	pip freeze > requirements.txt

app:
	python3 manage.py startapp $(name)
    # make app name=mynewapp

run:
	python3 manage.py runserver

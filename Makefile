mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser --username=ravshanjon --email=test@gmail.com

test:
	python3 manage.py test

check:
	black .
	isort .

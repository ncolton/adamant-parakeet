pip: dev-requirements.txt requirements.txt
	pip install --upgrade -r dev-requirements.txt

tests:
	cd parakeet; python manage.py test

pep8:
	pep8 .

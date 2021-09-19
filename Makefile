deps:
	pip install --upgrade pip pip-tools
	pip-compile requirements.in
	pip-compile dev-requirements.in

	pip-sync requirements.txt dev-requirements.txt

lint:
	isort backend
	flake8 backend

test:
	cd backend && pytest
	rm -r backend/media/recipes

coverage:
	cd backend && pytest --cov=./ --cov-report=xml

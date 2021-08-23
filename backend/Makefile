deps:
	pip install --upgrade pip pip-tools
	pip-compile requirements.in
	pip-sync requirements.txt

lint:
	isort .
	cd .. && flake8 backend

test:
	pytest
	rm -r media/recipes

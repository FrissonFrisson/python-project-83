install:
	poetry self update
	poetry install
dev:
	poetry run flask --app page_analyzer:app run
lint:
	poetry run flake8 page_analyzer
	
test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

PORT ?= 8000
start:
	poetry run gunicorn -w 5poetry -b 0.0.0.0:$(PORT) page_analyzer:app
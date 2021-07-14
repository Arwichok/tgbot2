include .env
export


dev:
	python -m app


prod:
	python -m app


test:
	pytest tests


wsgi:
	gunicorn -c python:app.utils.config


migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "${m}"

downgrade:
	alembic downgrade -1

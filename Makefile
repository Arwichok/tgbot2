include config/.env

dev:
	python -m app


prod:
	ENV_FOR_DYNACONF=production \
	python -m app


test:
	ENV_FOR_DYNACONF=testing \
	pytest tests


wsgi:
	gunicorn -c python:app.utils.config


autogen:
	alembic -c config/alembic.ini revision --autogenerate -m $(m)

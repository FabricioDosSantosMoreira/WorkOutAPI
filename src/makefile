.PHONY: run create-migrations run-migrations first-run

run:
	@cd api && uvicorn main:app --reload --port 8080

create-migrations:
	@alembic -c alembic/alembic.ini revision --autogenerate -m "$(m)"

run-migrations:
	@alembic -c alembic/alembic.ini upgrade head

first-run: create-migrations run-migrations run
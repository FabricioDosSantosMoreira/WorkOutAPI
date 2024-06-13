run:
	@uvicorn main:app --reload --port 8080

create-migrations:
	@alembic revision --autogenerate -m "$(m)"

run-migrations:
	@alembic upgrade head
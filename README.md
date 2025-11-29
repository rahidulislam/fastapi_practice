### alembic package configuration
pip install alembic
alembic init -t async migrations

### alembic migration
alembic revision --autogenerate -m "Initial migration"

### alembic upgrade
alembic upgrade head
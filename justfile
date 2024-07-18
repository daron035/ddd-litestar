DC := "docker compose"
EXEC := "docker exec -it"
LOGS := "docker logs"
ENV := "--env-file .env"
APP_FILE := "docker_compose/app.yaml"

# Show help message
help:
    just -l

# Litestar run
run:
  uvicorn src.presentation.api.main:create_app --reload

# Install package with dependencies
install:
	poetry install --with dev,test,lint --no-root

# Run pre-commit
lint:
	just _py pre-commit run --all-files

# Run tests
test *args:
  just _py pytest {{args}}

# Run test coverage
cov:
  just _py pytest --cov=src tests

# Up container
up:
  docker compose --profile api up --build -d

# Downd container
down:
  docker compose --profile api down

_py *args:
    poetry run {{args}}

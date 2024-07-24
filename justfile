DC := "docker compose"
EXEC := "docker exec -it"
LOGS := "docker logs"
ENV := "--env-file .env"
APP_FILE := "docker_compose/app.yaml"
package_dir := "src"

# Show help message
help:
    just -l

# Litestar run
run:
  # $(py) python -m {{package_dir}}
  uvicorn src.presentation.api.main:init_api --reload

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

# Up all container
all:
  docker compose --profile api up --build -d

# App logs
logs:
  docker logs -f litestar.api

# Kafka logs
messaging-logs:
  docker compose --profile kafka logs -f

_py *args:
  poetry run {{args}}

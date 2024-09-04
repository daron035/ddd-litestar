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


# Kafka setup
kafka-setup:
  echo "Waiting for Kafka to be ready..."
  docker exec -it main-kafka cub kafka-ready -b kafka:29092 1 20

  # echo "Creating topics if they do not exist..."
  docker exec -it main-kafka kafka-topics --create --topic Chat --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server kafka:29092
  docker exec -it main-kafka kafka-topics --create --topic Message --partitions 2 --replication-factor 1 --if-not-exists --bootstrap-server kafka:29092

  # Alter partitions for existing topics
  # docker exec -it main-kafka kafka-topics --alter --topic Chat --partitions 10 --bootstrap-server kafka:29092
  # docker exec -it main-kafka kafka-topics --alter --topic Message --partitions 40 --bootstrap-server kafka:29092

  echo "Topics updated!"


# Alembic migrate
migrate:
	alembic upgrade head


# Alembic migrations
makemigrations:
	alembic revision --autogenerate -m="$(m)"


# Alembic downgrade
downgrade:
	alembic downgrade -1


_py *args:
  poetry run {{args}}

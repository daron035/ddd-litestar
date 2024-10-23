DC := "docker compose"
EXEC := "docker exec -it"
LOGS := "docker logs"
ENV := "--env-file .env"
APP_FILE := "docker_compose/app.yaml"
package_dir := "src"

# Show help message
help:
    just -l

# Fastapi run
run:
  python -Om src

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

# Up all containers
all:
  docker compose --profile api \
    --profile postgres_db \
    --profile mongo_db \
    --profile kafka up --build -d

# Up all containers
elk:
  docker compose --profile api \
    --profile postgres_db \
    --profile mongo_db \
    --profile elk \
    --profile kafka up --build -d

# Dev mod (KAFKA_ADVERTISED_LISTENERS)
dev:
  docker compose \
    --profile postgres_db \
    --profile mongo_db \
    --profile kafka up --build -d

# Api logs
logs:
  docker logs -f user_service.api

# Exec -it api
api:
  {{EXEC}} user_service.api sh

# Exec -it postgres
postgres:
  {{EXEC}} user_service.postgres psql -U admin -d postgres_db

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

# Alembic migrations
makemigrations message="$(m)":
	alembic revision --autogenerate -m="{{message}}"

# Alembic migrate
migrate:
	alembic upgrade head

# Alembic downgrade
downgrade:
	alembic downgrade -1

# # Run migration for postgres database
# migrate:
# 	docker compose --profile migration up --build

_py *args:
  poetry run {{args}}

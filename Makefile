compose-install:
	docker compose build
	docker compose run --rm web alembic upgrade head

dev:
	poetry run fastapi dev memesapi/main.py

compose-dev:
	docker compose up -d --remove-orphans
	make dev

start:
	make migrate
	poetry run fastapi run memesapi/main.py

compose-start:
	docker compose up -d --remove-orphans
	make start

compose-full-start:
	docker compose --profile full up --remove-orphans

lint:
	poetry run ruff check

lint_fix:
	poetry run ruff check --fix

format:
	poetry run ruff format

test:
	docker compose -f docker-compose-test.yml up -d --remove-orphans
	trap 'docker compose -f docker-compose-test.yml stop' EXIT && poetry run pytest -vv -s

check_in_ci_cd:
	make lint
	docker compose -f docker-compose-test.yml build
	make test

start_db:
	docker compose start db

# make migrations is not working for some reason
# make: 'migrations' is up to date.
db_migrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

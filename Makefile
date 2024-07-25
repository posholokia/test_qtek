DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
APP_FILE = ./docker/app.yml
APP_CONTAINER = fastapi
STOR_FILE = ./docker/storage.yml
DB_CONTAINER = test_db
ALEMBIC_MIGRATIONS = alembic revision --autogenerate


.PHONY: run
run:
	${DC} -f ${STOR_FILE} up -d
	${DC} -f ${APP_FILE} up --build -d
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: app
app:
	${DC} -f ${APP_FILE} up --build -d

.PHONY: stor
stor:
	${DC} -f ${STOR_FILE} up --build -d

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} {ALEMBIC_MIGRATIONS} -m "${COMMIT}"

.PHONY: down
down:
	${DC} -f ${APP_FILE} down
	${DC} -f ${STOR_FILE} down
.PHONY: run

default: run

define set-default-container
	ifndef c
	c = django
	else ifeq (${c},all)
	override c=
	endif
endef

set-container:
	$(eval $(call set-default-container))

build: set-container
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build ${c}

prod:
	docker compose up -d --force-recreate ${c}

up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --force-recreate ${c}

restart: set-container
	docker compose restart ${c}

stop: set-container
	docker compose stop ${c}

down:
	docker compose down

exec: set-container
	docker compose exec ${c} /bin/bash

logs: set-container
	docker compose logs -f ${c}

makemigrations:
	docker compose exec server ./manage.py makemigrations

migrate:
	docker compose exec server ./manage.py migrate

collectstatic:
	docker compose exec server ./manage.py collectstatic --noinput

build-static:
	docker compose up --force-recreate frontend

frontend: build-static collectstatic

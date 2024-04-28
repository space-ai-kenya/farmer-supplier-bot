# Makefile for managing Docker containers

# Variables


# Targets
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "\n Product of SpaceAI.io Kenya 2024 \n"
	@echo "---------------------------------------------"
	@echo "Targets:"
	@echo "  build              Build containers"
	@echo "  start              Start containers"
	@echo "  stop               Stop containers"
	@echo "  restart            Restart containers"
	@echo "  logs               Display container logs"
	@echo "  down               Stop and remove containers"
	@echo "  clean              Remove all volumes and data"
	@echo "  run-service NAME   Run a specific service"
	@echo "---------------------------------------------"

.PHONY: build
build:
	sudo docker compose  build

.PHONY: start
start:
	sudo docker compose  up -d --build

.PHONY: stop
stop:
	sudo docker compose  stop

.PHONY: restart
restart: stop start

.PHONY: logs
logs:
	@read -p "Enter service name to follow logs: " SERVICE_NAME; \
	sudo docker compose  logs -f $$SERVICE_NAME

.PHONY: down
down:
	sudo docker compose  down -v

.PHONY: clean
clean: down
	sudo docker compose  rm -f
	sudo docker volume rm $(shell docker volume ls -q)
	sudo docker system prune -a

.PHONY: run-service
run-service:
	@read -p "Enter service name: " SERVICE_NAME; \
	sudo docker compose  up -d $$SERVICE_NAME --build

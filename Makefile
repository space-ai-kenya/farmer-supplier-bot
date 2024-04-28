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
	docker compose  build

.PHONY: start
start:
	docker compose  up -d

<<<<<<< HEAD
# -------- production
production: 
	echo "deploying to production"
=======
.PHONY: stop
stop:
	docker compose  stop

.PHONY: restart
restart: stop start

.PHONY: logs
logs:
	@read -p "Enter service name to follow logs: " SERVICE_NAME; \
	docker compose  logs -f $$SERVICE_NAME

.PHONY: down
down:
	docker compose  down -v

.PHONY: clean
clean: down
	docker compose  rm -f
	docker volume rm $(shell docker volume ls -q)
# rm -rf ./mongo_data
# rm -rf ./mysql_data
# rm -rf ./pg_db

.PHONY: run-service
run-service:
	@read -p "Enter service name: " SERVICE_NAME; \
	docker compose  up -d $$SERVICE_NAME --build
>>>>>>> main

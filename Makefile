.PHONY: stop remove rebuild

stop:
    @containers=$$(docker ps -aq); \
    if [ -n "$$containers" ]; then \
    	docker stop $$containers; \
    else \
        echo "No containers to stop."; \
    fi

remove: stop
    @containers=$$(docker ps -aq); \
    if [ -n "$$containers" ]; then \
        docker rm $$containers; \
    else \
        echo "No containers to remove."; \
    fi

# RECREATE DOCKER BUILD
rebuild: remove
	docker-compose up --build

.PHONY: up down build

build:
	docker-compose up --build

containers-up:
	docker-compose up

containers-down:
	docker-compose down

.PHONY: help build up down logs restart clean deploy ssl-init

help:
	@echo "Available commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - View logs from all services"
	@echo "  make restart    - Restart all services"
	@echo "  make clean      - Remove containers and volumes"
	@echo "  make deploy     - Deploy the application"
	@echo "  make ssl-init   - Initialize SSL certificates"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

clean:
	docker-compose down -v
	rm -rf data/certbot

deploy:
	./deploy.sh

ssl-init:
	./init-letsencrypt.sh
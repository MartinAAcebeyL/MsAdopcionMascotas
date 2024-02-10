run:
	docker-compose up
rerun:
	docker-compose up --build
down:
	docker-compose down
test:
	docker-compose exec app python -m pytest
app_entry:
	docker-compose exec app bash
monguito_entry:
	docker exec -it monguito sh
delete_cache:
	find . -name '__pycache__' -type d -exec rm -rf {} +
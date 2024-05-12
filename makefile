run:
	docker compose up
rerun:
	docker compose up --build
down:
	docker compose down
test:
	docker compose exec app python -m pytest
app_entry:
	docker compose exec app bash
app_migrate:
	python adoption_ms/manage.py makemigrations
	python adoption_ms/manage.py migrate
delete_cache:
	find . -name '__pycache__' -type d -exec rm -rf {} +
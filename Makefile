start-services:
	docker compose up -d

rebuild:
	docker compose up --build -d

help:
	docker compose run app

popula-db:
	docker compose run --rm app python src/tp1_3.2.py --input /data/amazon-meta.txt

gera-csv:
	docker compose run --rm app python src/tp1_3.3.py --output out

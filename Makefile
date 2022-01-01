-include .env
export

.PHONY: setup
setup: venv pip db-create db-migrate

venv:
	./setup-venv.sh

.PHONY: pip
pip: venv
	./venv/bin/python -m pip install -r requirements.txt

.PHONY: run
run:
	flask run -h 127.0.0.1 -p 8000

.PHONY: db-setup 
db-create: venv
	./create-db.sh

.PHONY: db-migrate
db-migrate:
	./venv/bin/python -m flask db migrate -d server/migrations

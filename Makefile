.PHONY: setup pip
setup: venv pip

venv:
	./setup-venv.sh

pip: venv
	./venv/bin/python -m pip install -r requirements.txt

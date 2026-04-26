setup:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt

test:
	. .venv/bin/activate && PYTHONPATH=src pytest -q

run:
	. .venv/bin/activate && set -a && . ./.env && set +a && PYTHONPATH=src python -m bot.main

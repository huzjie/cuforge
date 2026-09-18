.PHONY: doctor train eval serve test install

install:
	pip install -e ".[serve,yaml]"

doctor:
	python -m cuforge.cli.main doctor

train:
	python -m cuforge.cli.main train --episodes 64

eval:
	python -m cuforge.cli.main eval

serve:
	python -m cuforge.cli.main serve --port 8000

test:
	python -m pytest -q

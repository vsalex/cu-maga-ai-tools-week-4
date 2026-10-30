.PHONY: setup check

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install -e . pytest

check:
	.venv/bin/python -m pytest

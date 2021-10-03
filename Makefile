#PYTHON = 'poetry run python'
PYTHON = 'python3.9'

all:
	$(PYTHON) make.py
examples: FORCE
	cd examples ; make
FORCE:

#PYTHON = poetry run python
PYTHON = python3.9

PEGEN_PATH = ../pegen/src
PEGEN = PYTHONPATH=$(PEGEN_PATH) $(PYTHON) -m pegen 

parse.py: parseltongue.gram
	$(PEGEN) parseltongue.gram

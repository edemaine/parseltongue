#PYTHON = poetry run python
PYTHON = python3.9
PARSELTONGUE = PYTHONPATH="../pegen/src" $(PYTHON) ../src

%.py: %.pt ../src/*.py
	$(PARSELTONGUE) $<

all: simple.py

#PYTHON = poetry run python
PYTHON = python3.9
PARSELTONGUE = PYTHONPATH="../pegen/src" $(PYTHON) ../src

%.py: %.pt
	$(PARSELTONGUE) $<

all: simple.py

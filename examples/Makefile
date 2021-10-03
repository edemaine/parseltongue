#PYTHON = poetry run python
PYTHON = python3.9
PARSELTONGUE = $(PYTHON) ../lib

%.py: %.pt ../lib/*.py
	$(PARSELTONGUE) $<

all: simple.py

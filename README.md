# Parseltongue: Better Python

## Features So Far

* `if`, `elif`, `else`, `while` do not need colons after the condition,
  except when using one-line `if`, `elif`, `while`.

  ```py
  if x > 10
    print('big')
  elif x >= 0
    print('small')
  else print('negative')
  ```
* `unless` shorthand for `if not`.
* `until` shorthand for `while not`.
* `loop` shorthand for `while True`.

## Usage

For a development environment, be sure to clone this repository
with `git clone --recurse-submodules`.

You need Python 3.9.  Optionally, you can
[install Poetry](https://python-poetry.org/docs/#installation).

<!--
To get a development environment running, follow these steps:

1. [Install Poetry](https://python-poetry.org/docs/#installation)
2. Clone this repository
3. `poetry install`
-->

Currently, to rebuild the grammar, run `make` within `src`.
This will change once Parseltongue is written in itself.

To build the examples, run `make` within `examples`.

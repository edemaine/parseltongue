# Parseltongue: Better Python

## Features So Far

* `if`, `elif`, `else` do not need colons after the condition,
  except when using one-line `if` or `elif`.

  ```py
  if x > 10
    print('big')
  elif x >= 0
    print('small')
  else print('negative')
  ```

## Usage

To get a development environment running, follow these steps:

1. [Install Poetry](https://python-poetry.org/docs/#installation)
2. Clone this repository
3. `poetry install`

Currently, to rebuild the grammar, run `make` within `src`.
This will change once Parseltongue is written in itself.

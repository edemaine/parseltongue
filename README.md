# Parseltongue: Better Python

## Features So Far

* List, tuple, dict, set literals and function arguments can use newlines
  instead of commas (except for singleton tuples).
  You can use up to one indentation, possible in the middle of the items,
  to allow for things like:
  ```py
  [1, 2, 3
   4, 5, 6]
  ```
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
* Implicit continuation when ending a line with an operator:
  ```py
  sum = 12345 +
        54321
  ```
* Comments after `\` continuations:
  ```py
  string = \ # comment
    'hello'
  ```

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

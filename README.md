# Parseltongue: Better Python

## Goals and Design Principles

* Parseltongue **compiles to Python**
  (so it's fully compatible with existing Python libraries, etc.;
  and if there's ever any doubt about what some syntax means,
  you can study the compiled-to-Python code)
* **Most Python code** is still valid Parseltongue
  (but there are some unavoidable exceptions)
* Most **punctuation is optional** (including most colons and many commas)
* Simplify use of self (not yet implemented)

## Features

### Newline Alternative to Commas

`list`, `tuple`, `dict`, and `set` literals, and function arguments,
can use newlines instead of commas to separate elements:

```coffee
stuff = {
  'foo': 'bar'
  'list': [
    'hello'
    'world'
    42
  ]
  'set': {
    1
    2
    3
  }
]
```

The one exception is singleton tuples `(item,)`, which still need a comma to
distinguish from a parenthesized expression like `(item)`.

Commas are still allowed before newlines, as in Python.
Commas are still necessary between items on the same line.
You are allowed to put the items (or just a suffix of them) one indentation
level in, to allow for things like:

```coffee
[1, 2, 3
 4, 5, 6
 7, 8, 9]
```

### Optional Colons

`if`, `elif`, `else`, `while`, `for`, `with`, `try`, `except`, `finally`,
`def`, and `class` generally do not need colons after the condition.
The exception is that the one-line forms of `if`, `elif`, `while`, `for`,
`with`, `except`, and `def` need a colon to separate the condition from the body.
But `else`, `try`, and `finally` do not need a colon even in their
one-line forms (as they lack a condition).

```py
if x > 10
  print('big')
elif x >= 0
  print('small')
else print('negative')

try func()
finally close()
```

### Control Syntax Convenience

`unless` is shorthand for `if not`:

```coffee
unless error
  print('all good')
```

`until` is shorthand for `while not`:

```coffee
until done
  print('looping')
  done = True
```

`loop` shorthand for `while True`:

```coffee
loop
  if done: break
```

### Line Continuation

Lines are implicitly and automatically continued (as if they ended with `\`)
when they end with a binary or unary operator:

```coffee
sum = 12345 +
      54321
```

In addition, comments are allowed after explicit `\` continuations:

```py
string = 'hello' \ # comment
         'world'
```

## Planned Features / Ideas

* [x] Colon optional after `if`, `elif`, `else`, `while`, `for`, `with`, `try`, `except`, `finally`, `def`, `class`
* [ ] Colon optional after `match`, etc.
* [ ] Optional body for `class`, `except`, etc. (avoid `pass`)
* [ ] Multi-line lambdas via arrow functions
  * (?) Implicit return (but `def` remains as is)
* Most statements become expressions
  * `for`, `while` loops return list of results
  * `if`
  * `match`
  * `try`
  * More?
* CoffeeScript `do (var) -> ...` for easier scoping (or maybe `call`?)
* `do...while/until` loops and `do...if/unless` late conditions, like so:
  ```py
  do
    code()
  ...unless condition()
  ```
* Analog of CoffeeScript's `when` / analog from list comprehensions:
  `for x in list if condition` and `for x in list unless condition`.
  Also `while condition if condition` and `while condition unless condition`.
* `for key: value in dict` (like CoffeeScript `for key, value of object`)
* Multi-line list comprehensions:
  ```py
  [
    for x in list   # list comprehension
      ...
    for x in list   # concatenated list comprehension
      ...
    (for x in list  # parens make this a generator expression
      ...
    )
  ]
  ```
* self via `@`
  * `@foo` in constructor argument
  * Conflict with decorators?
* None coalescing: `?.`, `?[`, `?=` or `??=`, `?` or `??` operator
  (see [PEP 0505](https://www.python.org/dev/peps/pep-0505/))
* `return = value` changes return value for later `return` or
  implicit `return` at end of `def` (and arrow functions?)
* (?) Implicit function calls without parentheses
  (this would mean `foo (arg, arg)` is different from `foo(arg, arg)`)
* (?) Custom infix operators
* (?) Argument initializers that run each time instead of getting memoized
  (`:=`? or replace current behavior, and break Python compatibility)
* (?) Require `shadow` declaration (similar to `nonlocal`/`global`)
  when shadowing variable from parent scope (perhaps as an option)
* Minor helpful syntax
  * Block comments via `###` (incompatible with "Python is Parseltongue")
  * [x] Implicit continuation when ending line with operator
  * Implicit continuation when starting next line with `.`
  * [x] Comments on continuation lines
  * [x] `unless`, `until`, `loop`
  * `elunless`?
  * Ability to `break` or `continue` out of a specific loop,
    not just the immediately containing one (unsure which mechanism is best;
    see https://www.python.org/dev/peps/pep-3136/; maybe numeric plus 'all')
  * `for...then` (or `for...broken`), like the opposite of `for...else`;
    can have both `then` and `else` clause, in either order
  * Backwards one-line `if`, `unless`, `for`, `while`, `until`
  * `then` as alternative to `:` in one-line `if ...:`
  * `..` (and `...`?) alternative to range and slices
  * `and=`, `or=`

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

To build Parseltongue, run `python3.9 make.py`
(or `make` if you have `make` installed).
This transpiles the source code in `src` (mostly written in Parseltongue)
into Python code in `lib` (using the latter).
If you accidentally trash the transpiler, use `git checkout lib`
to reset to the last committed state.

To build the examples, run `make examples` from the root directory,
or run `make` from within `examples`.

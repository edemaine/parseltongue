## Goals

* (?) Every Python program is valid Parseltongue
* Parseltongue compiles to Python
* Most punctuation is optional
  * Especially colons
* Simplify use of self

## Planned Features

* Multi-line lambdas via arrow functions
  * (?) Implicit return (but `def` remains as is)
* Most statements become expressions
  * `for`, `while` loops return list of results
  * `if`
  * `match`
  * `try`
  * More?
* `do` for easier scoping
* self via `@`
  * `@foo` in constructor argument
* (?) Implicit function calls without parens
* (?) Custom infix operators
* (?) Argument initializers that run instead of get memoized
  (`:=`? or replace current behavior, and break Python compatibility)
* Minor helpful syntax
  * Block comments via `###` (incompatible with "Python is Parseltongue")
  * Implicit continuation when ending line with operator
    or starting next line with `.`
  * Comments on continuation lines
  * `unless`, `elunless`?, `until`, `loop`
  * Backwards one-line `if`, `unless`, `for`, `while`, `until`
  * `then` as alternative for one-line `if ...:`
  * `..` (and `...`?) alternative to range and slices
  * `and=`, `or=`

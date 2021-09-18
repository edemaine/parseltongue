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
* Minor helpful syntax
  * Block comments via `###`
  * Implicit continuation when ending line with operator
    or starting next line with `.`
  * Comments on continuation lines
  * `unless`, `until`, `loop`
  * Backwards one-line `if`, `unless`, `for`, `while`, `until`
  * `then` as alternative for one-line `if ...:`
  * (?) `..` and `...` alternative to range

## Goals

* (?) Every Python program is valid Parseltongue
* Parseltongue compiles to Python
* Most punctuation is optional
  * Especially colons
* Simplify use of self

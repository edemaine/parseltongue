## Features

* Multi-line lambdas via arrow functions
  * (?) Implicit return (but `def` remains as is)
* Most statements become expressions
  * `for`, `while` loops return list of results
  * `if`
  * `match`
  * `try`
  * More?
* `do` for easier scoping
* self via @
* (?) Implicit function calls without parens
* (?) Custom infix operators
* Minor helpful syntax
  * Block comments via `###`
  * (?) Comments on continuation lines
  * `unless`, `until`
  * `then` as alternative for one-line `if ...:`
  * (?) `..` and `...` alternative to range

## Goals

* (?) Every Python program is valid Parseltongue
* Parseltongue compiles to Python
* Most punctuation is optional
  * Especially colons
* Simplify use of self

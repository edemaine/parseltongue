#!/usr/bin/python3.9

'''Lexer for Parseltongue

Much of this code is based on CPython's tokenize.py
[https://github.com/python/cpython/blob/main/Lib/tokenize.py]
and CoffeeScript's lexer
[https://coffeescript.org/annotated-source/lexer.html].
'''

import re

import pegen.tokenizer

import token, tokenize
tok_name = token.tok_name
tabsize = tokenize.tabsize
Token = TokenInfo = tokenize.TokenInfo

compile = lambda expr: re.compile(expr, re.UNICODE)
Comment = compile(tokenize.Comment)
Whitespace = compile(tokenize.Whitespace)
Newline_src = r'\r?\n'
Newline = compile(Newline_src)
Continuation = compile(r'\\' + tokenize.Whitespace +
  tokenize.maybe(tokenize.Comment) + Newline_src)
Triple = compile(
  tokenize.StringPrefix + "'''" + tokenize.Single3 + '|' +
  tokenize.StringPrefix + '"""' + tokenize.Double3)
token_rec = [
  (token.OP, compile(tokenize.Special)),
  (token.NUMBER, compile(tokenize.Number)),
  (token.STRING, Triple),
  (token.STRING, compile(tokenize.String)),
  (token.NAME, compile(tokenize.Name)),  # must go after NUMBER
]

# TODO: cookie_re

class ParselTongueLexerError(SyntaxError): pass

class Lexer:
  code: str           # entire input
  len: int            # len(code)
  pos: int            # current index into code
  line_num: int       # current line number within code (1-indexed)
  line_start: int     # pos of start of current line
  line: str           # current line (code[line_start:line_start + line_len])
  indent: int         # current indentation level
  indents: list[int]  # indentation levels we're nested within
  tokens: list[TokenInfo]  # output token list

  def __init__(self, code, filename = ''):
    self.filename = filename
    if hasattr(code, 'read'): code = code.read()
    self.code = code
    self.len = len(code)
    self.pos = 0
    self.line_num = 1
    # Like CoffeeScript but unlike Python, allow an overall indentation.
    # (Useful for copy/pasting portions of another file.)
    self.indents = [self.measure_indent()[0]]
    self.start_line()
    self.tokens = []
    self.tokenize()

  def __iter__(self):
    return iter(self.tokens)

  def start_line(self):
    # line_num is incremented in token_from_match
    #self.line_num += 1
    self.line_start = self.pos
    end_of_line = self.code.find('\n')
    if end_of_line < 0: index = self.len
    self.line = self.code[self.line_start:end_of_line]
    self.indent, self.pos = self.measure_indent()
    # Ignore indentation if this is a blank or comment line
    if self.pos == self.len or any(
      rec.match(self.code, self.pos) for rec in [Newline, Comment]): return

    indent = self.indents[-1]
    if self.indent > indent:
      self.indents.append(self.indent)
      self.indent_token(token.INDENT)
    while self.indent < indent:
      self.indents.pop()
      self.indent_token(token.DEDENT)
      if not self.indents:
        self.error('dedent beyond global indent')
      indent = self.indents[-1]
      if self.indent > indent:
        self.error(f'dedent to {self.indent} but expected {self.indents[-1]}')

  def indent_token(self, type):
    self.tokens.append(TokenInfo(type,
      self.code[self.line_start:self.pos],
      (self.line_num, 0), (self.line_num, self.pos - self.line_start),
      self.line))

  def measure_indent(self):
    indent = 0
    pos = self.pos
    while pos < self.len:
      char = self.code[pos]
      if char == ' ':
        indent += 1
      elif char == '\t':
        indent = (indent//tabsize + 1) * tabsize
      elif char == '\f':
        indent = 0
      else:
        break
      pos += 1
    return indent, pos

  def tokenize(self):
    while self.pos < self.len:
      self.token()
    while len(self.indents) > 1:
      self.indent_token(token.DEDENT)
      self.indents.pop()

  def token(self):
    # Strip leading whitespace
    match = Whitespace.match(self.code, self.pos)
    start, end = match.span()
    self.pos += end - start
    # Match regular tokens
    #print(f'matching {self.filename}:{self.line_num}.{self.pos - self.line_start} {match.group()}|{repr(self.code[self.pos:self.pos+20])[1:-1]}')
    for type, rec in token_rec:
      if match := rec.match(self.code, self.pos):
        self.token_from_match(type, match)
        break
    else:
      if match := Newline.match(self.code, self.pos):
        prev = self.prev()
        if prev and prev.type != token.NEWLINE:
          self.token_from_match(token.NEWLINE, match)
        else:
          self.token_from_match(None, match)
        self.start_line()
      elif match := Comment.match(self.code, self.pos):
        #self.token_from_match(token.COMMENT, match)
        self.token_from_match(None, match)
      elif match := Continuation.match(self.code, self.pos):
        self.token_from_match(None, match)
      else:
        self.error('failed to parse token')

  def token_from_match(self, type, match):
    start, end = match.span()
    end_line_start = self.code.rfind('\n', start, end)
    if end_line_start < 0:
      end_line_start = self.line_start
      end_line_num = self.line_num
    else:
      end_line_start += 1
      end_line_num = self.line_num + self.code.count('\n', start, end)
    token = TokenInfo(type, match.group(),
      (self.line_num, start - self.line_start),
      (end_line_num, end - self.line_start), self.line)
    if type:
      self.tokens.append(token)
    self.line_start = end_line_start
    self.line_num = end_line_num
    self.pos += end - start
    return token

  def prev(self):
    if self.tokens:
      return self.tokens[-1]

  def error(self, msg):
    self.dump()
    raise ParselTongueLexerError('\n'.join([
      f'{self.filename}:{self.line_num}.{self.pos - self.line_start + 1} - {msg}',
      self.line,
      ' ' * (self.pos - self.line_start) + '^'
    ]))

  def dump(self):
    line = None
    line_width = len(str(self.tokens[-1].start[0]))
    for token in self:
      if line != token.start[0]:
        if line is not None: print()
        print(f'{token.start[0]:{line_width}}', end = '')
        line = token.end[0]
      print(f' {tok_name[token.type]}{repr(token.string)}', end = '')
    print()

class Tokenizer(pegen.tokenizer.Tokenizer):
  def __init__(self, file, filename):
    def tokengen():
      lexer = Lexer(file, filename)
      yield from iter(lexer)
      while True:
        yield TokenInfo(token.ENDMARKER, '',
          (lexer.line_num, 0), (lexer.line_num, len(lexer.line)), lexer.line)
    super().__init__(tokengen(), path = filename)

def main():
  import sys
  for filename in sys.argv[1:]:
    print(f'# {filename}')
    lexer = Lexer(open(filename, 'r').read(), filename)
    lexer.dump()

if __name__ == '__main__': main()

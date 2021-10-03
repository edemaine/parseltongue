"""Lexer for Parseltongue

Much of this code is based on CPython's tokenize.py
[https://github.com/python/cpython/blob/main/Lib/tokenize.py]
and CoffeeScript's lexer
[https://coffeescript.org/annotated-source/lexer.html].
"""
import re
import pegen.tokenizer
import token, tokenize
tok_name = token.tok_name
tabsize = tokenize.tabsize
Token = TokenInfo = tokenize.TokenInfo
compile = lambda expr: re.compile(expr, re.UNICODE)
Comment = compile(tokenize.Comment)
Whitespace = compile(tokenize.Whitespace)
Newline_src = '\\r?\\n'
Newline = compile(Newline_src)
NewlineOrComment = compile(tokenize.Whitespace + tokenize.group(Newline_src, tokenize.Comment))
Continuation = compile('\\\\' + tokenize.Whitespace + tokenize.maybe(tokenize.Comment) + Newline_src)
Triple = compile(tokenize.StringPrefix + "'''" + tokenize.Single3 + '|' + tokenize.StringPrefix + '"""' + tokenize.Double3)
token_rec = [(token.OP, compile(tokenize.Special)), (token.NUMBER, compile(tokenize.Number)), (token.STRING, Triple), (token.STRING, compile(tokenize.String)), (token.NAME, compile(tokenize.Name))]
IMPLICIT_CONTINUATION = {token.OP: {'+', '-', '*', '/', '|', '&', '<', '>', '.', '%', '==', '!=', '<=', '>=', '~', '^', '<<', '>>', '**', '//', '@', '=', '+=', '-=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '**=', '//=', '@=', ':='}, token.NAME: {'and', 'or', 'not', 'is', 'in'}}

def implicit_continuation(tok):
    return tok.type in IMPLICIT_CONTINUATION and tok.string in IMPLICIT_CONTINUATION[tok.type]
nest_open_ops = {'(': ')', '[': ']', '{': '}'}
nest_close_ops = set(nest_open_ops.values())

class ParselTongueLexerError(SyntaxError):
    pass

class Lexer:
    code: str
    len: int
    pos: int
    line_num: int
    line_start: int
    line: str
    indent: int
    indents: list[int]
    tokens: list[TokenInfo]

    def __init__(self, code, filename=''):
        self.filename = filename
        if hasattr(code, 'read'):
            code = code.read()
        self.code = code
        self.len = len(code)
        self.pos = 0
        self.line_start = self.pos
        self.line_num = 1
        self.set_line()
        self.skip_blank_lines()
        self.indents = [self.measure_indent()[0]]
        self.nests = []
        self.start_line()
        self.tokens = []
        self.tokenize()

    def __iter__(self):
        return iter(self.tokens)

    def set_line(self):
        end_of_line = self.code.find('\n', self.line_start)
        if end_of_line < 0:
            end_of_line = self.len
        self.line = self.code[self.line_start:end_of_line]

    def start_line(self):
        (self.indent, self.pos) = self.measure_indent()
        if self.pos == self.len:
            return
        indent = self.indents[-1]
        if self.indent > indent:
            self.indents.append(self.indent)
            tok = self.indent_token(token.INDENT)
            tok.closing = lambda tok2: tok2.type == token.DEDENT
            self.nests.append(tok)
        while self.indent < indent:
            self.dedent()
            indent = self.indents[-1]
            if self.indent > indent:
                self.error(f'dedent to {self.indent} but expected {self.indents[-1]}')

    def indent_token(self, type, tok=None):
        if tok is None:
            tok = TokenInfo(type, self.code[self.line_start:self.pos], (self.line_num, 0), (self.line_num, self.pos - self.line_start), self.line)
        else:
            tok = TokenInfo(type, tok.string, tok.start, tok.end, tok.line)
        self.tokens.append(tok)
        return tok

    def dedent(self, tok=None):
        self.indents.pop()
        tok = self.indent_token(token.DEDENT, tok)
        self.unnest(tok)
        if not self.indents:
            self.error('dedent beyond global indent')

    def unnest(self, tok):
        while True:
            if not self.nests:
                self.error(f'Extra closing {tok}')
            nest = self.nests[-1]
            if nest.closing(tok):
                return self.nests.pop()
            elif nest.type == token.INDENT:
                self.dedent(tok)
            else:
                self.error(f'{nest} closed by {tok}')

    def measure_indent(self):
        indent = 0
        pos = self.pos
        while pos < self.len:
            char = self.code[pos]
            if char == ' ':
                indent += 1
            elif char == '\t':
                indent = (indent // tabsize + 1) * tabsize
            elif char == '\x0c':
                indent = 0
            else:
                break
            pos += 1
        return (indent, pos)

    def tokenize(self):
        while self.pos < self.len:
            self.token()
        while len(self.indents) > 1:
            self.dedent()

    def token(self):
        match = Whitespace.match(self.code, self.pos)
        (start, end) = match.span()
        self.pos += end - start
        for (type, rec) in token_rec:
            if (match := rec.match(self.code, self.pos)):
                self.token_from_match(type, match)
                break
        else:
            if (match := Newline.match(self.code, self.pos)):
                prev = self.prev()
                newline = prev and prev.type != token.NEWLINE and (not implicit_continuation(prev))
                self.token_from_match(token.NEWLINE if newline else None, match)
                self.skip_blank_lines()
                if newline:
                    self.start_line()
            elif (match := Comment.match(self.code, self.pos)):
                self.token_from_match(None, match)
            elif (match := Continuation.match(self.code, self.pos)):
                self.token_from_match(None, match)
            else:
                self.error('failed to parse token')

    def skip_blank_lines(self):
        """Skip over any blank/comment-only lines,
      in particular to ignore indentation."""
        while (match := NewlineOrComment.match(self.code, self.pos)):
            self.token_from_match(None, match)

    def token_from_match(self, type, match):
        (start, end) = match.span()
        end_line_start = self.code.rfind('\n', start, end)
        if end_line_start < 0:
            end_line_start = self.line_start
            end_line_num = self.line_num
        else:
            end_line_start += 1
            end_line_num = self.line_num + self.code.count('\n', start, end)
        tok = TokenInfo(type, match.group(), (self.line_num, start - self.line_start), (end_line_num, end - self.line_start), self.line)
        self.line_start = end_line_start
        self.line_num = end_line_num
        self.set_line()
        self.pos += end - start
        if type == token.OP:
            if tok.string in nest_open_ops:
                closing = nest_open_ops[tok.string]
                tok.closing = lambda tok2: tok2.type == token.OP and tok2.string == closing
                self.nests.append(tok)
            elif tok.string in nest_close_ops:
                self.unnest(tok)
        if type:
            self.tokens.append(tok)
        return tok

    def prev(self):
        if self.tokens:
            return self.tokens[-1]

    def error(self, msg):
        self.dump()
        raise ParselTongueLexerError('\n'.join([f'{self.filename}:{self.line_num}.{self.pos - self.line_start + 1} - {msg}', self.line, ' ' * (self.pos - self.line_start) + '^']))

    def dump(self):
        line = None
        line_width = len(str(self.tokens[-1].start[0]))
        for token in self:
            if not line == token.start[0]:
                if line is not None:
                    print()
                print(f'{token.start[0]:{line_width}}', end='')
                line = token.end[0]
            print(f' {tok_name[token.type]}{repr(token.string)}', end='')
        print()

class Tokenizer(pegen.tokenizer.Tokenizer):

    def __init__(self, file, filename):

        def tokengen():
            lexer = Lexer(file, filename)
            yield from iter(lexer)
            while True:
                yield TokenInfo(token.ENDMARKER, '', (lexer.line_num, 0), (lexer.line_num, len(lexer.line)), lexer.line)
        super().__init__(tokengen(), path=filename)

def main():
    import sys
    for filename in sys.argv[1:]:
        print(f'# {filename}')
        lexer = Lexer(open(filename, 'r').read(), filename)
        lexer.dump()
if __name__ == '__main__':
    main()

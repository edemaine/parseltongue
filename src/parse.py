#!/usr/bin/env python3.9

import ast
from typing import List
from dataclasses import dataclass
from pegen.parser import *
import lexer

class waiting_for_py310: pass
ast.match_case = waiting_for_py310
ast.pattern = waiting_for_py310

@dataclass
class NameDefaultPair:
  arg: ast.arg
  value: ast.expr

@dataclass
class KeyValuePair:
  key: ast.expr
  value: ast.expr

@dataclass
class KeyPatternPair:
  key: ast.expr
  pattern: ast.pattern

@dataclass
class CmpopExprPair:
  cmpop: ast.cmpop
  expr: ast.expr

@dataclass
class KeywordOrStarred:
  keyword: Any
  starred: int

@dataclass
class SlashWithDefault:
  plain_names: List[ast.arg]
  names_with_default: list

@dataclass
class StarEtc:
  vararg: ast.arg
  kwonlyargs: List[NameDefaultPair]
  kwarg: ast.arg
def TypeComment(x):
  if x: x = str(x)
  return x

def seq_count_dots(seq) -> int:
  dots = 0
  for token in seq:
    if token.type == 'ELLIPSIS':
      dots += 3
    elif token.type == 'DOT':
      dots += 1
  return dots

def seq_flatten(seq):
  return [item for list in seq for item in list]

def set_expr_context(expr, context):
  expr.context = context()
  return expr

def empty_arguments():
  return ast.arguments([], [], None, [], [], None, posdefaults)

def map_names_to_ids(names):
  return [name.id for name in names]

def class_def_decorators(decorators: List[ast.expr], class_def: ast.stmt) -> ast.stmt:
  return ast.ClassDef(class_def.name, class_def.bases, class_def.keywords,
    class_def.body, decorators, **copy_locations(class_def))

def add_type_comment_to_arg(arg, tc):
  if not tc: return arg
  tc = TypeComment(tc)
  return ast.arg(arg.arg, arg.annotation, tc, **copy_locations(arg))

def make_arguments(slash_without_default: List[ast.arg],
    slash_with_default: SlashWithDefault,
    plain_names: List[ast.arg],
    names_with_default: List,
    star_etc: StarEtc):
  # xxx
  return ast.arguments()

def check_legacy_stmt(x):
  return x.id in ['print', 'exec']

def copy_locations(x):
  return dict(
    lineno = x.lineno,
    col_offset = x.col_offset,
    end_lineno = x.end_lineno,
    end_col_offset = x.end_col_offset,
  )

# Wrap tokens in ast structures
class Parser(Parser):
  def number(self): # -> Optional[ast.Constant]:
    number = super().number()
    if number: number = ast.Constant(lexer.parse_number(number))
    return number
  def name(self) -> Optional[ast.Name]:
    name = super().name()
    if name: name = ast.Name(name.string)
    return name
# Keywords and soft keywords are listed at the end of the parser definition.
class GeneratedParser(Parser):

    @memoize
    def file(self) -> Optional[ast . mod]:
        # file: statements? $
        mark = self._mark()
        if (
            (a := self.statements(),)
            and
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return ast . Module ( a , [] )
        self._reset(mark)
        return None

    @memoize
    def interactive(self) -> Optional[ast . mod]:
        # interactive: statement_newline
        mark = self._mark()
        if (
            (a := self.statement_newline())
        ):
            return ast . Interactive ( a , p . arena )
        self._reset(mark)
        return None

    @memoize
    def eval(self) -> Optional[ast . mod]:
        # eval: expressions NEWLINE* $
        mark = self._mark()
        if (
            (a := self.expressions())
            and
            (_loop0_1 := self._loop0_1(),)
            and
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return ast . Expression ( a , p . arena )
        self._reset(mark)
        return None

    @memoize
    def func_type(self) -> Optional[ast . mod]:
        # func_type: '(' type_expressions? ')' '->' expression NEWLINE* $
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (a := self.type_expressions(),)
            and
            (literal_1 := self.expect(')'))
            and
            (literal_2 := self.expect('->'))
            and
            (b := self.expression())
            and
            (_loop0_2 := self._loop0_2(),)
            and
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return ast . FunctionType ( a , b , p . arena )
        self._reset(mark)
        return None

    @memoize
    def fstring(self) -> Optional[ast . expr]:
        # fstring: star_expressions
        mark = self._mark()
        if (
            (star_expressions := self.star_expressions())
        ):
            return star_expressions
        self._reset(mark)
        return None

    @memoize
    def statements(self) -> Optional[List [ast . stmt]]:
        # statements: statement+
        mark = self._mark()
        if (
            (a := self._loop1_3())
        ):
            return seq_flatten ( a )
        self._reset(mark)
        return None

    @memoize
    def statement(self) -> Optional[List [ast . stmt]]:
        # statement: compound_stmt | simple_stmts
        mark = self._mark()
        if (
            (a := self.compound_stmt())
        ):
            return [a]
        self._reset(mark)
        if (
            (a := self.simple_stmts())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def statement_newline(self) -> Optional[List [ast . stmt]]:
        # statement_newline: compound_stmt NEWLINE | simple_stmts | NEWLINE | $
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.compound_stmt())
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return [a]
        self._reset(mark)
        if (
            (simple_stmts := self.simple_stmts())
        ):
            return simple_stmts
        self._reset(mark)
        if (
            (_newline := self.expect('NEWLINE'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return [ast . Pass ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )]
        self._reset(mark)
        if (
            (_endmarker := self.expect('ENDMARKER'))
        ):
            return _PyPegen_interactive_exit ( p )
        self._reset(mark)
        return None

    @memoize
    def simple_stmts(self) -> Optional[List [ast . stmt]]:
        # simple_stmts: simple_stmt !';' NEWLINE | ';'.simple_stmt+ ';'? NEWLINE
        mark = self._mark()
        if (
            (a := self.simple_stmt())
            and
            self.negative_lookahead(self.expect, ';')
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return [a]
        self._reset(mark)
        if (
            (a := self._gather_4())
            and
            (opt := self.expect(';'),)
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def simple_stmt(self) -> Optional[ast . stmt]:
        # simple_stmt: assignment | star_expressions | &'return' return_stmt | &('import' | 'from') import_stmt | &'raise' raise_stmt | 'pass' | &'del' del_stmt | &'yield' yield_stmt | &'assert' assert_stmt | 'break' | 'continue' | &'global' global_stmt | &'nonlocal' nonlocal_stmt
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (assignment := self.assignment())
        ):
            return assignment
        self._reset(mark)
        if (
            (e := self.star_expressions())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Expr ( e , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'return')
            and
            (return_stmt := self.return_stmt())
        ):
            return return_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self._tmp_6, )
            and
            (import_stmt := self.import_stmt())
        ):
            return import_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'raise')
            and
            (raise_stmt := self.raise_stmt())
        ):
            return raise_stmt
        self._reset(mark)
        if (
            (literal := self.expect('pass'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Pass ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'del')
            and
            (del_stmt := self.del_stmt())
        ):
            return del_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'yield')
            and
            (yield_stmt := self.yield_stmt())
        ):
            return yield_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'assert')
            and
            (assert_stmt := self.assert_stmt())
        ):
            return assert_stmt
        self._reset(mark)
        if (
            (literal := self.expect('break'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Break ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('continue'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Continue ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'global')
            and
            (global_stmt := self.global_stmt())
        ):
            return global_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'nonlocal')
            and
            (nonlocal_stmt := self.nonlocal_stmt())
        ):
            return nonlocal_stmt
        self._reset(mark)
        return None

    @memoize
    def compound_stmt(self) -> Optional[ast . stmt]:
        # compound_stmt: &('def' | '@' | ASYNC) function_def | &'if' if_stmt | &('class' | '@') class_def | &('with' | ASYNC) with_stmt | &('for' | ASYNC) for_stmt | &'try' try_stmt | &'while' while_stmt | match_stmt
        mark = self._mark()
        if (
            self.positive_lookahead(self._tmp_7, )
            and
            (function_def := self.function_def())
        ):
            return function_def
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'if')
            and
            (if_stmt := self.if_stmt())
        ):
            return if_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self._tmp_8, )
            and
            (class_def := self.class_def())
        ):
            return class_def
        self._reset(mark)
        if (
            self.positive_lookahead(self._tmp_9, )
            and
            (with_stmt := self.with_stmt())
        ):
            return with_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self._tmp_10, )
            and
            (for_stmt := self.for_stmt())
        ):
            return for_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'try')
            and
            (try_stmt := self.try_stmt())
        ):
            return try_stmt
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, 'while')
            and
            (while_stmt := self.while_stmt())
        ):
            return while_stmt
        self._reset(mark)
        if (
            (match_stmt := self.match_stmt())
        ):
            return match_stmt
        self._reset(mark)
        return None

    @memoize
    def assignment(self) -> Optional[ast . stmt]:
        # assignment: NAME ':' expression ['=' annotated_rhs] | ('(' single_target ')' | single_subscript_attribute_target) ':' expression ['=' annotated_rhs] | ((star_targets '='))+ (yield_expr | star_expressions) !'=' TYPE_COMMENT? | single_target augassign ~ (yield_expr | star_expressions) | invalid_assignment
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.name())
            and
            (literal := self.expect(':'))
            and
            (b := self.expression())
            and
            (c := self._tmp_11(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . AnnAssign ( set_expr_context ( a , ast . Store ) , b , c , 1 , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self._tmp_12())
            and
            (literal := self.expect(':'))
            and
            (b := self.expression())
            and
            (c := self._tmp_13(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . AnnAssign ( a , b , c , 0 , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self._loop1_14())
            and
            (b := self._tmp_15())
            and
            self.negative_lookahead(self.expect, '=')
            and
            (tc := self.type_comment(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Assign ( a , b , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        cut = False
        if (
            (a := self.single_target())
            and
            (b := self.augassign())
            and
            (cut := True)
            and
            (c := self._tmp_16())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . AugAssign ( a , b . kind , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if cut: return None
        if (
            (invalid_assignment := self.invalid_assignment())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def annotated_rhs(self) -> Optional[ast . expr]:
        # annotated_rhs: yield_expr | star_expressions
        mark = self._mark()
        if (
            (yield_expr := self.yield_expr())
        ):
            return yield_expr
        self._reset(mark)
        if (
            (star_expressions := self.star_expressions())
        ):
            return star_expressions
        self._reset(mark)
        return None

    @memoize
    def augassign(self) -> Optional[ast . operator]:
        # augassign: '+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=' | '**=' | '//='
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('+='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Add ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('-='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Sub ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('*='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Mult ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('@='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatMult ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('/='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Div ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('%='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Mod ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('&='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BitAnd ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('|='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BitOr ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('^='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BitXor ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('<<='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . LShift ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('>>='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . RShift ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('**='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Pow ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('//='))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . FloorDiv ( lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def return_stmt(self) -> Optional[ast . stmt]:
        # return_stmt: 'return' star_expressions?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('return'))
            and
            (a := self.star_expressions(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Return ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def raise_stmt(self) -> Optional[ast . stmt]:
        # raise_stmt: 'raise' expression ['from' expression] | 'raise'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('raise'))
            and
            (a := self.expression())
            and
            (b := self._tmp_17(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Raise ( a , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('raise'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Raise ( None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def global_stmt(self) -> Optional[ast . stmt]:
        # global_stmt: 'global' ','.NAME+
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('global'))
            and
            (a := self._gather_18())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Global ( map_names_to_ids ( a ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def nonlocal_stmt(self) -> Optional[ast . stmt]:
        # nonlocal_stmt: 'nonlocal' ','.NAME+
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('nonlocal'))
            and
            (a := self._gather_20())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Nonlocal ( map_names_to_ids ( a ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def del_stmt(self) -> Optional[ast . stmt]:
        # del_stmt: 'del' del_targets &(';' | NEWLINE) | invalid_del_stmt
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('del'))
            and
            (a := self.del_targets())
            and
            self.positive_lookahead(self._tmp_22, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Delete ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_del_stmt := self.invalid_del_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def yield_stmt(self) -> Optional[ast . stmt]:
        # yield_stmt: yield_expr
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (y := self.yield_expr())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Expr ( y , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def assert_stmt(self) -> Optional[ast . stmt]:
        # assert_stmt: 'assert' expression [',' expression]
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('assert'))
            and
            (a := self.expression())
            and
            (b := self._tmp_23(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Assert ( a , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def import_stmt(self) -> Optional[ast . stmt]:
        # import_stmt: import_name | import_from
        mark = self._mark()
        if (
            (import_name := self.import_name())
        ):
            return import_name
        self._reset(mark)
        if (
            (import_from := self.import_from())
        ):
            return import_from
        self._reset(mark)
        return None

    @memoize
    def import_name(self) -> Optional[ast . stmt]:
        # import_name: 'import' dotted_as_names
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('import'))
            and
            (a := self.dotted_as_names())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Import ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def import_from(self) -> Optional[ast . stmt]:
        # import_from: 'from' (('.' | '...'))* dotted_name 'import' import_from_targets | 'from' (('.' | '...'))+ 'import' import_from_targets
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('from'))
            and
            (a := self._loop0_24(),)
            and
            (b := self.dotted_name())
            and
            (literal_1 := self.expect('import'))
            and
            (c := self.import_from_targets())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . ImportFrom ( b . id , c , seq_count_dots ( a ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('from'))
            and
            (a := self._loop1_25())
            and
            (literal_1 := self.expect('import'))
            and
            (b := self.import_from_targets())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . ImportFrom ( None , b , seq_count_dots ( a ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def import_from_targets(self) -> Optional[List [ast . alias]]:
        # import_from_targets: '(' import_from_as_names ','? ')' | import_from_as_names !',' | '*' | invalid_import_from_targets
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('('))
            and
            (a := self.import_from_as_names())
            and
            (opt := self.expect(','),)
            and
            (literal_1 := self.expect(')'))
        ):
            return a
        self._reset(mark)
        if (
            (import_from_as_names := self.import_from_as_names())
            and
            self.negative_lookahead(self.expect, ',')
        ):
            return import_from_as_names
        self._reset(mark)
        if (
            (literal := self.expect('*'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return [ast . alias ( '*' , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )]
        self._reset(mark)
        if (
            (invalid_import_from_targets := self.invalid_import_from_targets())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def import_from_as_names(self) -> Optional[List [ast . alias]]:
        # import_from_as_names: ','.import_from_as_name+
        mark = self._mark()
        if (
            (a := self._gather_26())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def import_from_as_name(self) -> Optional[ast . alias]:
        # import_from_as_name: NAME ['as' NAME]
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.name())
            and
            (b := self._tmp_28(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . alias ( a . id , b . id if b else None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def dotted_as_names(self) -> Optional[List [ast . alias]]:
        # dotted_as_names: ','.dotted_as_name+
        mark = self._mark()
        if (
            (a := self._gather_29())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def dotted_as_name(self) -> Optional[ast . alias]:
        # dotted_as_name: dotted_name ['as' NAME]
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.dotted_name())
            and
            (b := self._tmp_31(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . alias ( a . id , b . id if b else None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize_left_rec
    def dotted_name(self) -> Optional[ast . expr]:
        # dotted_name: dotted_name '.' NAME | NAME
        mark = self._mark()
        if (
            (a := self.dotted_name())
            and
            (literal := self.expect('.'))
            and
            (b := self.name())
        ):
            return ast . Name ( f'{a.id}.{b.id}' )
        self._reset(mark)
        if (
            (name := self.name())
        ):
            return name
        self._reset(mark)
        return None

    @memoize
    def colon_block(self) -> Optional[List [ast . stmt]]:
        # colon_block: ':' block | NEWLINE INDENT statements DEDENT
        mark = self._mark()
        if (
            (literal := self.expect(':'))
            and
            (block := self.block())
        ):
            return [literal, block]
        self._reset(mark)
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (a := self.statements())
            and
            (_dedent := self.expect('DEDENT'))
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def block(self) -> Optional[List [ast . stmt]]:
        # block: NEWLINE INDENT statements DEDENT | simple_stmts | invalid_block
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (a := self.statements())
            and
            (_dedent := self.expect('DEDENT'))
        ):
            return a
        self._reset(mark)
        if (
            (simple_stmts := self.simple_stmts())
        ):
            return simple_stmts
        self._reset(mark)
        if (
            (invalid_block := self.invalid_block())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def decorators(self) -> Optional[List [ast . expr]]:
        # decorators: (('@' named_expression NEWLINE))+
        mark = self._mark()
        if (
            (a := self._loop1_32())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def class_def(self) -> Optional[ast . stmt]:
        # class_def: decorators class_def_raw | class_def_raw
        mark = self._mark()
        if (
            (a := self.decorators())
            and
            (b := self.class_def_raw())
        ):
            return class_def_decorators ( a , b )
        self._reset(mark)
        if (
            (class_def_raw := self.class_def_raw())
        ):
            return class_def_raw
        self._reset(mark)
        return None

    @memoize
    def class_def_raw(self) -> Optional[ast . stmt]:
        # class_def_raw: invalid_class_def_raw | 'class' NAME ['(' arguments? ')'] &&':' block
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_class_def_raw := self.invalid_class_def_raw())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('class'))
            and
            (a := self.name())
            and
            (b := self._tmp_33(),)
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (c := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . ClassDef ( a . id , b . args if b else None , b . keywords if b else None , c , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def function_def(self) -> Optional[ast . stmt]:
        # function_def: decorators function_def_raw | function_def_raw
        mark = self._mark()
        if (
            (d := self.decorators())
            and
            (f := self.function_def_raw())
        ):
            return _PyPegen_function_def_decorators ( p , d , f )
        self._reset(mark)
        if (
            (function_def_raw := self.function_def_raw())
        ):
            return function_def_raw
        self._reset(mark)
        return None

    @memoize
    def function_def_raw(self) -> Optional[ast . stmt]:
        # function_def_raw: invalid_def_raw | 'def' NAME '(' params? ')' ['->' expression] &&':' func_type_comment? block | ASYNC 'def' NAME '(' params? ')' ['->' expression] &&':' func_type_comment? block
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_def_raw := self.invalid_def_raw())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('def'))
            and
            (n := self.name())
            and
            (literal_1 := self.expect('('))
            and
            (params := self.params(),)
            and
            (literal_2 := self.expect(')'))
            and
            (a := self._tmp_34(),)
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (tc := self.func_type_comment(),)
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . FunctionDef ( n . id , params if params else empty_arguments ( ) , b , None , a , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (_async := self.expect('ASYNC'))
            and
            (literal := self.expect('def'))
            and
            (n := self.name())
            and
            (literal_1 := self.expect('('))
            and
            (params := self.params(),)
            and
            (literal_2 := self.expect(')'))
            and
            (a := self._tmp_35(),)
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (tc := self.func_type_comment(),)
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . stmt , 5 , "Async functions are" , ast . AsyncFunctionDef ( n . id , params if params else empty_arguments ( ) , b , None , a , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        return None

    @memoize
    def params(self) -> Optional[ast . arguments]:
        # params: invalid_parameters | parameters
        mark = self._mark()
        if (
            (invalid_parameters := self.invalid_parameters())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (parameters := self.parameters())
        ):
            return parameters
        self._reset(mark)
        return None

    @memoize
    def parameters(self) -> Optional[ast . arguments]:
        # parameters: slash_no_default param_no_default* param_with_default* star_etc? | slash_with_default param_with_default* star_etc? | param_no_default+ param_with_default* star_etc? | param_with_default+ star_etc? | star_etc
        mark = self._mark()
        if (
            (a := self.slash_no_default())
            and
            (b := self._loop0_36(),)
            and
            (c := self._loop0_37(),)
            and
            (d := self.star_etc(),)
        ):
            return make_arguments ( a , None , b , c , d )
        self._reset(mark)
        if (
            (a := self.slash_with_default())
            and
            (b := self._loop0_38(),)
            and
            (c := self.star_etc(),)
        ):
            return make_arguments ( None , a , None , b , c )
        self._reset(mark)
        if (
            (a := self._loop1_39())
            and
            (b := self._loop0_40(),)
            and
            (c := self.star_etc(),)
        ):
            return make_arguments ( None , None , a , b , c )
        self._reset(mark)
        if (
            (a := self._loop1_41())
            and
            (b := self.star_etc(),)
        ):
            return make_arguments ( None , None , None , a , b )
        self._reset(mark)
        if (
            (a := self.star_etc())
        ):
            return make_arguments ( None , None , None , None , a )
        self._reset(mark)
        return None

    @memoize
    def slash_no_default(self) -> Optional[List [ast . arg]]:
        # slash_no_default: param_no_default+ '/' ',' | param_no_default+ '/' &')'
        mark = self._mark()
        if (
            (a := self._loop1_42())
            and
            (literal := self.expect('/'))
            and
            (literal_1 := self.expect(','))
        ):
            return a
        self._reset(mark)
        if (
            (a := self._loop1_43())
            and
            (literal := self.expect('/'))
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def slash_with_default(self) -> Optional[SlashWithDefault]:
        # slash_with_default: param_no_default* param_with_default+ '/' ',' | param_no_default* param_with_default+ '/' &')'
        mark = self._mark()
        if (
            (a := self._loop0_44(),)
            and
            (b := self._loop1_45())
            and
            (literal := self.expect('/'))
            and
            (literal_1 := self.expect(','))
        ):
            return SlashWithDefault ( a , b )
        self._reset(mark)
        if (
            (a := self._loop0_46(),)
            and
            (b := self._loop1_47())
            and
            (literal := self.expect('/'))
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return SlashWithDefault ( a , b )
        self._reset(mark)
        return None

    @memoize
    def star_etc(self) -> Optional[StarEtc]:
        # star_etc: '*' param_no_default param_maybe_default* kwds? | '*' ',' param_maybe_default+ kwds? | kwds | invalid_star_etc
        mark = self._mark()
        if (
            (literal := self.expect('*'))
            and
            (a := self.param_no_default())
            and
            (b := self._loop0_48(),)
            and
            (c := self.kwds(),)
        ):
            return StarEtc ( a , b , c )
        self._reset(mark)
        if (
            (literal := self.expect('*'))
            and
            (literal_1 := self.expect(','))
            and
            (b := self._loop1_49())
            and
            (c := self.kwds(),)
        ):
            return StarEtc ( None , b , c )
        self._reset(mark)
        if (
            (a := self.kwds())
        ):
            return StarEtc ( None , None , a )
        self._reset(mark)
        if (
            (invalid_star_etc := self.invalid_star_etc())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def kwds(self) -> Optional[ast . arg]:
        # kwds: '**' param_no_default
        mark = self._mark()
        if (
            (literal := self.expect('**'))
            and
            (a := self.param_no_default())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def param_no_default(self) -> Optional[ast . arg]:
        # param_no_default: param ',' TYPE_COMMENT? | param TYPE_COMMENT? &')'
        mark = self._mark()
        if (
            (a := self.param())
            and
            (literal := self.expect(','))
            and
            (tc := self.type_comment(),)
        ):
            return add_type_comment_to_arg ( a , tc )
        self._reset(mark)
        if (
            (a := self.param())
            and
            (tc := self.type_comment(),)
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return add_type_comment_to_arg ( a , tc )
        self._reset(mark)
        return None

    @memoize
    def param_with_default(self) -> Optional[NameDefaultPair]:
        # param_with_default: param default ',' TYPE_COMMENT? | param default TYPE_COMMENT? &')'
        mark = self._mark()
        if (
            (a := self.param())
            and
            (c := self.default())
            and
            (literal := self.expect(','))
            and
            (tc := self.type_comment(),)
        ):
            return NameDefaultPair ( a , c , tc )
        self._reset(mark)
        if (
            (a := self.param())
            and
            (c := self.default())
            and
            (tc := self.type_comment(),)
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return NameDefaultPair ( a , c , tc )
        self._reset(mark)
        return None

    @memoize
    def param_maybe_default(self) -> Optional[NameDefaultPair]:
        # param_maybe_default: param default? ',' TYPE_COMMENT? | param default? TYPE_COMMENT? &')'
        mark = self._mark()
        if (
            (a := self.param())
            and
            (c := self.default(),)
            and
            (literal := self.expect(','))
            and
            (tc := self.type_comment(),)
        ):
            return NameDefaultPair ( a , c , tc )
        self._reset(mark)
        if (
            (a := self.param())
            and
            (c := self.default(),)
            and
            (tc := self.type_comment(),)
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return NameDefaultPair ( a , c , tc )
        self._reset(mark)
        return None

    @memoize
    def param(self) -> Optional[ast . arg]:
        # param: NAME annotation?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.name())
            and
            (b := self.annotation(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . arg ( a . id , b , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def annotation(self) -> Optional[ast . expr]:
        # annotation: ':' expression
        mark = self._mark()
        if (
            (literal := self.expect(':'))
            and
            (a := self.expression())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def default(self) -> Optional[ast . expr]:
        # default: '=' expression
        mark = self._mark()
        if (
            (literal := self.expect('='))
            and
            (a := self.expression())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def if_stmt(self) -> Optional[ast . stmt]:
        # if_stmt: invalid_if_stmt | 'if' named_expression colon_block elif_stmt | 'if' named_expression colon_block else_block?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_if_stmt := self.invalid_if_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('if'))
            and
            (a := self.named_expression())
            and
            (b := self.colon_block())
            and
            (c := self.elif_stmt())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . If ( a , b , [c] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('if'))
            and
            (a := self.named_expression())
            and
            (b := self.colon_block())
            and
            (c := self.else_block(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . If ( a , b , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def elif_stmt(self) -> Optional[ast . stmt]:
        # elif_stmt: invalid_elif_stmt | 'elif' named_expression colon_block elif_stmt | 'elif' named_expression colon_block else_block?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_elif_stmt := self.invalid_elif_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('elif'))
            and
            (a := self.named_expression())
            and
            (b := self.colon_block())
            and
            (c := self.elif_stmt())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . If ( a , b , [c] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('elif'))
            and
            (a := self.named_expression())
            and
            (b := self.colon_block())
            and
            (c := self.else_block(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . If ( a , b , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def else_block(self) -> Optional[List [ast . stmt]]:
        # else_block: invalid_else_stmt | 'else' ':'? block
        mark = self._mark()
        if (
            (invalid_else_stmt := self.invalid_else_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('else'))
            and
            (opt := self.expect(':'),)
            and
            (b := self.block())
        ):
            return b
        self._reset(mark)
        return None

    @memoize
    def while_stmt(self) -> Optional[ast . stmt]:
        # while_stmt: invalid_while_stmt | 'while' named_expression ':' block else_block?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_while_stmt := self.invalid_while_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('while'))
            and
            (a := self.named_expression())
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.block())
            and
            (c := self.else_block(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . While ( a , b , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def for_stmt(self) -> Optional[ast . stmt]:
        # for_stmt: invalid_for_stmt | 'for' star_targets 'in' ~ star_expressions &&':' TYPE_COMMENT? block else_block? | ASYNC 'for' star_targets 'in' ~ star_expressions &&':' TYPE_COMMENT? block else_block? | invalid_for_target
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_for_stmt := self.invalid_for_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        cut = False
        if (
            (literal := self.expect('for'))
            and
            (t := self.star_targets())
            and
            (literal_1 := self.expect('in'))
            and
            (cut := True)
            and
            (ex := self.star_expressions())
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (tc := self.type_comment(),)
            and
            (b := self.block())
            and
            (el := self.else_block(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . For ( t , ex , b , el , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if cut: return None
        cut = False
        if (
            (_async := self.expect('ASYNC'))
            and
            (literal := self.expect('for'))
            and
            (t := self.star_targets())
            and
            (literal_1 := self.expect('in'))
            and
            (cut := True)
            and
            (ex := self.star_expressions())
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (tc := self.type_comment(),)
            and
            (b := self.block())
            and
            (el := self.else_block(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . stmt , 5 , "Async for loops are" , ast . AsyncFor ( t , ex , b , el , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        if cut: return None
        if (
            (invalid_for_target := self.invalid_for_target())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def with_stmt(self) -> Optional[ast . stmt]:
        # with_stmt: invalid_with_stmt_indent | 'with' '(' ','.with_item+ ','? ')' ':' block | 'with' ','.with_item+ ':' TYPE_COMMENT? block | ASYNC 'with' '(' ','.with_item+ ','? ')' ':' block | ASYNC 'with' ','.with_item+ ':' TYPE_COMMENT? block | invalid_with_stmt
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_with_stmt_indent := self.invalid_with_stmt_indent())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('with'))
            and
            (literal_1 := self.expect('('))
            and
            (a := self._gather_50())
            and
            (opt := self.expect(','),)
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect(':'))
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . With ( a , b , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('with'))
            and
            (a := self._gather_52())
            and
            (literal_1 := self.expect(':'))
            and
            (tc := self.type_comment(),)
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . With ( a , b , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (_async := self.expect('ASYNC'))
            and
            (literal := self.expect('with'))
            and
            (literal_1 := self.expect('('))
            and
            (a := self._gather_54())
            and
            (opt := self.expect(','),)
            and
            (literal_2 := self.expect(')'))
            and
            (literal_3 := self.expect(':'))
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . stmt , 5 , "Async with statements are" , ast . AsyncWith ( a , b , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        if (
            (_async := self.expect('ASYNC'))
            and
            (literal := self.expect('with'))
            and
            (a := self._gather_56())
            and
            (literal_1 := self.expect(':'))
            and
            (tc := self.type_comment(),)
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . stmt , 5 , "Async with statements are" , ast . AsyncWith ( a , b , TypeComment ( tc ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        if (
            (invalid_with_stmt := self.invalid_with_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def with_item(self) -> Optional[ast . withitem]:
        # with_item: expression 'as' star_target &(',' | ')' | ':') | invalid_with_item | expression
        mark = self._mark()
        if (
            (e := self.expression())
            and
            (literal := self.expect('as'))
            and
            (t := self.star_target())
            and
            self.positive_lookahead(self._tmp_58, )
        ):
            return _PyAST_withitem ( e , t , p . arena )
        self._reset(mark)
        if (
            (invalid_with_item := self.invalid_with_item())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (e := self.expression())
        ):
            return _PyAST_withitem ( e , None , p . arena )
        self._reset(mark)
        return None

    @memoize
    def try_stmt(self) -> Optional[ast . stmt]:
        # try_stmt: invalid_try_stmt | 'try' &&':' block finally_block | 'try' &&':' block except_block+ else_block? finally_block?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_try_stmt := self.invalid_try_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('try'))
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (b := self.block())
            and
            (f := self.finally_block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Try ( b , None , None , f , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('try'))
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (b := self.block())
            and
            (ex := self._loop1_59())
            and
            (el := self.else_block(),)
            and
            (f := self.finally_block(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Try ( b , ex , el , f , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def except_block(self) -> Optional[ast . excepthandler]:
        # except_block: invalid_except_stmt_indent | 'except' expression ['as' NAME] ':' block | 'except' ':' block | invalid_except_stmt
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_except_stmt_indent := self.invalid_except_stmt_indent())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('except'))
            and
            (e := self.expression())
            and
            (t := self._tmp_60(),)
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . ExceptHandler ( e , t . id if t else None , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('except'))
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.block())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . ExceptHandler ( None , None , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_except_stmt := self.invalid_except_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def finally_block(self) -> Optional[List [ast . stmt]]:
        # finally_block: invalid_finally_stmt | 'finally' &&':' block
        mark = self._mark()
        if (
            (invalid_finally_stmt := self.invalid_finally_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect('finally'))
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
            and
            (a := self.block())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def match_stmt(self) -> Optional[ast . stmt]:
        # match_stmt: "match" subject_expr ':' NEWLINE INDENT case_block+ DEDENT | invalid_match_stmt
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect("match"))
            and
            (subject := self.subject_expr())
            and
            (literal_1 := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
            and
            (cases := self._loop1_61())
            and
            (_dedent := self.expect('DEDENT'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . stmt , 10 , "Pattern matching is" , ast . Match ( subject , cases , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        if (
            (invalid_match_stmt := self.invalid_match_stmt())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def subject_expr(self) -> Optional[ast . expr]:
        # subject_expr: star_named_expression ',' star_named_expressions? | named_expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (value := self.star_named_expression())
            and
            (literal := self.expect(','))
            and
            (values := self.star_named_expressions(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( [value] + values , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (named_expression := self.named_expression())
        ):
            return named_expression
        self._reset(mark)
        return None

    @memoize
    def case_block(self) -> Optional[ast . match_case]:
        # case_block: invalid_case_block | "case" patterns guard? ':' block
        mark = self._mark()
        if (
            (invalid_case_block := self.invalid_case_block())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (literal := self.expect("case"))
            and
            (pattern := self.patterns())
            and
            (guard := self.guard(),)
            and
            (literal_1 := self.expect(':'))
            and
            (body := self.block())
        ):
            return ast . match_case ( pattern , guard , body , p . arena )
        self._reset(mark)
        return None

    @memoize
    def guard(self) -> Optional[ast . expr]:
        # guard: 'if' named_expression
        mark = self._mark()
        if (
            (literal := self.expect('if'))
            and
            (guard := self.named_expression())
        ):
            return guard
        self._reset(mark)
        return None

    @memoize
    def patterns(self) -> Optional[ast . pattern]:
        # patterns: open_sequence_pattern | pattern
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (patterns := self.open_sequence_pattern())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchSequence ( patterns , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (pattern := self.pattern())
        ):
            return pattern
        self._reset(mark)
        return None

    @memoize
    def pattern(self) -> Optional[ast . pattern]:
        # pattern: as_pattern | or_pattern
        mark = self._mark()
        if (
            (as_pattern := self.as_pattern())
        ):
            return as_pattern
        self._reset(mark)
        if (
            (or_pattern := self.or_pattern())
        ):
            return or_pattern
        self._reset(mark)
        return None

    @memoize
    def as_pattern(self) -> Optional[ast . pattern]:
        # as_pattern: or_pattern 'as' pattern_capture_target | invalid_as_pattern
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (pattern := self.or_pattern())
            and
            (literal := self.expect('as'))
            and
            (target := self.pattern_capture_target())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchAs ( pattern , target . id , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_as_pattern := self.invalid_as_pattern())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def or_pattern(self) -> Optional[ast . pattern]:
        # or_pattern: '|'.closed_pattern+
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (patterns := self._gather_62())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return patterns [0] if len ( patterns ) == 1 else ast . MatchOr ( patterns , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def closed_pattern(self) -> Optional[ast . pattern]:
        # closed_pattern: literal_pattern | capture_pattern | wildcard_pattern | value_pattern | group_pattern | sequence_pattern | mapping_pattern | class_pattern
        mark = self._mark()
        if (
            (literal_pattern := self.literal_pattern())
        ):
            return literal_pattern
        self._reset(mark)
        if (
            (capture_pattern := self.capture_pattern())
        ):
            return capture_pattern
        self._reset(mark)
        if (
            (wildcard_pattern := self.wildcard_pattern())
        ):
            return wildcard_pattern
        self._reset(mark)
        if (
            (value_pattern := self.value_pattern())
        ):
            return value_pattern
        self._reset(mark)
        if (
            (group_pattern := self.group_pattern())
        ):
            return group_pattern
        self._reset(mark)
        if (
            (sequence_pattern := self.sequence_pattern())
        ):
            return sequence_pattern
        self._reset(mark)
        if (
            (mapping_pattern := self.mapping_pattern())
        ):
            return mapping_pattern
        self._reset(mark)
        if (
            (class_pattern := self.class_pattern())
        ):
            return class_pattern
        self._reset(mark)
        return None

    @memoize
    def literal_pattern(self) -> Optional[ast . pattern]:
        # literal_pattern: signed_number !('+' | '-') | complex_number | strings | 'None' | 'True' | 'False'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (value := self.signed_number())
            and
            self.negative_lookahead(self._tmp_64, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchValue ( value , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (value := self.complex_number())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchValue ( value , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (value := self.strings())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchValue ( value , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('None'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchSingleton ( Py_None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('True'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchSingleton ( Py_True , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('False'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchSingleton ( Py_False , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def literal_expr(self) -> Optional[ast . expr]:
        # literal_expr: signed_number !('+' | '-') | complex_number | strings | 'None' | 'True' | 'False'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (signed_number := self.signed_number())
            and
            self.negative_lookahead(self._tmp_65, )
        ):
            return signed_number
        self._reset(mark)
        if (
            (complex_number := self.complex_number())
        ):
            return complex_number
        self._reset(mark)
        if (
            (strings := self.strings())
        ):
            return strings
        self._reset(mark)
        if (
            (literal := self.expect('None'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('True'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_True , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('False'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_False , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def complex_number(self) -> Optional[ast . expr]:
        # complex_number: signed_real_number '+' imaginary_number | signed_real_number '-' imaginary_number
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (real := self.signed_real_number())
            and
            (literal := self.expect('+'))
            and
            (imag := self.imaginary_number())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( real , Add , imag , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (real := self.signed_real_number())
            and
            (literal := self.expect('-'))
            and
            (imag := self.imaginary_number())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( real , Sub , imag , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def signed_number(self) -> Optional[ast . expr]:
        # signed_number: NUMBER | '-' NUMBER
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (number := self.number())
        ):
            return number
        self._reset(mark)
        if (
            (literal := self.expect('-'))
            and
            (number := self.number())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . UnaryOp ( USub , number , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def signed_real_number(self) -> Optional[ast . expr]:
        # signed_real_number: real_number | '-' real_number
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (real_number := self.real_number())
        ):
            return real_number
        self._reset(mark)
        if (
            (literal := self.expect('-'))
            and
            (real := self.real_number())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . UnaryOp ( USub , real , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def real_number(self) -> Optional[ast . expr]:
        # real_number: NUMBER
        mark = self._mark()
        if (
            (real := self.number())
        ):
            return _PyPegen_ensure_real ( p , real )
        self._reset(mark)
        return None

    @memoize
    def imaginary_number(self) -> Optional[ast . expr]:
        # imaginary_number: NUMBER
        mark = self._mark()
        if (
            (imag := self.number())
        ):
            return _PyPegen_ensure_imaginary ( p , imag )
        self._reset(mark)
        return None

    @memoize
    def capture_pattern(self) -> Optional[ast . pattern]:
        # capture_pattern: pattern_capture_target
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (target := self.pattern_capture_target())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchAs ( None , target . id , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def pattern_capture_target(self) -> Optional[ast . expr]:
        # pattern_capture_target: !"_" NAME !('.' | '(' | '=')
        mark = self._mark()
        if (
            self.negative_lookahead(self.expect, "_")
            and
            (name := self.name())
            and
            self.negative_lookahead(self._tmp_66, )
        ):
            return set_expr_context ( name , ast . Store )
        self._reset(mark)
        return None

    @memoize
    def wildcard_pattern(self) -> Optional[ast . pattern]:
        # wildcard_pattern: "_"
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect("_"))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchAs ( None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def value_pattern(self) -> Optional[ast . pattern]:
        # value_pattern: attr !('.' | '(' | '=')
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (attr := self.attr())
            and
            self.negative_lookahead(self._tmp_67, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchValue ( attr , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize_left_rec
    def attr(self) -> Optional[ast . expr]:
        # attr: name_or_attr '.' NAME
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (value := self.name_or_attr())
            and
            (literal := self.expect('.'))
            and
            (attr := self.name())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Attribute ( value , attr . id , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @logger
    def name_or_attr(self) -> Optional[ast . expr]:
        # name_or_attr: attr | NAME
        mark = self._mark()
        if (
            (attr := self.attr())
        ):
            return attr
        self._reset(mark)
        if (
            (name := self.name())
        ):
            return name
        self._reset(mark)
        return None

    @memoize
    def group_pattern(self) -> Optional[ast . pattern]:
        # group_pattern: '(' pattern ')'
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (pattern := self.pattern())
            and
            (literal_1 := self.expect(')'))
        ):
            return pattern
        self._reset(mark)
        return None

    @memoize
    def sequence_pattern(self) -> Optional[ast . pattern]:
        # sequence_pattern: '[' maybe_sequence_pattern? ']' | '(' open_sequence_pattern? ')'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('['))
            and
            (patterns := self.maybe_sequence_pattern(),)
            and
            (literal_1 := self.expect(']'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchSequence ( patterns , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (patterns := self.open_sequence_pattern(),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchSequence ( patterns , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def open_sequence_pattern(self) -> Optional[List [ast . AST]]:
        # open_sequence_pattern: maybe_star_pattern ',' maybe_sequence_pattern?
        mark = self._mark()
        if (
            (pattern := self.maybe_star_pattern())
            and
            (literal := self.expect(','))
            and
            (patterns := self.maybe_sequence_pattern(),)
        ):
            return [pattern] + patterns
        self._reset(mark)
        return None

    @memoize
    def maybe_sequence_pattern(self) -> Optional[List [ast . AST]]:
        # maybe_sequence_pattern: ','.maybe_star_pattern+ ','?
        mark = self._mark()
        if (
            (patterns := self._gather_68())
            and
            (opt := self.expect(','),)
        ):
            return patterns
        self._reset(mark)
        return None

    @memoize
    def maybe_star_pattern(self) -> Optional[ast . pattern]:
        # maybe_star_pattern: star_pattern | pattern
        mark = self._mark()
        if (
            (star_pattern := self.star_pattern())
        ):
            return star_pattern
        self._reset(mark)
        if (
            (pattern := self.pattern())
        ):
            return pattern
        self._reset(mark)
        return None

    @memoize
    def star_pattern(self) -> Optional[ast . pattern]:
        # star_pattern: '*' pattern_capture_target | '*' wildcard_pattern
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('*'))
            and
            (target := self.pattern_capture_target())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchStar ( target . id , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('*'))
            and
            (wildcard_pattern := self.wildcard_pattern())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchStar ( None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def mapping_pattern(self) -> Optional[ast . pattern]:
        # mapping_pattern: '{' '}' | '{' double_star_pattern ','? '}' | '{' items_pattern ',' double_star_pattern ','? '}' | '{' items_pattern ','? '}'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('{'))
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchMapping ( None , None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('{'))
            and
            (rest := self.double_star_pattern())
            and
            (opt := self.expect(','),)
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchMapping ( None , None , rest . id , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('{'))
            and
            (items := self.items_pattern())
            and
            (literal_1 := self.expect(','))
            and
            (rest := self.double_star_pattern())
            and
            (opt := self.expect(','),)
            and
            (literal_2 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchMapping ( CHECK ( List [ast . expr] , _PyPegen_get_pattern_keys ( p , items ) ) , CHECK ( List [ast . pattern] , _PyPegen_get_patterns ( p , items ) ) , rest . id , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('{'))
            and
            (items := self.items_pattern())
            and
            (opt := self.expect(','),)
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchMapping ( CHECK ( List [ast . expr] , _PyPegen_get_pattern_keys ( p , items ) ) , CHECK ( List [ast . pattern] , _PyPegen_get_patterns ( p , items ) ) , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def items_pattern(self) -> Optional[List [ast . AST]]:
        # items_pattern: ','.key_value_pattern+
        mark = self._mark()
        if (
            (_gather_70 := self._gather_70())
        ):
            return _gather_70
        self._reset(mark)
        return None

    @memoize
    def key_value_pattern(self) -> Optional[List [KeyPatternPair]]:
        # key_value_pattern: (literal_expr | attr) ':' pattern
        mark = self._mark()
        if (
            (key := self._tmp_72())
            and
            (literal := self.expect(':'))
            and
            (pattern := self.pattern())
        ):
            return _PyPegen_key_pattern_pair ( p , key , pattern )
        self._reset(mark)
        return None

    @memoize
    def double_star_pattern(self) -> Optional[ast . expr]:
        # double_star_pattern: '**' pattern_capture_target
        mark = self._mark()
        if (
            (literal := self.expect('**'))
            and
            (target := self.pattern_capture_target())
        ):
            return target
        self._reset(mark)
        return None

    @memoize
    def class_pattern(self) -> Optional[ast . pattern]:
        # class_pattern: name_or_attr '(' ')' | name_or_attr '(' positional_patterns ','? ')' | name_or_attr '(' keyword_patterns ','? ')' | name_or_attr '(' positional_patterns ',' keyword_patterns ','? ')' | invalid_class_pattern
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (cls := self.name_or_attr())
            and
            (literal := self.expect('('))
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchClass ( cls , None , None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (cls := self.name_or_attr())
            and
            (literal := self.expect('('))
            and
            (patterns := self.positional_patterns())
            and
            (opt := self.expect(','),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchClass ( cls , patterns , None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (cls := self.name_or_attr())
            and
            (literal := self.expect('('))
            and
            (keywords := self.keyword_patterns())
            and
            (opt := self.expect(','),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchClass ( cls , None , map_names_to_ids ( _PyPegen_get_pattern_keys ( p , keywords ) ) , CHECK ( List [ast . pattern] , _PyPegen_get_patterns ( p , keywords ) ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (cls := self.name_or_attr())
            and
            (literal := self.expect('('))
            and
            (patterns := self.positional_patterns())
            and
            (literal_1 := self.expect(','))
            and
            (keywords := self.keyword_patterns())
            and
            (opt := self.expect(','),)
            and
            (literal_2 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . MatchClass ( cls , patterns , map_names_to_ids ( _PyPegen_get_pattern_keys ( p , keywords ) ) , CHECK ( List [ast . pattern] , _PyPegen_get_patterns ( p , keywords ) ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_class_pattern := self.invalid_class_pattern())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def positional_patterns(self) -> Optional[List [ast . pattern]]:
        # positional_patterns: ','.pattern+
        mark = self._mark()
        if (
            (args := self._gather_73())
        ):
            return args
        self._reset(mark)
        return None

    @memoize
    def keyword_patterns(self) -> Optional[List [ast . AST]]:
        # keyword_patterns: ','.keyword_pattern+
        mark = self._mark()
        if (
            (_gather_75 := self._gather_75())
        ):
            return _gather_75
        self._reset(mark)
        return None

    @memoize
    def keyword_pattern(self) -> Optional[List [KeyPatternPair]]:
        # keyword_pattern: NAME '=' pattern
        mark = self._mark()
        if (
            (arg := self.name())
            and
            (literal := self.expect('='))
            and
            (value := self.pattern())
        ):
            return _PyPegen_key_pattern_pair ( p , arg , value )
        self._reset(mark)
        return None

    @memoize
    def expressions(self) -> Optional[ast . expr]:
        # expressions: expression ((',' expression))+ ','? | expression ',' | expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.expression())
            and
            (b := self._loop1_77())
            and
            (opt := self.expect(','),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( [a] + b , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.expression())
            and
            (literal := self.expect(','))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( [a] , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (expression := self.expression())
        ):
            return expression
        self._reset(mark)
        return None

    @memoize
    def expression(self) -> Optional[ast . expr]:
        # expression: invalid_expression | disjunction 'if' disjunction 'else' expression | disjunction | lambdef
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_expression := self.invalid_expression())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (a := self.disjunction())
            and
            (literal := self.expect('if'))
            and
            (b := self.disjunction())
            and
            (literal_1 := self.expect('else'))
            and
            (c := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . IfExp ( b , a , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (disjunction := self.disjunction())
        ):
            return disjunction
        self._reset(mark)
        if (
            (lambdef := self.lambdef())
        ):
            return lambdef
        self._reset(mark)
        return None

    @memoize
    def yield_expr(self) -> Optional[ast . expr]:
        # yield_expr: 'yield' 'from' expression | 'yield' star_expressions?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('yield'))
            and
            (literal_1 := self.expect('from'))
            and
            (a := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . YieldFrom ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('yield'))
            and
            (a := self.star_expressions(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Yield ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def star_expressions(self) -> Optional[ast . expr]:
        # star_expressions: star_expression ((',' star_expression))+ ','? | star_expression ',' | star_expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.star_expression())
            and
            (b := self._loop1_78())
            and
            (opt := self.expect(','),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( [a] + b , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.star_expression())
            and
            (literal := self.expect(','))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( [a] , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (star_expression := self.star_expression())
        ):
            return star_expression
        self._reset(mark)
        return None

    @memoize
    def star_expression(self) -> Optional[ast . expr]:
        # star_expression: '*' bitwise_or | expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('*'))
            and
            (a := self.bitwise_or())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Starred ( a , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (expression := self.expression())
        ):
            return expression
        self._reset(mark)
        return None

    @memoize
    def star_named_expressions(self) -> Optional[List [ast . expr]]:
        # star_named_expressions: ','.star_named_expression+ ','?
        mark = self._mark()
        if (
            (a := self._gather_79())
            and
            (opt := self.expect(','),)
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def star_named_expression(self) -> Optional[ast . expr]:
        # star_named_expression: '*' bitwise_or | named_expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('*'))
            and
            (a := self.bitwise_or())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Starred ( a , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (named_expression := self.named_expression())
        ):
            return named_expression
        self._reset(mark)
        return None

    @memoize
    def assigment_expression(self) -> Optional[ast . expr]:
        # assigment_expression: NAME ':=' ~ expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        cut = False
        if (
            (a := self.name())
            and
            (literal := self.expect(':='))
            and
            (cut := True)
            and
            (b := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . NamedExpr ( CHECK ( ast . expr , set_expr_context ( a , ast . Store ) ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if cut: return None
        return None

    @memoize
    def named_expression(self) -> Optional[ast . expr]:
        # named_expression: assigment_expression | invalid_named_expression | expression !':='
        mark = self._mark()
        if (
            (assigment_expression := self.assigment_expression())
        ):
            return assigment_expression
        self._reset(mark)
        if (
            (invalid_named_expression := self.invalid_named_expression())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            self.negative_lookahead(self.expect, ':=')
        ):
            return expression
        self._reset(mark)
        return None

    @memoize
    def disjunction(self) -> Optional[ast . expr]:
        # disjunction: conjunction (('or' conjunction))+ | conjunction
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.conjunction())
            and
            (b := self._loop1_81())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BoolOp ( Or , [a] + b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (conjunction := self.conjunction())
        ):
            return conjunction
        self._reset(mark)
        return None

    @memoize
    def conjunction(self) -> Optional[ast . expr]:
        # conjunction: inversion (('and' inversion))+ | inversion
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.inversion())
            and
            (b := self._loop1_82())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BoolOp ( And , [a] + b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (inversion := self.inversion())
        ):
            return inversion
        self._reset(mark)
        return None

    @memoize
    def inversion(self) -> Optional[ast . expr]:
        # inversion: 'not' inversion | comparison
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('not'))
            and
            (a := self.inversion())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . UnaryOp ( Not , a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (comparison := self.comparison())
        ):
            return comparison
        self._reset(mark)
        return None

    @memoize
    def comparison(self) -> Optional[ast . expr]:
        # comparison: bitwise_or compare_op_bitwise_or_pair+ | bitwise_or
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.bitwise_or())
            and
            (b := self._loop1_83())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Compare ( a , [pair . cmpop for pair in b] , [pair . expr for pair in b] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (bitwise_or := self.bitwise_or())
        ):
            return bitwise_or
        self._reset(mark)
        return None

    @memoize
    def compare_op_bitwise_or_pair(self) -> Optional[CmpopExprPair]:
        # compare_op_bitwise_or_pair: eq_bitwise_or | noteq_bitwise_or | lte_bitwise_or | lt_bitwise_or | gte_bitwise_or | gt_bitwise_or | notin_bitwise_or | in_bitwise_or | isnot_bitwise_or | is_bitwise_or
        mark = self._mark()
        if (
            (eq_bitwise_or := self.eq_bitwise_or())
        ):
            return eq_bitwise_or
        self._reset(mark)
        if (
            (noteq_bitwise_or := self.noteq_bitwise_or())
        ):
            return noteq_bitwise_or
        self._reset(mark)
        if (
            (lte_bitwise_or := self.lte_bitwise_or())
        ):
            return lte_bitwise_or
        self._reset(mark)
        if (
            (lt_bitwise_or := self.lt_bitwise_or())
        ):
            return lt_bitwise_or
        self._reset(mark)
        if (
            (gte_bitwise_or := self.gte_bitwise_or())
        ):
            return gte_bitwise_or
        self._reset(mark)
        if (
            (gt_bitwise_or := self.gt_bitwise_or())
        ):
            return gt_bitwise_or
        self._reset(mark)
        if (
            (notin_bitwise_or := self.notin_bitwise_or())
        ):
            return notin_bitwise_or
        self._reset(mark)
        if (
            (in_bitwise_or := self.in_bitwise_or())
        ):
            return in_bitwise_or
        self._reset(mark)
        if (
            (isnot_bitwise_or := self.isnot_bitwise_or())
        ):
            return isnot_bitwise_or
        self._reset(mark)
        if (
            (is_bitwise_or := self.is_bitwise_or())
        ):
            return is_bitwise_or
        self._reset(mark)
        return None

    @memoize
    def eq_bitwise_or(self) -> Optional[CmpopExprPair]:
        # eq_bitwise_or: '==' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('=='))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . Eq ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def noteq_bitwise_or(self) -> Optional[CmpopExprPair]:
        # noteq_bitwise_or: ('!=') bitwise_or
        mark = self._mark()
        if (
            (tok := self.expect('!='))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . NotEq ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def lte_bitwise_or(self) -> Optional[CmpopExprPair]:
        # lte_bitwise_or: '<=' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('<='))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . LtE ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def lt_bitwise_or(self) -> Optional[CmpopExprPair]:
        # lt_bitwise_or: '<' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('<'))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . Lt ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def gte_bitwise_or(self) -> Optional[CmpopExprPair]:
        # gte_bitwise_or: '>=' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('>='))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . GtE ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def gt_bitwise_or(self) -> Optional[CmpopExprPair]:
        # gt_bitwise_or: '>' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('>'))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . Gt ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def notin_bitwise_or(self) -> Optional[CmpopExprPair]:
        # notin_bitwise_or: 'not' 'in' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('not'))
            and
            (literal_1 := self.expect('in'))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . NotIn ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def in_bitwise_or(self) -> Optional[CmpopExprPair]:
        # in_bitwise_or: 'in' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('in'))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . In ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def isnot_bitwise_or(self) -> Optional[CmpopExprPair]:
        # isnot_bitwise_or: 'is' 'not' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('is'))
            and
            (literal_1 := self.expect('not'))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . IsNot ( ) , a )
        self._reset(mark)
        return None

    @memoize
    def is_bitwise_or(self) -> Optional[CmpopExprPair]:
        # is_bitwise_or: 'is' bitwise_or
        mark = self._mark()
        if (
            (literal := self.expect('is'))
            and
            (a := self.bitwise_or())
        ):
            return CmpopExprPair ( ast . Is ( ) , a )
        self._reset(mark)
        return None

    @memoize_left_rec
    def bitwise_or(self) -> Optional[ast . expr]:
        # bitwise_or: bitwise_or '|' bitwise_xor | bitwise_xor
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.bitwise_or())
            and
            (literal := self.expect('|'))
            and
            (b := self.bitwise_xor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , BitOr , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (bitwise_xor := self.bitwise_xor())
        ):
            return bitwise_xor
        self._reset(mark)
        return None

    @memoize_left_rec
    def bitwise_xor(self) -> Optional[ast . expr]:
        # bitwise_xor: bitwise_xor '^' bitwise_and | bitwise_and
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.bitwise_xor())
            and
            (literal := self.expect('^'))
            and
            (b := self.bitwise_and())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , BitXor , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (bitwise_and := self.bitwise_and())
        ):
            return bitwise_and
        self._reset(mark)
        return None

    @memoize_left_rec
    def bitwise_and(self) -> Optional[ast . expr]:
        # bitwise_and: bitwise_and '&' shift_expr | shift_expr
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.bitwise_and())
            and
            (literal := self.expect('&'))
            and
            (b := self.shift_expr())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , BitAnd , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (shift_expr := self.shift_expr())
        ):
            return shift_expr
        self._reset(mark)
        return None

    @memoize_left_rec
    def shift_expr(self) -> Optional[ast . expr]:
        # shift_expr: shift_expr '<<' sum | shift_expr '>>' sum | sum
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.shift_expr())
            and
            (literal := self.expect('<<'))
            and
            (b := self.sum())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , LShift , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.shift_expr())
            and
            (literal := self.expect('>>'))
            and
            (b := self.sum())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , RShift , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (sum := self.sum())
        ):
            return sum
        self._reset(mark)
        return None

    @memoize_left_rec
    def sum(self) -> Optional[ast . expr]:
        # sum: sum '+' term | sum '-' term | term
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.sum())
            and
            (literal := self.expect('+'))
            and
            (b := self.term())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , ast . Add ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.sum())
            and
            (literal := self.expect('-'))
            and
            (b := self.term())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , ast . Sub ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (term := self.term())
        ):
            return term
        self._reset(mark)
        return None

    @memoize_left_rec
    def term(self) -> Optional[ast . expr]:
        # term: term '*' factor | term '/' factor | term '//' factor | term '%' factor | term '@' factor | factor
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.term())
            and
            (literal := self.expect('*'))
            and
            (b := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , ast . Mult ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.term())
            and
            (literal := self.expect('/'))
            and
            (b := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , ast . Div ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.term())
            and
            (literal := self.expect('//'))
            and
            (b := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , ast . FloorDiv ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.term())
            and
            (literal := self.expect('%'))
            and
            (b := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , ast . Mod ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.term())
            and
            (literal := self.expect('@'))
            and
            (b := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . expr , 5 , "The '@' operator is" , ast . BinOp ( a , ast . MatMult ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        if (
            (factor := self.factor())
        ):
            return factor
        self._reset(mark)
        return None

    @memoize
    def factor(self) -> Optional[ast . expr]:
        # factor: '+' factor | '-' factor | '~' factor | power
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('+'))
            and
            (a := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . UnaryOp ( ast . UAdd ( ) , a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('-'))
            and
            (a := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . UnaryOp ( ast . USub ( ) , a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('~'))
            and
            (a := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . UnaryOp ( ast . Invert ( ) , a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (power := self.power())
        ):
            return power
        self._reset(mark)
        return None

    @memoize
    def power(self) -> Optional[ast . expr]:
        # power: await_primary '**' factor | await_primary
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.await_primary())
            and
            (literal := self.expect('**'))
            and
            (b := self.factor())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . BinOp ( a , Pow , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (await_primary := self.await_primary())
        ):
            return await_primary
        self._reset(mark)
        return None

    @memoize
    def await_primary(self) -> Optional[ast . expr]:
        # await_primary: AWAIT primary | primary
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (_await := self.expect('AWAIT'))
            and
            (a := self.primary())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return CHECK_VERSION ( ast . expr , 5 , "Await expressions are" , ast . Await ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) )
        self._reset(mark)
        if (
            (primary := self.primary())
        ):
            return primary
        self._reset(mark)
        return None

    @memoize_left_rec
    def primary(self) -> Optional[ast . expr]:
        # primary: primary '.' NAME | primary genexp | primary '(' arguments? ')' | primary '[' slices ']' | atom
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.primary())
            and
            (literal := self.expect('.'))
            and
            (b := self.name())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Attribute ( a , b . id , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.primary())
            and
            (b := self.genexp())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Call ( a , [b] , [] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.primary())
            and
            (literal := self.expect('('))
            and
            (b := self.arguments(),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Call ( a , b . args if b else [] , b . keywords if b else [] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.primary())
            and
            (literal := self.expect('['))
            and
            (b := self.slices())
            and
            (literal_1 := self.expect(']'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Subscript ( a , b , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (atom := self.atom())
        ):
            return atom
        self._reset(mark)
        return None

    @memoize
    def slices(self) -> Optional[ast . expr]:
        # slices: slice !',' | ','.slice+ ','?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.slice())
            and
            self.negative_lookahead(self.expect, ',')
        ):
            return a
        self._reset(mark)
        if (
            (a := self._gather_84())
            and
            (opt := self.expect(','),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( a , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def slice(self) -> Optional[ast . expr]:
        # slice: expression? ':' expression? [':' expression?] | named_expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.expression(),)
            and
            (literal := self.expect(':'))
            and
            (b := self.expression(),)
            and
            (c := self._tmp_86(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Slice ( a , b , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.named_expression())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def atom(self) -> Optional[ast . expr]:
        # atom: NAME | 'True' | 'False' | 'None' | &STRING strings | NUMBER | &'(' (tuple | group | genexp) | &'[' (list | listcomp) | &'{' (dict | set | dictcomp | setcomp) | '...'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (name := self.name())
        ):
            return name
        self._reset(mark)
        if (
            (literal := self.expect('True'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_True , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('False'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_False , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('None'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            self.positive_lookahead(self.string, )
            and
            (strings := self.strings())
        ):
            return strings
        self._reset(mark)
        if (
            (number := self.number())
        ):
            return number
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, '(')
            and
            (_tmp_87 := self._tmp_87())
        ):
            return _tmp_87
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, '[')
            and
            (_tmp_88 := self._tmp_88())
        ):
            return _tmp_88
        self._reset(mark)
        if (
            self.positive_lookahead(self.expect, '{')
            and
            (_tmp_89 := self._tmp_89())
        ):
            return _tmp_89
        self._reset(mark)
        if (
            (literal := self.expect('...'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Constant ( Py_Ellipsis , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def group(self) -> Optional[ast . expr]:
        # group: '(' (yield_expr | named_expression) ')' | invalid_group
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (a := self._tmp_90())
            and
            (literal_1 := self.expect(')'))
        ):
            return a
        self._reset(mark)
        if (
            (invalid_group := self.invalid_group())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def lambdef(self) -> Optional[ast . expr]:
        # lambdef: 'lambda' lambda_params? ':' expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('lambda'))
            and
            (a := self.lambda_params(),)
            and
            (literal_1 := self.expect(':'))
            and
            (b := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Lambda ( a if a else empty_arguments ( ) , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def lambda_params(self) -> Optional[ast . arguments]:
        # lambda_params: invalid_lambda_parameters | lambda_parameters
        mark = self._mark()
        if (
            (invalid_lambda_parameters := self.invalid_lambda_parameters())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (lambda_parameters := self.lambda_parameters())
        ):
            return lambda_parameters
        self._reset(mark)
        return None

    @memoize
    def lambda_parameters(self) -> Optional[ast . arguments]:
        # lambda_parameters: lambda_slash_no_default lambda_param_no_default* lambda_param_with_default* lambda_star_etc? | lambda_slash_with_default lambda_param_with_default* lambda_star_etc? | lambda_param_no_default+ lambda_param_with_default* lambda_star_etc? | lambda_param_with_default+ lambda_star_etc? | lambda_star_etc
        mark = self._mark()
        if (
            (a := self.lambda_slash_no_default())
            and
            (b := self._loop0_91(),)
            and
            (c := self._loop0_92(),)
            and
            (d := self.lambda_star_etc(),)
        ):
            return make_arguments ( a , None , b , c , d )
        self._reset(mark)
        if (
            (a := self.lambda_slash_with_default())
            and
            (b := self._loop0_93(),)
            and
            (c := self.lambda_star_etc(),)
        ):
            return make_arguments ( None , a , None , b , c )
        self._reset(mark)
        if (
            (a := self._loop1_94())
            and
            (b := self._loop0_95(),)
            and
            (c := self.lambda_star_etc(),)
        ):
            return make_arguments ( None , None , a , b , c )
        self._reset(mark)
        if (
            (a := self._loop1_96())
            and
            (b := self.lambda_star_etc(),)
        ):
            return make_arguments ( None , None , None , a , b )
        self._reset(mark)
        if (
            (a := self.lambda_star_etc())
        ):
            return make_arguments ( None , None , None , None , a )
        self._reset(mark)
        return None

    @memoize
    def lambda_slash_no_default(self) -> Optional[List [ast . arg]]:
        # lambda_slash_no_default: lambda_param_no_default+ '/' ',' | lambda_param_no_default+ '/' &':'
        mark = self._mark()
        if (
            (a := self._loop1_97())
            and
            (literal := self.expect('/'))
            and
            (literal_1 := self.expect(','))
        ):
            return a
        self._reset(mark)
        if (
            (a := self._loop1_98())
            and
            (literal := self.expect('/'))
            and
            self.positive_lookahead(self.expect, ':')
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def lambda_slash_with_default(self) -> Optional[SlashWithDefault]:
        # lambda_slash_with_default: lambda_param_no_default* lambda_param_with_default+ '/' ',' | lambda_param_no_default* lambda_param_with_default+ '/' &':'
        mark = self._mark()
        if (
            (a := self._loop0_99(),)
            and
            (b := self._loop1_100())
            and
            (literal := self.expect('/'))
            and
            (literal_1 := self.expect(','))
        ):
            return SlashWithDefault ( a , b )
        self._reset(mark)
        if (
            (a := self._loop0_101(),)
            and
            (b := self._loop1_102())
            and
            (literal := self.expect('/'))
            and
            self.positive_lookahead(self.expect, ':')
        ):
            return SlashWithDefault ( a , b )
        self._reset(mark)
        return None

    @memoize
    def lambda_star_etc(self) -> Optional[StarEtc]:
        # lambda_star_etc: '*' lambda_param_no_default lambda_param_maybe_default* lambda_kwds? | '*' ',' lambda_param_maybe_default+ lambda_kwds? | lambda_kwds | invalid_lambda_star_etc
        mark = self._mark()
        if (
            (literal := self.expect('*'))
            and
            (a := self.lambda_param_no_default())
            and
            (b := self._loop0_103(),)
            and
            (c := self.lambda_kwds(),)
        ):
            return StarEtc ( a , b , c )
        self._reset(mark)
        if (
            (literal := self.expect('*'))
            and
            (literal_1 := self.expect(','))
            and
            (b := self._loop1_104())
            and
            (c := self.lambda_kwds(),)
        ):
            return StarEtc ( None , b , c )
        self._reset(mark)
        if (
            (a := self.lambda_kwds())
        ):
            return StarEtc ( None , None , a )
        self._reset(mark)
        if (
            (invalid_lambda_star_etc := self.invalid_lambda_star_etc())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def lambda_kwds(self) -> Optional[ast . arg]:
        # lambda_kwds: '**' lambda_param_no_default
        mark = self._mark()
        if (
            (literal := self.expect('**'))
            and
            (a := self.lambda_param_no_default())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def lambda_param_no_default(self) -> Optional[ast . arg]:
        # lambda_param_no_default: lambda_param ',' | lambda_param &':'
        mark = self._mark()
        if (
            (a := self.lambda_param())
            and
            (literal := self.expect(','))
        ):
            return a
        self._reset(mark)
        if (
            (a := self.lambda_param())
            and
            self.positive_lookahead(self.expect, ':')
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def lambda_param_with_default(self) -> Optional[NameDefaultPair]:
        # lambda_param_with_default: lambda_param default ',' | lambda_param default &':'
        mark = self._mark()
        if (
            (a := self.lambda_param())
            and
            (c := self.default())
            and
            (literal := self.expect(','))
        ):
            return NameDefaultPair ( a , c , None )
        self._reset(mark)
        if (
            (a := self.lambda_param())
            and
            (c := self.default())
            and
            self.positive_lookahead(self.expect, ':')
        ):
            return NameDefaultPair ( a , c , None )
        self._reset(mark)
        return None

    @memoize
    def lambda_param_maybe_default(self) -> Optional[NameDefaultPair]:
        # lambda_param_maybe_default: lambda_param default? ',' | lambda_param default? &':'
        mark = self._mark()
        if (
            (a := self.lambda_param())
            and
            (c := self.default(),)
            and
            (literal := self.expect(','))
        ):
            return NameDefaultPair ( a , c , None )
        self._reset(mark)
        if (
            (a := self.lambda_param())
            and
            (c := self.default(),)
            and
            self.positive_lookahead(self.expect, ':')
        ):
            return NameDefaultPair ( a , c , None )
        self._reset(mark)
        return None

    @memoize
    def lambda_param(self) -> Optional[ast . arg]:
        # lambda_param: NAME
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.name())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . arg ( a . id , None , None , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def strings(self) -> Optional[ast . expr]:
        # strings: STRING+
        mark = self._mark()
        if (
            (a := self._loop1_105())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def list(self) -> Optional[ast . expr]:
        # list: '[' star_named_expressions? ']'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('['))
            and
            (a := self.star_named_expressions(),)
            and
            (literal_1 := self.expect(']'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . List ( a , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def tuple(self) -> Optional[ast . expr]:
        # tuple: '(' [star_named_expression ',' star_named_expressions?] ')'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('('))
            and
            (a := self._tmp_106(),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( a , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def set(self) -> Optional[ast . expr]:
        # set: '{' star_named_expressions '}'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('{'))
            and
            (a := self.star_named_expressions())
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Set ( a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def dict(self) -> Optional[ast . expr]:
        # dict: '{' double_starred_kvpairs? '}' | '{' invalid_double_starred_kvpairs '}'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('{'))
            and
            (a := self.double_starred_kvpairs(),)
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Dict ( CHECK ( List [ast . expr] , _PyPegen_get_keys ( p , a ) ) , CHECK ( List [ast . expr] , _PyPegen_get_values ( p , a ) ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('{'))
            and
            (invalid_double_starred_kvpairs := self.invalid_double_starred_kvpairs())
            and
            (literal_1 := self.expect('}'))
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def double_starred_kvpairs(self) -> Optional[List]:
        # double_starred_kvpairs: ','.double_starred_kvpair+ ','?
        mark = self._mark()
        if (
            (a := self._gather_107())
            and
            (opt := self.expect(','),)
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def double_starred_kvpair(self) -> Optional[KeyValuePair]:
        # double_starred_kvpair: '**' bitwise_or | kvpair
        mark = self._mark()
        if (
            (literal := self.expect('**'))
            and
            (a := self.bitwise_or())
        ):
            return KeyValuePair ( None , a )
        self._reset(mark)
        if (
            (kvpair := self.kvpair())
        ):
            return kvpair
        self._reset(mark)
        return None

    @memoize
    def kvpair(self) -> Optional[KeyValuePair]:
        # kvpair: expression ':' expression
        mark = self._mark()
        if (
            (a := self.expression())
            and
            (literal := self.expect(':'))
            and
            (b := self.expression())
        ):
            return KeyValuePair ( a , b )
        self._reset(mark)
        return None

    @memoize
    def for_if_clauses(self) -> Optional[List [ast . comprehension]]:
        # for_if_clauses: for_if_clause+
        mark = self._mark()
        if (
            (a := self._loop1_109())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def for_if_clause(self) -> Optional[ast . comprehension]:
        # for_if_clause: ASYNC 'for' star_targets 'in' ~ disjunction (('if' disjunction))* | 'for' star_targets 'in' ~ disjunction (('if' disjunction))* | invalid_for_target
        mark = self._mark()
        cut = False
        if (
            (_async := self.expect('ASYNC'))
            and
            (literal := self.expect('for'))
            and
            (a := self.star_targets())
            and
            (literal_1 := self.expect('in'))
            and
            (cut := True)
            and
            (b := self.disjunction())
            and
            (c := self._loop0_110(),)
        ):
            return CHECK_VERSION ( ast . comprehension , 6 , "Async comprehensions are" , _PyAST_comprehension ( a , b , c , 1 , p . arena ) )
        self._reset(mark)
        if cut: return None
        cut = False
        if (
            (literal := self.expect('for'))
            and
            (a := self.star_targets())
            and
            (literal_1 := self.expect('in'))
            and
            (cut := True)
            and
            (b := self.disjunction())
            and
            (c := self._loop0_111(),)
        ):
            return _PyAST_comprehension ( a , b , c , 0 , p . arena )
        self._reset(mark)
        if cut: return None
        if (
            (invalid_for_target := self.invalid_for_target())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def listcomp(self) -> Optional[ast . expr]:
        # listcomp: '[' named_expression for_if_clauses ']' | invalid_comprehension
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('['))
            and
            (a := self.named_expression())
            and
            (b := self.for_if_clauses())
            and
            (literal_1 := self.expect(']'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . ListComp ( a , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_comprehension := self.invalid_comprehension())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def setcomp(self) -> Optional[ast . expr]:
        # setcomp: '{' named_expression for_if_clauses '}' | invalid_comprehension
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('{'))
            and
            (a := self.named_expression())
            and
            (b := self.for_if_clauses())
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . SetComp ( a , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_comprehension := self.invalid_comprehension())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def genexp(self) -> Optional[ast . expr]:
        # genexp: '(' (assigment_expression | expression !':=') for_if_clauses ')' | invalid_comprehension
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('('))
            and
            (a := self._tmp_112())
            and
            (b := self.for_if_clauses())
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . GeneratorExp ( a , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_comprehension := self.invalid_comprehension())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def dictcomp(self) -> Optional[ast . expr]:
        # dictcomp: '{' kvpair for_if_clauses '}' | invalid_dict_comprehension
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('{'))
            and
            (a := self.kvpair())
            and
            (b := self.for_if_clauses())
            and
            (literal_1 := self.expect('}'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . DictComp ( a . key , a . value , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (invalid_dict_comprehension := self.invalid_dict_comprehension())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def arguments(self) -> Optional[ast . expr]:
        # arguments: args ','? &')' | invalid_arguments
        mark = self._mark()
        if (
            (a := self.args())
            and
            (opt := self.expect(','),)
            and
            self.positive_lookahead(self.expect, ')')
        ):
            return a
        self._reset(mark)
        if (
            (invalid_arguments := self.invalid_arguments())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        return None

    @memoize
    def args(self) -> Optional[ast . expr]:
        # args: ','.(starred_expression | (assigment_expression | expression !':=') !'=')+ [',' kwargs] | kwargs
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self._gather_113())
            and
            (b := self._tmp_115(),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Call ( None , a , [] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.kwargs())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Call ( _PyPegen_dummy_name ( p ) , CHECK_NULL_ALLOWED ( List [ast . expr] , _PyPegen_seq_extract_starred_exprs ( p , a ) ) , CHECK_NULL_ALLOWED ( List [ast . keyword] , _PyPegen_seq_delete_starred_exprs ( p , a ) ) , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def kwargs(self) -> Optional[List [ast . AST]]:
        # kwargs: ','.kwarg_or_starred+ ',' ','.kwarg_or_double_starred+ | ','.kwarg_or_starred+ | ','.kwarg_or_double_starred+
        mark = self._mark()
        if (
            (a := self._gather_116())
            and
            (literal := self.expect(','))
            and
            (b := self._gather_118())
        ):
            return _PyPegen_join_sequences ( p , a , b )
        self._reset(mark)
        if (
            (_gather_120 := self._gather_120())
        ):
            return _gather_120
        self._reset(mark)
        if (
            (_gather_122 := self._gather_122())
        ):
            return _gather_122
        self._reset(mark)
        return None

    @memoize
    def starred_expression(self) -> Optional[ast . expr]:
        # starred_expression: '*' expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('*'))
            and
            (a := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Starred ( a , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def kwarg_or_starred(self) -> Optional[KeywordOrStarred]:
        # kwarg_or_starred: invalid_kwarg | NAME '=' expression | starred_expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_kwarg := self.invalid_kwarg())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (a := self.name())
            and
            (literal := self.expect('='))
            and
            (b := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return KeywordOrStarred ( ast . keyword ( a . id , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) , 1 )
        self._reset(mark)
        if (
            (a := self.starred_expression())
        ):
            return KeywordOrStarred ( a , 0 )
        self._reset(mark)
        return None

    @memoize
    def kwarg_or_double_starred(self) -> Optional[KeywordOrStarred]:
        # kwarg_or_double_starred: invalid_kwarg | NAME '=' expression | '**' expression
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (invalid_kwarg := self.invalid_kwarg())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (a := self.name())
            and
            (literal := self.expect('='))
            and
            (b := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return KeywordOrStarred ( ast . keyword ( a . id , b , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) , 1 )
        self._reset(mark)
        if (
            (literal := self.expect('**'))
            and
            (a := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return KeywordOrStarred ( ast . keyword ( None , a , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset ) , 1 )
        self._reset(mark)
        return None

    @memoize
    def star_targets(self) -> Optional[ast . expr]:
        # star_targets: star_target !',' | star_target ((',' star_target))* ','?
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.star_target())
            and
            self.negative_lookahead(self.expect, ',')
        ):
            return a
        self._reset(mark)
        if (
            (a := self.star_target())
            and
            (b := self._loop0_124(),)
            and
            (opt := self.expect(','),)
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( [a] + b , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def star_targets_list_seq(self) -> Optional[List [ast . expr]]:
        # star_targets_list_seq: ','.star_target+ ','?
        mark = self._mark()
        if (
            (a := self._gather_125())
            and
            (opt := self.expect(','),)
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def star_targets_tuple_seq(self) -> Optional[List [ast . expr]]:
        # star_targets_tuple_seq: star_target ((',' star_target))+ ','? | star_target ','
        mark = self._mark()
        if (
            (a := self.star_target())
            and
            (b := self._loop1_127())
            and
            (opt := self.expect(','),)
        ):
            return [a] + b
        self._reset(mark)
        if (
            (a := self.star_target())
            and
            (literal := self.expect(','))
        ):
            return [a]
        self._reset(mark)
        return None

    @memoize
    def star_target(self) -> Optional[ast . expr]:
        # star_target: '*' (!'*' star_target) | target_with_star_atom
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (literal := self.expect('*'))
            and
            (a := self._tmp_128())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Starred ( set_expr_context ( a , ast . Store ) , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (target_with_star_atom := self.target_with_star_atom())
        ):
            return target_with_star_atom
        self._reset(mark)
        return None

    @memoize
    def target_with_star_atom(self) -> Optional[ast . expr]:
        # target_with_star_atom: t_primary '.' NAME !t_lookahead | t_primary '[' slices ']' !t_lookahead | star_atom
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('.'))
            and
            (b := self.name())
            and
            self.negative_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Attribute ( a , b . id , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('['))
            and
            (b := self.slices())
            and
            (literal_1 := self.expect(']'))
            and
            self.negative_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Subscript ( a , b , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (star_atom := self.star_atom())
        ):
            return star_atom
        self._reset(mark)
        return None

    @memoize
    def star_atom(self) -> Optional[ast . expr]:
        # star_atom: NAME | '(' target_with_star_atom ')' | '(' star_targets_tuple_seq? ')' | '[' star_targets_list_seq? ']'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.name())
        ):
            return set_expr_context ( a , ast . Store )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.target_with_star_atom())
            and
            (literal_1 := self.expect(')'))
        ):
            return set_expr_context ( a , ast . Store )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.star_targets_tuple_seq(),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( a , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('['))
            and
            (a := self.star_targets_list_seq(),)
            and
            (literal_1 := self.expect(']'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . List ( a , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def single_target(self) -> Optional[ast . expr]:
        # single_target: single_subscript_attribute_target | NAME | '(' single_target ')'
        mark = self._mark()
        if (
            (single_subscript_attribute_target := self.single_subscript_attribute_target())
        ):
            return single_subscript_attribute_target
        self._reset(mark)
        if (
            (a := self.name())
        ):
            return set_expr_context ( a , ast . Store )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.single_target())
            and
            (literal_1 := self.expect(')'))
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def single_subscript_attribute_target(self) -> Optional[ast . expr]:
        # single_subscript_attribute_target: t_primary '.' NAME !t_lookahead | t_primary '[' slices ']' !t_lookahead
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('.'))
            and
            (b := self.name())
            and
            self.negative_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Attribute ( a , b . id , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('['))
            and
            (b := self.slices())
            and
            (literal_1 := self.expect(']'))
            and
            self.negative_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Subscript ( a , b , ast . Store , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize_left_rec
    def t_primary(self) -> Optional[ast . expr]:
        # t_primary: t_primary '.' NAME &t_lookahead | t_primary '[' slices ']' &t_lookahead | t_primary genexp &t_lookahead | t_primary '(' arguments? ')' &t_lookahead | atom &t_lookahead
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('.'))
            and
            (b := self.name())
            and
            self.positive_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Attribute ( a , b . id , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('['))
            and
            (b := self.slices())
            and
            (literal_1 := self.expect(']'))
            and
            self.positive_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Subscript ( a , b , ast . Load , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.t_primary())
            and
            (b := self.genexp())
            and
            self.positive_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Call ( a , [b] , [] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('('))
            and
            (b := self.arguments(),)
            and
            (literal_1 := self.expect(')'))
            and
            self.positive_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Call ( a , b . args if b else [] , b . keywords if b else [] , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.atom())
            and
            self.positive_lookahead(self.t_lookahead, )
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def t_lookahead(self) -> Optional[Any]:
        # t_lookahead: '(' | '[' | '.'
        mark = self._mark()
        if (
            (literal := self.expect('('))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('['))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def del_targets(self) -> Optional[List [ast . expr]]:
        # del_targets: ','.del_target+ ','?
        mark = self._mark()
        if (
            (a := self._gather_129())
            and
            (opt := self.expect(','),)
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def del_target(self) -> Optional[ast . expr]:
        # del_target: t_primary '.' NAME !t_lookahead | t_primary '[' slices ']' !t_lookahead | del_t_atom
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('.'))
            and
            (b := self.name())
            and
            self.negative_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Attribute ( a , b . id , Del , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (a := self.t_primary())
            and
            (literal := self.expect('['))
            and
            (b := self.slices())
            and
            (literal_1 := self.expect(']'))
            and
            self.negative_lookahead(self.t_lookahead, )
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Subscript ( a , b , Del , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (del_t_atom := self.del_t_atom())
        ):
            return del_t_atom
        self._reset(mark)
        return None

    @memoize
    def del_t_atom(self) -> Optional[ast . expr]:
        # del_t_atom: NAME | '(' del_target ')' | '(' del_targets? ')' | '[' del_targets? ']'
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.name())
        ):
            return set_expr_context ( a , Del )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.del_target())
            and
            (literal_1 := self.expect(')'))
        ):
            return set_expr_context ( a , Del )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.del_targets(),)
            and
            (literal_1 := self.expect(')'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . Tuple ( a , Del , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (literal := self.expect('['))
            and
            (a := self.del_targets(),)
            and
            (literal_1 := self.expect(']'))
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . List ( a , Del , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        return None

    @memoize
    def type_expressions(self) -> Optional[List [ast . expr]]:
        # type_expressions: ','.expression+ ',' '*' expression ',' '**' expression | ','.expression+ ',' '*' expression | ','.expression+ ',' '**' expression | '*' expression ',' '**' expression | '*' expression | '**' expression | ','.expression+
        mark = self._mark()
        if (
            (a := self._gather_131())
            and
            (literal := self.expect(','))
            and
            (literal_1 := self.expect('*'))
            and
            (b := self.expression())
            and
            (literal_2 := self.expect(','))
            and
            (literal_3 := self.expect('**'))
            and
            (c := self.expression())
        ):
            return a + [b , c]
        self._reset(mark)
        if (
            (a := self._gather_133())
            and
            (literal := self.expect(','))
            and
            (literal_1 := self.expect('*'))
            and
            (b := self.expression())
        ):
            return a + [b]
        self._reset(mark)
        if (
            (a := self._gather_135())
            and
            (literal := self.expect(','))
            and
            (literal_1 := self.expect('**'))
            and
            (b := self.expression())
        ):
            return a + [b]
        self._reset(mark)
        if (
            (literal := self.expect('*'))
            and
            (a := self.expression())
            and
            (literal_1 := self.expect(','))
            and
            (literal_2 := self.expect('**'))
            and
            (b := self.expression())
        ):
            return a + [b]
        self._reset(mark)
        if (
            (literal := self.expect('*'))
            and
            (a := self.expression())
        ):
            return [a]
        self._reset(mark)
        if (
            (literal := self.expect('**'))
            and
            (a := self.expression())
        ):
            return [a]
        self._reset(mark)
        if (
            (a := self._gather_137())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def func_type_comment(self) -> Optional[lexer . Token]:
        # func_type_comment: NEWLINE TYPE_COMMENT &(NEWLINE INDENT) | invalid_double_type_comments | TYPE_COMMENT
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (t := self.type_comment())
            and
            self.positive_lookahead(self._tmp_139, )
        ):
            return t
        self._reset(mark)
        if (
            (invalid_double_type_comments := self.invalid_double_type_comments())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (type_comment := self.type_comment())
        ):
            return type_comment
        self._reset(mark)
        return None

    @memoize
    def invalid_arguments(self) -> Optional[Any]:
        # invalid_arguments: args ',' '*' | expression for_if_clauses ',' [args | expression for_if_clauses] | NAME '=' expression for_if_clauses | args for_if_clauses | args ',' expression for_if_clauses | args ',' args
        mark = self._mark()
        if (
            (a := self.args())
            and
            (literal := self.expect(','))
            and
            (literal_1 := self.expect('*'))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "iterable argument unpacking follows keyword argument unpacking" )
        self._reset(mark)
        if (
            (a := self.expression())
            and
            (b := self.for_if_clauses())
            and
            (literal := self.expect(','))
            and
            (opt := self._tmp_140(),)
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , PyPegen_last_item ( b , ast . comprehension ) . target , "Generator expression must be parenthesized" )
        self._reset(mark)
        if (
            (a := self.name())
            and
            (b := self.expect('='))
            and
            (expression := self.expression())
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "invalid syntax. Maybe you meant '==' or ':=' instead of '='?" )
        self._reset(mark)
        if (
            (a := self.args())
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return _PyPegen_nonparen_genexp_in_call ( p , a )
        self._reset(mark)
        if (
            (args := self.args())
            and
            (literal := self.expect(','))
            and
            (a := self.expression())
            and
            (b := self.for_if_clauses())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b [len ( b ) - 1] . target , "Generator expression must be parenthesized" )
        self._reset(mark)
        if (
            (a := self.args())
            and
            (literal := self.expect(','))
            and
            (args := self.args())
        ):
            return _PyPegen_arguments_parsing_error ( p , a )
        self._reset(mark)
        return None

    @memoize
    def invalid_kwarg(self) -> Optional[Any]:
        # invalid_kwarg: NAME '=' expression for_if_clauses | !(NAME '=') expression '='
        mark = self._mark()
        if (
            (a := self.name())
            and
            (b := self.expect('='))
            and
            (expression := self.expression())
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "invalid syntax. Maybe you meant '==' or ':=' instead of '='?" )
        self._reset(mark)
        if (
            self.negative_lookahead(self._tmp_141, )
            and
            (a := self.expression())
            and
            (b := self.expect('='))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "expression cannot contain assignment, perhaps you meant \"==\"?" )
        self._reset(mark)
        return None

    @memoize
    def expression_without_invalid(self) -> Optional[ast . expr]:
        # expression_without_invalid: disjunction 'if' disjunction 'else' expression | disjunction | lambdef
        mark = self._mark()
        tok = self._tokenizer.peek()
        start_lineno, start_col_offset = tok.start
        if (
            (a := self.disjunction())
            and
            (literal := self.expect('if'))
            and
            (b := self.disjunction())
            and
            (literal_1 := self.expect('else'))
            and
            (c := self.expression())
        ):
            tok = self._tokenizer.get_last_non_whitespace_token()
            end_lineno, end_col_offset = tok.end
            return ast . IfExp ( b , a , c , lineno=start_lineno, col_offset=start_col_offset, end_lineno=end_lineno, end_col_offset=end_col_offset )
        self._reset(mark)
        if (
            (disjunction := self.disjunction())
        ):
            return disjunction
        self._reset(mark)
        if (
            (lambdef := self.lambdef())
        ):
            return lambdef
        self._reset(mark)
        return None

    @memoize
    def invalid_legacy_expression(self) -> Optional[Any]:
        # invalid_legacy_expression: NAME !'(' star_expressions
        mark = self._mark()
        if (
            (a := self.name())
            and
            self.negative_lookahead(self.expect, '(')
            and
            (b := self.star_expressions())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "Missing parentheses in call to '%U'. Did you mean %U(...)?" , a . id , a . id ) if check_legacy_stmt ( a ) else None
        self._reset(mark)
        return None

    @memoize
    def invalid_expression(self) -> Optional[Any]:
        # invalid_expression: invalid_legacy_expression | !(NAME STRING | SOFT_KEYWORD) disjunction expression_without_invalid | disjunction 'if' disjunction !('else' | ':')
        mark = self._mark()
        if (
            (invalid_legacy_expression := self.invalid_legacy_expression())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            self.negative_lookahead(self._tmp_142, )
            and
            (a := self.disjunction())
            and
            (b := self.expression_without_invalid())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "invalid syntax. Perhaps you forgot a comma?" )
        self._reset(mark)
        if (
            (a := self.disjunction())
            and
            (literal := self.expect('if'))
            and
            (b := self.disjunction())
            and
            self.negative_lookahead(self._tmp_143, )
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "expected 'else' after 'if' expression" )
        self._reset(mark)
        return None

    @memoize
    def invalid_named_expression(self) -> Optional[Any]:
        # invalid_named_expression: expression ':=' expression | NAME '=' bitwise_or !('=' | ':=') | !(list | tuple | genexp | 'True' | 'None' | 'False') bitwise_or '=' bitwise_or !('=' | ':=')
        mark = self._mark()
        if (
            (a := self.expression())
            and
            (literal := self.expect(':='))
            and
            (expression := self.expression())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "cannot use assignment expressions with %s" , _PyPegen_get_expr_name ( a ) )
        self._reset(mark)
        if (
            (a := self.name())
            and
            (literal := self.expect('='))
            and
            (b := self.bitwise_or())
            and
            self.negative_lookahead(self._tmp_144, )
        ):
            return None if p . in_raw_rule else RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "invalid syntax. Maybe you meant '==' or ':=' instead of '='?" )
        self._reset(mark)
        if (
            self.negative_lookahead(self._tmp_145, )
            and
            (a := self.bitwise_or())
            and
            (b := self.expect('='))
            and
            (bitwise_or := self.bitwise_or())
            and
            self.negative_lookahead(self._tmp_146, )
        ):
            return None if p . in_raw_rule else RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "cannot assign to %s here. Maybe you meant '==' instead of '='?" , _PyPegen_get_expr_name ( a ) )
        self._reset(mark)
        return None

    @memoize
    def invalid_assignment(self) -> Optional[Any]:
        # invalid_assignment: invalid_ann_assign_target ':' expression | star_named_expression ',' star_named_expressions* ':' expression | expression ':' expression | ((star_targets '='))* star_expressions '=' | ((star_targets '='))* yield_expr '=' | star_expressions augassign (yield_expr | star_expressions)
        mark = self._mark()
        if (
            (a := self.invalid_ann_assign_target())
            and
            (literal := self.expect(':'))
            and
            (expression := self.expression())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "only single target (not %s) can be annotated" , _PyPegen_get_expr_name ( a ) )
        self._reset(mark)
        if (
            (a := self.star_named_expression())
            and
            (literal := self.expect(','))
            and
            (_loop0_147 := self._loop0_147(),)
            and
            (literal_1 := self.expect(':'))
            and
            (expression := self.expression())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "only single target (not tuple) can be annotated" )
        self._reset(mark)
        if (
            (a := self.expression())
            and
            (literal := self.expect(':'))
            and
            (expression := self.expression())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "illegal target for annotation" )
        self._reset(mark)
        if (
            (_loop0_148 := self._loop0_148(),)
            and
            (a := self.star_expressions())
            and
            (literal := self.expect('='))
        ):
            return RAISE_SYNTAX_ERROR_INVALID_TARGET ( STAR_TARGETS , a )
        self._reset(mark)
        if (
            (_loop0_149 := self._loop0_149(),)
            and
            (a := self.yield_expr())
            and
            (literal := self.expect('='))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "assignment to yield expression not possible" )
        self._reset(mark)
        if (
            (a := self.star_expressions())
            and
            (augassign := self.augassign())
            and
            (_tmp_150 := self._tmp_150())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "'%s' is an illegal expression for augmented assignment" , _PyPegen_get_expr_name ( a ) )
        self._reset(mark)
        return None

    @memoize
    def invalid_ann_assign_target(self) -> Optional[ast . expr]:
        # invalid_ann_assign_target: list | tuple | '(' invalid_ann_assign_target ')'
        mark = self._mark()
        if (
            (list := self.list())
        ):
            return list
        self._reset(mark)
        if (
            (tuple := self.tuple())
        ):
            return tuple
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.invalid_ann_assign_target())
            and
            (literal_1 := self.expect(')'))
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def invalid_del_stmt(self) -> Optional[Any]:
        # invalid_del_stmt: 'del' star_expressions
        mark = self._mark()
        if (
            (literal := self.expect('del'))
            and
            (a := self.star_expressions())
        ):
            return RAISE_SYNTAX_ERROR_INVALID_TARGET ( DEL_TARGETS , a )
        self._reset(mark)
        return None

    @memoize
    def invalid_block(self) -> Optional[Any]:
        # invalid_block: NEWLINE !INDENT
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block" )
        self._reset(mark)
        return None

    @memoize
    def invalid_comprehension(self) -> Optional[Any]:
        # invalid_comprehension: ('[' | '(' | '{') starred_expression for_if_clauses | ('[' | '{') star_named_expression ',' star_named_expressions for_if_clauses | ('[' | '{') star_named_expression ',' for_if_clauses
        mark = self._mark()
        if (
            (_tmp_151 := self._tmp_151())
            and
            (a := self.starred_expression())
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "iterable unpacking cannot be used in comprehension" )
        self._reset(mark)
        if (
            (_tmp_152 := self._tmp_152())
            and
            (a := self.star_named_expression())
            and
            (literal := self.expect(','))
            and
            (b := self.star_named_expressions())
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , PyPegen_last_item ( b , ast . expr ) , "did you forget parentheses around the comprehension target?" )
        self._reset(mark)
        if (
            (_tmp_153 := self._tmp_153())
            and
            (a := self.star_named_expression())
            and
            (b := self.expect(','))
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( a , b , "did you forget parentheses around the comprehension target?" )
        self._reset(mark)
        return None

    @memoize
    def invalid_dict_comprehension(self) -> Optional[Any]:
        # invalid_dict_comprehension: '{' '**' bitwise_or for_if_clauses '}'
        mark = self._mark()
        if (
            (literal := self.expect('{'))
            and
            (a := self.expect('**'))
            and
            (bitwise_or := self.bitwise_or())
            and
            (for_if_clauses := self.for_if_clauses())
            and
            (literal_1 := self.expect('}'))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "dict unpacking cannot be used in dict comprehension" )
        self._reset(mark)
        return None

    @memoize
    def invalid_parameters(self) -> Optional[Any]:
        # invalid_parameters: param_no_default* invalid_parameters_helper param_no_default
        mark = self._mark()
        if (
            (_loop0_154 := self._loop0_154(),)
            and
            (invalid_parameters_helper := self.invalid_parameters_helper())
            and
            (a := self.param_no_default())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "non-default argument follows default argument" )
        self._reset(mark)
        return None

    @memoize
    def invalid_parameters_helper(self) -> Optional[Any]:
        # invalid_parameters_helper: slash_with_default | param_with_default+
        mark = self._mark()
        if (
            (a := self.slash_with_default())
        ):
            return [a]
        self._reset(mark)
        if (
            (_loop1_155 := self._loop1_155())
        ):
            return _loop1_155
        self._reset(mark)
        return None

    @memoize
    def invalid_lambda_parameters(self) -> Optional[Any]:
        # invalid_lambda_parameters: lambda_param_no_default* invalid_lambda_parameters_helper lambda_param_no_default
        mark = self._mark()
        if (
            (_loop0_156 := self._loop0_156(),)
            and
            (invalid_lambda_parameters_helper := self.invalid_lambda_parameters_helper())
            and
            (a := self.lambda_param_no_default())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "non-default argument follows default argument" )
        self._reset(mark)
        return None

    @memoize
    def invalid_lambda_parameters_helper(self) -> Optional[Any]:
        # invalid_lambda_parameters_helper: lambda_slash_with_default | lambda_param_with_default+
        mark = self._mark()
        if (
            (a := self.lambda_slash_with_default())
        ):
            return [a]
        self._reset(mark)
        if (
            (_loop1_157 := self._loop1_157())
        ):
            return _loop1_157
        self._reset(mark)
        return None

    @memoize
    def invalid_star_etc(self) -> Optional[Any]:
        # invalid_star_etc: '*' (')' | ',' (')' | '**')) | '*' ',' TYPE_COMMENT
        mark = self._mark()
        if (
            (a := self.expect('*'))
            and
            (_tmp_158 := self._tmp_158())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "named arguments must follow bare *" )
        self._reset(mark)
        if (
            (literal := self.expect('*'))
            and
            (literal_1 := self.expect(','))
            and
            (type_comment := self.type_comment())
        ):
            return RAISE_SYNTAX_ERROR ( "bare * has associated type comment" )
        self._reset(mark)
        return None

    @memoize
    def invalid_lambda_star_etc(self) -> Optional[Any]:
        # invalid_lambda_star_etc: '*' (':' | ',' (':' | '**'))
        mark = self._mark()
        if (
            (literal := self.expect('*'))
            and
            (_tmp_159 := self._tmp_159())
        ):
            return RAISE_SYNTAX_ERROR ( "named arguments must follow bare *" )
        self._reset(mark)
        return None

    @memoize
    def invalid_double_type_comments(self) -> Optional[Any]:
        # invalid_double_type_comments: TYPE_COMMENT NEWLINE TYPE_COMMENT NEWLINE INDENT
        mark = self._mark()
        if (
            (type_comment := self.type_comment())
            and
            (_newline := self.expect('NEWLINE'))
            and
            (type_comment_1 := self.type_comment())
            and
            (_newline_1 := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
        ):
            return RAISE_SYNTAX_ERROR ( "Cannot have two type comments on def" )
        self._reset(mark)
        return None

    @memoize
    def invalid_with_item(self) -> Optional[Any]:
        # invalid_with_item: expression 'as' expression &(',' | ')' | ':')
        mark = self._mark()
        if (
            (expression := self.expression())
            and
            (literal := self.expect('as'))
            and
            (a := self.expression())
            and
            self.positive_lookahead(self._tmp_160, )
        ):
            return RAISE_SYNTAX_ERROR_INVALID_TARGET ( STAR_TARGETS , a )
        self._reset(mark)
        return None

    @memoize
    def invalid_for_target(self) -> Optional[Any]:
        # invalid_for_target: ASYNC? 'for' star_expressions
        mark = self._mark()
        if (
            (opt := self.expect('ASYNC'),)
            and
            (literal := self.expect('for'))
            and
            (a := self.star_expressions())
        ):
            return RAISE_SYNTAX_ERROR_INVALID_TARGET ( FOR_TARGETS , a )
        self._reset(mark)
        return None

    @memoize
    def invalid_group(self) -> Optional[Any]:
        # invalid_group: '(' starred_expression ')' | '(' '**' expression ')'
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (a := self.starred_expression())
            and
            (literal_1 := self.expect(')'))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "cannot use starred expression here" )
        self._reset(mark)
        if (
            (literal := self.expect('('))
            and
            (a := self.expect('**'))
            and
            (expression := self.expression())
            and
            (literal_1 := self.expect(')'))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "cannot use double starred expression here" )
        self._reset(mark)
        return None

    @memoize
    def invalid_import_from_targets(self) -> Optional[Any]:
        # invalid_import_from_targets: import_from_as_names ',' NEWLINE
        mark = self._mark()
        if (
            (import_from_as_names := self.import_from_as_names())
            and
            (literal := self.expect(','))
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return RAISE_SYNTAX_ERROR ( "trailing comma not allowed without surrounding parentheses" )
        self._reset(mark)
        return None

    @memoize
    def invalid_with_stmt(self) -> Optional[Any]:
        # invalid_with_stmt: ASYNC? 'with' ','.(expression ['as' star_target])+ &&':' | ASYNC? 'with' '(' ','.(expressions ['as' star_target])+ ','? ')' &&':'
        mark = self._mark()
        if (
            (opt := self.expect('ASYNC'),)
            and
            (literal := self.expect('with'))
            and
            (_gather_161 := self._gather_161())
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
        ):
            return [opt, literal, _gather_161, forced]
        self._reset(mark)
        if (
            (opt := self.expect('ASYNC'),)
            and
            (literal := self.expect('with'))
            and
            (literal_1 := self.expect('('))
            and
            (_gather_163 := self._gather_163())
            and
            (opt_1 := self.expect(','),)
            and
            (literal_2 := self.expect(')'))
            and
            (forced := self.expect_forced(self.expect(':'), "':'"))
        ):
            return [opt, literal, literal_1, _gather_163, opt_1, literal_2, forced]
        self._reset(mark)
        return None

    @memoize
    def invalid_with_stmt_indent(self) -> Optional[Any]:
        # invalid_with_stmt_indent: ASYNC? 'with' ','.(expression ['as' star_target])+ ':' NEWLINE !INDENT | ASYNC? 'with' '(' ','.(expressions ['as' star_target])+ ','? ')' ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (opt := self.expect('ASYNC'),)
            and
            (a := self.expect('with'))
            and
            (_gather_165 := self._gather_165())
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'with' statement on line %d" , a . lineno )
        self._reset(mark)
        if (
            (opt := self.expect('ASYNC'),)
            and
            (a := self.expect('with'))
            and
            (literal := self.expect('('))
            and
            (_gather_167 := self._gather_167())
            and
            (opt_1 := self.expect(','),)
            and
            (literal_1 := self.expect(')'))
            and
            (literal_2 := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'with' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_try_stmt(self) -> Optional[Any]:
        # invalid_try_stmt: 'try' ':' NEWLINE !INDENT | 'try' ':' block !('except' | 'finally')
        mark = self._mark()
        if (
            (a := self.expect('try'))
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'try' statement on line %d" , a . lineno )
        self._reset(mark)
        if (
            (literal := self.expect('try'))
            and
            (literal_1 := self.expect(':'))
            and
            (block := self.block())
            and
            self.negative_lookahead(self._tmp_169, )
        ):
            return RAISE_SYNTAX_ERROR ( "expected 'except' or 'finally' block" )
        self._reset(mark)
        return None

    @memoize
    def invalid_except_stmt(self) -> Optional[Any]:
        # invalid_except_stmt: 'except' expression ',' expressions ['as' NAME] ':' | 'except' expression ['as' NAME] NEWLINE | 'except' NEWLINE
        mark = self._mark()
        if (
            (literal := self.expect('except'))
            and
            (a := self.expression())
            and
            (literal_1 := self.expect(','))
            and
            (expressions := self.expressions())
            and
            (opt := self._tmp_170(),)
            and
            (literal_2 := self.expect(':'))
        ):
            return RAISE_SYNTAX_ERROR_STARTING_FROM ( a , "multiple exception types must be parenthesized" )
        self._reset(mark)
        if (
            (a := self.expect('except'))
            and
            (expression := self.expression())
            and
            (opt := self._tmp_171(),)
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return RAISE_SYNTAX_ERROR ( "expected ':'" )
        self._reset(mark)
        if (
            (a := self.expect('except'))
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return RAISE_SYNTAX_ERROR ( "expected ':'" )
        self._reset(mark)
        return None

    @memoize
    def invalid_finally_stmt(self) -> Optional[Any]:
        # invalid_finally_stmt: 'finally' ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (a := self.expect('finally'))
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'finally' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_except_stmt_indent(self) -> Optional[Any]:
        # invalid_except_stmt_indent: 'except' expression ['as' NAME] ':' NEWLINE !INDENT | 'except' ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (a := self.expect('except'))
            and
            (expression := self.expression())
            and
            (opt := self._tmp_172(),)
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'except' statement on line %d" , a . lineno )
        self._reset(mark)
        if (
            (a := self.expect('except'))
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_SYNTAX_ERROR ( "expected an indented block after except statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_match_stmt(self) -> Optional[Any]:
        # invalid_match_stmt: "match" subject_expr !':' | "match" subject_expr ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (literal := self.expect("match"))
            and
            (subject_expr := self.subject_expr())
            and
            self.negative_lookahead(self.expect, ':')
        ):
            return CHECK_VERSION ( None , 10 , "Pattern matching is" , RAISE_SYNTAX_ERROR ( "expected ':'" ) )
        self._reset(mark)
        if (
            (a := self.expect("match"))
            and
            (subject := self.subject_expr())
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'match' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_case_block(self) -> Optional[Any]:
        # invalid_case_block: "case" patterns guard? !':' | "case" patterns guard? ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (literal := self.expect("case"))
            and
            (patterns := self.patterns())
            and
            (opt := self.guard(),)
            and
            self.negative_lookahead(self.expect, ':')
        ):
            return RAISE_SYNTAX_ERROR ( "expected ':'" )
        self._reset(mark)
        if (
            (a := self.expect("case"))
            and
            (patterns := self.patterns())
            and
            (opt := self.guard(),)
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'case' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_as_pattern(self) -> Optional[Any]:
        # invalid_as_pattern: or_pattern 'as' "_" | or_pattern 'as' !NAME expression
        mark = self._mark()
        if (
            (or_pattern := self.or_pattern())
            and
            (literal := self.expect('as'))
            and
            (a := self.expect("_"))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "cannot use '_' as a target" )
        self._reset(mark)
        if (
            (or_pattern := self.or_pattern())
            and
            (literal := self.expect('as'))
            and
            self.negative_lookahead(self.name, )
            and
            (a := self.expression())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "invalid pattern target" )
        self._reset(mark)
        return None

    @memoize
    def invalid_class_pattern(self) -> Optional[Any]:
        # invalid_class_pattern: name_or_attr '(' invalid_class_argument_pattern
        mark = self._mark()
        if (
            (name_or_attr := self.name_or_attr())
            and
            (literal := self.expect('('))
            and
            (a := self.invalid_class_argument_pattern())
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_RANGE ( PyPegen_first_item ( a , ast . pattern ) , PyPegen_last_item ( a , ast . pattern ) , "positional patterns follow keyword patterns" )
        self._reset(mark)
        return None

    @memoize
    def invalid_class_argument_pattern(self) -> Optional[List [ast . pattern]]:
        # invalid_class_argument_pattern: [positional_patterns ','] keyword_patterns ',' positional_patterns
        mark = self._mark()
        if (
            (opt := self._tmp_173(),)
            and
            (keyword_patterns := self.keyword_patterns())
            and
            (literal := self.expect(','))
            and
            (a := self.positional_patterns())
        ):
            return a
        self._reset(mark)
        return None

    @memoize
    def invalid_if_stmt(self) -> Optional[Any]:
        # invalid_if_stmt: 'if' named_expression ':'? NEWLINE !INDENT
        mark = self._mark()
        if (
            (a := self.expect('if'))
            and
            (a_1 := self.named_expression())
            and
            (opt := self.expect(':'),)
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'if' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_elif_stmt(self) -> Optional[Any]:
        # invalid_elif_stmt: 'elif' named_expression ':'? NEWLINE !INDENT
        mark = self._mark()
        if (
            (a := self.expect('elif'))
            and
            (named_expression := self.named_expression())
            and
            (opt := self.expect(':'),)
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'elif' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_else_stmt(self) -> Optional[Any]:
        # invalid_else_stmt: 'else' ':'? NEWLINE !INDENT
        mark = self._mark()
        if (
            (a := self.expect('else'))
            and
            (opt := self.expect(':'),)
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'else' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_while_stmt(self) -> Optional[Any]:
        # invalid_while_stmt: 'while' named_expression NEWLINE | 'while' named_expression ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (literal := self.expect('while'))
            and
            (named_expression := self.named_expression())
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return RAISE_SYNTAX_ERROR ( "expected ':'" )
        self._reset(mark)
        if (
            (a := self.expect('while'))
            and
            (named_expression := self.named_expression())
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'while' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_for_stmt(self) -> Optional[Any]:
        # invalid_for_stmt: ASYNC? 'for' star_targets 'in' star_expressions ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (opt := self.expect('ASYNC'),)
            and
            (a := self.expect('for'))
            and
            (star_targets := self.star_targets())
            and
            (literal := self.expect('in'))
            and
            (star_expressions := self.star_expressions())
            and
            (literal_1 := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after 'for' statement on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_def_raw(self) -> Optional[Any]:
        # invalid_def_raw: ASYNC? 'def' NAME '(' params? ')' ['->' expression] ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (opt := self.expect('ASYNC'),)
            and
            (a := self.expect('def'))
            and
            (name := self.name())
            and
            (literal := self.expect('('))
            and
            (opt_1 := self.params(),)
            and
            (literal_1 := self.expect(')'))
            and
            (opt_2 := self._tmp_174(),)
            and
            (literal_2 := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after function definition on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_class_def_raw(self) -> Optional[Any]:
        # invalid_class_def_raw: 'class' NAME ['(' arguments? ')'] ':' NEWLINE !INDENT
        mark = self._mark()
        if (
            (a := self.expect('class'))
            and
            (name := self.name())
            and
            (opt := self._tmp_175(),)
            and
            (literal := self.expect(':'))
            and
            (_newline := self.expect('NEWLINE'))
            and
            self.negative_lookahead(self.expect, 'INDENT')
        ):
            return RAISE_INDENTATION_ERROR ( "expected an indented block after class definition on line %d" , a . lineno )
        self._reset(mark)
        return None

    @memoize
    def invalid_double_starred_kvpairs(self) -> Optional[Any]:
        # invalid_double_starred_kvpairs: ','.double_starred_kvpair+ ',' invalid_kvpair | expression ':' '*' bitwise_or | expression ':' &('}' | ',')
        mark = self._mark()
        if (
            (_gather_176 := self._gather_176())
            and
            (literal := self.expect(','))
            and
            (invalid_kvpair := self.invalid_kvpair())
        ):
            return None  # pragma: no cover
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            (literal := self.expect(':'))
            and
            (a := self.expect('*'))
            and
            (bitwise_or := self.bitwise_or())
        ):
            return RAISE_SYNTAX_ERROR_STARTING_FROM ( a , "cannot use a starred expression in a dictionary value" )
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            (a := self.expect(':'))
            and
            self.positive_lookahead(self._tmp_178, )
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "expression expected after dictionary key and ':'" )
        self._reset(mark)
        return None

    @memoize
    def invalid_kvpair(self) -> Optional[Any]:
        # invalid_kvpair: expression !(':') | expression ':' '*' bitwise_or | expression ':'
        mark = self._mark()
        if (
            (a := self.expression())
            and
            self.negative_lookahead(self.expect, ':')
        ):
            return RAISE_ERROR_KNOWN_LOCATION ( p , PyExc_SyntaxError , a . lineno , a . end_col_offset - 1 , a . end_lineno , - 1 , "':' expected after dictionary key" )
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            (literal := self.expect(':'))
            and
            (a := self.expect('*'))
            and
            (bitwise_or := self.bitwise_or())
        ):
            return RAISE_SYNTAX_ERROR_STARTING_FROM ( a , "cannot use a starred expression in a dictionary value" )
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            (a := self.expect(':'))
        ):
            return RAISE_SYNTAX_ERROR_KNOWN_LOCATION ( a , "expression expected after dictionary key and ':'" )
        self._reset(mark)
        return None

    @memoize
    def _loop0_1(self) -> Optional[Any]:
        # _loop0_1: NEWLINE
        mark = self._mark()
        children = []
        while (
            (_newline := self.expect('NEWLINE'))
        ):
            children.append(_newline)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_2(self) -> Optional[Any]:
        # _loop0_2: NEWLINE
        mark = self._mark()
        children = []
        while (
            (_newline := self.expect('NEWLINE'))
        ):
            children.append(_newline)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_3(self) -> Optional[Any]:
        # _loop1_3: statement
        mark = self._mark()
        children = []
        while (
            (statement := self.statement())
        ):
            children.append(statement)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_5(self) -> Optional[Any]:
        # _loop0_5: ';' simple_stmt
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(';'))
            and
            (elem := self.simple_stmt())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_4(self) -> Optional[Any]:
        # _gather_4: simple_stmt _loop0_5
        mark = self._mark()
        if (
            (elem := self.simple_stmt())
            is not None
            and
            (seq := self._loop0_5())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_6(self) -> Optional[Any]:
        # _tmp_6: 'import' | 'from'
        mark = self._mark()
        if (
            (literal := self.expect('import'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('from'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_7(self) -> Optional[Any]:
        # _tmp_7: 'def' | '@' | ASYNC
        mark = self._mark()
        if (
            (literal := self.expect('def'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('@'))
        ):
            return literal
        self._reset(mark)
        if (
            (_async := self.expect('ASYNC'))
        ):
            return _async
        self._reset(mark)
        return None

    @memoize
    def _tmp_8(self) -> Optional[Any]:
        # _tmp_8: 'class' | '@'
        mark = self._mark()
        if (
            (literal := self.expect('class'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('@'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_9(self) -> Optional[Any]:
        # _tmp_9: 'with' | ASYNC
        mark = self._mark()
        if (
            (literal := self.expect('with'))
        ):
            return literal
        self._reset(mark)
        if (
            (_async := self.expect('ASYNC'))
        ):
            return _async
        self._reset(mark)
        return None

    @memoize
    def _tmp_10(self) -> Optional[Any]:
        # _tmp_10: 'for' | ASYNC
        mark = self._mark()
        if (
            (literal := self.expect('for'))
        ):
            return literal
        self._reset(mark)
        if (
            (_async := self.expect('ASYNC'))
        ):
            return _async
        self._reset(mark)
        return None

    @memoize
    def _tmp_11(self) -> Optional[Any]:
        # _tmp_11: '=' annotated_rhs
        mark = self._mark()
        if (
            (literal := self.expect('='))
            and
            (d := self.annotated_rhs())
        ):
            return d
        self._reset(mark)
        return None

    @memoize
    def _tmp_12(self) -> Optional[Any]:
        # _tmp_12: '(' single_target ')' | single_subscript_attribute_target
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (b := self.single_target())
            and
            (literal_1 := self.expect(')'))
        ):
            return b
        self._reset(mark)
        if (
            (single_subscript_attribute_target := self.single_subscript_attribute_target())
        ):
            return single_subscript_attribute_target
        self._reset(mark)
        return None

    @memoize
    def _tmp_13(self) -> Optional[Any]:
        # _tmp_13: '=' annotated_rhs
        mark = self._mark()
        if (
            (literal := self.expect('='))
            and
            (d := self.annotated_rhs())
        ):
            return d
        self._reset(mark)
        return None

    @memoize
    def _loop1_14(self) -> Optional[Any]:
        # _loop1_14: (star_targets '=')
        mark = self._mark()
        children = []
        while (
            (_tmp_179 := self._tmp_179())
        ):
            children.append(_tmp_179)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_15(self) -> Optional[Any]:
        # _tmp_15: yield_expr | star_expressions
        mark = self._mark()
        if (
            (yield_expr := self.yield_expr())
        ):
            return yield_expr
        self._reset(mark)
        if (
            (star_expressions := self.star_expressions())
        ):
            return star_expressions
        self._reset(mark)
        return None

    @memoize
    def _tmp_16(self) -> Optional[Any]:
        # _tmp_16: yield_expr | star_expressions
        mark = self._mark()
        if (
            (yield_expr := self.yield_expr())
        ):
            return yield_expr
        self._reset(mark)
        if (
            (star_expressions := self.star_expressions())
        ):
            return star_expressions
        self._reset(mark)
        return None

    @memoize
    def _tmp_17(self) -> Optional[Any]:
        # _tmp_17: 'from' expression
        mark = self._mark()
        if (
            (literal := self.expect('from'))
            and
            (z := self.expression())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _loop0_19(self) -> Optional[Any]:
        # _loop0_19: ',' NAME
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.name())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_18(self) -> Optional[Any]:
        # _gather_18: NAME _loop0_19
        mark = self._mark()
        if (
            (elem := self.name())
            is not None
            and
            (seq := self._loop0_19())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_21(self) -> Optional[Any]:
        # _loop0_21: ',' NAME
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.name())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_20(self) -> Optional[Any]:
        # _gather_20: NAME _loop0_21
        mark = self._mark()
        if (
            (elem := self.name())
            is not None
            and
            (seq := self._loop0_21())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_22(self) -> Optional[Any]:
        # _tmp_22: ';' | NEWLINE
        mark = self._mark()
        if (
            (literal := self.expect(';'))
        ):
            return literal
        self._reset(mark)
        if (
            (_newline := self.expect('NEWLINE'))
        ):
            return _newline
        self._reset(mark)
        return None

    @memoize
    def _tmp_23(self) -> Optional[Any]:
        # _tmp_23: ',' expression
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (z := self.expression())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _loop0_24(self) -> Optional[Any]:
        # _loop0_24: ('.' | '...')
        mark = self._mark()
        children = []
        while (
            (_tmp_180 := self._tmp_180())
        ):
            children.append(_tmp_180)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_25(self) -> Optional[Any]:
        # _loop1_25: ('.' | '...')
        mark = self._mark()
        children = []
        while (
            (_tmp_181 := self._tmp_181())
        ):
            children.append(_tmp_181)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_27(self) -> Optional[Any]:
        # _loop0_27: ',' import_from_as_name
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.import_from_as_name())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_26(self) -> Optional[Any]:
        # _gather_26: import_from_as_name _loop0_27
        mark = self._mark()
        if (
            (elem := self.import_from_as_name())
            is not None
            and
            (seq := self._loop0_27())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_28(self) -> Optional[Any]:
        # _tmp_28: 'as' NAME
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (z := self.name())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _loop0_30(self) -> Optional[Any]:
        # _loop0_30: ',' dotted_as_name
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.dotted_as_name())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_29(self) -> Optional[Any]:
        # _gather_29: dotted_as_name _loop0_30
        mark = self._mark()
        if (
            (elem := self.dotted_as_name())
            is not None
            and
            (seq := self._loop0_30())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_31(self) -> Optional[Any]:
        # _tmp_31: 'as' NAME
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (z := self.name())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _loop1_32(self) -> Optional[Any]:
        # _loop1_32: ('@' named_expression NEWLINE)
        mark = self._mark()
        children = []
        while (
            (_tmp_182 := self._tmp_182())
        ):
            children.append(_tmp_182)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_33(self) -> Optional[Any]:
        # _tmp_33: '(' arguments? ')'
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (z := self.arguments(),)
            and
            (literal_1 := self.expect(')'))
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _tmp_34(self) -> Optional[Any]:
        # _tmp_34: '->' expression
        mark = self._mark()
        if (
            (literal := self.expect('->'))
            and
            (z := self.expression())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _tmp_35(self) -> Optional[Any]:
        # _tmp_35: '->' expression
        mark = self._mark()
        if (
            (literal := self.expect('->'))
            and
            (z := self.expression())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _loop0_36(self) -> Optional[Any]:
        # _loop0_36: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_37(self) -> Optional[Any]:
        # _loop0_37: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_38(self) -> Optional[Any]:
        # _loop0_38: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_39(self) -> Optional[Any]:
        # _loop1_39: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_40(self) -> Optional[Any]:
        # _loop0_40: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_41(self) -> Optional[Any]:
        # _loop1_41: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_42(self) -> Optional[Any]:
        # _loop1_42: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_43(self) -> Optional[Any]:
        # _loop1_43: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_44(self) -> Optional[Any]:
        # _loop0_44: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_45(self) -> Optional[Any]:
        # _loop1_45: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_46(self) -> Optional[Any]:
        # _loop0_46: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_47(self) -> Optional[Any]:
        # _loop1_47: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_48(self) -> Optional[Any]:
        # _loop0_48: param_maybe_default
        mark = self._mark()
        children = []
        while (
            (param_maybe_default := self.param_maybe_default())
        ):
            children.append(param_maybe_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_49(self) -> Optional[Any]:
        # _loop1_49: param_maybe_default
        mark = self._mark()
        children = []
        while (
            (param_maybe_default := self.param_maybe_default())
        ):
            children.append(param_maybe_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_51(self) -> Optional[Any]:
        # _loop0_51: ',' with_item
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.with_item())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_50(self) -> Optional[Any]:
        # _gather_50: with_item _loop0_51
        mark = self._mark()
        if (
            (elem := self.with_item())
            is not None
            and
            (seq := self._loop0_51())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_53(self) -> Optional[Any]:
        # _loop0_53: ',' with_item
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.with_item())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_52(self) -> Optional[Any]:
        # _gather_52: with_item _loop0_53
        mark = self._mark()
        if (
            (elem := self.with_item())
            is not None
            and
            (seq := self._loop0_53())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_55(self) -> Optional[Any]:
        # _loop0_55: ',' with_item
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.with_item())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_54(self) -> Optional[Any]:
        # _gather_54: with_item _loop0_55
        mark = self._mark()
        if (
            (elem := self.with_item())
            is not None
            and
            (seq := self._loop0_55())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_57(self) -> Optional[Any]:
        # _loop0_57: ',' with_item
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.with_item())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_56(self) -> Optional[Any]:
        # _gather_56: with_item _loop0_57
        mark = self._mark()
        if (
            (elem := self.with_item())
            is not None
            and
            (seq := self._loop0_57())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_58(self) -> Optional[Any]:
        # _tmp_58: ',' | ')' | ':'
        mark = self._mark()
        if (
            (literal := self.expect(','))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(')'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(':'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _loop1_59(self) -> Optional[Any]:
        # _loop1_59: except_block
        mark = self._mark()
        children = []
        while (
            (except_block := self.except_block())
        ):
            children.append(except_block)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_60(self) -> Optional[Any]:
        # _tmp_60: 'as' NAME
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (z := self.name())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _loop1_61(self) -> Optional[Any]:
        # _loop1_61: case_block
        mark = self._mark()
        children = []
        while (
            (case_block := self.case_block())
        ):
            children.append(case_block)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_63(self) -> Optional[Any]:
        # _loop0_63: '|' closed_pattern
        mark = self._mark()
        children = []
        while (
            (literal := self.expect('|'))
            and
            (elem := self.closed_pattern())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_62(self) -> Optional[Any]:
        # _gather_62: closed_pattern _loop0_63
        mark = self._mark()
        if (
            (elem := self.closed_pattern())
            is not None
            and
            (seq := self._loop0_63())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_64(self) -> Optional[Any]:
        # _tmp_64: '+' | '-'
        mark = self._mark()
        if (
            (literal := self.expect('+'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('-'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_65(self) -> Optional[Any]:
        # _tmp_65: '+' | '-'
        mark = self._mark()
        if (
            (literal := self.expect('+'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('-'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_66(self) -> Optional[Any]:
        # _tmp_66: '.' | '(' | '='
        mark = self._mark()
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('('))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('='))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_67(self) -> Optional[Any]:
        # _tmp_67: '.' | '(' | '='
        mark = self._mark()
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('('))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('='))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _loop0_69(self) -> Optional[Any]:
        # _loop0_69: ',' maybe_star_pattern
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.maybe_star_pattern())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_68(self) -> Optional[Any]:
        # _gather_68: maybe_star_pattern _loop0_69
        mark = self._mark()
        if (
            (elem := self.maybe_star_pattern())
            is not None
            and
            (seq := self._loop0_69())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_71(self) -> Optional[Any]:
        # _loop0_71: ',' key_value_pattern
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.key_value_pattern())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_70(self) -> Optional[Any]:
        # _gather_70: key_value_pattern _loop0_71
        mark = self._mark()
        if (
            (elem := self.key_value_pattern())
            is not None
            and
            (seq := self._loop0_71())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_72(self) -> Optional[Any]:
        # _tmp_72: literal_expr | attr
        mark = self._mark()
        if (
            (literal_expr := self.literal_expr())
        ):
            return literal_expr
        self._reset(mark)
        if (
            (attr := self.attr())
        ):
            return attr
        self._reset(mark)
        return None

    @memoize
    def _loop0_74(self) -> Optional[Any]:
        # _loop0_74: ',' pattern
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.pattern())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_73(self) -> Optional[Any]:
        # _gather_73: pattern _loop0_74
        mark = self._mark()
        if (
            (elem := self.pattern())
            is not None
            and
            (seq := self._loop0_74())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_76(self) -> Optional[Any]:
        # _loop0_76: ',' keyword_pattern
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.keyword_pattern())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_75(self) -> Optional[Any]:
        # _gather_75: keyword_pattern _loop0_76
        mark = self._mark()
        if (
            (elem := self.keyword_pattern())
            is not None
            and
            (seq := self._loop0_76())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_77(self) -> Optional[Any]:
        # _loop1_77: (',' expression)
        mark = self._mark()
        children = []
        while (
            (_tmp_183 := self._tmp_183())
        ):
            children.append(_tmp_183)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_78(self) -> Optional[Any]:
        # _loop1_78: (',' star_expression)
        mark = self._mark()
        children = []
        while (
            (_tmp_184 := self._tmp_184())
        ):
            children.append(_tmp_184)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_80(self) -> Optional[Any]:
        # _loop0_80: ',' star_named_expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.star_named_expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_79(self) -> Optional[Any]:
        # _gather_79: star_named_expression _loop0_80
        mark = self._mark()
        if (
            (elem := self.star_named_expression())
            is not None
            and
            (seq := self._loop0_80())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_81(self) -> Optional[Any]:
        # _loop1_81: ('or' conjunction)
        mark = self._mark()
        children = []
        while (
            (_tmp_185 := self._tmp_185())
        ):
            children.append(_tmp_185)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_82(self) -> Optional[Any]:
        # _loop1_82: ('and' inversion)
        mark = self._mark()
        children = []
        while (
            (_tmp_186 := self._tmp_186())
        ):
            children.append(_tmp_186)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_83(self) -> Optional[Any]:
        # _loop1_83: compare_op_bitwise_or_pair
        mark = self._mark()
        children = []
        while (
            (compare_op_bitwise_or_pair := self.compare_op_bitwise_or_pair())
        ):
            children.append(compare_op_bitwise_or_pair)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_85(self) -> Optional[Any]:
        # _loop0_85: ',' slice
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.slice())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_84(self) -> Optional[Any]:
        # _gather_84: slice _loop0_85
        mark = self._mark()
        if (
            (elem := self.slice())
            is not None
            and
            (seq := self._loop0_85())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_86(self) -> Optional[Any]:
        # _tmp_86: ':' expression?
        mark = self._mark()
        if (
            (literal := self.expect(':'))
            and
            (d := self.expression(),)
        ):
            return d
        self._reset(mark)
        return None

    @memoize
    def _tmp_87(self) -> Optional[Any]:
        # _tmp_87: tuple | group | genexp
        mark = self._mark()
        if (
            (tuple := self.tuple())
        ):
            return tuple
        self._reset(mark)
        if (
            (group := self.group())
        ):
            return group
        self._reset(mark)
        if (
            (genexp := self.genexp())
        ):
            return genexp
        self._reset(mark)
        return None

    @memoize
    def _tmp_88(self) -> Optional[Any]:
        # _tmp_88: list | listcomp
        mark = self._mark()
        if (
            (list := self.list())
        ):
            return list
        self._reset(mark)
        if (
            (listcomp := self.listcomp())
        ):
            return listcomp
        self._reset(mark)
        return None

    @memoize
    def _tmp_89(self) -> Optional[Any]:
        # _tmp_89: dict | set | dictcomp | setcomp
        mark = self._mark()
        if (
            (dict := self.dict())
        ):
            return dict
        self._reset(mark)
        if (
            (set := self.set())
        ):
            return set
        self._reset(mark)
        if (
            (dictcomp := self.dictcomp())
        ):
            return dictcomp
        self._reset(mark)
        if (
            (setcomp := self.setcomp())
        ):
            return setcomp
        self._reset(mark)
        return None

    @memoize
    def _tmp_90(self) -> Optional[Any]:
        # _tmp_90: yield_expr | named_expression
        mark = self._mark()
        if (
            (yield_expr := self.yield_expr())
        ):
            return yield_expr
        self._reset(mark)
        if (
            (named_expression := self.named_expression())
        ):
            return named_expression
        self._reset(mark)
        return None

    @memoize
    def _loop0_91(self) -> Optional[Any]:
        # _loop0_91: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_92(self) -> Optional[Any]:
        # _loop0_92: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_93(self) -> Optional[Any]:
        # _loop0_93: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_94(self) -> Optional[Any]:
        # _loop1_94: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_95(self) -> Optional[Any]:
        # _loop0_95: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_96(self) -> Optional[Any]:
        # _loop1_96: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_97(self) -> Optional[Any]:
        # _loop1_97: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_98(self) -> Optional[Any]:
        # _loop1_98: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_99(self) -> Optional[Any]:
        # _loop0_99: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_100(self) -> Optional[Any]:
        # _loop1_100: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_101(self) -> Optional[Any]:
        # _loop0_101: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_102(self) -> Optional[Any]:
        # _loop1_102: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_103(self) -> Optional[Any]:
        # _loop0_103: lambda_param_maybe_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_maybe_default := self.lambda_param_maybe_default())
        ):
            children.append(lambda_param_maybe_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_104(self) -> Optional[Any]:
        # _loop1_104: lambda_param_maybe_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_maybe_default := self.lambda_param_maybe_default())
        ):
            children.append(lambda_param_maybe_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_105(self) -> Optional[Any]:
        # _loop1_105: STRING
        mark = self._mark()
        children = []
        while (
            (string := self.string())
        ):
            children.append(string)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_106(self) -> Optional[Any]:
        # _tmp_106: star_named_expression ',' star_named_expressions?
        mark = self._mark()
        if (
            (y := self.star_named_expression())
            and
            (literal := self.expect(','))
            and
            (z := self.star_named_expressions(),)
        ):
            return [y] + z
        self._reset(mark)
        return None

    @memoize
    def _loop0_108(self) -> Optional[Any]:
        # _loop0_108: ',' double_starred_kvpair
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.double_starred_kvpair())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_107(self) -> Optional[Any]:
        # _gather_107: double_starred_kvpair _loop0_108
        mark = self._mark()
        if (
            (elem := self.double_starred_kvpair())
            is not None
            and
            (seq := self._loop0_108())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_109(self) -> Optional[Any]:
        # _loop1_109: for_if_clause
        mark = self._mark()
        children = []
        while (
            (for_if_clause := self.for_if_clause())
        ):
            children.append(for_if_clause)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_110(self) -> Optional[Any]:
        # _loop0_110: ('if' disjunction)
        mark = self._mark()
        children = []
        while (
            (_tmp_187 := self._tmp_187())
        ):
            children.append(_tmp_187)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_111(self) -> Optional[Any]:
        # _loop0_111: ('if' disjunction)
        mark = self._mark()
        children = []
        while (
            (_tmp_188 := self._tmp_188())
        ):
            children.append(_tmp_188)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_112(self) -> Optional[Any]:
        # _tmp_112: assigment_expression | expression !':='
        mark = self._mark()
        if (
            (assigment_expression := self.assigment_expression())
        ):
            return assigment_expression
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            self.negative_lookahead(self.expect, ':=')
        ):
            return expression
        self._reset(mark)
        return None

    @memoize
    def _loop0_114(self) -> Optional[Any]:
        # _loop0_114: ',' (starred_expression | (assigment_expression | expression !':=') !'=')
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self._tmp_189())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_113(self) -> Optional[Any]:
        # _gather_113: (starred_expression | (assigment_expression | expression !':=') !'=') _loop0_114
        mark = self._mark()
        if (
            (elem := self._tmp_189())
            is not None
            and
            (seq := self._loop0_114())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_115(self) -> Optional[Any]:
        # _tmp_115: ',' kwargs
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (k := self.kwargs())
        ):
            return k
        self._reset(mark)
        return None

    @memoize
    def _loop0_117(self) -> Optional[Any]:
        # _loop0_117: ',' kwarg_or_starred
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.kwarg_or_starred())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_116(self) -> Optional[Any]:
        # _gather_116: kwarg_or_starred _loop0_117
        mark = self._mark()
        if (
            (elem := self.kwarg_or_starred())
            is not None
            and
            (seq := self._loop0_117())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_119(self) -> Optional[Any]:
        # _loop0_119: ',' kwarg_or_double_starred
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.kwarg_or_double_starred())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_118(self) -> Optional[Any]:
        # _gather_118: kwarg_or_double_starred _loop0_119
        mark = self._mark()
        if (
            (elem := self.kwarg_or_double_starred())
            is not None
            and
            (seq := self._loop0_119())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_121(self) -> Optional[Any]:
        # _loop0_121: ',' kwarg_or_starred
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.kwarg_or_starred())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_120(self) -> Optional[Any]:
        # _gather_120: kwarg_or_starred _loop0_121
        mark = self._mark()
        if (
            (elem := self.kwarg_or_starred())
            is not None
            and
            (seq := self._loop0_121())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_123(self) -> Optional[Any]:
        # _loop0_123: ',' kwarg_or_double_starred
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.kwarg_or_double_starred())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_122(self) -> Optional[Any]:
        # _gather_122: kwarg_or_double_starred _loop0_123
        mark = self._mark()
        if (
            (elem := self.kwarg_or_double_starred())
            is not None
            and
            (seq := self._loop0_123())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_124(self) -> Optional[Any]:
        # _loop0_124: (',' star_target)
        mark = self._mark()
        children = []
        while (
            (_tmp_190 := self._tmp_190())
        ):
            children.append(_tmp_190)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_126(self) -> Optional[Any]:
        # _loop0_126: ',' star_target
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.star_target())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_125(self) -> Optional[Any]:
        # _gather_125: star_target _loop0_126
        mark = self._mark()
        if (
            (elem := self.star_target())
            is not None
            and
            (seq := self._loop0_126())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop1_127(self) -> Optional[Any]:
        # _loop1_127: (',' star_target)
        mark = self._mark()
        children = []
        while (
            (_tmp_191 := self._tmp_191())
        ):
            children.append(_tmp_191)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_128(self) -> Optional[Any]:
        # _tmp_128: !'*' star_target
        mark = self._mark()
        if (
            self.negative_lookahead(self.expect, '*')
            and
            (star_target := self.star_target())
        ):
            return star_target
        self._reset(mark)
        return None

    @memoize
    def _loop0_130(self) -> Optional[Any]:
        # _loop0_130: ',' del_target
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.del_target())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_129(self) -> Optional[Any]:
        # _gather_129: del_target _loop0_130
        mark = self._mark()
        if (
            (elem := self.del_target())
            is not None
            and
            (seq := self._loop0_130())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_132(self) -> Optional[Any]:
        # _loop0_132: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_131(self) -> Optional[Any]:
        # _gather_131: expression _loop0_132
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_132())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_134(self) -> Optional[Any]:
        # _loop0_134: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_133(self) -> Optional[Any]:
        # _gather_133: expression _loop0_134
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_134())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_136(self) -> Optional[Any]:
        # _loop0_136: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_135(self) -> Optional[Any]:
        # _gather_135: expression _loop0_136
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_136())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_138(self) -> Optional[Any]:
        # _loop0_138: ',' expression
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.expression())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_137(self) -> Optional[Any]:
        # _gather_137: expression _loop0_138
        mark = self._mark()
        if (
            (elem := self.expression())
            is not None
            and
            (seq := self._loop0_138())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_139(self) -> Optional[Any]:
        # _tmp_139: NEWLINE INDENT
        mark = self._mark()
        if (
            (_newline := self.expect('NEWLINE'))
            and
            (_indent := self.expect('INDENT'))
        ):
            return [_newline, _indent]
        self._reset(mark)
        return None

    @memoize
    def _tmp_140(self) -> Optional[Any]:
        # _tmp_140: args | expression for_if_clauses
        mark = self._mark()
        if (
            (args := self.args())
        ):
            return args
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            (for_if_clauses := self.for_if_clauses())
        ):
            return [expression, for_if_clauses]
        self._reset(mark)
        return None

    @memoize
    def _tmp_141(self) -> Optional[Any]:
        # _tmp_141: NAME '='
        mark = self._mark()
        if (
            (name := self.name())
            and
            (literal := self.expect('='))
        ):
            return [name, literal]
        self._reset(mark)
        return None

    @memoize
    def _tmp_142(self) -> Optional[Any]:
        # _tmp_142: NAME STRING | SOFT_KEYWORD
        mark = self._mark()
        if (
            (name := self.name())
            and
            (string := self.string())
        ):
            return [name, string]
        self._reset(mark)
        if (
            (soft_keyword := self.soft_keyword())
        ):
            return soft_keyword
        self._reset(mark)
        return None

    @memoize
    def _tmp_143(self) -> Optional[Any]:
        # _tmp_143: 'else' | ':'
        mark = self._mark()
        if (
            (literal := self.expect('else'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(':'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_144(self) -> Optional[Any]:
        # _tmp_144: '=' | ':='
        mark = self._mark()
        if (
            (literal := self.expect('='))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(':='))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_145(self) -> Optional[Any]:
        # _tmp_145: list | tuple | genexp | 'True' | 'None' | 'False'
        mark = self._mark()
        if (
            (list := self.list())
        ):
            return list
        self._reset(mark)
        if (
            (tuple := self.tuple())
        ):
            return tuple
        self._reset(mark)
        if (
            (genexp := self.genexp())
        ):
            return genexp
        self._reset(mark)
        if (
            (literal := self.expect('True'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('None'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('False'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_146(self) -> Optional[Any]:
        # _tmp_146: '=' | ':='
        mark = self._mark()
        if (
            (literal := self.expect('='))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(':='))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _loop0_147(self) -> Optional[Any]:
        # _loop0_147: star_named_expressions
        mark = self._mark()
        children = []
        while (
            (star_named_expressions := self.star_named_expressions())
        ):
            children.append(star_named_expressions)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_148(self) -> Optional[Any]:
        # _loop0_148: (star_targets '=')
        mark = self._mark()
        children = []
        while (
            (_tmp_192 := self._tmp_192())
        ):
            children.append(_tmp_192)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_149(self) -> Optional[Any]:
        # _loop0_149: (star_targets '=')
        mark = self._mark()
        children = []
        while (
            (_tmp_193 := self._tmp_193())
        ):
            children.append(_tmp_193)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_150(self) -> Optional[Any]:
        # _tmp_150: yield_expr | star_expressions
        mark = self._mark()
        if (
            (yield_expr := self.yield_expr())
        ):
            return yield_expr
        self._reset(mark)
        if (
            (star_expressions := self.star_expressions())
        ):
            return star_expressions
        self._reset(mark)
        return None

    @memoize
    def _tmp_151(self) -> Optional[Any]:
        # _tmp_151: '[' | '(' | '{'
        mark = self._mark()
        if (
            (literal := self.expect('['))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('('))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('{'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_152(self) -> Optional[Any]:
        # _tmp_152: '[' | '{'
        mark = self._mark()
        if (
            (literal := self.expect('['))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('{'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_153(self) -> Optional[Any]:
        # _tmp_153: '[' | '{'
        mark = self._mark()
        if (
            (literal := self.expect('['))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('{'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _loop0_154(self) -> Optional[Any]:
        # _loop0_154: param_no_default
        mark = self._mark()
        children = []
        while (
            (param_no_default := self.param_no_default())
        ):
            children.append(param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_155(self) -> Optional[Any]:
        # _loop1_155: param_with_default
        mark = self._mark()
        children = []
        while (
            (param_with_default := self.param_with_default())
        ):
            children.append(param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop0_156(self) -> Optional[Any]:
        # _loop0_156: lambda_param_no_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_no_default := self.lambda_param_no_default())
        ):
            children.append(lambda_param_no_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _loop1_157(self) -> Optional[Any]:
        # _loop1_157: lambda_param_with_default
        mark = self._mark()
        children = []
        while (
            (lambda_param_with_default := self.lambda_param_with_default())
        ):
            children.append(lambda_param_with_default)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _tmp_158(self) -> Optional[Any]:
        # _tmp_158: ')' | ',' (')' | '**')
        mark = self._mark()
        if (
            (literal := self.expect(')'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(','))
            and
            (_tmp_194 := self._tmp_194())
        ):
            return [literal, _tmp_194]
        self._reset(mark)
        return None

    @memoize
    def _tmp_159(self) -> Optional[Any]:
        # _tmp_159: ':' | ',' (':' | '**')
        mark = self._mark()
        if (
            (literal := self.expect(':'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(','))
            and
            (_tmp_195 := self._tmp_195())
        ):
            return [literal, _tmp_195]
        self._reset(mark)
        return None

    @memoize
    def _tmp_160(self) -> Optional[Any]:
        # _tmp_160: ',' | ')' | ':'
        mark = self._mark()
        if (
            (literal := self.expect(','))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(')'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(':'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _loop0_162(self) -> Optional[Any]:
        # _loop0_162: ',' (expression ['as' star_target])
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self._tmp_196())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_161(self) -> Optional[Any]:
        # _gather_161: (expression ['as' star_target]) _loop0_162
        mark = self._mark()
        if (
            (elem := self._tmp_196())
            is not None
            and
            (seq := self._loop0_162())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_164(self) -> Optional[Any]:
        # _loop0_164: ',' (expressions ['as' star_target])
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self._tmp_197())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_163(self) -> Optional[Any]:
        # _gather_163: (expressions ['as' star_target]) _loop0_164
        mark = self._mark()
        if (
            (elem := self._tmp_197())
            is not None
            and
            (seq := self._loop0_164())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_166(self) -> Optional[Any]:
        # _loop0_166: ',' (expression ['as' star_target])
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self._tmp_198())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_165(self) -> Optional[Any]:
        # _gather_165: (expression ['as' star_target]) _loop0_166
        mark = self._mark()
        if (
            (elem := self._tmp_198())
            is not None
            and
            (seq := self._loop0_166())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _loop0_168(self) -> Optional[Any]:
        # _loop0_168: ',' (expressions ['as' star_target])
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self._tmp_199())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_167(self) -> Optional[Any]:
        # _gather_167: (expressions ['as' star_target]) _loop0_168
        mark = self._mark()
        if (
            (elem := self._tmp_199())
            is not None
            and
            (seq := self._loop0_168())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_169(self) -> Optional[Any]:
        # _tmp_169: 'except' | 'finally'
        mark = self._mark()
        if (
            (literal := self.expect('except'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('finally'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_170(self) -> Optional[Any]:
        # _tmp_170: 'as' NAME
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (name := self.name())
        ):
            return [literal, name]
        self._reset(mark)
        return None

    @memoize
    def _tmp_171(self) -> Optional[Any]:
        # _tmp_171: 'as' NAME
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (name := self.name())
        ):
            return [literal, name]
        self._reset(mark)
        return None

    @memoize
    def _tmp_172(self) -> Optional[Any]:
        # _tmp_172: 'as' NAME
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (name := self.name())
        ):
            return [literal, name]
        self._reset(mark)
        return None

    @memoize
    def _tmp_173(self) -> Optional[Any]:
        # _tmp_173: positional_patterns ','
        mark = self._mark()
        if (
            (positional_patterns := self.positional_patterns())
            and
            (literal := self.expect(','))
        ):
            return [positional_patterns, literal]
        self._reset(mark)
        return None

    @memoize
    def _tmp_174(self) -> Optional[Any]:
        # _tmp_174: '->' expression
        mark = self._mark()
        if (
            (literal := self.expect('->'))
            and
            (expression := self.expression())
        ):
            return [literal, expression]
        self._reset(mark)
        return None

    @memoize
    def _tmp_175(self) -> Optional[Any]:
        # _tmp_175: '(' arguments? ')'
        mark = self._mark()
        if (
            (literal := self.expect('('))
            and
            (opt := self.arguments(),)
            and
            (literal_1 := self.expect(')'))
        ):
            return [literal, opt, literal_1]
        self._reset(mark)
        return None

    @memoize
    def _loop0_177(self) -> Optional[Any]:
        # _loop0_177: ',' double_starred_kvpair
        mark = self._mark()
        children = []
        while (
            (literal := self.expect(','))
            and
            (elem := self.double_starred_kvpair())
        ):
            children.append(elem)
            mark = self._mark()
        self._reset(mark)
        return children

    @memoize
    def _gather_176(self) -> Optional[Any]:
        # _gather_176: double_starred_kvpair _loop0_177
        mark = self._mark()
        if (
            (elem := self.double_starred_kvpair())
            is not None
            and
            (seq := self._loop0_177())
            is not None
        ):
            return [elem] + seq
        self._reset(mark)
        return None

    @memoize
    def _tmp_178(self) -> Optional[Any]:
        # _tmp_178: '}' | ','
        mark = self._mark()
        if (
            (literal := self.expect('}'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect(','))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_179(self) -> Optional[Any]:
        # _tmp_179: star_targets '='
        mark = self._mark()
        if (
            (z := self.star_targets())
            and
            (literal := self.expect('='))
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _tmp_180(self) -> Optional[Any]:
        # _tmp_180: '.' | '...'
        mark = self._mark()
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('...'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_181(self) -> Optional[Any]:
        # _tmp_181: '.' | '...'
        mark = self._mark()
        if (
            (literal := self.expect('.'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('...'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_182(self) -> Optional[Any]:
        # _tmp_182: '@' named_expression NEWLINE
        mark = self._mark()
        if (
            (literal := self.expect('@'))
            and
            (f := self.named_expression())
            and
            (_newline := self.expect('NEWLINE'))
        ):
            return f
        self._reset(mark)
        return None

    @memoize
    def _tmp_183(self) -> Optional[Any]:
        # _tmp_183: ',' expression
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (c := self.expression())
        ):
            return c
        self._reset(mark)
        return None

    @memoize
    def _tmp_184(self) -> Optional[Any]:
        # _tmp_184: ',' star_expression
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (c := self.star_expression())
        ):
            return c
        self._reset(mark)
        return None

    @memoize
    def _tmp_185(self) -> Optional[Any]:
        # _tmp_185: 'or' conjunction
        mark = self._mark()
        if (
            (literal := self.expect('or'))
            and
            (c := self.conjunction())
        ):
            return c
        self._reset(mark)
        return None

    @memoize
    def _tmp_186(self) -> Optional[Any]:
        # _tmp_186: 'and' inversion
        mark = self._mark()
        if (
            (literal := self.expect('and'))
            and
            (c := self.inversion())
        ):
            return c
        self._reset(mark)
        return None

    @memoize
    def _tmp_187(self) -> Optional[Any]:
        # _tmp_187: 'if' disjunction
        mark = self._mark()
        if (
            (literal := self.expect('if'))
            and
            (z := self.disjunction())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _tmp_188(self) -> Optional[Any]:
        # _tmp_188: 'if' disjunction
        mark = self._mark()
        if (
            (literal := self.expect('if'))
            and
            (z := self.disjunction())
        ):
            return z
        self._reset(mark)
        return None

    @memoize
    def _tmp_189(self) -> Optional[Any]:
        # _tmp_189: starred_expression | (assigment_expression | expression !':=') !'='
        mark = self._mark()
        if (
            (starred_expression := self.starred_expression())
        ):
            return starred_expression
        self._reset(mark)
        if (
            (_tmp_200 := self._tmp_200())
            and
            self.negative_lookahead(self.expect, '=')
        ):
            return _tmp_200
        self._reset(mark)
        return None

    @memoize
    def _tmp_190(self) -> Optional[Any]:
        # _tmp_190: ',' star_target
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (c := self.star_target())
        ):
            return c
        self._reset(mark)
        return None

    @memoize
    def _tmp_191(self) -> Optional[Any]:
        # _tmp_191: ',' star_target
        mark = self._mark()
        if (
            (literal := self.expect(','))
            and
            (c := self.star_target())
        ):
            return c
        self._reset(mark)
        return None

    @memoize
    def _tmp_192(self) -> Optional[Any]:
        # _tmp_192: star_targets '='
        mark = self._mark()
        if (
            (star_targets := self.star_targets())
            and
            (literal := self.expect('='))
        ):
            return [star_targets, literal]
        self._reset(mark)
        return None

    @memoize
    def _tmp_193(self) -> Optional[Any]:
        # _tmp_193: star_targets '='
        mark = self._mark()
        if (
            (star_targets := self.star_targets())
            and
            (literal := self.expect('='))
        ):
            return [star_targets, literal]
        self._reset(mark)
        return None

    @memoize
    def _tmp_194(self) -> Optional[Any]:
        # _tmp_194: ')' | '**'
        mark = self._mark()
        if (
            (literal := self.expect(')'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('**'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_195(self) -> Optional[Any]:
        # _tmp_195: ':' | '**'
        mark = self._mark()
        if (
            (literal := self.expect(':'))
        ):
            return literal
        self._reset(mark)
        if (
            (literal := self.expect('**'))
        ):
            return literal
        self._reset(mark)
        return None

    @memoize
    def _tmp_196(self) -> Optional[Any]:
        # _tmp_196: expression ['as' star_target]
        mark = self._mark()
        if (
            (expression := self.expression())
            and
            (opt := self._tmp_201(),)
        ):
            return [expression, opt]
        self._reset(mark)
        return None

    @memoize
    def _tmp_197(self) -> Optional[Any]:
        # _tmp_197: expressions ['as' star_target]
        mark = self._mark()
        if (
            (expressions := self.expressions())
            and
            (opt := self._tmp_202(),)
        ):
            return [expressions, opt]
        self._reset(mark)
        return None

    @memoize
    def _tmp_198(self) -> Optional[Any]:
        # _tmp_198: expression ['as' star_target]
        mark = self._mark()
        if (
            (expression := self.expression())
            and
            (opt := self._tmp_203(),)
        ):
            return [expression, opt]
        self._reset(mark)
        return None

    @memoize
    def _tmp_199(self) -> Optional[Any]:
        # _tmp_199: expressions ['as' star_target]
        mark = self._mark()
        if (
            (expressions := self.expressions())
            and
            (opt := self._tmp_204(),)
        ):
            return [expressions, opt]
        self._reset(mark)
        return None

    @memoize
    def _tmp_200(self) -> Optional[Any]:
        # _tmp_200: assigment_expression | expression !':='
        mark = self._mark()
        if (
            (assigment_expression := self.assigment_expression())
        ):
            return assigment_expression
        self._reset(mark)
        if (
            (expression := self.expression())
            and
            self.negative_lookahead(self.expect, ':=')
        ):
            return expression
        self._reset(mark)
        return None

    @memoize
    def _tmp_201(self) -> Optional[Any]:
        # _tmp_201: 'as' star_target
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (star_target := self.star_target())
        ):
            return [literal, star_target]
        self._reset(mark)
        return None

    @memoize
    def _tmp_202(self) -> Optional[Any]:
        # _tmp_202: 'as' star_target
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (star_target := self.star_target())
        ):
            return [literal, star_target]
        self._reset(mark)
        return None

    @memoize
    def _tmp_203(self) -> Optional[Any]:
        # _tmp_203: 'as' star_target
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (star_target := self.star_target())
        ):
            return [literal, star_target]
        self._reset(mark)
        return None

    @memoize
    def _tmp_204(self) -> Optional[Any]:
        # _tmp_204: 'as' star_target
        mark = self._mark()
        if (
            (literal := self.expect('as'))
            and
            (star_target := self.star_target())
        ):
            return [literal, star_target]
        self._reset(mark)
        return None

    KEYWORDS = ('return', 'import', 'from', 'raise', 'pass', 'del', 'yield', 'assert', 'break', 'continue', 'global', 'nonlocal', 'def', 'if', 'class', 'with', 'for', 'try', 'while', 'as', 'elif', 'else', 'in', 'except', 'finally', 'None', 'True', 'False', 'or', 'and', 'not', 'is', 'lambda')
    SOFT_KEYWORDS = ('_', 'match', 'case')

def main():
  for filename in sys.argv[1:]:
    file = open(filename, 'r')
    parser = GeneratedParser(lexer.Tokenizer(file, filename), verbose=True)
    parsed = parser.file()
    print(ast.dump(parsed))

if __name__ == '__main__': main()

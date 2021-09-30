import ast, os, sys, traceback
import lexer, parse

def main():
  for pt_filename in sys.argv[1:]:
    basename, ext = os.path.splitext(pt_filename)
    if ext == '.py':
      py_filename = pt_filename + '.py'
    else:
      py_filename = basename + '.py'
    print(pt_filename, '->', py_filename)
    pt_file = open(pt_filename, 'r')
    parser = parse.ParseltongueParser(
      lexer.Tokenizer(pt_file, pt_filename),
      filename = pt_filename,
    )
    parsed = parser.file()
    if parsed is None:
      err = parser.make_syntax_error('Parseltongue parse error')
      traceback.print_exception(err.__class__, err, None, file = sys.stdout)
      continue
    # For debugging:
    #unparser = ast._Unparser()
    #unparser._source = []
    #unparser.traverse(parsed)
    #print(unparser._source)
    py_content = ast.unparse(parsed) + '\n'
    with open(py_filename, 'w') as py_file:
      py_file.write(py_content)

if __name__ == '__main__': main()
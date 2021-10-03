import ast, os, sys, traceback
import lexer, parse

def detect_newline(filename):
  '''Detect newline character sequence in given filename by reading first line
  '''
  with open(filename, 'rb') as f:
    line = f.readline()
    for newline in [b'\r\n', b'\n', b'\r']:
      if line.endswith(newline):
        return newline.decode('ascii')
  # No newline character => None tells Python to use OS default

def copy_mode(old_filename, new_filename):
  os.chmod(new_filename, os.stat(old_filename).st_mode)
  try:
    import win32security
  except ImportError:
    pass  # not Windows
  else:
    win32security.SetFileSecurity(new_filename,
      win32security.DACL_SECURITY_INFORMATION,
      win32security.GetFileSecurity(
        old_filename, win32security.DACL_SECURITY_INFORMATION))

def main():
  for pt_filename in sys.argv[1:]:
    basename, ext = os.path.splitext(pt_filename)
    if ext == '.py':
      py_filename = pt_filename + '.py'
    else:
      py_filename = basename + '.py'
    print(pt_filename, '->', py_filename)
    newline = detect_newline(pt_filename)
    pt_file = open(pt_filename, 'r')
    tokenizer = lexer.Tokenizer(pt_file, pt_filename)
    parser = parse.ParseltongueParser(tokenizer, filename = pt_filename)
    parsed = parser.file()
    pt_file.close()
    if parsed is None:
      tok = tokenizer.diagnose()
      err = parser.make_syntax_error(
        f'Parseltongue parse error at {lexer.tok_name[tok.type]} token {repr(tok.string)}')
      traceback.print_exception(err.__class__, err, None, file = sys.stdout)
      continue
    # For debugging:
    #unparser = ast._Unparser()
    #unparser._source = []
    #unparser.traverse(parsed)
    #print(unparser._source)
    py_content = ast.unparse(parsed) + '\n'
    with open(py_filename, 'w', newline = newline) as py_file:
      py_file.write(py_content)
    copy_mode(pt_filename, py_filename)

if __name__ == '__main__': main()

import argparse, ast, os, sys, traceback
import lexer, parse
import util
argparser = argparse.ArgumentParser('parseltongue')
argparser.add_argument('filenames', metavar='file.pt', nargs='+', help='Parseltongue source files')
argparser.add_argument('-o', '--output', dest='output', help='destination directory for Python output')
argparser.add_argument('-c', '--check', dest='check', action='store_true', help="check for changes, don't modify files")

def main():
    args = argparser.parse_args()
    exitcode = 0
    for pt_filename in args.filenames:
        (basename, ext) = os.path.splitext(pt_filename)
        py_filename = basename + '.py'
        if args.output is not None:
            py_filename = os.path.join(args.output, os.path.basename(py_filename))
        try:
            if pt_filename == py_filename or os.path.samefile(pt_filename, py_filename):
                py_filename += '.py'
        except FileNotFoundError:
            pass
        if args.check:
            print(pt_filename, 'vs', py_filename)
        else:
            print(pt_filename, '->', py_filename)
        newline = util.detect_newline(pt_filename)
        pt_file = open(pt_filename, 'r')
        tokenizer = lexer.Tokenizer(pt_file, pt_filename)
        parser = parse.ParseltongueParser(tokenizer, filename=pt_filename)
        parsed = parser.file()
        pt_file.close()
        if parsed is None:
            tok = tokenizer.diagnose()
            err = parser.make_syntax_error(f'Parseltongue parse error at {lexer.tok_name[tok.type]} token {repr(tok.string)}')
            traceback.print_exception(err.__class__, err, None, file=sys.stdout)
            continue
        py_content = ast.unparse(parsed) + '\n'
        if args.check:
            with open(py_filename, 'r', newline=newline) as py_file:
                if not py_file.read() == py_content:
                    print(' -- DIFFERENT')
                    exitcode += 1
        else:
            with open(py_filename, 'w', newline=newline) as py_file:
                py_file.write(py_content)
            util.copy_mode(pt_filename, py_filename)
    if __name__ == '__main__':
        sys.exit(exitcode)
    else:
        return exitcode
if __name__ == '__main__':
    main()

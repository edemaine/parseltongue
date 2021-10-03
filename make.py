#!/usr/bin/env python3.9

import glob, importlib, os, shutil, subprocess, sys

#PYTHON = 'poetry run python'
PYTHON = 'python3.9'

ROOT_DIR = os.path.relpath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
BUILD_DIR = os.path.join(ROOT_DIR, 'lib')

PEGEN_PATH = os.path.join(ROOT_DIR, 'pegen', 'src')
PEGEN_COPY = ['tokenizer.py', 'parser.py']
PEGEN_COPY_DEST = os.path.join(BUILD_DIR, 'pegen')

GRAMMAR_INPUT = os.path.join(SRC_DIR, 'parseltongue.gram')
GRAMMAR_OUTPUT = os.path.join(BUILD_DIR, 'parse.py')

sys.path.insert(0, PEGEN_PATH)
import pegen.__main__ as pegen

sys.path.insert(0, BUILD_DIR)
import util

def need_build(dest, srcs):
  if isinstance(srcs, str): srcs = [srcs]
  try:
    last = os.stat(dest).st_mtime 
  except FileNotFoundError:
    return True
  for src in srcs:
    if last <= os.stat(src).st_mtime:
      return True
  return False

def mkdir(dir):
  if not os.path.isdir(dir):
    print(f'\tmkdir -p {dir}')
    os.makedirs(dir)

def copy(src, destdir):
  mkdir(destdir)
  destfile = os.path.join(destdir, os.path.basename(src))
  if need_build(destfile, src):
    print(f'\tcp {src} {destfile}')
    shutil.copy(src, destfile)
    util.copy_mode(src, destfile)

class new_argv:
  def __init__(self, new_argv):
    self.new_argv = new_argv
  def __enter__(self):
    self.old_argv = sys.argv
    sys.argv = self.new_argv
  def __exit__(self, *exc):
    sys.argv = self.old_argv

def run_python_main(main, argv):
  print('\t' + ' '.join(argv))
  with new_argv(argv):
    return main()

def make_grammar():
  if need_build(GRAMMAR_OUTPUT, GRAMMAR_INPUT):
    mkdir(os.path.dirname(GRAMMAR_OUTPUT))
    run_python_main(pegen.main,
      ['pegen', '--quiet', GRAMMAR_INPUT, '-o', GRAMMAR_OUTPUT])
  for filename in PEGEN_COPY:
    copy(os.path.join(PEGEN_PATH, 'pegen', filename), PEGEN_COPY_DEST)

def make_transpile(check = False):
  # Import after compiling parser
  sys.path.insert(0, ROOT_DIR)
  import lib.__main__ as parseltongue

  # Reload all Parseltongue modules in case changed
  reload = []
  for module in sys.modules.values():
    if hasattr(module, '__file__') and module.__file__ is not None:
      path = os.path.relpath(module.__file__, BUILD_DIR)
      if not path.startswith(os.pardir):
        reload.append((module, path))
  if (parseltongue, '__main__.py') not in reload:
    reload.append((parseltongue, '__main__.py'))
  print('Reloading modules', ', '.join(path for module, path in reload))
  for module, path in reload:
    importlib.reload(module)

  mkdir(BUILD_DIR)
  return run_python_main(parseltongue.main,
    ['parseltongue', '-o', BUILD_DIR] +
    (['--check'] if check else []) +
    glob.glob(os.path.join(SRC_DIR, '*.pt')))

iterations = 5
def make_transpile_loop():
  for count in range(iterations):
    make_transpile()
    if make_transpile(check = True) == 0:
      break
  else:
    print('FAILED TO CONVERGE AFTER {iterations} ITERATIONS')

def make():
  make_grammar()
  make_transpile_loop()

if __name__ == '__main__': make()

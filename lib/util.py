import os

def detect_newline(filename):
    """Detect newline character sequence in given filename by reading first line
  """
    with open(filename, 'rb') as f:
        line = f.readline()
        for newline in [b'\r\n', b'\n', b'\r']:
            if line.endswith(newline):
                return newline.decode('ascii')

def copy_mode(old_filename, new_filename):
    os.chmod(new_filename, os.stat(old_filename).st_mode)
    try:
        import win32security
    except ImportError:
        pass
    else:
        win32security.SetFileSecurity(new_filename, win32security.DACL_SECURITY_INFORMATION, win32security.GetFileSecurity(old_filename, win32security.DACL_SECURITY_INFORMATION))

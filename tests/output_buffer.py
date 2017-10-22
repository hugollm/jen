from io import StringIO
import sys


class OutputBuffer(object):

    def __init__(self):
        self.stdout = StringIO()
        self.stderr = StringIO()

    def __enter__(self):
        self.original_stdout, self.original_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self.stdout, self.stderr
        return self

    def __exit__(self, exception_type, exception, traceback):
        sys.stdout, sys.stderr = self.original_stdout, self.original_stderr

    @property
    def out(self):
        return self.stdout.getvalue()

    @property
    def err(self):
        return self.stderr.getvalue()

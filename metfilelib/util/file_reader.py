# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

import collections
import os


Error = collections.namedtuple('Error', 'line, error_code, error_message')


class FileReader(object):
    """A simple file reader for line-based files. It provides a line
    lookahead and line numbering, and can log error messages. Error
    messages are sent to stderr by default, but it is possible to
    provide another error message handler (any object with a write()
    method).

    Files are opened with universal line endings (\n, \r\n or
    \n\r)."""

    def __init__(
        self,
        file_path,
        skip_empty_lines=False):
        """File_path is a full path to a file. It will be opened immediately,
        so if any exceptions occur, they will probably happen here.

        This immediately reads the first line of the file.

        error_message_handler is any object with a write() method. It
        will receive error messages of the form "filename 1: error
        message\n", where "filename" is the basename of the file_path
        and "1" is the line number.
        """

        self._open_file = open(file_path, 'rU')
        self.filename = os.path.basename(file_path)
        self._skip_empty_lines = skip_empty_lines
        self.line_number = 0
        self.current_line = None
        self.errors = []
        self.success = True

        # Read the first line
        self.next()

    def next(self):
        """Read the next line, if we are not already at EOF. Updates
        self.current_line and self.line_number. May result in a change
        in self.eof."""

        while not self.eof:
            byteline = self._open_file.readline()

            if (self.line_number == 0 and
                byteline.startswith(b'\xef\xbb\xbf')):
                # UTF8 BOM
                self.current_line = byteline[3:].decode('utf8')
            else:
                self.current_line = byteline.decode('utf8')

            self.line_number += 1

            if not self._skip_empty_lines or self.current_line.strip():
                break

    @property
    def eof(self):
        """Return True if we are at end of file."""
        return self.current_line == ''

    def record_error(self, error_message, error_code=None):
        """Record an error and set success to False."""

        self.errors.append(Error(
                line=self.line_number,
                error_code=error_code,
                error_message=error_message))

        self.success = False

"""Tests for metfilelib.util.file_reader"""

# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

from unittest import TestCase

import mock


from metfilelib.util import file_reader


def mock_file_factory(lines):
    copied_lines = lines[:]

    def readline():
        if copied_lines:
            return copied_lines.pop(0)
        else:
            return ''

    mock_file = mock.MagicMock()
    mock_file.readline = readline

    return mock_file


class TestFileReader(TestCase):
    def test_with_two_lines(self):
        # Must be byte strings -- when they come out of the file,
        # they're bytes
        lines = [
            b"This is the first line\n",
            b"This is the second line\n"
            ]

        with mock.patch(
            '__builtin__.open',
            return_value=mock_file_factory(lines)):
            reader = file_reader.FileReader("/some/filename")

        self.assertEquals(reader.filename, "filename")
        self.assertEquals(reader.line_number, 1)
        self.assertEquals(
            reader.current_line, "This is the first line\n")
        self.assertFalse(reader.eof)
        self.assertTrue(reader.success)

        reader.next()

        self.assertEquals(reader.line_number, 2)
        self.assertEquals(
            reader.current_line, "This is the second line\n")
        self.assertFalse(reader.eof)
        self.assertTrue(reader.success)

        reader.next()

        self.assertEquals(reader.line_number, 3)
        self.assertEquals(
            reader.current_line, "")
        self.assertTrue(reader.eof)
        self.assertTrue(reader.success)

    def test_record_error(self):
        with mock.patch('__builtin__.open'):
            reader = file_reader.FileReader(
                file_path="/some/filename")

        self.assertTrue(reader.success)

        reader.record_error("test error", "CODE")

        self.assertFalse(reader.success)
        self.assertEquals(len(reader.errors), 1)

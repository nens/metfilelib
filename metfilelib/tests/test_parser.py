# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import mock
from unittest import TestCase

from metfilelib.util.tests.test_file_reader import mock_file_factory
from metfilelib.util import file_reader
from metfilelib import parser


class TestParseMeting(TestCase):
    def test_numbers_converted_to_float(self):
        lines = [
            b"<METING>22,999,152168.401,444100.055,2.206,2.206</METING>\n"
            ]
        with mock.patch(
            '__builtin__.open',
            return_value=mock_file_factory(lines)):
            reader = file_reader.FileReader("/some/filename")

        meting = parser.parse_meting(reader)

        self.assertTrue(reader.success)
        self.assertTrue(meting)
        self.assertTrue(isinstance(meting.x, float))
        self.assertTrue(isinstance(meting.y, float))
        self.assertTrue(isinstance(meting.z1, float))
        self.assertTrue(isinstance(meting.z2, float))

    def test_x_is_not_a_valid_float(self):
        lines = [
            b"<METING>22,999,152.168.401,444100.055,2.206,2.206</METING>\n"
            ]
        with mock.patch(
            '__builtin__.open',
            return_value=mock_file_factory(lines)):
            reader = file_reader.FileReader("/some/filename")

        parser.parse_meting(reader)

        self.assertFalse(reader.success)

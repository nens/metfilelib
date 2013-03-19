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


def get_mock_reader(lines):
    with mock.patch(
        '__builtin__.open',
        return_value=mock_file_factory(lines)):
        reader = file_reader.FileReader("/some/filename")
    return reader


class TestVersion(TestCase):
    def test_success_with_correct_line(self):
        reader = get_mock_reader([
                b"<VERSIE>1.0</VERSIE>\n"
            ])

        parser.parse_version(reader)
        self.assertTrue(reader.success)

    def test_error_if_version_not_10(self):
        reader = get_mock_reader([
                b"<VERSIE>2.0</VERSIE>\n"
            ])

        parser.parse_version(reader)
        self.assertFalse(reader.success)


class TestParseSeries(TestCase):
    def test_success_with_correct_line(self):
        reader = get_mock_reader([
                b"<REEKS>deeleen,deeltwee,</REEKS>\n",
                b"<PROFIEL>O-BR00001927_516,PROFIEL_516,20120421,0.00,NAP,ABS,2,XY,152168.401,444100.055,\n",
b"<METING>22,999,152168.401,444100.055,2.206,2.206</METING>\n",
b"<METING>99,999,152168.475,444100.136,1.556,1.661</METING>\n",
                b"</PROFIEL>\n"
                ])

        print(reader.errors)
        self.assertTrue(reader.success)

    def test_error_with_a_result_when_second_comma_missing(self):
        reader = get_mock_reader([
                b"<REEKS>deeleen,deeltwee</REEKS>\n",
                b"<PROFIEL>O-BR00001927_516,PROFIEL_516,20120421,0.00,NAP,ABS,2,XY,152168.401,444100.055,\n",
b"<METING>22,999,152168.401,444100.055,2.206,2.206</METING>\n",
b"<METING>99,999,152168.475,444100.136,1.556,1.661</METING>\n",
                b"</PROFIEL>\n"
                ])

        result = parser.parse_series(reader)
        self.assertFalse(reader.success)
        self.assertNotEqual(result, None)


class TestParseMeting(TestCase):
    def test_numbers_converted_to_float(self):
        reader = get_mock_reader([
            b"<METING>22,999,152168.401,444100.055,2.206,2.206</METING>\n"
            ])

        meting = parser.parse_meting(reader)

        self.assertTrue(reader.success)
        self.assertTrue(meting)
        self.assertTrue(isinstance(meting.x, float))
        self.assertTrue(isinstance(meting.y, float))
        self.assertTrue(isinstance(meting.z1, float))
        self.assertTrue(isinstance(meting.z2, float))

    def test_x_is_not_a_valid_float(self):
        reader = get_mock_reader([
            b"<METING>22,999,152.168.401,444100.055,2.206,2.206</METING>\n"
            ])

        parser.parse_meting(reader)

        self.assertFalse(reader.success)

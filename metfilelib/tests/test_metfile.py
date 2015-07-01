# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Tests for metfile.py"""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from unittest import TestCase

from metfilelib import parser

from metfilelib.tests.test_parser import get_mock_reader


class TestProfile(TestCase):
    def test_this_example_appears_to_loop_forever(self):
        reader = get_mock_reader([
            b"<PROFIEL>W81-2_1,Profiel_1,20130114,0,NAP,ABS,2,XY,112372.752,485955.504,\n",
            b"<METING>2,999,15.0,15.0,-5.241,-5.241</METING>\n",
            b"<METING>1,999,-5.0,-5.0,-4.255,-4.255</METING>\n",
            b"<METING>22,999,0.0,0.0,-5.824,-5.824</METING>\n",
            b"<METING>22,999,10.0,10.0,-5.824,-5.824</METING>\n",
            b"<METING>5,999,2.0,2.0,-5.874,-5.844</METING>\n",
            b"<METING>5,999,4.0,4.0,-6.044,-5.984</METING>\n",
            b"<METING>5,999,7.0,7.0,-6.084,-6.02</METING>\n",
            b"</PROFIEL>\n"
        ])

        profile = parser.parse_profile(reader)

        sorted_measurements = profile.sorted_measurements
        self.assertEquals(len(sorted_measurements), 7)
        self.assertEquals(sorted_measurements[0].profile_point_type, '1')
        self.assertEquals(sorted_measurements[-1].profile_point_type, '2')

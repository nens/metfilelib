# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Tests for linear_algebra.py."""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math
from unittest import TestCase

from metfilelib.util import linear_algebra

# Things aren't as exact as we'd like
EPSILON = 0.000000001



class TestPoint(TestCase):
    def test_multiply(self):
        p = linear_algebra.Point(x=2, y=3)
        p = p.multiply(3)
        self.assertEquals(p.x, 6)
        self.assertEquals(p.y, 9)

    def test_add(self):
        p1 = linear_algebra.Point(x=2, y=2)
        p2 = linear_algebra.Point(x=7, y=13)
        p = p1.add(p2)

        self.assertEquals(p.x, 9)
        self.assertEquals(p.y, 15)

        p = p2.add(p1)

        self.assertEquals(p.x, 9)
        self.assertEquals(p.y, 15)

    def test_subtract(self):
        p1 = linear_algebra.Point(x=2, y=2)
        p2 = linear_algebra.Point(x=7, y=13)
        p = p1.subtract(p2)

        self.assertEquals(p.x, -5)
        self.assertEquals(p.y, -11)

        p = p2.subtract(p1)

        self.assertEquals(p.x, 5)
        self.assertEquals(p.y, 11)

    def test_size(self):
        p = linear_algebra.Point(3, 4)
        self.assertEquals(p.size, 5)  # 3, 4, 5 triangle

    def test_dot_product(self):
        p1 = linear_algebra.Point(1, 2)
        p2 = linear_algebra.Point(3, 4)

        d1 = p1.dot_product(p2)
        d2 = p2.dot_product(p1)

        self.assertEquals(d1, d2)
        self.assertEquals(d1, 1 * 3 + 2 * 4)

    def test_eq(self):
        p1 = linear_algebra.Point(1, 2)
        p2 = linear_algebra.Point(3, 4)
        p3 = linear_algebra.Point(3, 4)

        self.assertEquals(p2, p3)
        self.assertNotEquals(p1, p2)
        self.assertNotEquals(p1, p3)


class TestLine(TestCase):
    def test_project_at_y_axis(self):
        """Project at Y axis"""
        l1 = linear_algebra.Point(0, 0)
        l2 = linear_algebra.Point(0, 1)
        line = linear_algebra.Line(start=l1, end=l2)

        p = linear_algebra.Point(4, 4)
        p_p = line.project(p)
        self.assertEquals(p_p, linear_algebra.Point(0, 4))

    def test_project_on_diagonal(self):
        """Project at line through origin and (1, 1)"""
        l1 = linear_algebra.Point(0, 0)
        l2 = linear_algebra.Point(4, 4)
        line = linear_algebra.Line(start=l1, end=l2)

        p1 = linear_algebra.Point(0, 4)
        p2 = linear_algebra.Point(4, 0)

        p1_p = line.project(p1)
        p2_p = line.project(p2)

        self.assertEquals(p1_p, p2_p)

        # Check that p1_p is more or less (2, 2)
        self.assertTrue(abs(p1_p.x - 2) < EPSILON)
        self.assertTrue(abs(p1_p.y - 2) < EPSILON)

    def test_distance_to_line(self):
        """Wrote down an example on paper using a 3,4,5 triangle and a
        smaller one of the same shape... The point projects to (2.25,
        3)."""
        l = linear_algebra.Line(
            start=linear_algebra.Point(0, 0),
            end=linear_algebra.Point(2.25, 3))
        p = linear_algebra.Point(6.25, 0)

        self.assertEquals(l.distance(p), 5)

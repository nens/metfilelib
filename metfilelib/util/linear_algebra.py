# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Helper functions for reprojecting measurement points on the central
line.

ASSUMPTION: all coordinates are on a flat plane, and pixels are
"square" (the distance between (0, 0) and (1, 0) is the same as the
distance between (0, 0) and (0, 1)). This is obviously not true in the
real world, but close enough for RD coordinates in the Netherlands
over short distances.
"""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import namedtuple

import math


class Point(namedtuple('Point', 'x, y')):
    def multiply(self, scalar):
        return Point(x=scalar * self.x, y=scalar * self.y)

    def add(self, point):
        return Point(x=self.x + point.x, y=self.y + point.y)

    def subtract(self, point):
        return Point(x=self.x - point.x, y=self.y - point.y)

    @property
    def size(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def dot_product(self, point):
        return self.x * point.x + self.y * point.y

    def __eq__(self, point):
        return (self.x == point.x) and (self.y == point.y)

ORIGIN = Point(x=0.0, y=0.0)


class Line(namedtuple('Line', 'start, end')):
    def scaled_scalar_projection(self, point):
        """Project point on this line, return place on the line where
        start is at 0.0 and end is at 1.0.

        Useful for sorting points based on their projection on a line."""
        # Translate points so that self.start is (0, 0)
        t_end = self.end.subtract(self.start)
        t_point = point.subtract(self.start)

        # Project point, projection = (t_end . t_point) / |t_end| * t_end
        len_a_cos_theta = t_end.dot_product(t_point) / t_end.size

        scaled_scalar_projection = len_a_cos_theta / t_end.size

        return scaled_scalar_projection

    def project(self, point):
        """Return point projected onto this line."""

        # Translate points so that self.start is (0, 0)
        t_end = self.end.subtract(self.start)
        t_point = point.subtract(self.start)

        # Project point, projection = (t_end . t_point) / |t_end| * t_end
        t_line = Line(start=ORIGIN, end=t_end)
        t_projected = t_end.multiply(t_line.scaled_scalar_projection(t_point))

        # Translate back
        projected = t_projected.add(self.start)

        return projected

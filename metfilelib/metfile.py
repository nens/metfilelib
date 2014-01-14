# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Python classes that represent the data in a .met file."""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import namedtuple

from metfilelib.util import linear_algebra


MetFile = namedtuple('MetFile', 'version, series')

Series = namedtuple('Series', 'line_number, id, name, profiles')


class Profile(namedtuple(
    'Profile',
    '''line_number, id, description, date_measurement, level_value, level_type,
    coordinate_type, number_of_z_values, profile_type_placing,
    start_x, start_y, measurements''')):

    @property
    def line(self):
        """Return the base line of this profile. We use the line
        through the two mandatory '22' profile point types."""
        twentytwos = [m for m in self.measurements
                      if m.profile_point_type == '22']

        if len(twentytwos) != 2:
            return None

        start = twentytwos[0].point
        end = twentytwos[1].point

        if start == end:
            return None

        return linear_algebra.Line(start=start, end=end)

    @property
    def waterlevel(self):
        """Return the water level.

        If there are exactly two '22' profile point types, and their
        z1 and z2 values are all equal, then that's the water
        level. Otherwise return None."""

        twentytwos = [m for m in self.measurements
                      if m.profile_point_type == '22']

        if len(twentytwos) != 2:
            return None

        start = twentytwos[0]
        end = twentytwos[1]

        if start.z1 == start.z2 == end.z1 == end.z2:
            return start.z1

        return None

    @property
    def midpoint(self):
        """Point in the middle of the base line"""
        line = self.line
        if line is None:
            return None

        # Say line is A to B
        # Midpoint is ((B-A)*0.5)+A
        return line.midpoint

    @property
    def sorted_measurements(self):
        """Project points on the base line, return them in order."""
        line = self.line
        if line is None:
            # We can't project without line
            return self.measurements

        return sorted(
            self.measurements,
            key=lambda measurement: (
                line.scaled_scalar_projection(measurement.point)))

    @property
    def water_measurements(self):
        """Return the 22 codes and the measurements in between
        (sorted)"""
        water_indices = []
        measurements = list(self.sorted_measurements)

        for i, measurement in enumerate(measurements):
            if measurement.profile_point_type == '22':
                water_indices.append(i)

        if len(water_indices) != 2:
            # Can't do this
            return None

        return measurements[water_indices[0]:water_indices[1] + 1]

    @property
    def start_point(self):
        return linear_algebra.Point(x=self.start_x, y=self.start_y)


class Measurement(namedtuple(
   'Measurement',
   'line_number, profile_point_type, profile_point_drawing_code, x, y, z1, z2'
        )):
    ALLOWED_PROFILE_POINT_TYPES = set(
        ('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 '
         '22 98 99').split())

    ALLOWED_DRAWING_CODES = set(
        ('5 10 15 17 19 23 24 25 27 29 30 32 34 35 37 39 41 43 45 47 49 '
         '50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 '
         '88 90 92 94 96 98 130 135 140 150 999').split())

    @property
    def point(self):
        if not isinstance(self.x, float) or not isinstance(self.y, float):
            return None

        return linear_algebra.Point(x=self.x, y=self.y)

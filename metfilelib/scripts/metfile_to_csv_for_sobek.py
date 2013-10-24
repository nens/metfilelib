# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""
Read a metfile, turn it into profiles for SOBEK

Usage: bin/python metfilelib/scripts/metfile_to_csv_for_sobek <metfile>

Output: CSV to stdout, with one line per measurement point:
profile_id, distance_to_midpoint, max(z1, z2)

distance to midpoint is negative for the start point, positive for
the end point, so that the points are ordered by distance. Midpoint
is the point in between the 22 codes.
"""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

from metfilelib.util.file_reader import FileReader
from metfilelib.parser import parse_metfile


def error(message):
    sys.stderr.write("{}\n".format(message))
    sys.exit(1)


def main():
    filename = None
    if len(sys.argv) != 2:
        error(
            "Usage: bin/python metfilelib/scripts/"
            "metfile_to_csv_for_sobek <metfile>")

    filename = os.path.abspath(sys.argv[1])
    if not os.path.exists(filename):
        error("{} does not exist.".format(filename))

    file_object = FileReader(filename)
    metfile = parse_metfile(file_object)

    if file_object.errors:
        error("\n".join(unicode(e) for e in file_object.errors))

    for series in metfile.series:
        for profile in series.profiles:
            line = profile.line
            for measurement in profile.measurements:
                print("{profile_id},{dist},{z}".format(
                    profile_id=profile.id,
                    dist=line.distance_to_midpoint(measurement.point),
                    z=max(measurement.z1, measurement.z2)))


if __name__ == '__main__':
    main()


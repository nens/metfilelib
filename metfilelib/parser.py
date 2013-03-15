# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import datetime
import re

from metfilelib import metfile


def parse_metfile(file_object):
    # file_object has properties:
    # file_object.record_error(error_message, error_code)
    # file_object.line_number
    # file_object.filename
    # file_object.current_line  # Lookahead
    # file_object.next() # Goes to the next line
    # file_object.eof # True if end of file
    # file_object.success  # True if record_error() was never called

    if (not file_object.filename.lower().endswith(b".met")
        or not file_object.current_line.strip().startswith("<VERSIE>")):
        # File isn't a MET file
        return None

    version = parse_version(file_object)

    series = []
    while not file_object.eof:
        serie = parse_series(file_object)
        if serie is not None:
            series.append(serie)

    return metfile.MetFile(version=version, series=tuple(series))


def parse_version(file_object):
    l = file_object.current_line.strip()
    if l.startswith("<VERSIE>") and l.endswith("</VERSIE>"):
        version = l[len("<VERSIE>"):-len("</VERSIE>")]
    else:
        file_object.record_error(
            "Regel moet beginnen met <VERSIE> en eindigen met </VERSIE>",
            "VERSIE")
        version = "?"

    file_object.next()
    return version


def parse_series(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    seriesre = re.compile("<REEKS>(.*),(.*),</REEKS>")
    match = seriesre.match(l)
    if not match:
        file_object.record_error(
            "Verwachtte een correcte <REEKS>, vond {0}".format(l),
            "REEKS")
        file_object.next()
        return
    series_id = match.group(1)
    series_name = match.group(2)

    file_object.next()

    profiles = []
    while file_object.current_line.startswith("<PROFIEL>"):
        profile = parse_profile(file_object)
        if profile is not None:
            profiles.append(profile)

    if not profiles:
        file_object.record_error("Reeks zonder profielen", "NOPROFILES")

    return metfile.Series(
            line_number=line_number, id=series_id,
            name=series_name, profiles=tuple(profiles))


def parse_profile(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    profilere = re.compile("<PROFIEL>" + 10 * "(.*),")
    match = profilere.match(l)

    if not match:
        file_object.record_error(
            "Verwachtte een correct <PROFIEL>, vond {0}".format(l), "PROFIEL")
        return

    file_object.next()

    measurements = []
    while file_object.current_line.strip().startswith("<METING>"):
        meting = parse_meting(file_object)
        if meting is not None:
            measurements.append(meting)

    if file_object.current_line.strip() != "</PROFIEL>":
        file_object.record_error("Verwachtte </PROFIEL> tag.", "NO/PROFIEL")
    else:
        file_object.next()

    date_measurement = parse_date(match.group(3))
    if date_measurement is None:
        file_object.record_error(
            "Ongeldige JJJJMMDD datum: {0}".format(match.group(3)))
        return

    return metfile.Profile(
        line_number=line_number,
        id=match.group(1),
        description=match.group(2),
        date_measurement=date_measurement,
        level_value=match.group(4),
        level_type=match.group(5),
        coordinate_type=match.group(6),
        number_of_z_values=match.group(7),
        profile_type_placing=match.group(8),
        start_x=match.group(9),
        start_y=match.group(10),
        measurements=tuple(measurements))


def parse_meting(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    metingre = re.compile("<METING>" + 5 * "(.*)," + "(.*)</METING>")
    match = metingre.match(l)

    if not match:
        file_object.record_error(
            "Verwachtte een <METING> regel, vond {0}".format(l), "NOMETING")
        file_object.next()
        return

    file_object.next()

    return metfile.Measurement(
        line_number=line_number,
        profile_point_type=match.group(1),
        profile_point_drawing_code=match.group(2),
        x=match.group(3),
        y=match.group(4),
        z1=match.group(5),
        z2=match.group(6))


def parse_date(date_string):
    """Turn a YYYYMMDD string into a datetime.date object."""

    if len(date_string) != 8 or not date_string.isdigit():
        return None

    try:
        return datetime.date(int(date_string[:4]),
                         int(date_string[4:6]),
                         int(date_string[6:8]))
    except ValueError:
        return None

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
            "Versie regel moet beginnen met <VERSIE> en eindigen met </VERSIE>",
            "MET_NOVERSION")
        version = "?"

    file_object.next()
    return version


def parse_series(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    if not l.startswith("<REEKS>") or not l.endswith("</REEKS>"):
        file_object.record_error(
            "Reeks regel moet beginnen met <REEKS> en eindigen met </REEKS>",
            "MET_NOREEKS")

    seriesre = re.compile("<REEKS>(.*),(.*),</REEKS>")
    match = seriesre.match(l)
    if not match:
        file_object.record_error(
            "Reeks regel moet 2 door komma's gevolgde elementen bevatten",
            "MET_REEKSELEMENTS")
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
        file_object.record_error(
            "Reeks werd niet gevolgd door profielen",
            "MET_NOPROFILES")

    return metfile.Series(
            line_number=line_number, id=series_id,
            name=series_name, profiles=tuple(profiles))


def parse_profile(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    if not l.startswith("<PROFIEL>"):
        file_object.record_error(
            "Profiel regel moet beginnen met <PROFIEL>",
            "MET_NOPROFIEL")

    profilere = re.compile("<PROFIEL>" + 10 * "(.*),")
    match = profilere.match(l)

    if not match:
        file_object.record_error(
            "Profiel regel moet 10 door komma's gescheiden elementen bevatten",
            "MET_PROFIELELEMENTS")
        return

    try:
        number_of_z_values = int(match.group(7))
    except ValueError:
        file_object.record_error(
            "Aantal z waarden moet een geheel getal zijn.")
        number_of_z_values = 2

    file_object.next()

    measurements = []
    while file_object.current_line.strip().startswith("<METING>"):
        meting = parse_meting(file_object)
        if meting is not None:
            measurements.append(meting)

    if file_object.current_line.strip() != "</PROFIEL>":
        file_object.record_error(
            "Eerste regel na <METING> regels moet </PROFIEL> zijn",
            "MET_NOENDPROFIEL")
    else:
        file_object.next()

    date_measurement = parse_date(match.group(3))
    if date_measurement is None:
        file_object.record_error(
      "Ongeldige datum, niet in JJJJMMDD formaat: {0}".format(match.group(3)),
            "MET_WRONGDATE")
        return

    return metfile.Profile(
        line_number=line_number,
        id=match.group(1),
        description=match.group(2),
        date_measurement=date_measurement,
        level_value=match.group(4),
        level_type=match.group(5),
        coordinate_type=match.group(6),
        number_of_z_values=number_of_z_values,
        profile_type_placing=match.group(8),
        start_x=match.group(9),
        start_y=match.group(10),
        measurements=tuple(measurements))


def parse_meting(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    if not l.startswith("<METING>"):
        file_object.record_error("Regel moet beginnen met <METING>.")
        file_object.next()
        return
    if not l.endswith("</METING>"):
        file_object.record_error("Regel moet eindigen met </METING>.")
        file_object.next()
        return

    metingre = re.compile("<METING>(.*)</METING>")
    match = metingre.match(l)

    groups = match.group(1).split(",")
    if len(groups) != 6:
        file_object.record_error(
     "Een <METING> regel moet 6 met komma's gescheiden elementen bevatten")
        file_object.next()
        return

    try:
        z1 = float(groups[4])
    except ValueError:
        z1 = 0.0
        file_object.record_error("Z1 moet een decimaal getal zijn.")

    try:
        z2 = float(groups[5])
    except ValueError:
        z2 = 0.0
        file_object.record_error("Z2 moet een decimaal getal zijn.")

    file_object.next()

    return metfile.Measurement(
        line_number=line_number,
        profile_point_type=groups[0],
        profile_point_drawing_code=groups[1],
        x=groups[2],
        y=groups[3],
        z1=z1,
        z2=z2)


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

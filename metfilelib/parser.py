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


def skip_until_x_in_line(file_object, x):
    while not file_object.eof and x not in file_object.current_line.lower():
        file_object.next()


def parse_metfile(file_object):
    if not file_object.filename.lower().endswith(b".met"):
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
    if "versie" in l.lower():
        if l.startswith("<VERSIE>") and l.endswith("</VERSIE>"):
            version = l[len("<VERSIE>"):-len("</VERSIE>")]
            if version != '1.0':
                file_object.record_error(
                    "Versie moet 1.0 zijn.", "MET_WRONGVERSION")
                version = "?"
        else:
            file_object.record_error(
                "Versie regel moet beginnen met <VERSIE> en eindigen met </VERSIE>",
                "MET_NOVERSION")
            version = "?"
        file_object.next()
        return version
    else:
        file_object.record_error(
            "Geen versieregel gevonden.", "MET_NOVERSION")
        # If the line probably wasn't the VERSIE line (because it's
        # missing?), don't go to the next line.


def parse_series(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    match = None

    series_id = None
    series_name = None

    if "reeks" not in l.lower():
        file_object.record_error(
            "Verwachtte een <REEKS> regel.",
            "MET_REEKSNOTFOUND")
        file_object.next()
        return
    else:
        if not l.startswith("<REEKS>") or not l.endswith("</REEKS>"):
            file_object.record_error(
                "Reeks regel moet beginnen met <REEKS> en eindigen met </REEKS>",
                "MET_NOREEKS")
        else:
            seriesre = re.compile("<REEKS>([^<>,]*),([^<>,]*),</REEKS>")
            match = seriesre.match(l)

            if match:
                series_id = match.group(1)
                series_name = match.group(2)
            else:
                file_object.record_error(
                    "Reeks regel moet 2 door komma's gevolgde elementen bevatten",
                    "MET_REEKSELEMENTS")

                # Try to continue parsing without the second comma
                seriesre = re.compile("<REEKS>([^<>,]*),([^<>,]*)</REEKS>")
                match = seriesre.match(l)

        file_object.next()

    profiles = []

    while (not file_object.eof and
           not file_object.current_line.lower().startswith("<reeks")):
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

    profilere = re.compile("<PROFIEL>" + 10 * "([^<>,]*),")
    match = profilere.match(l)

    if not match:
        file_object.record_error(
            "Profiel regel moet 10 door komma's gescheiden elementen bevatten",
            "MET_PROFIELELEMENTS")
        skip_until_x_in_line(file_object, "</profiel>")
        file_object.next()
        return

    try:
        number_of_z_values = int(match.group(7))
    except ValueError:
        file_object.record_error(
            "Aantal z waarden moet een geheel getal zijn.",
            "MET_NUMZVALUES_INT")
        number_of_z_values = 2

    try:
        level_value = float(match.group(4))
    except ValueError:
        file_object.record_error(
            "Peilniveau moet een decimaal getal zijn, was {0}".
            format(match.group(4)),
            "MET_LEVELVALUEFLOAT")
        level_value = 0.0

    try:
        start_x = float(match.group(9))
    except ValueError:
        file_object.record_error(
            "X moet een decimaal getal zijn, was {0}".
            format(match.group(9)),
            "MET_STARTXFLOAT")
        start_x = 0

    try:
        start_y = float(match.group(10))
    except ValueError:
        file_object.record_error(
            "Y moet een decimaal getal zijn, was {0}".
            format(match.group(10)),
            "MET_STARTYFLOAT")
        start_y = 0

    date_measurement = parse_date(match.group(3))
    if date_measurement is None:
        file_object.record_error(
            "Ongeldige datum, niet in JJJJMMDD formaat: {0}".format(match.group(3)),
            "MET_WRONGDATE")

    file_object.next()

    measurements = []
    while "meting" in file_object.current_line.strip().lower():
        meting = parse_meting(file_object)
        if meting is not None:
            measurements.append(meting)

    if file_object.current_line.strip() != "</PROFIEL>":
        file_object.record_error(
            "Eerste regel na <METING> regels moet </PROFIEL> zijn",
            "MET_NOENDPROFIEL")
    else:
        file_object.next()

    return metfile.Profile(
        line_number=line_number,
        id=match.group(1),
        description=match.group(2),
        date_measurement=date_measurement,
        level_value=level_value,
        level_type=match.group(5),
        coordinate_type=match.group(6),
        number_of_z_values=number_of_z_values,
        profile_type_placing=match.group(8),
        start_x=start_x,
        start_y=start_y,
        measurements=tuple(measurements))


def parse_meting(file_object):
    l = file_object.current_line.strip()
    line_number = file_object.line_number

    if not l.startswith("<METING>"):
        file_object.record_error(
            "Regel moet beginnen met <METING>.",
            "MET_METINGLINEWRONG")
        file_object.next()
        return
    if not l.endswith("</METING>"):
        file_object.record_error(
            "Regel moet eindigen met </METING>.",
            "MET_METINGLINEWRONG")
        file_object.next()
        return

    metingre = re.compile("<METING>([\d\s.,-]*)</METING>")
    match = metingre.match(l)

    try:
        groups = match.group(1).split(",")
    except AttributeError:
        file_object.record_error(
            "Een <METING> object bevat invalide tekens.",
            "MET_METINGSIXVALUES")
        file_object.next()
        return

    if len(groups) == 7 and not groups[6]:
        # There are 7, but the last one is empty (extra comma):
        # just remove it, because apparently that's sometimes treated as
        # the right way to do it
        groups = groups[:6]

    if len(groups) != 6:
        file_object.record_error(
            "Een <METING> regel moet 6 met komma's gescheiden elementen bevatten",
            "MET_METINGSIXVALUES")
        file_object.next()
        return

    try:
        z1 = float(groups[4])
    except ValueError:
        z1 = 0.0
        file_object.record_error(
            "Z1 moet een decimaal getal zijn.",
            "MET_Z1FLOAT")

    try:
        z2 = float(groups[5])
    except ValueError:
        z2 = 0.0
        file_object.record_error(
            "Z2 moet een decimaal getal zijn.",
            "MET_Z2FLOAT")

    try:
        x = float(groups[2])
    except ValueError:
        x = 0.0
        file_object.record_error(
            "X moet een decimaal getal zijn.",
            "MET_XFLOAT")

    try:
        y = float(groups[3])
    except ValueError:
        y = 0.0
        file_object.record_error(
            "Y moet een decimaal getal zijn.",
            "MET_YFLOAT")

    profile_point_type = groups[0]
    profile_drawing_code = groups[1]

    if (profile_point_type
            not in metfile.Measurement.ALLOWED_PROFILE_POINT_TYPES):
        file_object.record_error(
            "Onbekende profielpunttype {0}".format(profile_point_type),
            "MET_UNKNOWN_PROFILE_POINT_TYPE")

    if (profile_drawing_code
            not in metfile.Measurement.ALLOWED_DRAWING_CODES):
        file_object.record_error(
            "Onbekende profieltekencode {0}".format(profile_drawing_code),
            "MET_UNKNOWN_PROFILE_DRAWING_CODE")

    file_object.next()

    return metfile.Measurement(
        line_number=line_number,
        profile_point_type=profile_point_type,
        profile_point_drawing_code=profile_drawing_code,
        x=x,
        y=y,
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

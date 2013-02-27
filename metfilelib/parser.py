# Python 3 is coming to town
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

from metfilelib import metfile

import re


def parse_metfile(file_object):
    # file_object has properties:
    # file_object.make_error(error_message)  # Stores errors somewhere
    # file_object.line_number
    # file_object.filename
    # file_object.current_line  # Lookahead
    # file_object.next() # Goes to the next line
    # file_object.eof # True if end of file
    # file_object.success  # True if make_error() was never called

    if (not file_object.filename.lower().endswith(b".met")
        or not file_object.current_line.strip().startswith("<VERSIE>")):
        # File isn't a MET file
        return None

    version = parse_version(file_object)

    series = []
    while not file_object.eof:
        series.append(parse_series(file_object))

    return metfile.MetFile(version=version, series=tuple(series))


def parse_version(file_object):
    l = file_object.current_line.strip()
    if l.startswith("<VERSIE>") and l.endswith("</VERSIE>"):
        version = l[len("<VERSIE>"):-len("</VERSIE>")]
    else:
        file_object.make_error(
            "Regel moet beginnen met <VERSIE> en eindigen met </VERSIE>")
        version = "?"

    file_object.next()
    return version


def parse_series(file_object):
    l = file_object.current_line.strip()
    file_object.next()

    seriesre = re.compile("<REEKS>(.*),(.*),</REEKS>")
    match = seriesre.match(l)
    if not match:
        file_object.make_error(
            "Verwachtte een correcte <REEKS>, vond {0}".format(l))
        return

    series_id = match.group(1)
    series_name = match.group(2)

    profiles = []
    while file_object.current_line.startswith("<PROFIEL>"):
        profiles.append(parse_profile(file_object))

    if not profiles:
        file_object.make_error("Reeks zonder profielen")

    return metfile.Series(
            id=series_id, name=series_name, profiles=tuple(profiles))


def parse_profile(file_object):
    l = file_object.current_line.strip()
    file_object.next()

    profilere = re.compile("<PROFIEL>" + 10 * "(.*),")
    match = profilere.match(l)

    if not match:
        file_object.make_error(
            "Verwachtte een correct <PROFIEL>, vond {0}".format(l))
        return

    measurements = []
    while file_object.current_line.strip().startswith("<METING>"):
        measurements.append(parse_meting(file_object))

    if file_object.current_line.strip() != "</PROFIEL>":
        file_object.make_error("Verwachtte </PROFIEL> tag.")
    else:
        file_object.next()

    return metfile.Profile(
        id=match.group(1),
        description=match.group(2),
        date_measurement=match.group(3),
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
    file_object.next()

    metingre = re.compile("<METING>" + 5 * "(.*)," + "(.*)</METING>")
    match = metingre.match(l)

    if not match:
        file_object.make_error(
            "Verwachtte een <METING> regel, vond {0}".format(l))
        return

    return metfile.Measurement(
        profile_point_type=match.group(1),
        profile_point_drawing_code=match.group(2),
        x=match.group(3),
        y=match.group(4),
        z1=match.group(5),
        z2=match.group(6))

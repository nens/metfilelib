"""Helper function that gets a given profiel from a MET file."""

from metfilelib import metfile
from metfilelib import parser
from metfilelib.util import file_reader


def retrieve(metfile, profile_id):
    """Return the given profile_id from the metfile found at path
    'metfile', and information on the series it was in, in the format
    of a 3 element tuple:

    (series_id, series_name, profile_object)
    """

    met = parser.parse_metfile(file_reader.FileReader(
            metfile, skip_empty_lines=True))

    for series in met.series:
        for profile in series.profiles:
            if profile.id == profile_id:
                return series.id, series.name, profile


def recreate_metfile(profile_list):
    """Return a MetFile object created by retrieving profiles and
    combining them.

    Profile_list is a list of metfile_path, profile_id tuples."""

    profiles = [
        retrieve(metfile_path, profile_id)
        for metfile_path, profile_id in profile_list
        ]

    profiles = [profile for profile in profiles if profile is not None]

    series = dict()
    for series_id, series_name, profile in profiles:
        if series_id in series:
            series[series_id]['profiles'].append(profile)
        else:
            series[series_id] = {
                'profiles': [profile],
                'series_name': series_name
                }

    series_list = []
    for series_id in sorted(series):
        series_list.append(metfile.Series(
                line_number=None,
                id=series_id,
                name=series[series_id]['series_name'],
                profiles=tuple(series[series_id]['profiles'])))

    return metfile.MetFile(version="1.0", series=tuple(series_list))

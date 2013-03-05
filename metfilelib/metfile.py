"""Python classes that represent the data in a .met file."""

from collections import namedtuple

MetFile = namedtuple('MetFile', 'version, series')

Series = namedtuple('Series', 'line_number, id, name, profiles')

Profile = namedtuple(
    'Profile',
    '''line_number, id, description, date_measurement, level_value, level_type,
    coordinate_type, number_of_z_values, profile_type_placing,
    start_x, start_y, measurements''')

Measurement = namedtuple(
    'Measurement',
    'line_number, profile_point_type, profile_point_drawing_code, x, y, z1, z2'
    )

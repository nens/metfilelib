"""Python classes that represent the data in a .met file."""


class MetFile(object):
    def __init__(self):
        self.version = None
        self.series = []  # Reeksen


class Series(object):
    # Contains one or more Profiles
    pass


class Profile(object):
    pass


class Measurement(object):
    def __init__(self):


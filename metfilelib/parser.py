from metfilelib import metfile


def parse_metfile(file_object):
    # file_object has properties:
    # file_object.make_error(error_message)  # Stores errors somewhere
    # file_object.line_number
    # file_object.filename
    # file_object.current_line  # Lookahead
    # file_object.next() # Goes to the next line
    # file_object.eof # True if end of file
    # file_object.success  # True if make_error() was never called

    metfile_instance = metfile.MetFile()

    if (not file_object.filename.lower().endswith(".met")
        or metfile_instance.current_line.strip() != "<VERSION>1.0</VERSION>"):
        # File isn't a MET file
        return None

    metfile_instance.version = "1.0"

    while not file_object.eof:
        metfile_instance.series.append(parse_reeks(file_object))

    return metfile_instance



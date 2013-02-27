"""Command that reads in a MET-file and either prints errors (if there
are any), or prints the MET file."""

import argparse
import os

from metfilelib.util.file_reader import FileReader
from metfilelib.parser import parse_metfile
from metfilelib.exporters import MetfileExporter


def main():
    parser = argparse.ArgumentParser(
 description="Read a MET file, and print errors or a copy of the MET file.")
    parser.add_argument("filename")

    filename = parser.parse_args().filename

    if not os.path.exists(filename) or not os.path.isfile(filename):
        print "File does not exist: {0}.".format(filename)
    elif not filename.endswith(".met"):
        print "File is not a .met file: {0}.".format(filename)
    else:
        file_reader = FileReader(filename, skip_empty_lines=True)
        metfile = parse_metfile(file_reader)
        if not file_reader.success:
            print "Errors."
        elif metfile is None:
            print "Apparently the MET parser decided this was not a MET file."
        else:
            exporter = MetfileExporter()
            print exporter.export_metfile(metfile)

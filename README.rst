metfilelib
==========================================

This is a library for working with MET files as read by IRIS.

A MET file is represented by the metfilelib.metfile.MetFile
class. Class instances are immutable.

To read in a MET file, use the metfilelib.parser.parse_metfile()
function.  The file_object argument can be created using
metfilelib.util.file_read.FileReader. By default, errors go to stderr,
but you can pass your own error handler to the FileReader.

To write a MET file, use metfilelib.exporters.MetfileExporter.

Changelog of metfilelib
===================================================


0.5 (unreleased)
----------------

- Nothing changed yet.


0.4 (2013-03-21)
----------------

- Check on version number 1.0.

- Try to continue parsing if the second comma in a <REEKS> element is
  missing.

- Fix some bugs in parsing

- Added tools that retrieve some profile from a MET file, and can recreate
  an entire MetFile object from such retrieved profiles

- Added tools for projection X, Y points from measurements, projecting them on
  a base line, and sorting measurements based on their projection on the line.


0.3 (2013-03-19)
----------------

- Translate coordinates to floats.

- Add tests.


0.2 (2013-03-15)
----------------

- Increased the number of error messages. Only error messages to do
  with the correctness of the file are given, checking that the
  content is up to some spec is left to client code.

- See error_codes.rst in the docs/ dir for a list of error codes.


0.1 (2013-03-05)
----------------

- Initial project structure created with nensskel 1.31.dev0.

- Added a util.file_reader.FileReader class that will probably be used
  by the site, or some object with the same API. The metfile parser
  should assume it gets instances of this class.

- Developed metfile.py, parser.parse_metfile and
  exporters.MetfileExporter to the point where a correct MET file can
  be read in and printed out.

- Developed a bit further so that a file can be uploaded now, but still
  definitely work in progress.

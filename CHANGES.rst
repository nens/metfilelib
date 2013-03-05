Changelog of metfilelib
===================================================


0.1 (unreleased)
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

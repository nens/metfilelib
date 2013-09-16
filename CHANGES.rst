Changelog of metfilelib
===================================================


0.13 (unreleased)
-----------------

- Add missing drawing point code '47'.


0.12 (2013-05-07)
-----------------

- Moved DXF generation from lizard_progress to here.


0.11 (2013-04-23)
-----------------

- Added a helper function to linear_algebra that calculates the
  distance of a point to a line.

- Measurement.point now returns None if something is wrong with one of
  the coordinates.


0.10 (2013-04-22)
-----------------

- Fixes bug with infinite loop in case of wrong date format.


0.9 (2013-04-16)
----------------

- Fixed bug where date format error message was shown on the wrong
  line (lizard-progress #66).

- Added test for #69, but it's working correctly. Perhaps an old
  version?

- Export to MET file used a wrong date format, fixed.


0.8 (2013-04-05)
----------------

- Add lists of all the existing profile point codes and drawing codes,
  check for them.


0.7 (2013-03-29)
----------------

- Make it possible to generate a MET file that sorts its measurements
  based on the projection on the base line.


0.6 (2013-03-27)
----------------

- Add a waterlevel property to Profile, that checks the z1/z2 values at the
  22 profile point codes.

- Improved error handling, we got infinite loops in some cases, avoid them.

- Line now has midpoint and length properties.

- Line has a function distance_to_midpoint, which projects points on the line then
  checks how far from the midpoint it is, with the side of the start point getting
  negative numbers. Useful as X values on plots.

0.5 (2013-03-22)
----------------

- Add version codes for all parser errors.

- Add a method distance() to Point that calculates distance to another
  point.


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

Error codes returned by the metfile parser:

MET_NOVERSION - No <VERSIE> or </VERSIE> on the first line
MET_NOREEKS - A 'reeks' line doesn't start with <REEKS> or end with </REEKS>
MET_REEKSELEMENTS - Reeks line did not have 2 elements
MET_NOPROFILES - There were no Profile lines after the reeks
MET_NOPROFIEL - Profiel line did not start with <PROFIEL> (actually it is likely that the previous error is shown in that case)
MET_PROFIELELEMENTS - Number of elements of the profiel line was not 10
MET_NOENDPROFIEL - There was no </PROFIEL> line after the measurements
MET_WRONGDATE - Measurement date was not in YYYYMMDD format


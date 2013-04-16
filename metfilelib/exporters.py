"""Functions to export MET file objects to other formats."""


class MetfileExporter(object):
    def __init__(self, want_sorted_measurements=False, line_ending="\r\n"):
        self.want_sorted_measurements = want_sorted_measurements
        self._line_ending = line_ending

    def export_metfile(self, metfile):
        s = "<VERSIE>{0}</VERSIE>\n".format(metfile.version)

        for series in metfile.series:
            s += self.export_series(series)

        return s.replace("\n", self._line_ending)

    def export_series(self, series):
        s = "<REEKS>{series_id},{series_name},</REEKS>\n".format(
            series_id=series.id, series_name=series.name)

        for profile in series.profiles:
            s += self.export_profile(profile)

        return s

    def export_profile(self, profile):
        measurements = (
            profile.sorted_measurements if self.want_sorted_measurements
            else profile.measurements)

        s = ("<PROFIEL>{profiel_id},{description},{date:%Y%m%d},{level_value},"
             "{level_type},{coordinate_type},{number_of_z_values},"
             "{profile_type_placing},{start_x},{start_y},\n").format(
            profiel_id=profile.id,
            description=profile.description,
            date=profile.date_measurement,
            level_value=profile.level_value,
            level_type=profile.level_type,
            coordinate_type=profile.coordinate_type,
            number_of_z_values=profile.number_of_z_values,
            profile_type_placing=profile.profile_type_placing,
            start_x=profile.start_x,
            start_y=profile.start_y)

        for measurement in measurements:
            s += self.export_measurement(measurement)

        s += "</PROFIEL>\n"

        return s

    def export_measurement(self, measurement):
        return ("<METING>{profile_point_type},{profile_point_drawing_code},"
                "{x},{y},{z1},{z2}</METING>\n").format(
            profile_point_type=measurement.profile_point_type,
            profile_point_drawing_code=measurement.profile_point_drawing_code,
            x=measurement.x,
            y=measurement.y,
            z1=measurement.z1,
            z2=measurement.z2)

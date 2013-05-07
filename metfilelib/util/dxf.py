# Save a dwarsprofiel as DXF

from dxfwrite import DXFEngine as dxf


def draw_z(drawing, line, measurement):
    x = line.distance_to_midpoint(measurement.point)
    y = measurement.z1 - 0.2

    text = "({x:.2f}, z1={y:.2f})".format(x=x, y=measurement.z1)

    drawing.add(dxf.text(
            text,
            insert=(x, y),
            height=0.1))


def save_as_dxf(profile, dxf_path):
    """Save the profile in DXF format, with filename dxf_path. Return
    success"""
    line = profile.line
    if line is None:
        # No base line. Skip!
        return False
    midpoint = line.midpoint

    leftmost = profile.sorted_measurements[0]

    drawing = dxf.drawing(dxf_path)

    measurements = profile.sorted_measurements

    x = line.distance_to_midpoint(leftmost.point)

    # Draw location code to the left of the profile, 1m above the
    # highest z1/z2 there
    drawing.add(dxf.text(
            '{location_code} ({x}, {y}) {date}'.format(
                location_code=profile.id,
                x=midpoint.x,
                y=midpoint.y,
                date=profile.date_measurement),
            insert=(x, max([leftmost.z1, leftmost.z2]) + 1),
            height=0.4))  # 40cm high

    previous = None
    previous_z1 = None
    previous_z2 = None
    previous_x = None
    for m in measurements:
        projected_m = line.project(m.point)

        draw_z(drawing, line, m)

        if previous is not None:
            # Add distance between previous and this one to x
            # projected on the line
            p_m = line.project(m.point)
            x += p_m.distance(previous)

            drawing.add(dxf.line((previous_x, previous_z1),
                                 (x, m.z1)))
            drawing.add(dxf.line((previous_x, previous_z2),
                                 (x, m.z2)))

        previous = projected_m
        previous_z1 = m.z1
        previous_z2 = m.z2
        previous_x = x

    # Draw water line
    waterlevel = profile.waterlevel
    if waterlevel is not None:
        drawing.add(dxf.line(
                (-line.start.distance(line.midpoint), waterlevel),
                (line.end.distance(line.midpoint), waterlevel)))

    drawing.save()
    return True

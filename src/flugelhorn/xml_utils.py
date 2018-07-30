"""XML utilities for Stitching Automations."""

import xml.etree.ElementTree as ET


def convert_to_xml(obj, tag_name=None):
    """Convert a Python settings object to xml.

    This includes type convert to strings, removing bools, ints and floats.

    Args:
        obj: Python object that contains properties and tag information
        tag_name: Alternate name to be used for the tag.
                If tag name is None, then the name attached to the original
                object will be used.
    """
    # TODO(ryan): A more sophisticated framework is to allow nested objects
    # And to converts these nested objects to XML subelements via recursion.
    # For simplicity, this is not currently supported, but may make sense
    # to support in the future

    attribs = {}
    for key, value in obj.to_dict().items():
        if type(value) in [int, float, str, bool]:
            attribs[key] = _convert_to_str(value)
    # attribs = {key: _convert_to_str(value) for key, value in obj.to_dict().items()}
    if not tag_name:
        tag_name = obj.tag
    elem = ET.Element(tag_name, attribs)

    return elem


def _convert_to_str(value):
    """Ensure that a value is converted to a string.

    This ensure proper XML build.
    """
    if type(value) in [int, float]:
        return str(value)
    elif type(value) == bool:
        return str(int(value))
    return value


def build_config_xml(config, stitch_source):
    """Build a configuration XML from a validated config dict."""
    # Build root element and tree
    root = ET.Element('stitchParam')
    tree = ET.ElementTree(root)

    inputs = convert_to_xml(config.input)

    # root.append(convert_to_xml(config['input']))

    # inputs = ET.SubElement(root, 'input', config['input'].to_dict())

    video_groups = build_video_groups(stitch_source)

    for vid_grp in video_groups:
        ET.dump(vid_grp)
        inputs.append(vid_grp)
    root.append(inputs)

    blend = build_blend_settings(config)
    root.append(blend)

    # Add preference
    pref = build_preference(config)
    root.append(pref)

    # Add gyro
    gyro = build_gyro(config)
    root.append(gyro)

    # Add color, depthMap and output
    root.append(convert_to_xml(config.color))
    root.append(convert_to_xml(config.depthMap))
    root.append(build_output(config))

    return tree


def build_blend_settings(config):
    """Build a blend setting XML element."""
    blend = convert_to_xml(config.blend)
    blend.append(convert_to_xml(config.blend.calibration, 'calibration'))

    return blend


def build_preference(config):
    """Build a preference XML element."""
    pref = ET.Element('preference', {})

    pref.append(convert_to_xml(config.preference.encode))
    pref.append(convert_to_xml(config.preference.decode))
    pref.append(convert_to_xml(config.preference.blender))

    return pref


def build_gyro(config):
    """Build a gyro XML element."""
    # Root gyro element
    gyro_attribs = {'version': _convert_to_str(config.gyro.version),
                    'type': _convert_to_str(config.gyro.type),
                    'enable': _convert_to_str(config.gyro.enable),
                    'filter': _convert_to_str(config.gyro.filter)}
    gyro = ET.Element('gyro', gyro_attribs)

    # Add timeOffset
    time_offset = ET.Element('timeOffset')
    time_offset.text = config.gyro.timeOffset
    gyro.append(time_offset)

    # Add files
    files = ET.Element('files')
    f = ET.Element('file')
    f.text = config.gyro.filename
    files.append(f)
    gyro.append(files)

    # Calibration and angle elements
    gyro.append(convert_to_xml(config.gyro_calibration, 'calibration'))
    gyro.append(convert_to_xml(config.gyro_angle, 'angle'))

    return gyro


def build_output(config):
    """Build an output XML element."""
    output = convert_to_xml(config.output)
    output.append(convert_to_xml(config.video))
    output.append(convert_to_xml(config.audio))

    return output


def build_video_groups(stitch_source):
    """Build a list of video group XML element from a stitch source.
    Args:
        stitch_source: StitchSource object
    """
    video_groups = []
    for group in stitch_source.media:
        print(group)
        video_group_attrib = {
            'ptsOffset': '%0.3f' % group['ptsOffset'],
            'enable': '1'}
        video_group = ET.Element('videoGroup', video_group_attrib)

        # Add trim data
        ET.SubElement(video_group, 'trim', {'start': '%0.3f' % group['start'],
                                            'end': '%0.3f' % group['end']})

        # Add file data
        for n in range(6):
            ET.SubElement(video_group, 'file', {'src': group[n]})

        video_groups.append(video_group)

    return video_groups


def parse_proj_xml(path):
    """Parse a proj xml file and return a dict."""
    proj_dict = {}
    raw_xml = ET.parse(path)

    # Add file groups (to be later used as videoGroups
    filegroups = []
    for x in raw_xml.getiterator('filegroup'):
        files = [f.text for f in x]
        filegroups.append(files)
    proj_dict['file_groups'] = filegroups

    # Add gyro calibration
    proj_dict['gyro_version'] = raw_xml.find('gyro').attrib['version']
    proj_dict['gravity_x'] = raw_xml.find('./gyro/calibration/gravity_x').text
    proj_dict['gravity_y'] = raw_xml.find('./gyro/calibration/gravity_y').text
    proj_dict['gravity_z'] = raw_xml.find('./gyro/calibration/gravity_z').text
    proj_dict['timeOffset'] = raw_xml.find('./gyro/start_ts').text

    return proj_dict


def write_config_xml(config, stitch_source, save_path):
    """Build and write a config xml file to disk.

    """
    config_xml = build_config_xml(config, stitch_source)
    config_xml.write(save_path)

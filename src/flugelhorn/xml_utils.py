"""XML utilities for Stitching Automations."""

from collections import namedtuple
import xml.etree.ElementTree as ET 

from stitcher_preferences import create_stitcher_config


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
    else:
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


if __name__ == '__main__':

    test_vid_paths = [
        '/path_to/video/origin_0.mp4',
        '/path_to/video/origin_1.mp4',
        '/path_to/video/origin_2.mp4',
        '/path_to/video/origin_3.mp4',
        '/path_to/video/origin_4.mp4',
        '/path_to/video/origin_5.mp4']

    all_settings = {
        'input': {
            'type': 'video',
            'lensCount': 6,
            'fileCount': 1
        }, 
        'blend': {
            'useOpticalFlow': True,
            'useNewOpticalFlow': True,
            'mode': '?????',
            'samplingLevel': 'fast',
            'useTopFixer': False
        },
        'blend_calibration': {
            'lensVersion': 7,
            'lensType': 12,
            'captureTime': '?????',
            'captureTimeIndex': '?????',
            'useDefaultCircle': True,
            'useDefaultOffset': True
        },
        # Check local hardware setting
        'encode': {
            'useHardware': True,
            'threads': 1,
            'preset': 'superfast',
            'profile': 'baseline'
        },
        'decode': {
            'useHardware': True,
            'threads': 1,
            'count': 1
        },
        'blender': {
            'type': 'auto'
        },
        'gyro': {
            'version': 3,
            'type': 'pro',
            'enable': True,
            'filter': 'akf'
        },
        'gyro_calibration': {
            'gravity_x': 0.0008186848958333335,
            'gravity_y': -0.00043326822916666665,
            'gravity_z': 0.9980732421875
        },
        'gyro_angle': {
            'diff_pan': 0,
            'diff_tilt': 0,
            'diff_roll': 0,
            'distance': 603.3333333333334
        },
        'color': {
            'brightness': 0,
            'contrast':0,
            'highlight': 0,
            'shadow': 0,
            'saturation': 0,
            'tempture': 0,
            'tint': 0,
            'sharpness': 0 
        },
        'depthMap': {
            'enable': False,
            'path': '',
            'inverse': True
        },
        'output': {
            'width': 3840,
            'height':1920,
            'dst': '~/stitchertest/test.mp4',
            'type': 'video'
        },
        'video': {
            'fps': 29.97,
            'codec': 'h264',
            # TODO(ryan): This should be calculated?
            'bitrate': 62914560,
            'useInterpolation': False
        },
        'audio': {
            'type': 'pano',
            'device': 'insta360'
            }
    }

    test_proj = '/Users/ryan/Projects/test_videos/new_source/VID_2018_07_13_00_04_31/pro.prj'
    proj_dict = parse_proj_xml(test_proj)

    # config = create_stitcher_config(all_settings)

    # inputs = ET.SubElement(root, 'input', config['input'].to_dict())
    # test = convert_to_xml(config['input'])
    # test = build_config_xml(test_vid_paths, config)

    # blend_attrib = {
    #     'useOpticalFlow': '1',
    #     'useNewOpticalFlow': '1',
    #     'mode': 'pano',
    #     'samplingLevel': 'fast',
    #     'useTopFixer': '0'}
    # x = dict_to_xml(blend_attrib) 
    

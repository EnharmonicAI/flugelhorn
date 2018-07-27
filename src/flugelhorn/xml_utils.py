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
    # attribs = {}
    # for key, value in obj.to_dict().items():
    #     if typ

    # This works for single level objects, but not nested
    attribs = {key: _convert_to_str(value) for key, value in obj.to_dict().items()}
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


def build_config_xml(video_file_paths, config):
    """Build a configuration XML from a validated config dict."""
    # Build root element and tree
    root = ET.Element('stitchParam')
    tree = ET.ElementTree(root)

    # # Add inputs
    # input_attrib = {
    #     'type': 'video',
    #     'lensCount': '6',
    #     'fileCount': '1'}

    inputs = convert_to_xml(config['input'])

    # root.append(convert_to_xml(config['input'])) 
    
    # inputs = ET.SubElement(root, 'input', config['input'].to_dict())

    #TODO(ryan): supports single video group only for now
    video_group = build_video_group(video_file_paths)

    inputs.append(video_group)    
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
    root.append(convert_to_xml(config['color']))
    root.append(convert_to_xml(config['depthMap']))
    root.append(build_output(config))    
    

    return tree


def build_blend_settings(config):
    """Build a blend setting XML element."""
    blend = convert_to_xml(config['blend'])
    blend.append(convert_to_xml(config['blend_calibration'], 'calibration'))

    return blend


def build_preference(config):
    """Build a preference XML element."""
    pref = ET.Element('preference', {})

    pref.append(convert_to_xml(config['encode']))
    pref.append(convert_to_xml(config['decode']))
    pref.append(convert_to_xml(config['blender']))
     
    return pref 


def build_gyro(config):
    """Build a gyro XML element."""
    gyro = convert_to_xml(config['gyro'])
    # TODO(ryan): Add Gyro files and timeOffset

    gyro.append(convert_to_xml(config['gyro_calibration'], 'calibration'))
    gyro.append(convert_to_xml(config['gyro_angle'], 'angle'))

    return gyro


def build_output(config):
    """Build an output XML element."""
    output = convert_to_xml(config['output'])
    output.append(convert_to_xml(config['video']))
    output.append(convert_to_xml(config['audio']))

    return output


def build_video_group(video_file_paths):
    """Build a video group XML element from a list of video files.
    Args:
        video_file_paths: list of video_file paths
    """
    video_group_attrib = {
        'ptsOffset': '0',
        'enable': '1'}
    video_group = ET.Element('videoGroup', video_group_attrib)

    # Add trim data
    ET.SubElement(video_group, 'trim', {'start': '0', 'end': '5'})
   
    # Add file data
    for path in video_file_paths:
        ET.SubElement(video_group, 'file', {'src': path}) 

    return video_group




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

    config = create_stitcher_config(all_settings)

    # inputs = ET.SubElement(root, 'input', config['input'].to_dict())
    # test = convert_to_xml(config['input'])
    test = build_config_xml(test_vid_paths, config)

    # blend_attrib = {
    #     'useOpticalFlow': '1',
    #     'useNewOpticalFlow': '1',
    #     'mode': 'pano',
    #     'samplingLevel': 'fast',
    #     'useTopFixer': '0'}
    # x = dict_to_xml(blend_attrib) 
    

"""Setting definitions for Insta360 Pro Stitching automation."""

from collections import namedtuple

PropertyDef = namedtuple('PropertyDef', 'allowed default')

# The allowed values for these settings was discovered by investigating the files
# written by the Stitcher GUI
# On Windows, these can be found C:\Users\username\AppData\Local\Temp\flaF59D.tmp (etc)
SETTING_DEFINITIONS= {
    'input': {
        'type': PropertyDef(['image', 'video'], 'video'),
        'lensCount': PropertyDef([6], 6),
        'fileCount': PropertyDef(None, 1)
    }, 
    'blend': {
        'useOpticalFlow': PropertyDef([True, False], True),
        'useNewOpticalFlow': PropertyDef([True, False], True),
        'mode': PropertyDef(['pano', 'stereo_top_left', 'stereo_top_right',
                             'stereo_separate'], 'pano'),
        'samplingLevel': PropertyDef(['slow', 'medium', 'fast'], 'fast'),
        'useTopFixer': PropertyDef([True, False], False),
        'calibration': {
            'lensVersion': PropertyDef(None, 7),
            'lensType': PropertyDef(None, 12),
            'captureTime': PropertyDef(None, None),
            'captureTimeIndex': PropertyDef(None, None),
            'useDefaultCircle': PropertyDef([True, False], True),
            'useDefaultOffset': PropertyDef([True, False], True)
        },
    },
    'preference': {
        'encode': {
            'useHardware': PropertyDef([True, False], False),
            'threads': PropertyDef(None, 1),
            'preset': PropertyDef(['superfast', 'veryfast', 'faster', 'fast', 'medium'],
                                  'superfast'),
            'profile': PropertyDef(['baseline', 'main', 'high'], 'baseline')
        },
        'decode': {
            'useHardware': PropertyDef([True, False], False),
            'threads': PropertyDef(None, 1),
            'count': PropertyDef(None, 1)
        },
        'blender': {
            'type': PropertyDef(['auto', 'cuda', 'opencl', 'cpu'], 'auto')
        }
    },
    'gyro': {
        'version': PropertyDef([1, 2, 3], 2),
        'type': PropertyDef(['pro'], 'pro'),
        'enable': PropertyDef([True, False], True),
        'filter': PropertyDef(['akf'], 'akf'),
        'timeOffset': PropertyDef(None, None),
        'filename': PropertyDef(None, None)
    },
    'gyro_calibration': {
        'gravity_x': PropertyDef(None, None),
        'gravity_y': PropertyDef(None, None),
        'gravity_z': PropertyDef(None, None)
    },
    'gyro_angle': {
        'diff_pan': PropertyDef(None, 0),
        'diff_tilt': PropertyDef(None, 0),
        'diff_roll': PropertyDef(None, 0),
        'distance': PropertyDef(None, 603.3333333333334)
    },
    'color': {
        'brightness': PropertyDef(None, None),
        'contrast': PropertyDef(None, None),
        'highlight': PropertyDef(None, None),
        'shadow': PropertyDef(None, None),
        'saturation': PropertyDef(None, None),
        'tempture': PropertyDef(None, None),
        'tint': PropertyDef(None, None),
        'sharpness': PropertyDef(None, None)
    },
    'depthMap': {
        'enable': PropertyDef([True, False], False),
        'path': PropertyDef(None, ''),
        'inverse': PropertyDef([True, False], True)
    },
    'output': {
        'width': PropertyDef([2560, 3840, 5120, 6400, 7680], 3840),
        'height': PropertyDef([1280, 1920, 2560, 3200, 3840], 1920),
        'dst': PropertyDef(None, None),
        'type': PropertyDef(['video'], 'video')
    },
    'video': {
        'fps': PropertyDef([1, 5, 23.98, 24, 25, 29.97, 30, 60], 29.97),
        'codec': PropertyDef(['h264', 'h265'], 'h264'),
        # TODO(ryan): This should be calculated?
        'bitrate': PropertyDef(None, 62914560),
        'useInterpolation': PropertyDef([True, False], False) 
    },
    'audio': {
        'type': PropertyDef(['pano', 'normal', 'none'], 'pano'),
        'device': PropertyDef(['insta360', ''], 'insta360')
    }
}



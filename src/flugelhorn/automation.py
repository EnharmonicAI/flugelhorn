"""Simple 360 Video Processing Automation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil

from absl import app
from absl import flags

flags.DEFINE_string(
    'source', None,
    'Source path to recursively search for image and video files for stitching.'
    'This will likely be an SD card or the storage device used by the camera.')
flags.DEFINE_string(
    'raw', None,
    'Destination path for files to be copied.'
    'This will probably be a local HDD or SSD.')
flags.DEFINE_string(
    'stitched', None,
    'Base path for stitched files.')
flags.DEFINE_string(
    'settings', None,
    'Path to a yaml file defining your stitching and encoding settings.'
    'This can be one of the Flugelhorn-included yaml files or a custom user'
    'defined settings file.')

FLAGS = flags.FLAGS

def check_paths(paths):
    """Check that all supplied paths are directories."""
    for p in paths:
        if not os.path.isdir(p):
            raise NotADirectoryError('%s is not a directory.' % p)


def find_video_image_dirs(path):
    """Scan a directory and return lists of video and image dirs for processing."""
    source_video_dirs = []
    source_image_dirs = []
    for entry in os.scandir(path):
        if entry.is_dir():
            # todo(ryan): divide by video and images
            # print(entry.path)
            # print(entry.name)
            source_video_dirs.append((entry.path, entry.name)) 
    
    print('{0} video directories, {1} images directories found.'.format(
        len(source_video_dirs), len(source_image_dirs)))

    return source_video_dirs, source_image_dirs
    

def copy_source_to_raw_dirs(source_dirs, dest_base):
    for d in source_dirs:
        dest_path = os.path.join(dest_base, d[1])
        print('Copying {0} to {1}.'.format(d[0], dest_path))
        shutil.copytree(d[0], dest_path) 
        
    # TODO(ryan): return list of new raw dir paths


def build_stitching_settings(base_settings, raw_dirs, stitched_dir):
    """Build stitching settings."""

    # Assume VIDEO for now 
    # TODO(ryan):
    # fileCount should be defined by looking at directories
    base_settings = {
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
            'version': 3, # Version from pro.prj file
            'type': 'pro', 
            'enable': True,
            'filter': 'akf'
        },
        # Add timeOffset tag, based on start_ts from pro.pj XML file
        # Add files tag, w/ path to desired gyro.dat file in our image folder
        'gyro_calibration': {
            # These values fcome from pro.pj XML file
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



def main(argv):
    if not FLAGS.source:
        print('Error: Source path must be supplied (--source).')
        return
    if not FLAGS.raw:
        print('Error: Raw destination path must be supplied (--raw).')
        return
    if not FLAGS.stitched:
        print('Error: Stitched path must be supplied (--stitched).')
        return
    source_dir = os.path.abspath(FLAGS.source)
    raw_dir = os.path.abspath(FLAGS.raw)
    stitched_dir = os.path.abspath(FLAGS.stitched)
    
    # Check that all paths are directories
    try:
        check_paths([source_dir, raw_dir, stitched_dir])
    except NotADirectoryError as e:
        print(e) 

    print('Searching source path for files to be stitched: {0}'.format(source_dir))
    source_video_dirs, source_image_dirs = find_video_image_dirs(source_dir)

    print('Copying video directories.')
    copy_source_to_raw_dirs(source_video_dirs, raw_dir) 

    print('Copying image directories.')
    copy_source_to_raw_dirs(source_image_dirs, raw_dir) 

    print('Copying complete')

    print('------Beginning Stitching-------')
    build_stitching_settings(source_video_dirs, stitched_dir)



if __name__ == '__main__':
    # Find source files given a starting directory
    app.run(main) 

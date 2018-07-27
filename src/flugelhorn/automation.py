"""Simple 360 Video Processing Automation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil

from absl import app
from absl import flags

from flugelhorn.yaml_utils import load_configuration_from_yaml


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

def _check_paths(paths):
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
    dest_paths = []
    for d in source_dirs:
        dest_path = os.path.join(dest_base, d[1])
        print('Copying {0} to {1}.'.format(d[0], dest_path))
        shutil.copytree(d[0], dest_path) 
        dest_paths.append(dest_path)
        
    return dest_paths


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
        _check_paths([source_dir, raw_dir, stitched_dir])
    except NotADirectoryError as e:
        print(e) 

    print('Searching source path for files to be stitched: {0}'.format(source_dir))
    source_video_dirs, source_image_dirs = find_video_image_dirs(source_dir)

    print('Copying video directories.')
    # raw_video_paths = copy_source_to_raw_dirs(source_video_dirs, raw_dir) 

    # print('Copying image directories.')
    # raw_image_dirs = copy_source_to_raw_dirs(source_image_dirs, raw_dir) 

    print('Copying complete')

    # Find source files
    


    print('------Beginning Stitching-------')
    build_stitching_sources(raw_video_paths)
    build_stitching_settings(source_video_dirs, stitched_dir)



if __name__ == '__main__':
    app.run(main) 

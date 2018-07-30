"""Simple 360 Video Processing Automation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import subprocess

from absl import app
from absl import flags

from flugelhorn.file_ops import find_video_image_dirs, copy_source_to_raw_dirs, check_paths
from flugelhorn.stitching import stitch_from_raw


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

def run_copy(source_dir, raw_dir):
    """Copy all unstitched media files from a source dir to a raw directory.

    Example use case: copy files from SD card to a local directory on an SSD
    for backup and/or stitching.

    Args:
        source_dir: Source path to recursively search for image and video
                    files for stitching. This will likely be an SD card
                    or the storage device used by the camera.
        raw_dir: Destination path for files to be copied. This will probably
                 be a local HDD or SSD.
    Returns:
        (raw_video_paths, raw_image_paths): tuple containing two lists:
            raw_video_paths: paths to directories containing raw video files
            raw_image_paths: paths to directories containing raw image files 
    """
    print('Searching source path for files to be stitched: {0}'.format(source_dir))
    source_video_dirs, source_image_dirs = find_video_image_dirs(source_dir)

    print('Copying video directories.')
    if source_video_dirs:
        raw_video_paths = copy_source_to_raw_dirs(source_video_dirs, raw_dir) 
    else:
        raw_video_paths = []

    print('Copying image directories.')
    if source_image_dirs:
        raw_image_paths = copy_source_to_raw_dirs(source_image_dirs, raw_dir) 
    else:
        raw_image_paths = []

    print('Copying complete')
    
    return raw_video_paths, raw_image_paths


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
    # Ensure directories exist
    for directory in [raw_dir, stitched_dir]:
        os.makedirs(directory, exist_ok=True)
    settings_path = os.path.abspath(FLAGS.settings)

    # Check that all paths are directories
    try:
        check_paths([source_dir, raw_dir, stitched_dir])
    except NotADirectoryError as e:
        print(e) 

    # Copy
    raw_video_paths, raw_image_dirs = run_copy(source_dir, raw_dir)
    
    # For testing...
    # raw_video_paths = ['/Users/ryan/Projects/test_videos/raw/VID_2018_07_13_00_32_26',
    #                   '/Users/ryan/Projects/test_videos/raw/VID_2018_07_13_00_04_31']

    print('------Beginning Stitching-------')
    for path in raw_video_paths:
        stitch_from_raw(path, stitched_dir, settings_path)


if __name__ == '__main__':
    app.run(main) 

"""Simple 360 Video Processing Automation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from absl import app
from absl import flags

from flugelhorn.file_ops import find_video_image_dirs, check_paths
from flugelhorn.stitching import stitch_from_raw


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


def main(argv):
    if not FLAGS.raw:
        print('Error: Raw destination path must be supplied (--raw).')
        return
    if not FLAGS.stitched:
        print('Error: Stitched path must be supplied (--stitched).')
        return
    raw_dir = os.path.abspath(FLAGS.raw)
    stitched_dir = os.path.abspath(FLAGS.stitched)
    # Ensure directories exist
    os.makedirs(stitched_dir, exist_ok=True)
    settings_path = os.path.abspath(FLAGS.settings)

    # Check that all paths are directories
    try:
        check_paths([raw_dir, stitched_dir])
    except NotADirectoryError as e:
        print(e) 

    # Find raw video paths
    print('Searching raw path for files to be stitched: {0}'.format(raw_dir))
    raw_video_paths, raw_image_paths = find_video_image_dirs(raw_dir)

    print(raw_video_paths)

    print('------Beginning Stitching-------')
    for path in raw_video_paths:
        stitch_from_raw(path, stitched_dir, settings_path)


if __name__ == '__main__':
    app.run(main) 

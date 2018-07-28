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
from flugelhorn.yaml_utils import load_configuration_from_yaml
from flugelhorn.build_config import build_stitching_config, build_stitching_source
from flugelhorn.xml_utils import write_config_xml

STITCHER_APP = '/Applications/Insta360Stitcher.app/Contents/Resources/tools/ProStitcher/ProStitcher'

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


def run_stitching(xml_path, log_path):
    subprocess.run([STITCHER_APP, '-l', log_path, '-x', xml_path, '-w', 'stitch'])


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

    # For testing...
    raw_video_paths = ['/Users/ryan/Projects/test_videos/raw/VID_2018_07_13_00_32_26',
                       '/Users/ryan/Projects/test_videos/raw/VID_2018_07_13_00_04_31']

    print('------Beginning Stitching-------')
    for path in raw_video_paths:
        base_filename = os.path.split(path)[1]
        stitched_path = os.path.join(stitched_dir, base_filename)
        print(stitched_path)
        stitch_source = build_stitching_source(path)
        print(stitch_source)
        config = load_configuration_from_yaml(settings_path) 
        final_config = build_stitching_config(config, stitch_source, stitched_path)
        
        # Write XML for stitching
        xml_save_path = '{0}.xml'.format(stitched_path)
        write_config_xml(final_config, stitch_source, xml_save_path)

        # Run stitching
        log_path = '{0}.log'.format(stitched_path)
        run_stitching(xml_save_path, log_path)


if __name__ == '__main__':
    app.run(main) 

"""Module containing functions to automate Stitching workflow."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import platform
import subprocess

from flugelhorn.config_builder import create_and_write_stitching_config_from_raw

OSX_STITCHER_APP = '/Applications/Insta360Stitcher.app/Contents/Resources/tools/ProStitcher/ProStitcher'
WINDOWS_STITCHER_APP = 'C:\\Program Files (x86)\\Insta360Stitcher\\tools\\prostitcher\\proStitcher.exe'


class StitcherInstallError(Exception):
    """Raised when Insta360 ProStitcher not found."""


def stitch_from_raw(raw_video_dir, stitched_dir, settings_yaml, start=None, end=None):
    """Stitch the files in a directory based on user-defined settings.

    Parses user-defined settings YAML file for base settings.
    Based on data found in the raw_video_dir, sets additional parameters
    for stitching.
    Writes all parameters to an XML file stored in the stitched_dir.
    Runs stitching app based on this XML file.
    Log files are stored alongside stitched video file and XML settings.

    Args:
        raw_video_dir: directory path containing raw video (.mp4) files,
                       pro.prj file, and gyro.dat file
        stitched_dir: directory path to output stitched video (.mp4) file
        settings_yaml: path to a settings YAML file
        start:
        end:
    Returns:
        None
    """
    xml_save_path = create_and_write_stitching_config_from_raw(
        raw_video_dir, stitched_dir, settings_yaml, start, end)

    # Write XML for stitching
    # stitched_path = os.path.join(stitched_dir, os.path.split(raw_video_dir)[1])
    # xml_save_path = '{0}.xml'.format(stitched_path)
    # write_config_xml(config, stitch_source, xml_save_path)

    # Run stitching
    log_path = '{0}.log'.format(os.path.join(stitched_dir, os.path.split(raw_video_dir)[1]))
    run_stitching_app(xml_save_path, log_path)


def run_stitching_app(xml_path, log_path):
    """Run the local machine stitching app w/ XML file settings.

    This currently supports the Insta360 ProStitcher app only.
    """
    stitching_app = get_stitching_app_path()
    subprocess.run([stitching_app, '-l', log_path, '-x', xml_path, '-w', 'stitch'])


def get_stitching_app_path():
    """Return the path to a preinstalled Insta360 ProStitcher app.

    Args:
        None
    Returns:
        Path to Insta360 ProStitcher application.
    Raises:
        StitcherInstallError: if Insta360 ProStitcher application not found
    """
    system = platform.system()
    if system == 'Darwin':
        if os.path.isfile(OSX_STITCHER_APP):
            return OSX_STITCHER_APP
        raise StitcherInstallError('Mac OSX ProStitcher App not found at {0}'.format(
            OSX_STITCHER_APP))
    elif system == 'Windows':
        if os.path.isfile(WINDOWS_STITCHER_APP):
            return WINDOWS_STITCHER_APP
        raise StitcherInstallError('Windows ProStitcher App not found at {0}'.format(
            WINDOWS_STITCHER_APP))

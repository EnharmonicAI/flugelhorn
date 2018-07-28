"""Configuration builder module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import namedtuple
import os

import imageio

from flugelhorn.xml_utils import parse_proj_xml, build_config_xml
from flugelhorn.yaml_utils import load_configuration_from_yaml

# Ensure ffmpeg exists
imageio.plugins.ffmpeg.download()

# A simple object to represent the source data for stitching
# media: list of source files to be used for stitching
# proj: the project file written by the camera
# gyro: gyro stabilization data
StitchSource = namedtuple('StitchSource', 'media proj gyro')
# VideoGroup = namedtuple('VideoGroup', 'file_0 file_1 file_2 file_3 file_4 file_5 offset')

def build_stitching_config(config, stitch_source, stitched_dest):
    """Build stitching configuration.

    Read a starting configuration from a YAML file,
    and add in specific file names and destinations."""

    # Assume VIDEO for now 
    print(config)


    # Define stitched file path
    # TODO(ryan): Currently only support single mp4 file output
    stitched_path = '{0}.{1}'.format(stitched_dest, 'mp4')
    config.output.dst = stitched_path


    proj_dict = parse_proj_xml(stitch_source.proj)

    # TODO(ryan): Add capture time and captureTimeIndex to blend.configuration
    # TODO(ryan): Add bitrate

    # Add gyro configuration
    config.gyro.version = int(proj_dict['gyro_version'])
    config.gyro.timeOffset = proj_dict['timeOffset']
    config.gyro.filename = stitch_source.gyro

    config.gyro_calibration.gravity_x = proj_dict['gravity_x']
    config.gyro_calibration.gravity_y = proj_dict['gravity_y']
    config.gyro_calibration.gravity_z = proj_dict['gravity_z']

    return config


def build_stitching_source(path):
    """Build a list of StitchSource objects from a list of paths."""
    media = []
    # print(p)
    for f in os.listdir(path):
        # print(f)
        if os.path.splitext(f)[1] == '.mp4':
            media.append(os.path.join(path, f))

    # Make Video Groups
    # NOTE: These groups could also be created by using the file names
    # in the pro.prj file.
    # The below method ensures that all numbered files exist and groups are complete.
    num_groups = int((len(media) - 1) / 6)
    video_groups = []
    
    for n in range(0, num_groups):
        vid_group = {} 
        for i in range(6):
            if n == 0:
                f = os.path.join(path, 'origin_{0}.mp4'.format(i))
            else:
                f = os.path.join(path, 'origin_{0}_00{1}.mp4'.format(i, n))
            vid_group[i] = f
            print(f)
            media.remove(f)

        metadata = _get_video_grp_metadata(vid_group[0])
        vid_group['start'] = metadata['start']
        vid_group['end'] = metadata['end']
        # Use the previous group's end time as the offset
        if n == 0: 
            vid_group['ptsOffset'] = 0
        else:
            vid_group['ptsOffset'] = video_groups[-1]['end']
        video_groups.append(vid_group)
    assert len(media) <= 1
    print(video_groups) 
    
    proj = os.path.join(path, 'pro.prj')
    gyro = os.path.join(path, 'gyro.dat')

    return StitchSource(video_groups, proj, gyro)
    

def _get_video_grp_metadata(mp4_file):
    """Get metadata of a video group based on the first origin.mp4 file."""
    reader = imageio.get_reader(mp4_file)
    raw_metadata = reader.get_meta_data()
    grp_metadata = {}
    grp_metadata['start'] = 0
    grp_metadata['end'] = round(raw_metadata['nframes'] / raw_metadata['fps'], 3)
    
    return grp_metadata


if __name__ == '__main__':
    test_path = '/Users/ryan/Projects/flugelhorn/settings/daily_mono.yaml' 
    # config = load_configuration_from_yaml(test_path)
    
    # stitch source
    test_raw = ['/Users/ryan/Projects/test_videos/new_source/VID_2018_07_13_00_04_31',
                '/Users/ryan/Projects/test_videos/new_source/VID_2018_07_13_00_32_26']
    # stitch_sources = build_stitching_sources(test_raw)

    test_proj = '/Users/ryan/Projects/test_videos/new_source/VID_2018_07_13_00_04_31/pro.prj'
    proj_dict = parse_proj_xml(test_proj)

    dest = '/Users/ryan/Projects/test_videos/stitched/VID_2018_07_13_00_04_31'

    # TODO(ryan): just build a single stitch source at a time
    for path in [test_raw[0]]:
        stitch_source = build_stitching_source(path)
        print(stitch_source) 
        config = load_configuration_from_yaml(test_path)
        final_config = build_stitching_config(config, stitch_source, dest)

    x = build_config_xml(final_config, stitch_source)
    # test_source = StitchSource(['test', 'test2'], 'proj', 'gyro')
    
    # test_image = '/Users/ryan/Projects/test_videos/new_source/VID_2018_07_13_00_04_31.origin_0.mp4'
    # reader = imageio.get_reader(test_image)
    # 
    # 
    # test_dest = '/Users/ryan/Projects/test_videos/stitched/VID_2018_07_13_00_04_31'

    # final = build_stitching_config(config, test_source, test_dest)
    


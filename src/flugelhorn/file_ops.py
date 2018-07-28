"""File operations module for copying."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil


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


def check_paths(paths):
    """Check that all supplied paths are directories."""
    for p in paths:
        if not os.path.isdir(p):
            raise NotADirectoryError('%s is not a directory.' % p)




#!/usr/bin/env python

import os
from glob import glob

from setuptools import find_packages
from setuptools import setup

setup(
    name='flugelhorn',
    version='0.0.1',
    license='MIT License',
    description='Quick toolset for automating VR / 360 Video processing pipelines.',
    author='Ryan Stauffer',
    author_email='ryan@enharmonic.ai',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    include_packagge_data=True,
    zip_safe=False,
    scripts=['scripts/copy-and-stitch', 'scripts/stitch'],
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'absl-py',
	'ruamel.yaml',
	'imageio'
    ]
)

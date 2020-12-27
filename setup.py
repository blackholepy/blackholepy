#!/usr/bin/env python3
#
# Copyright (C) 2020 Chi-kwan Chan
# Copyright (C) 2020 Steward Observatory
#
# This file is part of `blackholepy`.
#
# `Blackholepy` is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# `Blackholepy` is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with `blackholepy`.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(
    name='blackholepy',
    version='0.1.0',
    url='https://github.com/blackholepy/blackholepy',
    author='Chi-kwan Chan',
    author_email='chanc@arizona.edu',
    description='Python for Black Hole Astrophysics',
    packages=find_packages('mod'),
    package_dir={'': 'mod'},
    entry_points={
        'console_scripts': [
            'sed-pack = blackholepy.sed.pack:pack',
        ],
    },
    python_requires='>=3.6', # `blackholepy` uses python3's f-string and typing
    install_requires=[
        'click>=7.1.2',
        'hallmark>=0.1',
        'h5py>=3.1',
        'matplotlib>=3.2',
        'numpy>=1.19',
        'scipy>=1.5.4',
        'tqdm>=4.46.1',
    ],
)

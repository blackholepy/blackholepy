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

import click
import numpy as np
import h5py

from tqdm import tqdm

from .. import ParaFrame
from .  import load

@click.command()
@click.argument('path', nargs=1, required=True)
@click.option('-i', '--inclination', default=70,        help='Inclination angle.'  )
@click.option('-o', '--output',      default='pack.h5', help='Name of output dump.')
def pack(path, inclination, output):
    """Pack multiple `igrmonty` output hdf5 files into one file"""

    pf  = ParaFrame(path)
    frm = np.unique(pf.frame)
    knd = np.array([
        "total",
        "(synch) base", "(synch) once", "(synch) twice", "(synch) > twice",
        "(brems) base", "(brems) once", "(brems) twice", "(brems) > twice",
    ], dtype='a16')

    avgs, errs, lens = [], [], []
    for f in tqdm(frm):
        paths = pf(frame=f).path
        nu, avg, err = load(paths, i=inclination)
        avgs.append(avg)
        errs.append(err)
        lens.append(len(paths))

    with h5py.File(output, 'w') as f:
        f['frm'] = frm
        f['nu']  = nu
        f['knd'] = knd
        f['avg'] = np.array(avgs)
        f['err'] = np.array(errs)
        f['len'] = np.array(lens)

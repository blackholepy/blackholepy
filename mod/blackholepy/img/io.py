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

import h5py
import numpy as np

def value(g, s):
    return g[s][()]

def load_one(file):
    with h5py.File(file, "r") as f:
        h = f['header']
        c = h['camera']
        u = h['units']

        dx  = value(c, 'dx') * value(u, 'L_unit')
        fov = dx / value(h, 'dsource') * 2.06265e11
        nx  = value(c, 'nx')
        X   = np.linspace(-fov, fov, nx)

        try:
            dy  = value(c, 'dy') * value(u, 'L_unit')
            fov = dy / value(h, 'dsource') * 2.06265e11
            ny  = value(c, 'ny')
            Y   = np.linspace(-fov, fov, ny)
        except:
            Y = X

        I = np.copy(f['unpol']).transpose((1,0)) * value(h, 'scale')

    return X, Y, I

def load(files, **kwargs):
    if isinstance(files, str):
        files = [files]

    imgs = [] # collect arrays in list and then cast to np.array()
              # all at once is faster than concatenate
    for f in files:
        X, Y, I = load_one(f, **kwargs)
        imgs.append(I)
    imgs = np.array(imgs)

    return X, Y, imgs

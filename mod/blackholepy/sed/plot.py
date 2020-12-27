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

from scipy.stats import poisson, norm

def interval(avg, std, sigma=1):
    """We model the different realizations of grmonty results follow a
    Poisson distribution, which has mean and variance both equal to
    `mu`.  Therefore,

        avg = dnuLnu * mu
        std = dnuLnu * sqrt(mu)

        mu = (avg/std)**2

    One we obtain `mu`, we can estimate the lower and upper intervals
    according to `sigma`.

    """
    with np.errstate(invalid='ignore', divide='ignore'):
        mu = (avg/std)**2

    lower = poisson.ppf(norm.cdf(-sigma), mu)
    upper = poisson.ppf(norm.cdf(+sigma), mu)
    units = avg / mu

    return lower * units, upper * units

def step_one(ax, nu, avg, std=None, sigma=1,
             shade=True, ylog=True, **kwargs):
    p = ax.step(nu, avg, where='mid', **kwargs)

    if std is not None and shade:
        l, u = interval(avg, std, sigma=sigma)
        ax.fill_between(nu, l, u, step='mid',
                        color=p[0].get_color(), alpha=1/3, linewidth=0)

    # x-axis must be in log scale; otherwise the bin boundaries are wrong
    ax.set_xscale('log')
    # optionally we may set y-axis to log sacle
    if ylog:
        ax.set_yscale('log')

def step(ax, nu, avg, std=None, color=None, shade=None, label=None, **kwargs):
    n   = len(nu)
    avg = avg.reshape(n,-1)
    for i in range(avg.shape[-1]):
        stdi   = std.reshape(n,-1)[:,i] if std is not None else None
        colori = color if color is not None else ('k'  if i == 0 else None)
        widthi = 2 if i == 0 else 1
        shadei = shade if shade is not None else (True if i == 0 else False)
        labeli = label[i] if label is not None else None
        step_one(ax, nu, avg[:,i], stdi,
                 color=colori, linewidth=widthi,
                 shade=shadei, label=labeli,
                 **kwargs)

"""Gemeinsame Testfunktion der Kongressmessung."""
import itertools

import numpy as np


def perm_p(x, grp, reps=None):
    """Exakter Permutationstest (einseitig): Mittelwert der Gruppe True groesser als der Rest."""
    x, grp = np.asarray(x, float), np.asarray(grp, bool)
    ok = ~np.isnan(x)
    x, grp = x[ok], grp[ok]
    obs = x[grp].mean() - x[~grp].mean()
    n, k = len(x), grp.sum()
    cnt = tot = 0
    for idx in itertools.combinations(range(n), k):
        m = np.zeros(n, bool)
        m[list(idx)] = True
        tot += 1
        cnt += (x[m].mean() - x[~m].mean()) >= obs - 1e-12
    return obs, cnt / tot, int(k), int(n - k)

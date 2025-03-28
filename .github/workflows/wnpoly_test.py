import math
import wnpoly as wp
import numpy as np

def test_identity_1():
    chsp = wp.symm.Complete()
    ehsp = wp.symm.Elementary()
    n = 10
    x = np.random.default_rng().integers(1, high=10, size=n)
    h = chsp.compute(x, n)
    e = ehsp.compute(x, n)

    for n in range(1, len(x)):
        d = 0
        for k in range(n+1):
            d += np.power(-1, k) * h[n-k] * e[k]
        assert d == 0

def test_identity_2():
    chsp = wp.symm.Complete()
    pssp = wp.symm.PowerSum()
    n = 10
    x = np.random.default_rng().integers(1, high=10, size=n)
    h = chsp.compute(x, n)
    p = pssp.compute(x, n)

    for n in range(1, len(x)):
        sum = 0
        for k in range(1, n+1):
            sum += h[n-k] * p[k]
        assert n*h[n] - sum == 0

def test_identity_3():
    ehsp = wp.symm.Elementary()
    pssp = wp.symm.PowerSum()
    n = 15
    x = np.random.default_rng().integers(1, high=10, size=n)
    p = pssp.compute(x, n)
    e = ehsp.compute(x, n)

    for n in range(1, len(x)):
        sum = 0
        for k in range(1, n+1):
            sum += np.power(-1, k-1) * e[n-k] * p[k]
        assert n*e[n] - sum == 0

def test_norm():
    n = 10
    x = np.ones(n, dtype=int)
    chsp = wp.symm.Complete()
    ehsp = wp.symm.Elementary()
    pssp = wp.symm.PowerSum()

    h_norm = chsp.compute_normalized(x, n)
    p_norm = pssp.compute_normalized(x, n)
    e_norm = ehsp.compute_normalized(x, n)

    for j in range(n):
        assert h_norm[n] == 1
        assert p_norm[n] == 1
        assert e_norm[n] == 1

def test_bell():
    my_bell = wp.bell.Bell()
    n = 5
    b = np.random.default_rng().uniform(low=1, high=10, size=n)
    b = np.insert(b, 0, 1.)

    x = my_bell.invert(b)

    bc = my_bell.compute(x)

    for n in range(len(x)):
        math.isclose(b[n], bc[n], abs_tol=0.0001)
   
def test_partial_bell():
    my_bell = wp.bell.Bell()
    my_partial_bell = wp.bell.PartialBell()
    n = 5
    x = np.random.default_rng().uniform(low=1, high=10, size=n)
    x = np.insert(x, 0, 0.)
    bc = my_bell.compute(x)
    pbc = my_partial_bell.compute(x)

    for n in range(len(x)):
        bn = 0
        for k in range(0, n+1):
            bn += pbc[n, k]
        assert math.isclose(bc[n], bn, abs_tol=0.0001)

def test_partial_bell_invert():
    my_partial_bell = wp.bell.PartialBell()
    n = 5
    x = np.random.default_rng().uniform(low=1, high=10, size=n)
    x = np.insert(x, 0, 0.)
    pbc = my_partial_bell.compute(x)

    xc = my_partial_bell.invert(pbc)

    for n in range(len(x)):
        assert math.isclose(x[n], xc[n], abs_tol=0.0001)

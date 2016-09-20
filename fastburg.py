"""BURG method of AR model estimate

.. topic:: This module provides BURG method and BURG PSD estimate

    .. autosummary::

        arburg
        pburg

    .. codeauthor:: Thomas Cokelaer 2011

"""

# TODO: convert arburg into arburg2 to get a nicer and faster algorithm.

import numpy

__all__ = ["arburg", 'pburg']


def _arburg2(X, order):
    """This version is 10 times faster than arburg, but the output rho is not correct.


    returns [1 a0,a1, an-1]

    """
    x = numpy.array(X)
    N = len(x)

    if order == 0.:
        raise ValueError("order must be > 0")

    # Initialisation
    # ------ rho, den
    rho = sum(abs(x)**2.) / N  # Eq 8.21 [Marple]_
    den = rho * 2. * N

    # ------ backward and forward errors
    ef = numpy.zeros(N, dtype=complex)
    eb = numpy.zeros(N, dtype=complex)
    for j in range(0, N):  # eq 8.11
        ef[j] = x[j]
        eb[j] = x[j]

    # AR order to be stored
    a = numpy.zeros(1, dtype=complex)
    a[0] = 1
    # ---- rflection coeff to be stored
    ref = numpy.zeros(order, dtype=complex)

    E = numpy.zeros(order+1)
    E[0] = rho

    for m in range(0, order):
        # print m
        # Calculate the next order reflection (parcor) coefficient
        efp = ef[1:]
        ebp = eb[0:-1]
        # print efp, ebp
        num = -2. * numpy.dot(ebp.conj().transpose(), efp)
        den = numpy.dot(efp.conj().transpose(),  efp)
        den += numpy.dot(ebp,  ebp.conj().transpose())
        ref[m] = num / den

        # Update the forward and backward prediction errors
        ef = efp + ref[m] * ebp
        eb = ebp + ref[m].conj().transpose() * efp

        # Update the AR coeff.
        a.resize(len(a)+1)
        a = a + ref[m] * numpy.flipud(a).conjugate()

        # Update the prediction error
        E[m+1] = numpy.real((1 - ref[m].conj().transpose() * ref[m])) * E[m]
        # print 'REF', ref, num, den
    return a, E[-1], ref

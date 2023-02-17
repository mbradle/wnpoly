"""This module computes Bell polynomials."""

import numpy as np
import scipy.special as sc


class bell:
    """A class for complete Bell polynomials."""

    def compute(self, x):
        """Method to compute Bell polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which to compute the polynomials.

        Returns:
            An :obj:`numpy.array` containing the Bell polynomials for the input `x` up to order `n`.

        """

        result = np.zeros(len(x))
        result[0] = 1
        for m in range(len(x)-1):
            for i in range(m+1):
                result[m+1] += sc.binom(m, i) * result[m-i] * x[i+1]
        return result

    def invert(self, b):
        """Method to invert Bell polynomials, that is, to find the x elements from a set of Bell polynomials.

        Args:
            ``b`` (:obj:`list` or :obj:`numpy.array`): An array containing the Bell polynomials.

        Returns:
            A :obj:`numpy.array` containing the x's giving rise to the input polynomials.

        """
        x = np.array([0])
        for n in range(len(b) - 1):
            sum = b[n + 1]
            for i in range(n):
                sum -= sc.binom(n, i) * b[n - i] * x[i + 1]
            x = np.append(x, sum)
        return x

    def negate(self, b):
        """Method to negate Bell polynomials, that is, to find the corresponding Bell polynomials with negative x's from the input ones.

        Args:
            ``b`` (:obj:`list` or :obj:`numpy.array`): An array containing the Bell polynomials.

        Returns:
            A :obj:`numpy.array` containing the negated polynomials.

        """
        bn = np.array([1])
        for n in range(1, len(b)):
            bn = np.append(bn, 0)
            for i in range(n):
                bn[n] -= sc.binom(n, i) * bn[i] * b[n - i]
        return bn


class partial_bell:
    """A class for partial Bell polynomials."""

    def __init__(self):
        self.b_hash = {}

    def compute(self, n, k, x):
        """Method to compute partial Bell polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute the polynomial.  The value must be less than or equal to the length of the input array.

            ``k`` (:obj:`int`): A non-negative integer giving the partial order to which to compute the polynomial.  The value must be less than or equal to the length of the input array.

        Returns:
            The partial Bell polynomial of order `n` and `k`.

        """

        assert n >= k
        assert len(x) + k > n + 1
        if n == 0 and k == 0:
            return 1
        elif (n == 0 and k > 0) or (n > 0 and k == 0):
            return 0
        else:
            result = 0
            for i in range(1, n - k + 2):
                result += sc.binom(n - 1, i - 1) * x[i] * self.compute(n - i, k - 1, x)
            return result

    def _r_bell(self, n, k, x):
        if n == 0 and k == 0:
            return 1
        elif n == 0 or k == 0 or n < k:
            return 0
        elif (n, k) in self.b_hash:
            return self.b_hash[(n, k)]
        else:
            result = 0
            for i in range(1, n - k + 1):
                result += sc.binom(n - 1, i - 1) * x[i] * self._r_bell(n - i, k - 1, x)
            return result

    def invert(self, k, b):
        """Method to invert partial Bell polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute the polynomial.  The value must be less than or equal to the length of the input array.

            ``k`` (:obj:`int`): A non-negative integer giving the partial order to which to compute the polynomial.  The value must be less than or equal to the length of the input array.

        Returns:
            The partial Bell polynomial of order `n` and `k`.

        """

        x = np.array([0])
        self.b_hash.clear()
        x = np.append(x, np.power(b[0], 1.0 / k))
        for m in range(1, len(b)):
            sum = b[m]
            for i in range(1, m + 1):
                sum -= (
                    sc.binom(k + m - 1, i - 1)
                    * self._r_bell(k + m - i, k - 1, x)
                    * x[i]
                )
            x = np.append(x, sum / (sc.binom(k + m, m + 1) * np.power(x[1], k - 1)))
            for n in range(1, k + 1):
                self.b_hash[(n + m, n)] = self.compute(n + m, n, x)
        return x

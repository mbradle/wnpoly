"""This module computes Bernoulli polynomials."""

import numpy as np
import scipy.special as sc


class bernoulli:
    """A class for Bernoulli polynomials."""

    def compute(self, n, x):
        """Method to compute Bernoulli polynomials.

        Args:
            ``n`` (:obj:`int`): The order of the desired polynomial

            ``x`` (:obj:`float`): The value for which to compute the polynomial.

        Returns:
            A :obj:`float` giving the polynomial.

        """

        bn = self._compute_bernoulli_numbers(n)

        result = 0
        for k in range(n + 1):
            result += sc.binom(n, k) * bn[n - k] * np.power(x, k)

        return result

    def _compute_bernoulli_numbers(self, n):

        result = np.array([1])

        for m in range(1, n+1):
            bt = 0
            for k in range(m):
                bt -= sc.binom(m, k) * result[k] / (m - k + 1)
            result = np.append(result, bt)

        return result

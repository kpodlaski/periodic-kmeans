import math

import numpy as np
import scipy.special
from sklearn.metrics.cluster._supervised import contingency_matrix


def binom_over_two(x):
    return scipy.special.binom(x,2)

matrix_binom_over_two = np.vectorize(binom_over_two)

def compare_clusters(labelsA, labelsB):
    c_matrix = contingency_matrix(labelsA, labelsB)
    m_i_plus = c_matrix.sum(axis=0)
    m_plus_j = c_matrix.sum(axis=1)
    T = matrix_binom_over_two(c_matrix).sum()
    P = matrix_binom_over_two(m_i_plus).sum()
    Q = matrix_binom_over_two(m_plus_j).sum()
    N = binom_over_two(m_i_plus.sum())
    a = T
    b = P - T
    c = Q - T
    d = N + T - P - Q
    metrics = {}
    metrics['Rand'] = (a + d) / N
    E_R = 1 + 2 * P * Q / N / N - (P + Q) / N
    metrics['Adjusted Rand'] = (metrics['Rand'] - E_R) / (1 - E_R)
    metrics['Arabie Boorman'] = (b + c) / N
    metrics['Hubert'] = (a + d - b - c) / N
    metrics['Fowles Mallows'] = a / math.sqrt((a + b) * (a + c))
    metrics['Jaccard'] = a / (a + b + c)
    return metrics

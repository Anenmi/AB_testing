import numpy as np


def get_bernoulli_confidence_interval(values: np.array):
    """Вычисляет доверительный интервал для параметра распределения Бернулли.

    :param values: массив элементов из нулей и единиц.
    :return (left_bound, right_bound): границы доверительного интервала.
    """
    z = 1.96
    n = len(values)
    p = np.mean(values)
    K = np.sum(values)
    return (K / n - z * np.sqrt((K / n * (1 - K / n)) / n), 
            K / n + z * np.sqrt((K / n * (1 - K / n)) / n))
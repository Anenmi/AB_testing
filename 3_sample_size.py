import numpy as np
import pandas as pd
from scipy.stats import norm

def estimate_sample_size(df, metric_name, effects, alpha=0.05, beta=0.2):
    """Оцениваем sample size для списка эффектов.

    df - pd.DataFrame, датафрейм с данными
    metric_name - str, название столбца с целевой метрикой
    effects - List[float], список ожидаемых эффектов. Например, [1.03] - увеличение на 3%
    alpha - float, ошибка первого рода
    beta - float, ошибка второго рода

    return - pd.DataFrame со столбцами ['effect', 'sample_size']    
    """
    # YOUR_CODE_HERE
    result = {'effect': [], 'sample_size': []}
    for effect in effects:
        t_alpha = norm.ppf(1 - alpha / 2, loc=0, scale=1)
        t_beta = norm.ppf(1 - beta, loc=0, scale=1)
        z_scores_sum_squared = (t_alpha + t_beta) ** 2
        std = np.std(df[metric_name])
        mu = np.mean(df[metric_name])
        sample_size = int(
            np.ceil(
                z_scores_sum_squared * (2 * std ** 2) / (((effect - 1)*mu) ** 2)
            )
        )
        result['effect'].append(effect)
        result['sample_size'].append(sample_size)
    return pd.DataFrame(result)

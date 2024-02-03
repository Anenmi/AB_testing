import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


def estimate_first_type_error(df_pilot_group, df_control_group, metric_name, alpha=0.05, n_iter=10000, seed=None):
    """Оцениваем ошибку первого рода.

    Бутстрепим выборки из пилотной и контрольной групп тех же размеров, считаем долю случаев с значимыми отличиями.
    
    df_pilot_group - pd.DataFrame, датафрейм с данными пилотной группы
    df_control_group - pd.DataFrame, датафрейм с данными контрольной группы
    metric_name - str, названия столбца с метрикой
    alpha - float, уровень значимости для статтеста
    n_iter - int, кол-во итераций бутстрапа
    seed - int or None, состояние генератора случайных чисел.

    return - float, ошибка первого рода
    """
    pilot_indices = np.random.randint(0, len(df_pilot_group), (n_iter, len(df_pilot_group)))
    control_indices = np.random.randint(0, len(df_control_group), (n_iter, len(df_control_group)))
    
    pilot = df_pilot_group[metric_name].values[pilot_indices]
    control = df_control_group[metric_name].values[control_indices]
    
    res = 0
    #p_value = []
    for i in range(n_iter):
        res += int(ttest_ind(pilot[i], control[i]).pvalue < alpha)
        #p_value.append(ttest_ind(pilot[i], control[i]).pvalue)
        
    return res / n_iter#, p_value
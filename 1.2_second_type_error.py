import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


def estimate_second_type_error(df_pilot_group, df_control_group, metric_name, effects, alpha=0.05, n_iter=10000, seed=None):
    """Оцениваем ошибки второго рода.

    Бутстрепим выборки из пилотной и контрольной групп тех же размеров, добавляем эффект к пилотной группе,
    считаем долю случаев без значимых отличий.
    
    df_pilot_group - pd.DataFrame, датафрейм с данными пилотной группы
    df_control_group - pd.DataFrame, датафрейм с данными контрольной группы
    metric_name - str, названия столбца с метрикой
    effects - List[float], список размеров эффектов ([1.03] - увеличение на 3%).
    alpha - float, уровень значимости для статтеста
    n_iter - int, кол-во итераций бутстрапа
    seed - int or None, состояние генератора случайных чисел

    return - dict, {размер_эффекта: ошибка_второго_рода}
    """
    np.random.seed(seed)
    
    pilot_indices = np.random.randint(0, len(df_pilot_group), (n_iter, len(df_pilot_group)))
    control_indices = np.random.randint(0, len(df_control_group), (n_iter, len(df_control_group)))
    
    #pilot = df_pilot_group[metric_name].values[pilot_indices]
    control = df_control_group[metric_name].values[control_indices]
    
    second_type_error = {}
    for effect in effects:
        res = 0
        pilot_with_effect = (df_pilot_group[metric_name] * np.random.normal(effect, 
                                                                            0.005, 
                                                                            len(df_pilot_group)
                                                                           )
                            ).values[pilot_indices]
        for i in range(n_iter):
            res += int(ttest_ind(pilot_with_effect[i], control[i]).pvalue < alpha)
            
        second_type_error[effect] = 1 - res / n_iter
        
    return second_type_error
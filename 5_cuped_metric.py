import numpy as np
import pandas as pd


def calculate_metric(
    df, value_name, user_id_name, list_user_id, date_name, period, metric_name
):
    """Вычисляет значение метрики для списка пользователей в определённый период.
    
    df - pd.DataFrame, датафрейм с данными
    value_name - str, название столбца со значениями для вычисления целевой метрики
    user_id_name - str, название столбца с идентификаторами пользователей
    list_user_id - List[int], список идентификаторов пользователей, для которых нужно посчитать метрики
    date_name - str, название столбца с датами
    period - dict, словарь с датами начала и конца периода, за который нужно посчитать метрики.
        Пример, {'begin': '2020-01-01', 'end': '2020-01-08'}. Дата начала периода входит нужный
        полуинтервал, а дата окончание нет, то есть '2020-01-01' <= date < '2020-01-08'.
    metric_name - str, название полученной метрики

    return - pd.DataFrame, со столбцами [user_id_name, metric_name], кол-во строк должно быть равно
        кол-ву элементов в списке list_user_id.
    """
    # YOUR_CODE_HERE
    df_subsample = df[(df[user_id_name].isin(list_user_id))&
                      (df[date_name]>=period['begin'])&
                      (df[date_name]<period['end'])]
    result = df_subsample.groupby(user_id_name, as_index=False)[value_name].agg(func='sum')
    result = pd.DataFrame(list_user_id, columns=[user_id_name]).merge(result, on=user_id_name, how='left').fillna(0)
    result.columns = [user_id_name, metric_name]
    return result



def calculate_metric_cuped(
    df, value_name, user_id_name, list_user_id, date_name, periods, metric_name
):
    """Вычисляет метрики во время пилота, коварианту и преобразованную метрику cuped.
    
    df - pd.DataFrame, датафрейм с данными
    value_name - str, название столбца со значениями для вычисления целевой метрики
    user_id_name - str, название столбца с идентификаторами пользователей
    list_user_id - List[int], список идентификаторов пользователей, для которых нужно посчитать метрики
    date_name - str, название столбца с датами
    periods - dict, словарь с датами начала и конца периода пилота и препилота.
        Пример, {
            'prepilot': {'begin': '2020-01-01', 'end': '2020-01-08'},
            'pilot': {'begin': '2020-01-08', 'end': '2020-01-15'}
        }.
        Дата начала периода входит в полуинтервал, а дата окончания нет,
        то есть '2020-01-01' <= date < '2020-01-08'.
    metric_name - str, название полученной метрики

    return - pd.DataFrame, со столбцами
        [user_id_name, metric_name, f'{metric_name}_prepilot', f'{metric_name}_cuped'],
        кол-во строк должно быть равно кол-ву элементов в списке list_user_id.
    """
    # YOUR_CODE_HERE
    
    
    prepilot = calculate_metric(df, value_name, user_id_name, list_user_id, date_name, periods['prepilot'], metric_name)
    pilot = calculate_metric(df, value_name, user_id_name, list_user_id, date_name, periods['pilot'], metric_name)
    prepilot.columns = [user_id_name, f'{metric_name}_prepilot']
    
    result = pilot.merge(prepilot, on=user_id_name, how='inner')
    
    covariance = np.cov(result[f'{metric_name}_prepilot'], result[metric_name])[0, 1]
    variance = np.var(result[f'{metric_name}_prepilot'])
    theta = covariance / variance
    
    result[f'{metric_name}_cuped'] = result[metric_name] - theta * result[f'{metric_name}_prepilot']
    
    return result
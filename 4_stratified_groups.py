import numpy as np
import pandas as pd


def select_stratified_groups(data, strat_columns, group_size, weights=None, seed=None):
    """Подбирает стратифицированные группы для эксперимента.

    data - pd.DataFrame, датафрейм с описанием объектов, содержит атрибуты для стратификации.
    strat_columns - List[str], список названий столбцов, по которым нужно стратифицировать.
    group_size - int, размеры групп.
    weights - dict, словарь весов страт {strat: weight}, где strat - либо tuple значений элементов страт,
        например, для strat_columns=['os', 'gender', 'birth_year'] будет ('ios', 'man', 1992), либо просто строка/число.
        Если None, определить веса пропорционально доле страт в датафрейме data.
    seed - int, исходное состояние генератора случайных чисел для воспроизводимости
        результатов. Если None, то состояние генератора не устанавливается.

    return (data_pilot, data_control) - два датафрейма того же формата, что и data
        c пилотной и контрольной группами.
    """
    # YOUR_CODE_HERE
    np.random.seed(seed=seed)
    if weights == None:
        weights_df = data.groupby(strat_columns, as_index=False).size()
        weights_df['weight'] = weights_df['size'] / weights_df['size'].sum()

        weights = {}
        for i in range(len(weights_df)):
            curr_row = weights_df.iloc[i]
            if len(strat_columns) > 1:
                weights[tuple(curr_row[col] for col in strat_columns)] = curr_row.weight
            else:
                weights[curr_row[strat_columns[0]]] = curr_row.weight
            
    data_pilot = data.head(0)
    data_control = data.head(0)

    for cols, val in weights.items():
        str_group_size = int(group_size * val + 0.5)
        
        data_curr = data   
        if type(cols) == tuple:
            for col_n, col_val in enumerate(cols):
                data_curr = data_curr[data_curr[strat_columns[col_n]]==col_val]
        else: 
            data_curr = data_curr[data_curr[strat_columns[0]]==cols]
        
        index = np.arange(0, len(data_curr))
        rand_index = np.random.choice(index, size=2*str_group_size, replace=False)
        pilot_rand_index = rand_index[:str_group_size]
        control_rand_index = rand_index[str_group_size:]

        data_pilot = pd.concat([data_pilot, data_curr.iloc[pilot_rand_index]])
        data_control = pd.concat([data_control, data_curr.iloc[control_rand_index]])
    return data_pilot, data_control
    
        
        
        
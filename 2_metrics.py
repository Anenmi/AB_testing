import numpy as np
import pandas as pd


def calculate_sales_metrics(df, cost_name, date_name, sale_id_name, period, filters=None):
    """Вычисляет метрики по продажам.
    
    df - pd.DataFrame, датафрейм с данными. Пример
        pd.DataFrame(
            [[820, '2021-04-03', 1, 213]],
            columns=['cost', 'date', 'sale_id', 'shop_id']
        )
    cost_name - str, название столбца с стоимостью товара
    date_name - str, название столбца с датой покупки
    sale_id_name - str, название столбца с идентификатором покупки (в одной покупке может быть несколько товаров)
    period - dict, словарь с датами начала и конца периода пилота.
        Пример, {'begin': '2020-01-01', 'end': '2020-01-08'}.
        Дата начала периода входит в полуинтервал, а дата окончания нет,
        то есть '2020-01-01' <= date < '2020-01-08'.
    filters - dict, словарь с фильтрами. Ключ - название поля, по которому фильтруем, значение - список значений,
        которые нужно оставить. Например, {'user_id': [111, 123, 943]}.
        Если None, то фильтровать не нужно.

    return - pd.DataFrame, в индексах все даты из указанного периода отсортированные по возрастанию, 
        столбцы - метрики ['revenue', 'number_purchases', 'average_check', 'average_number_items'].
        Формат данных столбцов - float, формат данных индекса - datetime64[ns].
    """
    # YOUR_CODE_HERE

    df_period = df[(df[date_name]>=period['begin'])&(df[date_name]<period['end'])]
    df_period[date_name] = df_period[date_name].astype('datetime64[ns]')

    if filters != None:
        for key, item in filters.items():
            df_period = df_period[df_period[key].isin(item)]
    
    agg_check = df_period.groupby([date_name, sale_id_name], as_index=False).agg(
        check = (cost_name, 'sum'),
        number_items = (cost_name, 'count')
        ).groupby(date_name).agg(
            average_check = ('check', 'mean'),
            average_number_items = ('number_items', 'mean')
        )
    
    
    result = df_period.groupby(date_name).agg(
        revenue = (cost_name, 'sum'),
        number_purchases = (sale_id_name, 'nunique')
        ).merge(agg_check, left_index=True, right_index=True)
    
    dates = pd.DataFrame(pd.date_range(period['begin'], period['end']), columns=['date']).iloc[:-1,:]
    result = dates.merge(result, left_on='date', right_index=True, how='left').set_index('date').fillna(0)
    
    return result


# import pandas as pd

# # Создаем список словарей
# data = [{'cost': 820, 'date': '2021-04-03', 'sale_id': 1, 'shop_id': 213},
#         {'cost': 500, 'date': '2021-04-04', 'sale_id': 2, 'shop_id': 101},
#         {'cost': 900, 'date': '2021-04-05', 'sale_id': 3, 'shop_id': 150},
#         {'cost': 600, 'date': '2021-04-06', 'sale_id': 4, 'shop_id': 200},
#         {'cost': 700, 'date': '2021-04-06', 'sale_id': 5, 'shop_id': 220},
#         {'cost': 850, 'date': '2021-04-08', 'sale_id': 6, 'shop_id': 250},
#         {'cost': 950, 'date': '2021-04-09', 'sale_id': 7, 'shop_id': 300},
#         {'cost': 750, 'date': '2021-04-10', 'sale_id': 8, 'shop_id': 320},
#         {'cost': 650, 'date': '2021-04-11', 'sale_id': 9, 'shop_id': 350},
#         {'cost': 800, 'date': '2021-04-12', 'sale_id': 10, 'shop_id': 380}]

# # Создаем DataFrame из списка словарей
# df = pd.DataFrame(data, columns=['cost', 'date', 'sale_id', 'shop_id'])

# # Выводим DataFrame на экран
# print(df)


# calculate_sales_metrics(df, cost_name='cost', date_name='date', sale_id_name='sale_id', period={'begin': '2021-04-03', 'end': '2021-04-11 '}, filters={'shop_id': [101, 300, 320]})
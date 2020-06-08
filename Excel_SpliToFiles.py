# coding: utf-8

import pandas as pd

pd.read_excel('Staff_list_05_18.xlsx',sheet_name='TDSheet').groupby(['Магазин','Должность', 'Мотив','Марка']).agg({'Сумма': sum}).reset_index().groupby(['Магазин','Должность', 'Мотив','Марка']).apply(lambda x: x.to_excel('staff_test/' + str(x.name) + '.xlsx',index=False,encoding='utf8'))

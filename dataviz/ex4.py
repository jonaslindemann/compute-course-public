# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:26:51 2017

@author: Jonas Lindemann
"""

import pandas as pd

cars = pd.read_excel('04cars.xls')

print(cars.columns)
#print(cars['Vehicle Name'])
#print(cars.Weight)
#print(cars.mean())
#print(cars[['Retail Price', 'SUV', 'Weight']])
print(cars[cars["SUV"]==1][['Vehicle Name','Weight','City MPG']].sort(columns=['Weight']).plot(kind='bar'))

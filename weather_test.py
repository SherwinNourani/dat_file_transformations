# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:36:43 2020

@author: 14698
"""

import re
import pandas as pd
import numpy as np

with open(r'C:\Users\14698\iCloudDrive\Documents\Python Files/w_data (5).dat') as w_data:
    text_data = w_data.readlines()

data_split = []

#removing excess rows
for i in text_data:
    if len(i) > 15:
        data_split.append([i])

pre_clean_data = []

#adding values for HHDay and WxType fields
for i in data_split:
    if re.search('\d\s{9,}', str(i)):
        pre_clean_data.append(re.sub('(\s{9,})',' NaN ', str(i)))
    else:
        pre_clean_data.append(i)
        
pre_clean_data2 = []

#adding values for 1HrP field
for i in pre_clean_data:
    if re.search('\s{7}0\.00', str(i)):
        pre_clean_data2.append(re.sub('(\s{7}0\.00)',' NaN 0.00', str(i)))
    else:
        pre_clean_data2.append(i)        

#preparing for clean data
pre_clean_data3 = []
for i in pre_clean_data2:
    pre_clean_data3.append(re.split('\s+', str(i).replace("'","").replace("*","")
                                    .replace("[","").replace("]","").replace(",","").replace("\\n","")))
#re-establishing numeric values
for i in range(len(pre_clean_data3)):
    for x in range(len(pre_clean_data3[i])):
        if re.search('^[^A-Za-z]+$', pre_clean_data3[i][x]):
            pre_clean_data3[i][x] = float(pre_clean_data3[i][x])
#staging temp Nans to Nonetype
for i in range(len(pre_clean_data3)):
    for x in range(len(pre_clean_data3[i])):
        if pre_clean_data3[i][x] == 'NaN':
            pre_clean_data3[i][x] = None

#creating dataframe for analysis of any/all fields       
clean_data = pd.DataFrame(pre_clean_data3)
clean_data.columns = clean_data.iloc[0]
clean_data = clean_data[1:]
clean_data = clean_data.drop(clean_data.columns[0], axis=1)
#final row manually cleaned, Nones converted to NaN
clean_data.iloc[-1] = ['mo', 82.9, 60.5, 71.7, 16, 58.8, None, 0.00, None, None, 6.9, None, None, 5.3, None, None, None]
clean_data.fillna(value=np.nan, inplace=True)


#creating subset of dataframe with relevant fields for analysis
min_spread = clean_data[['Dy']]
min_spread['Spread'] = clean_data['MxT'] - clean_data['MnT']

true_min_spread = min_spread.sort_values(by=['Spread']).head(1)

#Display the final output in the command line
print('\nThe day with the smallest temperature spread is',int(true_min_spread.iloc[0,0]),
      'with a spread of',int(true_min_spread.iloc[0,1]),'degrees.\n')








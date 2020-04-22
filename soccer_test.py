# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:05:33 2020

@author: 14698
"""


import re
import pandas as pd
import numpy as np

with open(r'C:\Users\14698\iCloudDrive\Documents\Python Files/soccer.dat') as soccer_data:
    text_data = soccer_data.readlines()

data_split = []

#removing excess rows
for i in text_data:
    if len(i) > 15 and re.search('\w+', str(i)):
        data_split.append([i])

#removing unneccessary data        
for i in range(len(data_split)):
    data_split[i] = str(data_split[i]).replace("-","").replace("\\n","")
    data_split[i] = re.sub('\d+\.','',str(data_split[i]))

#preparing for clean data    
pre_clean_data = []

for i in data_split:
    pre_clean_data.append(re.split('\s+', str(i).replace("'","")
                                    .replace("[","").replace("]","").replace(",","")))

#re-establishing numeric values
for i in range(len(pre_clean_data)):
    for x in range(len(pre_clean_data[i])):
        if re.search('^[^A-Za-z]+$', pre_clean_data[i][x]):
            pre_clean_data[i][x] = int(pre_clean_data[i][x])
            
#creating dataframe for analysis of any/all fields       
clean_data = pd.DataFrame(pre_clean_data)
clean_data.columns = clean_data.iloc[0]
clean_data = clean_data[1:]
clean_data = clean_data.drop(clean_data.columns[0], axis=1)

#creating subset of dataframe with relevant fields for analysis
min_diff = clean_data[['Team']]
min_diff['Diff'] = abs(clean_data['F'] - clean_data['A'])

true_min_diff = min_diff.sort_values(by=['Diff']).head(1)

#Display the final output in the command line
print('\nThe team with the smallest for/against goal difference is',
      str(true_min_diff.iloc[0,0]).replace("_"," ")+', with a difference of',
      int(true_min_diff.iloc[0,1]),'goal.\n')


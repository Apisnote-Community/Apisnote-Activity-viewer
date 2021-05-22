# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:06:02 2021
@author: t-takizawa
"""
import codecs
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
import ApisnoteActivityDF as aav
############################################
path = "TestFiles/"
stime = '4/21/2021 at 07:00AM'
etime = '4/21/2021 at 10:00AM'
filelist = "list.txt"
fsx = 8
fsy = 2.5
tincmin = 10
############################################
# データ読み込み: APISNOTEのCSVファイル名のリスト
filename = path + filelist
if os.path.isfile(filename):
    print('OK')    
else:
    path = path + '/'
    filename = path + filelist
with codecs.open(filename, 'r', 'utf-8') as f:
    reader = csv.reader(f)
    d = [row for row in reader]
st = datetime.datetime.strptime(stime, '%m/%d/%Y at %I:%M%p')
et = datetime.datetime.strptime(etime, '%m/%d/%Y at %I:%M%p')


# import makeAcitivityArray.py
df = aav.makeActivityArray(d,st,et,tincmin=tincmin,folder=path,action="all")


# Plot Figure #############################
font = {'family':'Yu Gothic'}
plt.rc('font', **font)
index = df.index
index = [s.replace('.csv','') for s in index]
fig, ax = plt.subplots(figsize=(int(fsx), int(fsy)))
heatmap = plt.pcolor(df,cmap = "Oranges")

ax.set_ylim(len(index), 0)
dff = aav.xAxisIndex(df)
#%%
plt.xticks(np.arange(0.5, len(dff.columns), 1), dff.columns.values,rotation=45,ha="right")
plt.yticks(np.arange(0.5, len(df.index), 1), index)
plt.show()

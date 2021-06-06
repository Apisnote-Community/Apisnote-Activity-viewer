# -*- coding: utf-8 -*-
"""
Created on Wed May 26 23:27:04 2021

@author: takiz
"""
import codecs
import csv
import os
import datetime
import ApisnoteActivityDF as aav
import numpy as np
import matplotlib.pyplot as plt
#%%
############################################
path = "C:/Users/takiz/Documents/Working/i.school/2105_ws1aav5/D"
stime = '4/13/2021 at 07:00PM'
etime = '4/30/2021 at 10:00PM'
filelist = "list.txt"
fsx = 20
fsy = 5
tincmin = 20
action = ["add","update"]  # or just "all"
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

#%%
# import makeAcitivityArray.py
df = aav.makeActivityArray(d,st,et,tincmin=tincmin,folder=path,action=action)

maxIdDF = df.idxmax(axis=0)   # Max Acitivity(MA) SheetName List (=index)
LmaxIdDF = len(maxIdDF)
maxValueArray = np.array(df.max(axis=0)).reshape((1,LmaxIdDF))

for i in range(LmaxIdDF):
    if i == 0:
        if maxValueArray[0,0] == 0:
            maxIdDF[0] = ""
    else:
        if maxValueArray[0,i] == 0:
            maxIdDF[i] = maxIdDF[i-1]
#print(maxValueArray[0,5])

index = df.index
index = [s for s in index]
conv = {}
for i in range(len(index)):
    conv[index[i]] = len(index)-i-1
    
maxIdDF2 = maxIdDF.replace(conv)

#%%
fig, ax = plt.subplots(figsize=(int(fsx), int(fsy)))
dff = aav.xAxisIndex(df)
ax.set_xlim(0,len(dff.columns)-1)
plt.xticks(np.arange(len(dff.columns)), dff.columns.values,rotation=45,ha="right")
index = [s.replace('.csv','') for s in index]
index.reverse()
plt.yticks(np.arange(0,len(index)),index,fontname="Yu Gothic")
plt.grid(linestyle='dotted')
print(np.arange(0,len(index)+1),index)
ax.plot(maxIdDF2)



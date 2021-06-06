# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:06:02 2021
@author: t-takizawa
"""
import codecs
import csv
import os
import datetime
import ApisnoteActivityDF as aav
import aav_heatmap as hp
import aav_processmap as pp
#%%
############################################
path = "C:/Users/takiz/Documents/Working/i.school/2105_ws1aav5/D"
stime = '04/13/2021 at 07:00PM'
etime = '04/30/2021 at 10:00PM'
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


# import makeAcitivityArray.py
df = aav.makeActivityArray(d,st,et,tincmin=tincmin,folder=path,action=action)

#%%
# Plot Figure #############################
pp.processmap(df, fsx, fsy)
hp.heatmap(df, fsx, fsy)


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
import ApisnoteActivityDF_longcsvf as aavl
import aav_heatmap as hp
import aav_processmap as pp
#%%
############################################
path = r'\\192.168.0.141\Data\20WS8\2020-10-14B19.11.31i.school20WS8\ApisnoteData'
stime = '10/14/2020 at 07:00PM'
etime = '10/14/2020 at 10:00PM'
filelist = ""
fsx = 10
fsy = 5
tincmin = 20
action = ["add","update"]  # or just "all"
############################################
# データ読み込み: APISNOTEのCSVファイル名のリスト

#%%
if filelist !="":
    filename = path + filelist
    mode = "severalcsv"
    if os.path.isfile(filename):
        print('OK')    
    else:
        path = path + '/'
        filename = path + filelist
    with codecs.open(filename, 'r', 'utf-8') as f:
        reader = csv.reader(f)
        d = [row for row in reader]

else:
    csvlist = os.listdir(path)
    mode = "onecsv"
    d = [[l] for l in csvlist if ".csv" in l ]

st = datetime.datetime.strptime(stime, '%m/%d/%Y at %I:%M%p')
et = datetime.datetime.strptime(etime, '%m/%d/%Y at %I:%M%p')


# import makeAcitivityArray.py
if mode == "severalcsv":
    df = aav.makeActivityArray(d,st,et,tincmin=tincmin,folder=path,action=action)
else:
    df = aavl.makeActivityArrayL(d,st,et,tincmin=tincmin,folder=path,action=action)

#%%
# Plot Figure #############################
pp.processmap(df, fsx, fsy)
hp.heatmap(df, fsx, fsy)


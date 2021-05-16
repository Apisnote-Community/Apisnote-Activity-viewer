# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 23:14:26 2021
@author: takiz
"""
import os
import datetime
import codecs
import csv
import numpy as np
import pandas as pd
def makeActivityArray(d,st,et,tincmin=10,folder="",account="all",action="all",color="all",zeroact=""):
    """
    Make APISNOTE csv files into pandas' DataFrame.
    
    Parameters
    ----------
    d : list
        csv files to be referred / 参照すべきcsvファイルリスト
          ex) [['xxx.csv'],['yyy.csv']]
    st : datetime object
        StartTime.開始時間.
        datetime.strptime()でdatetime objectに直しておく必要あり
    et : datetime object
        EndTime.終了時間.
    tincmin : int
        Time(min) for calclulating mean activity volume
        平均アクティビティ量を計算する時間(分). The default is 10.
    folder : path, optional
        Path for the folder including csv files. The default is "".
          ex) "Apisnote/"
    account : list, optional
        Account list. The default is "all" (all acounts).
          ex) ['xxx@gmail.com']
    action : list, optional
        Action list. The default is "all" (all actions).
          ex) ['link','edit']
    color : list, optional
        Color list. The default is "all" (all colors).
          ex) ['light red','brown']
    zeroact : "" or False, optional
        delete non-zero activity when "".
    Returns
    -------
    df : Pandas' DataFrame
        Mean Volume of APISNOTE Activity per min, calculated by each tincmin
        各シートにおける分当たり平均アクティビティ量.tincmin毎に計算される.
    """
    if folder != "":
        if (folder[-1] != "/"):
            folder = folder + "/"
    
    if action == "all":
        action = ["add","move","edit","update","link","delete"]

    if color == "all":
        color = ["white","light grey","yellow","green","light blue","light red","grey","brown","orange","blue","purple","red"]
    
    d = [x for x in d if x != []]
    print(d)
    
    tincmin = int(tincmin)
    tminc = datetime.timedelta(minutes=tincmin) #平均Activity頻度を計算する時間間隔（10分の平均）
    #timespan(min) for plotting color map
    tinc =datetime.timedelta(minutes=int(tincmin))  
    ntinc =int((et - st)/tinc)
    
    # preparing time list
    t = []    # timelist in "datetime" style
    t1 = []   # timelist in "mm/dd HH:MM"
    i = 0
    while i < ntinc+1:
        t.append(st + tinc*i)
        i += 1
    i = 0
    while i < ntinc:
        t1.append((st+ tinc*i).strftime("%m/%d %H:%M"))
        i += 1
    # Preparing 2dim Array
    act = [[0]*ntinc for i in range(len(d))]
    
    # データ読み込み: APISNOTEのCSVファイルの読み込み
    i = 0
    for x in d:
        fn = folder + x[0]
        with codecs.open(fn, 'r', 'utf-8') as f1:
            reader = csv.reader(f1)
            d1 = [row for row in reader]
        
        del d1[0]
        d1[len(d1)-1].append('')
        dt = pd.DataFrame(d1).T
        dt = dt.replace({None:""})
        accountlist = dt.iloc[1,:]
        actionlist = dt.iloc[2,:]
        colorlist = dt.iloc[4,:]
        tm = dt.iloc[5,:]
        tlist = [datetime.datetime.strptime(x, '%m/%d/%Y at %I:%M%p') for x in tm if x != ""]
        l = len(tm)
        
        # 平均Activity頻度 avact を計算する
        j = 0
        k = 0
        tm2 = t[0]      # section time
        tm3 = tlist[0]  # activity time
        nact = 0
        tm4 = []
        avact = []
        if tlist[-1] > tm2:
            while tm3 < t[0]:
                k += 1
                tm3 = tlist[k]
            while tm2 + tminc < tlist[len(tlist)-1]:
                while (tlist[k] < tm2 + tminc):
                    #count activity
                    if account == "all":
                        if (actionlist[k] in action) & (colorlist[k] in color):
                            nact = nact + 1
                    else:
                        if (actionlist[k] in action) & (colorlist[k] in color) & (accountlist[k] in account):
                            nact = nact + 1
                    tm3 = tlist[k]
                    k += 1
                tm4.append((j,tm2))
                #print(j,tm2,nact)
                avact.append(nact/tincmin)
                nact = 0
                tm2 = tm2 + tminc
                j += 1
        j = 0
        
        # act の準備
        while j < ntinc:
            a = [avact[m] for m,x in tm4 if t[j] <= x and x < t[j+1]]
            if a == []:
                act[i][j] = 0
            else:
                act[i][j] = max(a)
            j += 1
        i += 1
    
    # zero activity の削除
    tact = np.array(act).T
    if zeroact != False:
        i = 0
        while i < len(tact):
            if sum(tact[i]) == 0:
                tact = np.delete(tact, i, 0)
                del t1[i]
                i = i - 1
            i += 1
    
    csvf = []
    for x in d:
        y = x[0].encode('shift_jis')
        csvf.append(y.decode('shift_jis'))
    ttact = np.array(tact).T
    df = pd.DataFrame(data=ttact, index=csvf, columns=t1)
    return df

#%%

def xAxisIndex(df):
    '''
    Make Index Series for x-axis label.
    
    Parameters
    ----------
    df : Pandas' DataFrame
        Output of makeActivityArray().

    Returns
    -------
    dff : Pandas' DataFrame
        reindexed df for x-axis label.
    '''
    col = df.columns
    lcol = len(col)
    dff = df
    for i in range(lcol):
        if i > 0 :
            Cbf = col[i-1]
            Caf = col[i]
            DtCbf = datetime.datetime.strptime(Cbf,"%m/%d %H:%M")
            DtCaf = datetime.datetime.strptime(Caf,"%m/%d %H:%M")
            if DtCaf.date() == DtCbf.date():
                Caf = DtCaf.strftime("%H:%M")
                dff = dff.rename(columns={col[i]:Caf})
    return dff

#%%
"""
os.chdir("C:/Users/takiz/Documents/Working/i.school/2020-10-28B19.20.02test")
d = [["B_ 10_28 再アイディア発想.csv"],["B_ 6 10_28 アイディア精緻化.csv"]]
tincmin = 10
folder = "ApisnoteData/"
st = datetime.datetime.strptime('10/28/2020 at 07:00PM', '%m/%d/%Y at %I:%M%p')
et = datetime.datetime.strptime('10/28/2020 at 10:00PM', '%m/%d/%Y at %I:%M%p')
df = makeActivityArray(d,st,et,tincmin,folder)
"""
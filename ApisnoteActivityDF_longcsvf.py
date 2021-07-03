# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 15:27:47 2021

@author: takiz
"""
import numpy as np
import datetime
import pandas as pd
import codecs
import csv
import ast

def makeActivityArrayL(d,st,et,tincmin=10,folder="",account="all",action="all",color="all",zeroact=""):

    #%%
    if folder != "":
        if (folder[-1] != "/"):
            folder = folder + "/"
        
    if action == "all":
        action = ["add","move","edit","update","link","delete"]
    
    colorIn = color
    if colorIn == "all":
        colorIn = ["white","light grey","yellow","green","light blue","light red","grey","brown","orange","blue","purple","red",
                   "","0","1","2","3","4","5","6","7","8","9","10","11"]
    color = colorIn
    
    d = [x for x in d if x != []]
    #print(d)
    
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
        
    # データ読み込み: APISNOTEのCSVファイルの読み込み
    x = d[0]
    print("file",x)
    fn = folder + x[0]
    with codecs.open(fn, 'r', 'utf-8') as f1:
        reader = csv.reader(f1)
        d1 = [row for row in reader]
    del d1[0]
    d1[len(d1)-1].append('')
    dt = pd.DataFrame(d1)
    dt = dt.sort_values(by=5)
    dt = dt.reset_index(drop=True)
    dt = dt.T
    dt = dt.replace({None:""})
    valuelist   = dt.iloc[0,:] 
    accountlist = dt.iloc[1,:]
    typelist    = dt.iloc[2,:]
    actionlist  = dt.iloc[3,:]
    sheetlist   = dt.iloc[8,:]
    
    # make timelist from csv data
    tm = dt.iloc[5,:]
    tlist = [datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000Z')+datetime.timedelta(hours=9) for x in tm if x != ""]
    
    # Replace action for link and Make color list 
    Ldt = len(actionlist)
    colorlist = ["" for line in actionlist]
    for s in range(Ldt):
        if typelist[s] == "link":
            actionlist[s] = "link"
            colorlist[s] = ""
        
        else:
            Dvalue = valuelist[s].replace("false","0")
            Dvalue = Dvalue.replace("true","1")
            value = ast.literal_eval(Dvalue)
            if "color" in Dvalue:
                colorlist[s] = value["color"]
            else:
                colorlist[s] = ""
    
    #%%
    #i=0
    # 平均Activity頻度 avact を計算する
    j = 0
    k = 0
    tm2 = t[0]      # section time
    tm3 = tlist[0]  # activity time
    nact = np.zeros([1,1]).reshape([1,1])
    tm4 = []
    avact = np.zeros([1,1]).reshape([1,1])
    sheetN = 0
    sheet = []
    r = 0
    
    if tlist[-1] > tm2:
        while tm3 < t[0]:
            k += 1
            tm3 = tlist[k]
        while (tm2 + tminc < tlist[len(tlist)-1]):
            while (tlist[k] < tm2 + tminc):
                #count activity
                if (actionlist[k] in action) & (colorlist[k] in color):
                    if sheet==[]:
                        sheet.append(sheetlist[k])
                        nact[0,0] = 1/tincmin
                        r = 1
                        print(j,tm2)
                        
                    elif sheetlist[k] in sheet:
                        sheetN = sheet.index(sheetlist[k])
                        nact[sheetN,0] = nact[sheetN,0] + 1/tincmin
                        r=2
                    else:
                        sheetN = len(sheet)
                        sheet.append(sheetlist[k])
                        nact = np.append(nact,[[0]],axis=0)
                        nact[sheetN,0] = nact[sheetN,0] + 1/tincmin
                        r=3
                    #print(sheetN,r,nact)
                        
                tm3 = tlist[k]
                k += 1
            tm4.append((j,tm2))
            #print(j,tm2,nact)
            Li_avact = np.size(avact,axis=0)
            Lc_avact = np.size(avact,axis=1)
            Li_nact = np.size(nact,axis=0)
            
            dif = Li_nact - Li_avact
            if dif > 0:
                addarray = np.zeros([dif,Lc_avact]).reshape([dif,Lc_avact])
                #print(addarray,avact)
                print(j,tm2,nact)
                avact = np.append(avact,addarray,axis=0)
            avact = np.append(avact,nact,axis=1)
            nact = np.zeros_like(nact)
            tm2 = tm2 + tminc
            j += 1
    else:
        print("stが範囲外です / st is out of range")
    #%%
    j=0
    
    # act の準備
    Lc_avact = np.size(avact,axis=1)
    Li_avact = np.size(avact,axis=0)
    # avact は[[0]]にappendしているため，最初余計な0が入ってしまう
    if Lc_avact >=ntinc:
        act = avact[:,1:ntinc+1]
    else:
        diff = ntinc - Lc_avact + 1
        addarray = np.zeros([Li_avact,diff]).reshape([Li_avact,diff])
        avact = np.append(avact,addarray,axis=1)
        act = avact[:,1:ntinc+1]
    #print(ntinc,np.size(act,axis=1),len(t1))
    
    #%%
    # zero activity の削除
    tact = np.array(act).T
    if zeroact != False:
        ai = 0
        while ai < len(tact):
            if sum(tact[ai]) == 0:
                tact = np.delete(tact, ai, 0)
                del t1[ai]
                ai = ai - 1
            ai += 1
    
    csvf = []
    for x in sheet:
        y = x.encode('utf-8')
        y = y.decode('utf-8')
        csvf.append(y)
    ttact = np.array(tact).T
    df = pd.DataFrame(data=ttact, index=csvf, columns=t1)
    df = df[(df.T != 0).any()]
    return df
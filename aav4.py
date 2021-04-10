# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:06:02 2021

@author: t-takizawa
"""
import sys
import os
import csv
import pprint
import numpy as np
import matplotlib.pyplot as plt
import datetime
import heapq
import collections
import math
import pandas as pd
import pdb
import codecs
import tkinter
from tkinter import messagebox

def drawaa(folder,filelist,stime,etime,tincmin,fsx,fsy):
    # an3.py 191122 by H.Horii
    # an4.py 201218 by H.Horii
    # a
    # APISNOTE csv ファイルからActivity Heat Mapを作成する
    # >Python a43.py filename stime etime tinc
    
    font = {'family':'Yu Gothic'}
    plt.rc('font', **font)
    
    args = sys.argv
    # filename = args[1]
    filename = folder + filelist
    if os.path.isfile(filename):
        print('OK')    
    else:
        folder = folder + '/'
        filename = folder + '/' + filelist
    # stime = args[2]
    # etime = args[3]
    # tincmin = args[4]
    tinc =datetime.timedelta(minutes=int(tincmin))
    st = datetime.datetime.strptime(stime, '%m/%d/%Y at %I:%M%p')
    et = datetime.datetime.strptime(etime, '%m/%d/%Y at %I:%M%p')
    
    # ntinc: Heatmap の時間（横）軸の分割数
    # ntinc = 50
    #tinc =(et - st)/ntinc
    ntinc =int((et - st)/tinc)
    
    t = []
    t1 = []
    
    i = 0
    while i < ntinc+1:
        t.append(st + tinc*i)
        i += 1
    i = 0
    while i < ntinc:
        t1.append((st+ tinc*i).strftime("%m/%d %H:%M"))
        i += 1
    
    # tminc: 平均Activity頻度を計算する時間間隔（10分の平均）
    tminc = datetime.timedelta(minutes=10)
    
    # データ読み込み: APISNOTEのCSVファイル名のリスト
    with codecs.open(filename, 'r', 'utf-8') as f:
        reader = csv.reader(f)
        d = [row for row in reader]
        
    # アクティビティのHeatmap作成用の二次元配列 act の初期化
    act = [[0]*ntinc for i in range(len(d))]
    
    # データ読み込み: APISNOTEのCSVファイルの読み込み
    i = 0
    for x in d:
        fn = folder + x[0]
        with codecs.open(fn, 'r', 'utf_8') as f1:
            reader = csv.reader(f1)
            d1 = [row for row in reader]
            
        #for z in d1:
        #    print(len(z))
        
        del d1[0]
        d1[len(d1)-1].append('')
    
        dt = np.array(d1).T
        account = dt[1]
        action = dt[2]
        color = dt[4]
        tm = dt[5]
    
        #pdb.set_trace()
    
    
        tm1 = [datetime.datetime.strptime(x, '%m/%d/%Y at %I:%M%p') for x in tm]
    
        # 平均Activity頻度 avact を計算する
        j = 0
        k = 0
        tm2 = tm1[0]
        tm3 = tm2
        nact = 0
        tm4 = []
        avact = []
    
        while tm2 + tminc < tm1[len(tm1)-1]:
            while tm3 < tm2 + tminc:
                nact = nact + 1
                k += 1
                tm3 = tm1[k]
            tm4.append((j,tm2))
            avact.append(nact/10)
            nact = 0
            tm2 = tm2 + tminc
            j += 1
        j = 0
    
        # act の準備
        while j < ntinc:
            a = [avact[m] for m,x in tm4 if t[j] < x and x < t[j+1]]
            if a == []:
                act[i][j] = 0
            else:
                act[i][j] = max(a)
            j += 1
        i += 1
    
    # zero activity の削除
    tact = np.array(act).T
    
    i = 0
    while i < len(tact):
        if sum(tact[i]) == 0:
            tact = np.delete(tact, i, 0)
            del t1[i]
            i = i - 1
        i += 1
    
    
    # HeatMap 作画
    ttact = np.array(tact).T
    
    #csvf = sum(d,[])
    csvf = []
    for x in d:
        y = x[0].encode('shift_jis')
        csvf.append(y.decode('shift_jis'))
    
    #df = pd.DataFrame(data=ttact, columns=t1)
    df = pd.DataFrame(data=ttact, index=csvf, columns=t1)
    
    index = df.index
    index = [s.replace('.csv','') for s in index]
    
    fig, ax = plt.subplots(figsize=(int(fsx), int(fsy)))
    heatmap = plt.pcolor(df,cmap = "Oranges")
    
    ax.set_ylim(len(d), 0)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns.values)
    plt.yticks(np.arange(0.5, len(df.index), 1), index)
    
    plt.show()
    return

##############################################################
# APISNOTE Activity Viewer


root = tkinter.Tk()
root.title(u"APISNOTE Activity Viewer")
root.geometry("440x200")

#ラベル
Static1 = tkinter.Label(text=u'APISNOTE Activity Viewer')
Static1.place(x=10, y=10)

Static2 = tkinter.Label(text=u'Folder')
Static2.place(x=20, y=40)

EditBox1 = tkinter.Entry()
EditBox1.place(x=140, y=40)

Static3 = tkinter.Label(text=u'Ex) D:\\APISNOTE\\')
Static3.place(x=280, y=40)

Static4 = tkinter.Label(text=u'CSV file list')
Static4.place(x=20, y=65)

EditBox2 = tkinter.Entry()
EditBox2.place(x=140, y=65)

Static5 = tkinter.Label(text=u'Ex) list.txt')
Static5.place(x=280, y=65)

Static4 = tkinter.Label(text=u'Starting Datetime')
Static4.place(x=20, y=90)

EditBox3 = tkinter.Entry()
EditBox3.place(x=140, y=90)

Static5 = tkinter.Label(text=u'Ex) 09/30/2020 at 7:53PM')
Static5.place(x=280, y=90)

Static6 = tkinter.Label(text=u'Ending Datetime')
Static6.place(x=20, y=115)

EditBox4 = tkinter.Entry()
EditBox4.place(x=140, y=115)

Static7 = tkinter.Label(text=u'Ex) 12/09/2020 at 08:40PM')
Static7.place(x=280, y=115)

Static8 = tkinter.Label(text=u'Time interval (min)')
Static8.place(x=20, y=140)

EditBox5 = tkinter.Entry()
EditBox5.insert(tkinter.END,"20")
EditBox5.place(x=140, y=140)

Static9 = tkinter.Label(text=u'Ex) 20')
Static9.place(x=280, y=140)

Static10 = tkinter.Label(text=u'Figsize (inch)')
Static10.place(x=20, y=165)

EditBox6 = tkinter.Entry(width=9)
EditBox6.insert(tkinter.END,"27")
EditBox6.place(x=140, y=165)

EditBox7 = tkinter.Entry(width=9)
EditBox7.insert(tkinter.END,"9")
EditBox7.place(x=205, y=165)


#ボタン

Button = tkinter.Button(text=u'Execute', background='DodgerBlue', command=lambda:\
    drawaa(EditBox1.get(),EditBox2.get(),EditBox3.get(),EditBox4.get(),EditBox5.get(),\
    EditBox6.get(),EditBox7.get()))
#Button.bind("<Button-1>",callback) 
Button.place(x=280, y=165)

root.mainloop()



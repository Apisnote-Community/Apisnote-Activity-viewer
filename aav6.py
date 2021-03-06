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
import tkinter

def drawaa(path,filelist,stime,etime,tincmin,color,action,fsx,fsy):
    """
    Function for aav5 GUI.
    
    Parameters
    ----------
    folder : str
        Path where csv files downloaded / csvファイルがあるディレクトリ
    filelist : str
        File name of a csv file list / csvファイルの一覧を記載したtxtファイル
    stime : str
        Starting Time / 開始時間．開始時間と終了時間の間のみ可視化される．
    etime : TYPE
        End Time
    tincmin : int
        Time(min) for calclulating mean activity volume
        平均アクティビティ量を計算する時間(分). The default is 10.
    color : list
        Color list. The default is "all" (all colors).
          ex) ['light red','brown']
    action : list
        Action list. The default is "all" (all actions).
          ex) ['link','edit']
    fsx : float
        Figure size for x direction / x方向図の大きさ
    fsy : float
        Figure size for y direction / y方向図の大きさ

    Returns
    -------
    None.

    """
    # データ読み込み: APISNOTEのCSVファイル名のリスト
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
    print(d,st,et,tincmin,)
    # import makeAcitivityArray.py
    if mode == "severalcsv":
        df = aav.makeActivityArray(d,st,et,tincmin=tincmin,folder=path,action=action)
    else:
        df = aavl.makeActivityArrayL(d,st,et,tincmin=tincmin,folder=path,action=action)
    
    # Plot Figure
    pp.processmap(df, fsx, fsy)
    hp.heatmap(df, fsx, fsy)
    return

##############################################################
# APISNOTE Activity Viewer


root = tkinter.Tk()
root.title(u"APISNOTE Activity Viewer")
root.geometry("440x300")

#ラベル
Static1 = tkinter.Label(text=u'APISNOTE Activity Viewer')
Static1.place(x=10, y=10)

Static2 = tkinter.Label(text=u'Folder')
Static2.place(x=20, y=40)

EditBox1 = tkinter.Entry()
EditBox1.place(x=140, y=40)

Static3 = tkinter.Label(text=u'Ex) D:\\APISNOTE\\')
Static3.place(x=280, y=40)

Static4 = tkinter.Label(text=u'CSV file list*')
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

Static12 = tkinter.Label(text=u'Color')
Static12.place(x=20, y=165)
Static13 = tkinter.Label(text=u'Ex) ["yellow","light blue"]')
Static13.place(x=280, y=165)
EditBox8 = tkinter.Entry()
EditBox8.insert(tkinter.END,"all")
EditBox8.place(x=140, y=165)

Static14 = tkinter.Label(text=u'Action')
Static14.place(x=20, y=190)
Static13 = tkinter.Label(text=u'Ex) ["add","edit"]')
Static13.place(x=280, y=190)
EditBox9 = tkinter.Entry()
EditBox9.insert(tkinter.END,"all")
EditBox9.place(x=140, y=190)

Static10 = tkinter.Label(text=u'Figsize (inch)')
Static10.place(x=20, y=215)

EditBox6 = tkinter.Entry(width=9)
EditBox6.insert(tkinter.END,"27")
EditBox6.place(x=140, y=215)

EditBox7 = tkinter.Entry(width=9)
EditBox7.insert(tkinter.END,"9")
EditBox7.place(x=205, y=215)

Static11 = tkinter.Label(text=u'*No need to fill out when all-worksheets csv is downloaded')
Static11.place(x=20, y=265)



#ボタン

Button = tkinter.Button(text=u'Execute', background='DodgerBlue', command=lambda:\
    drawaa(EditBox1.get(),EditBox2.get(),EditBox3.get(),EditBox4.get(),EditBox5.get(),\
    EditBox8.get(),EditBox9.get(),\
    EditBox6.get(),EditBox7.get()))
#Button.bind("<Button-1>",callback) 
Button.place(x=280, y=215)

root.mainloop()
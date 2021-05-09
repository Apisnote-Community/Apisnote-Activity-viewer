# Apisnote-Activity-viewer
Apisnote-Acitivity-viewer is a tool to visualize Apisnote Activity (Frequency of Acitivity at each sheet) by getting csv data from Apisnote. The user can see active worksheet at the moment you choose.

Latest version is aav5 (only in python file). 


## File Summary

  aav4.exe   :Main exe File
  
  aav4.py    :Python file converted to exe file using PyInstaller 
  
  aav5.py    :New version of Python file (only in python)
  
  ApisnoteActivityDF.py :Python file for aav5.py.


## Python Version for aav5.py

  Python 3.7

## Environment
1) Save "ApisnoteActivityDF.py" in the same folder of "aav5.py"
2) Save APISNOTE csv files and list.txt in the same folder.
3) list.txt should be a list of file names. Put each file name in a new line.
   ex)  xxx.csv
        yyy.csv

# Apisnote 活動可視化ツール(aav)
Apisnote Acitivity viewer は Apisnoteの各worksheetよりダウンロードしたcsvファイルより、どのシートがどの時間帯でよく使われているか可視化するツールです。

最新バージョンはaav5(pythonファイルのみ)です。


## ファイル概要

  aav4.exe   :aav4.pyから作成されたexeファイル。
  
  aav4.py
  
  aav5.py    :最新のApisnote-Acitivity-viewer. ノートの色、アクティビティの種類を選択することが可能に。

  ApisnoteActivityDF.py :aav5.py 用の関数。

## 環境
1) "ApisnoteActivityDF.py"は"aav5.py"と同じディレクトリに保存。
2) csvファイルとlist.txtも同じディレクトリに保存。
3) list.txt にファイル名を列挙。一ファイルごとに改行して記入。
   ex)  xxx.csv
        yyy.csv


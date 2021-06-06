# Apisnote-Activity-viewer
Apisnote-Acitivity-viewer is a tool to visualize Apisnote Activity (Frequency of Acitivity at each sheet) by getting csv data from Apisnote. The user can see active worksheet at the moment you choose.

Latest version is aav5 (only in python file). 


## File Summary
  aav5.exe   :Main exe File
  
  aav5.py    :New version of Python file converted to exe file using PyInstaller 
  
  ApisnoteActivityDF.py :Python File. Make APISNOTE activity DataFrame for aav5.py

  aav_heatmap.py　:Python File. Show heatmap for aav5.py

  aav_processmap.py :Python File. Show processmap for aav5.py


## Python Version for aav5.py
  Python 3.7

## Steps for aav5
1) Save "ApisnoteActivityDF.py" in the same folder of "aav5.py"
2) Save APISNOTE csv files and list.txt in the same folder.
3) list.txt should be a list of file names. Put each file name in a new line. If you want to set colors of note to be visualized, add color name with ",".

   ex) In the list.txt
    
    xxx.csv
    
    yyy.csv,yellow,blue

# Apisnote 活動可視化ツール(aav)
Apisnote Acitivity viewer は Apisnoteの各worksheetよりダウンロードしたcsvファイルより、どのシートがどの時間帯でよく使われているか可視化するツールです。

最新バージョンはaav5(pythonファイルのみ)です。


## ファイル概要
  aav5.exe   :aav5.pyから作成されたexeファイル。
 
  aav5.py    :最新のApisnote-Acitivity-viewer. ノートの色、アクティビティの種類を選択することが可能に。
 
  ApisnoteActivityDF.py :aav5.py 用の関数。APISNOTEの活動量を記録したDataFrameを出力。

  aav_heatmap.py　:aav5.py 用の関数。heatmapを描画する。

  aav_processmap.py :aav5.py 用の関数。processmap(折れ線グラフ）を描画する。

## 手順
1) "ApisnoteActivityDF.py"は"aav5.py"と同じディレクトリに保存(exe版の場合不要）。
2) csvファイルとlist.txtをpython/exeファイルと同じディレクトリに保存。
3) list.txt にファイル名を列挙。１ファイルごとに改行して記入。ノートの色指定を行う場合は，csv名のあとに",yellow"などと追記する．

   ex) 例えばlist.txtの1-2行目に以下のように記載
   
      xxx.csv
      
      yyy.csv,yellow,blue
4) 実行

## Quick Startはこちらから
https://qiita.com/ApisnoteDevelopers/items/1ec7fb9886af71f991d1

# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 14:21:31 2021

@author: takiz
"""
import numpy as np
import matplotlib.pyplot as plt
import ApisnoteActivityDF as aav
def processmap(df,fsx,fsy):
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
    print("p:",index)
    ax.plot(maxIdDF2)
    #plt.show()
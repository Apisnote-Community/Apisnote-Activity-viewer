# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import ApisnoteActivityDF as aav

#cmap customize
def heatmap(df,fsx,fsy,vmax=""):
    """
    To make heatmap figure for APISNOTE Activity viewer

    Parameters
    ----------
    df : Pandas DataFrame
        Output of makeActivityArray()
    fsx : float
        Figure size for x axis
    fsy : float
        Figure size for y axis
    vmax : float
        Palameter for heatmap.

    Returns
    -------
    None.

    """
    cmap = cm.Oranges
    cmap_data = cmap(np.arange(cmap.N))
    cmap_data[0,3] = 0
    customized_orange = colors.ListedColormap(cmap_data)
    
    font = {'family':'Yu Gothic'}
    plt.rc('font', **font)
    index = df.index
    index = [s.replace('.csv','') for s in index]
    fig, ax = plt.subplots(figsize=(int(fsx), int(fsy)))
    if vmax == "":
        heatmap = plt.pcolor(df,cmap = customized_orange,vmin=0)
    else:
        heatmap = plt.pcolor(df,cmap = customized_orange,vmax=vmax,vmin=0)
    
    ax.set_ylim(len(index), 0)
    dff = aav.xAxisIndex(df)
    
    plt.xticks(np.arange(0.5, len(dff.columns), 1), dff.columns.values,rotation=45,ha="right")
    plt.yticks(np.arange(0.5, len(index)), index)
    print("h:",index)
    plt.show()
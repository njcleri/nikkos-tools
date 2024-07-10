import os
import numpy as np
import pandas as pd
import matplotlib as mpl

def find_nearest(array, target_value):
    '''
    Finds the nearest value in an array to the target value
    '''
    array = np.asarray(array)
    idx = (np.abs(array - target_value)).argmin()
    
    return array[idx]


def generate_colors_from_colormap(cmap, ncolors):
    '''
    Generates a list of evenly spaced colors from a colormap
    '''
    normalized_cmap = mpl.colors.Normalize(vmin=0,vmax=1)
    colormap = mpl.colormaps[cmap]
    colors = np.linspace(0.1, 0.9, num=ncolors)
    
    return colormap(normalized_cmap(colors))


def make_directories(path):
    '''
    Makes directories directories/parent directories given a path
    '''
    try:
        os.makedirs(path)
        print("Folder %s created!" % path)
    except FileExistsError:
        print("Folder %s already exists" % path)
        
    return path
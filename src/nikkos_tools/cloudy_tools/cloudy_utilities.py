import numpy as np
import pandas as pd

def clean_cloudy_line_file(filename):
    '''
    My method for making cloudy line emissivity files more user friendly. 
    To pull emissivities for a given line from each grid step, 
    read in the df and use df.loc['HE_2_1640.00A'] format. 
    '''
    df = pd.read_csv(filename, sep='\t+', header=None, comment='#')
    df = df[df.index.str.contains('iteration') == False]
    df.index = df.index.str.replace('  ', '_')
    df.index = df.index.str.replace(' ', '_')
    df.index = df.index.str[:-1]
    
    return df


def clean_cloudy_con_file(filename):
    '''
    My method for making cloudy continuum files which are run on a single grid
    more user friendly. 
    '''
    df = pd.read_csv(filename, delimiter='\t+', comment='##')
    df.rename(columns={'#Cont  nu':'wave'}, inplace=True)
    df['step'] = np.zeros(len(df['wave']))
    df['step'] = pd.qcut(df.index, int(len(df['wave'])/df['wave'].nunique()))
    df['step'] = df['step'].cat.rename_categories(np.arange(0,len(df['step'].unique())))
    
    return df
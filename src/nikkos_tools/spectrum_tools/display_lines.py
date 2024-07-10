import pandas as pd
from pathlib import Path
BASE_PATH = Path(__file__).parent
LINESDF_PATH = (BASE_PATH / "linesdf.csv").resolve()


def generate_default_axvspan_kwargs():
    axvspan_kwargs = {
        'color':'k',
        'ec':None,
        'alpha':0.1,
    }
    return axvspan_kwargs


def generate_default_text_kwargs():
    text_kwargs = {
        'fontsize':15,
        'rotation':'vertical',
        'verticalalignment':'top'
    }
    return text_kwargs


def load_lines(file=LINESDF_PATH):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        print('FileNotFoundError: lines file not found')


def display_lines_air(ax, vertical_anchor, lines_to_show=[], redshift=0, 
                      wavelength_per_angstrom=1, width=20, show_text=False, lines_file=LINESDF_PATH, axvspan_kwargs={}, text_kwargs={}):
    linesdf = load_lines(lines_file)
    axvspan_kwargs = generate_default_axvspan_kwargs() | axvspan_kwargs
    text_kwargs = generate_default_text_kwargs() | text_kwargs
    
    for line in lines_to_show:
        line_data = linesdf[linesdf.line == line]
        wave_min = (line_data.wavelength_air.values[0]-width/2)*wavelength_per_angstrom*(1+redshift)
        wave_max = (line_data.wavelength_air.values[0]+width/2)*wavelength_per_angstrom*(1+redshift)
        offset = line_data.offset.values[0]*wavelength_per_angstrom*(1+redshift)
        label = line_data.label.values[0]
        if type(label) != str:
            label = ''

        ax.axvspan(wave_min, wave_max, **axvspan_kwargs)
        if show_text and (offset > 0):
            ax.text(wave_max, vertical_anchor, f'{label}', horizontalalignment='left', **text_kwargs)
        
        if show_text and (offset < 0):
            ax.text(wave_min, vertical_anchor, f'{label}', horizontalalignment='right', **text_kwargs)
       
            
def display_lines_air(ax, vertical_anchor, lines_to_show=[], redshift=0, 
                      wavelength_per_angstrom=1, width=20, show_text=False, lines_file=LINESDF_PATH, axvspan_kwargs={}, text_kwargs={}):
    linesdf = load_lines(lines_file)
    axvspan_kwargs = generate_default_axvspan_kwargs() | axvspan_kwargs
    text_kwargs = generate_default_text_kwargs() | text_kwargs
    
    for line in lines_to_show:
        line_data = linesdf[linesdf.line == line]
        wave_min = (line_data.wavelength_vacuum.values[0]-width/2)*wavelength_per_angstrom*(1+redshift)
        wave_max = (line_data.wavelength_vacuum.values[0]+width/2)*wavelength_per_angstrom*(1+redshift)
        offset = line_data.offset.values[0]*wavelength_per_angstrom*(1+redshift)
        label = line_data.label.values[0]
        if type(label) != str:
            label = ''

        ax.axvspan(wave_min, wave_max, **axvspan_kwargs)
        if show_text and (offset > 0):
            ax.text(wave_max, vertical_anchor, f'{label}', horizontalalignment='left', **text_kwargs)
        
        if show_text and (offset < 0):
            ax.text(wave_min, vertical_anchor, f'{label}', horizontalalignment='right', **text_kwargs)
            
            
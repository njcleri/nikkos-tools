import pandas as pd
from nikkos_tools import physics_functions as pf
from pathlib import Path
BASE_PATH = Path(__file__).parent
LINESDF_PATH = (BASE_PATH / "linesdf.csv").resolve()


def generate_default_line_list():
    lines = {
        'Lya': [1215.67, 'Ly$\\alpha$', -1],
        'NV': [1240, 'NV', 1],
        'CIV_1548': [1548, 'CIV', -1],
        'HeII_1640': [1640.4, 'HeII', 1],
        'OIII_1664': [1664, 'OIII]', 1],
        'SiIII_1883': [1883, 'SiIII]', -1],
        'CIII_1907': [1906.8, 'CIII]', 1],
        'MgII_2798': [2798, 'MgII', 1],
        'NeV_3346': [3346, '', -1],
        'NeV_3426': [3426, '[NeV]', -1],
        'OII_3727': [3727, '[OII]', -1],
        'NeIII_3869': [3869, '[NeIII]', 1],
        'Hdelta': [4102, 'H$\\delta$', 1],
        'Hgamma': [4341, 'H$\\gamma$', -1],
        'OIII_4363': [4363, '[OIII]', 1],
        'HeII_4686': [4686, 'HeII', -1],
        'Hbeta': [4861, 'H$\\beta$', -1],
        'OIII_4959': [4959, '', 1],
        'OIII_5007': [5007, '[OIII]', 1],
        'HeI': [5876, 'HeI', -1],
        'Halpha': [6563, 'H$\\alpha$', -1],
        'SII_6716': [6716, '', -1],
        'SII_6731': [6731, '[SII]', -1]
    }
    return lines


def make_linesdf(save_path=LINESDF_PATH):
    linesdf = (pd.DataFrame(generate_default_line_list())
            .T
            .reset_index()
            .rename(columns={'index':'line', 0:'wavelength_air', 1:'label', 2:'offset'})
            .assign(wavelength_vacuum = lambda x: pf.convert_wavelength_air_to_vacuum(x.wavelength_air))
            )
    linesdf.to_csv(save_path, index=False)
    
    
def load_lines(file=LINESDF_PATH):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        print('FileNotFoundError: lines file not found')
    
    
def generate_new_line_data_air(line, wavelength, label, offset):
    new_line = pd.DataFrame([{
        'line':line,
        'wavelength_air':wavelength,
        'label':label,
        'offset':offset,
        'wavelength_vacuum': pf.convert_wavelength_air_to_vacuum(wavelength)
        }])
    return new_line

    
def generate_new_line_data_vacuum(line, wavelength, label, offset):
    new_line = pd.DataFrame([{
        'line':line,
        'wavelength_air':pf.convert_wavelength_vacuum_to_air(wavelength),
        'label':label,
        'offset':offset,
        'wavelength_vacuum': wavelength
        }])
    return new_line

    
def add_line_air(line,wavelength_air,label,offset=1):
    new_line = generate_new_line_data_air(line,wavelength_air,label,offset)
    linesdf = load_lines()
    
    if line in linesdf.line.values:
        print(f'{line} already exists. Overwriting data for {line}.')
        linesdf = linesdf[linesdf.line != line]
    
    linesdf = pd.concat([linesdf, new_line], ignore_index=True)
    linesdf.to_csv(LINESDF_PATH, index=False)
    return linesdf
    

def add_line_vacuum(line,wavelength_vacuum,label,offset=1):
    new_line = generate_new_line_data_vacuum(line,wavelength_vacuum,label,offset)
    linesdf = load_lines()
    
    if line in linesdf.line.values:
        print(f'{line} already exists. Overwriting data for {line}.')
        linesdf = linesdf[linesdf.line != line]
    
    linesdf = pd.concat([linesdf, new_line], ignore_index=True)
    linesdf.to_csv(LINESDF_PATH, index=False)
    return linesdf
    
    
if __name__ == '__main__':
    remake_linesdf = input('Reset linesdf to default? (y/n): ')
    if remake_linesdf.lower() == 'y':
        make_linesdf()
    
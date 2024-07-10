import numpy as np
import glob
import os
import stat

class CloudyModel:
    """For making Cloudy .in files"""
    
    def __init__(self, linelist='LineList_NJC.dat', wavelength_units='angstroms'):
        self.model = []
        self.linelist = linelist
        self.wavelength_units = wavelength_units
        
    def set_model_parameter(self, model_parameter):
        self.model.append(model_parameter)
    
    def delete_model_parameter(self, model_parameter):
        self.model = [item for item in self.model if item not in model_parameter]
        
    def add_grid(self, parameter, start, stop, step, initial_value=0):
        self.set_model_parameter(f'{parameter} {initial_value} vary')
        self.set_model_parameter(f'grid {start} to {stop} step {step}')
        
    def set_other(self, *args):
        for arg in args:
            self.set_model_parameter(f'{arg}')
        
    def set_sed(self, sed):
        self.sed = sed
        self.set_model_parameter(f'table SED "{sed}"')
        
    def set_star(self, sed, age, stellar_metallicity_solar, log_age=True):
        """Note: this requires intensity/luminosity/ionization parameter to be set or else Cloudy will break"""
        if not log_age:
            self.sed = f'{sed.rstrip(".ascii")}_age{np.round(np.log10(age), decimals=2)}_zstar{np.round(stellar_metallicity_solar, decimals=4)}'
            z_absolute = np.round(np.log10(0.02*stellar_metallicity_solar), decimals=4)
            self.set_model_parameter(f'table star "{sed}" {age} {z_absolute}')
            return
        self.sed = f'{sed}_age{age}_zstar{np.round(stellar_metallicity_solar, decimals=4)}'
        z_absolute = np.round(np.log10(0.02*stellar_metallicity_solar), decimals=2)
        self.set_model_parameter(f'table star "{sed}" {10**age} {z_absolute}')

    def set_hden(self, hden):
        """Cloudy will break if there is no hden set"""
        self.hden = hden
        self.set_model_parameter(f'hden {hden}')
        
    def set_ionization_parameter(self, logU):
        self.logU = logU
        self.set_model_parameter(f'ionization parameter {logU}')
    
    def set_geometry(self, geometry):
        self.geometry = geometry
        self.set_model_parameter(f'{geometry}')
        
    def set_abundance_pattern(self, abundance_pattern, grains='no grains'):
        self.abundance_pattern = abundance_pattern
        self.set_model_parameter(f'abundances {abundance_pattern} {grains}')
        
    def set_grains(self, grains):
        self.grains = grains
        self.set_model_parameter(f'grains {grains}')
        
    def set_metals_and_grains(self, gas_metallicity):
        self.gas_metallicity = gas_metallicity
        self.set_model_parameter(f'metals and grains {gas_metallicity}')
        
    def set_element_scale_factor(self, element, element_scale_factor):
        self.set_model_parameter(f'element scale factor {element} {element_scale_factor}')
        
    def save_overview(self):
        self.set_model_parameter(f'save overview ".ovr" last')
        
    def save_continuum(self):
        self.set_model_parameter(f'save continuum units {self.wavelength_units} ".con" last')
    
    def save_lines_emergent(self):
        self.set_model_parameter(f'save linelist column emergent absolute last units {self.wavelength_units} ".elin" "{self.linelist}"')
        
    def save_lines_intrinsic(self):
        self.set_model_parameter(f'save linelist column intrinsic absolute last units {self.wavelength_units} ".ilin" "{self.linelist}"')
        
    def save_all(self):
        self.save_overview()
        self.save_continuum()
        self.save_lines_emergent()
        self.save_lines_intrinsic()
        
    def build_default_model(self, sed='NGC5548.sed', logU=-1, hden=2, abundance_pattern='gass10', grains='Orion', gas_metallicity=1.0):
        self.model = []
        self.set_sed(sed)
        self.set_hden(hden)
        self.set_abundance_pattern(abundance_pattern)
        self.set_grains(grains)
        self.set_metals_and_grains(gas_metallicity)
        self.set_ionization_parameter(logU)
        self.set_model_parameter('iterate_to_convergence')
        self.save_all() 
        
    def build_cleri_agn_model(self, sed='NGC5548.sed', hden=2, abundance_pattern='gass10', grains='Orion', gas_metallicity=1.0, element_scale_factor_dict={}, logU=-4):
        self.model = []
        self.set_sed(sed)
        self.set_hden(hden)
        self.set_abundance_pattern(abundance_pattern)
        self.set_grains(grains)
        self.set_metals_and_grains(gas_metallicity)
        for element in element_scale_factor_dict.keys():
            self.set_element_scale_factor(element, element_scale_factor_dict.get(element))
        self.set_ionization_parameter(logU)
        # self.add_grid('ionization parameter', -4, -1, 0.25)
        # self.set_model_parameter('iterate_to_convergence')
        self.save_all()   
        
    def build_template_model_bpass_gridU(self, sed="BPASSv2.2.1_imf135_300_burst_binary.ascii", age=1e7, stellar_metallicity=-1, 
                                  hden=2, abundance_pattern='gass10', grains='Orion', gas_metallicity=1.0, element_scale_factor_dict={}):
        self.model = []
        self.set_star(sed, age, stellar_metallicity)
        self.set_hden(hden)
        self.set_abundance_pattern(abundance_pattern)
        self.set_grains(grains)
        self.set_metals_and_grains(gas_metallicity)
        for element in element_scale_factor_dict.keys():
            self.set_element_scale_factor(element, element_scale_factor_dict.get(element))
        self.add_grid('ionization parameter', -4, -1, 0.25)
        self.set_model_parameter('iterate_to_convergence')
        self.save_all()   
    
    def build_template_model_bpass(self, sed="BPASSv2.2.1_imf135_300_burst_binary.ascii", age=1e7, stellar_metallicity=-1, logU=-4,
                                  hden=2, abundance_pattern='gass10', grains='Orion', gas_metallicity=1.0, element_scale_factor_dict={}):
        self.model = []
        self.set_star(sed=sed, age=age, stellar_metallicity_solar=stellar_metallicity)
        self.set_hden(hden)
        self.set_abundance_pattern(abundance_pattern)
        self.set_grains(grains)
        self.set_metals_and_grains(gas_metallicity)
        for element in element_scale_factor_dict.keys():
            self.set_element_scale_factor(element, element_scale_factor_dict.get(element))
        self.set_ionization_parameter(logU)
        self.set_model_parameter('iterate_to_convergence')
        self.save_all()  
        
    def make_cloudy_in_file(self, path='.', use_params=True, comment=None):
        if not use_params:
            np.savetxt(f'{path}/{comment}.in', self.model, fmt='%s')
            return 
        
        if comment:
            np.savetxt(f'{path}/sed{self.sed}_hden{self.hden}_z{self.gas_metallicity}_logU{self.logU}_{comment}.in', self.model, fmt='%s')
        else:
            np.savetxt(f'{path}/sed{self.sed}_hden{self.hden}_z{self.gas_metallicity}_logU{self.logU}.in', self.model, fmt='%s')
            
   
def make_cloudy_executable(path, executable_name, cloudy_run_script_name='run_cloudy'):
    files = glob.glob(f'{path}/**.in')
    lines = [f'{cloudy_run_script_name} {file.rstrip(".in")}' for file in files]
    np.savetxt(f'{path}/{executable_name}.exe', lines, fmt='%s')
    os.chmod(f'{path}/{executable_name}.exe', stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_IRUSR | stat.S_IWUSR)
        
        
        
        
        
        
        
import numpy as np
import astropy.units as u
from astropy import constants as const
from astropy.cosmology import WMAP9 as cosmo 
from astropy.units import cds
cds.enable() 

def redshift(rest_wavelength, redshift):
    return rest_wavelength * (1 + redshift)


def deredshift(observed_wavelength, redshift):
    return observed_wavelength / (1 + redshift)


def get_redshift_from_observed_wavelength(observed_wavelength, rest_wavelength):
    return observed_wavelength/rest_wavelength - 1


def get_wavelength_from_ev(energy_eV):
    '''
    Takes photon energy in eV and returns corresponding wavelength in Angstroms
    '''
    return (const.h*const.c/(energy_eV*u.eV)).to(u.Angstrom).value


def get_ev_from_wavelength(wave_A):
    '''
    Takes photon wavelength in Angstroms and returns energy in eV
    '''
    return (const.h*const.c/(wave_A*u.Angstrom)).to(u.eV).value
  
  
def convert_wavelength_air_to_vacuum(lam_air):
    '''
    Convert from air wavelength to vacuum wavelength
    '''
    s = 10**4/lam_air 
    n = 1 + 0.00008336624212083 + 0.02408926869968 / (130.1065924522 - s**2) + 0.0001599740894897 / (38.92568793293 - s**2)
    return lam_air*n


def convert_wavelength_vacuum_to_air(lam_vac):
    '''
    Convert from air wavelength to vacuum wavelength
    '''
    s = 10**4/lam_vac 
    n = 1 + 0.0000834254 + 0.02406147 / (130 - s**2) + 0.00015998 / (38.9 - s**2)
    return lam_vac/n


def get_luminosity(z, flux_cgs):
    '''
    Returns luminosity in ergs/s given redshift and flux in erg/s/cm^2
    '''
    return (4*np.pi*(cosmo.luminosity_distance(z).to(u.cm))**2*(flux_cgs*u.erg*u.cm**-2*u.s**-1)).to(u.erg/u.s)


def get_log_luminosity(z, flux_cgs):
    '''
    Returns base 10 log(luminosity) in ergs/s given redshift and flux in erg/s/cm^2
    '''
    return np.log10(((4*np.pi*(cosmo.luminosity_distance(z).to(u.cm))**2*(flux_cgs*u.erg*u.cm**-2*u.s**-1)).to(u.erg/u.s)).value)


def get_star_formation_rate_from_flux(z, flux_cgs, constant=41.27):
    '''
    Returns star formation rate in M_solar/year as a dimensionless quantity from the
    Schmidt Law given redshift, flux in erg/s/cm^2 and the corresponding
    constant for the given emission line. The default value 41.27 is 
    the Kennicutt and Evans 2012 calibration from Halpha SFR.
    '''
    return np.log10(((4*np.pi*(cosmo.luminosity_distance(z).to(u.cm))**2*(flux_cgs*u.erg*u.cm**-2*u.s**-1)).to(u.erg/u.s)).value) - constant


def get_star_formation_rate_from_luminosity(luminosity_cgs, constant=41.27):
    '''
    Returns SFR in M_solar/year as a dimensionless quantity from the
    Schmidt Law given luminosity in erg/s and the corresponding
    constant for the given emission line. The default value 41.27 is 
    the Kennicutt and Evans 2012 calibration from Halpha SFR.
    '''
    return np.log10(luminosity_cgs) - constant


def get_Lx_from_flux(log_fluxs, zs, gam=1.6, Lx_Elo=2., Lx_Eup=10., \
            flux_Elo=2., flux_Eup=7.):
    '''
    Convert flux to Lx (does not consider obscuration)
    Input:
        log_fluxs, the observed flux (cgs)
        zs, redshift
    Keyword:
        gam, the assumed photon index
        Lx_Elo, Lx_Eup, the energy range for the input Lx
        flux_Elo, flux_Eup, the energy range for the output flux
    Output:
        logLxs, log(Lx) (erg/s)
    '''
    log_fluxs = np.array(log_fluxs)
    zs = np.array(zs)
    # Luminosity distance, units: cm
    #logDls = np.interp(zs, z_grids_for_interp, logDl_grids_for_interp)
    logDls = np.log10(cosmo.luminosity_distance(zs).to(u.cm).value)
    # K correction, for the effect of redshift
    K_cor = (1+zs)**(gam-2.)
    # Convert to the Lx of the observed E range
    # call as "E correction"
    if gam==2:
        E_cor = np.log(flux_Eup/flux_Elo) / np.log(Lx_Eup/Lx_Elo)
    else:
        E_cor = (flux_Eup**(2-gam)-flux_Elo**(2-gam)) / \
                (Lx_Eup**(2-gam)-Lx_Elo**(2-gam))
    # Calculate the luminosity
    logLxs = log_fluxs+2*logDls+np.log10(4*np.pi)-np.log10(E_cor)+np.log10(K_cor)
    # Done
    return logLxs



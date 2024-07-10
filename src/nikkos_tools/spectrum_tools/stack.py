import numpy as np


def stack_spectra_without_weighting(wavelengths_list, fluxes_list):
    """
    Stack spectra without weighting them at each wavelength.

    Parameters:
    - wavelengths_list: List of numpy arrays, each containing wavelengths for a spectrum.
    - fluxes_list: List of numpy arrays, each containing fluxes for a spectrum.
    - flux_uncertainties_list: List of numpy arrays, each containing flux uncertainties for a spectrum.

    Returns:
    - Stacked wavelength array: A numpy array representing the common wavelength grid.
    - Stacked flux array: A numpy array representing the stacked flux spectrum without weighting.
    """

    # Check if input lists have the same length
    num_spectra = len(wavelengths_list)
    if len(fluxes_list) != num_spectra:
        raise ValueError("Input lists must have the same length.")

    # Determine the minimum and maximum wavelengths across all spectra
    min_wavelength = min(np.min(wavelengths) for wavelengths in wavelengths_list)
    max_wavelength = max(np.max(wavelengths) for wavelengths in wavelengths_list)

    # Create a common wavelength grid
    common_wavelengths = np.linspace(min_wavelength, max_wavelength, num=len(wavelengths_list[0]))

    # Initialize arrays for the stacked flux
    stacked_flux = np.zeros_like(common_wavelengths)

    # Iterate through each spectrum and its properties
    for wavelengths, fluxes in zip(wavelengths_list, fluxes_list):
        # Interpolate the fluxes onto the common wavelength grid
        interpolated_flux = np.interp(common_wavelengths, wavelengths, fluxes, left=0, right=0)
    
        interpolated_flux = np.where(interpolated_flux >=-1e-6, interpolated_flux, -1e-6)
    

        # Add the interpolated flux to the stacked spectrum
        stacked_flux += interpolated_flux

    return common_wavelengths, stacked_flux/len(wavelengths_list)
    # return common_wavelengths, stacked_flux
    

def stack_spectra_weighted_by_inverse_variance(wavelengths_list, fluxes_list, flux_uncertainties_list):
    """
    Stack spectra weighted by their inverse variance at each wavelength.

    Parameters:
    - wavelengths_list: List of numpy arrays, each containing wavelengths for a spectrum.
    - fluxes_list: List of numpy arrays, each containing fluxes for a spectrum.
    - flux_uncertainties_list: List of numpy arrays, each containing flux uncertainties for a spectrum.

    Returns:
    - Stacked wavelength array: A numpy array representing the common wavelength grid.
    - Stacked flux array: A numpy array representing the weighted stacked flux spectrum.
    """

    # Check if input lists have the same length
    num_spectra = len(wavelengths_list)
    if len(fluxes_list) != num_spectra or len(flux_uncertainties_list) != num_spectra:
        raise ValueError("Input lists must have the same length.")

    # Determine the minimum and maximum wavelengths across all spectra
    min_wavelength = min(np.min(wavelengths) for wavelengths in wavelengths_list)
    max_wavelength = max(np.max(wavelengths) for wavelengths in wavelengths_list)

    # Create a common wavelength grid
    common_wavelengths = np.linspace(min_wavelength, max_wavelength, num=len(wavelengths_list[0]))

    # Initialize arrays for the weighted sum and the total inverse variance
    weighted_sum = np.zeros_like(common_wavelengths)
    total_inverse_variance = np.zeros_like(common_wavelengths)

    # Iterate through each spectrum and its properties
    for wavelengths, fluxes, flux_uncertainties in zip(wavelengths_list, fluxes_list, flux_uncertainties_list):
        # Interpolate the fluxes and flux uncertainties onto the common wavelength grid
        interpolated_flux = np.interp(common_wavelengths, wavelengths, fluxes, left=0, right=0)
        interpolated_flux_uncertainties = np.interp(common_wavelengths, wavelengths, flux_uncertainties, left=0, right=0)

        # Calculate inverse variance for each data point
        interpolated_flux_uncertainties = np.where(interpolated_flux_uncertainties !=0, interpolated_flux_uncertainties, 10**1)
        interpolated_flux = np.where(interpolated_flux >=-1e-6, interpolated_flux, -1e-6)

        inverse_variance = 1 / (interpolated_flux_uncertainties ** 2)

            
        # Update the weighted sum and total inverse variance
        weighted_sum += interpolated_flux * inverse_variance
        total_inverse_variance += inverse_variance

    # Calculate the stacked flux spectrum by dividing the weighted sum by the total inverse variance
    stacked_flux = weighted_sum / total_inverse_variance

    return common_wavelengths, stacked_flux

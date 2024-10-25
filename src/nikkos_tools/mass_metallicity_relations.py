import numpy as np

def maiolino__2008(log_metallicity):
    return 0.7462 - 0.7149*log_metallicity - 0.9401*log_metallicity**2 - 0.6154*log_metallicity**3 - 0.2524*log_metallicity**4


def curti_2017(log_metallicity):
    return 0.527 - 1.569*log_metallicity - 1.652*log_metallicity**2 - 0.421*log_metallicity**3


def strom_2018(log_metallicity):
    return -((log_metallicity - 8.24)**2 - 0.85)/0.87


def kewley_2019(log_R23, logU=-2):
    return 9.7757 - 0.5059*log_R23 + 0.9707*logU - 0.1744*log_R23*logU - 0.0255*log_R23**2 + 0.3838*logU**2 - 0.0378*log_R23*logU**2 + 0.0806*log_R23**2*logU - 0.0852*log_R23**3 + 0.0462*logU**3


def papovich_2022(log_metallicity):
    return -1.07*(log_metallicity - 8.228)**2 + 1.041

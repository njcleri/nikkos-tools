import numpy as np

def propagate_uncertainty_addition(a_uncertainty, b_uncertainty):
    '''
    Returns the propagated uncertainty of a+b
    '''
    return np.sqrt(a_uncertainty**2 + b_uncertainty**2)


def propagate_uncertainty_division(a, a_uncertainty, b, b_uncertainty):
    '''
    Returns the propagated uncertainty of a ratio a/b
    '''
    return np.abs(a/b) * np.sqrt((a_uncertainty/a)**2 + (b_uncertainty/b)**2)


def propagate_uncertainty_log10(x, x_uncertainty):
    '''
    Returns uncertainty in log(x) given x and uncertainty in x
    '''
    return 0.434*x_uncertainty/x


def propagate_log_ratio_uncertainty(a, a_uncertainty, b, b_uncertainty):
    '''
    Returns uncertainty in log(a/b)
    '''
    return propagate_uncertainty_log10(a/b, propagate_uncertainty_division(a=a, a_uncertainty=a_uncertainty, b=b, b_uncertainty=b_uncertainty))

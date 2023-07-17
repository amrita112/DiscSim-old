import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

def get_n_samples(t_green = 0.3, t_red = 0.7, accuracy = 0.02, confidence = 0.9, tolerance = 0.001, n_high = 10000, n_low = 2, suppress_warnings = False):
    
    '''
    Return the number of samples required to accurately estimate discrepancy scores for discrete variables.
    
    Inputs:
    t_green (float between 0 and 1, default 0.3): Threshold for classifying workers in 'green band'. Discrepancy scores < t_green will be classified as green band.
    t_red (float between 0 and 1, default 0.7): Threshold for classifying workers in 'red band'. Discrepancy scores > t_red will be classified as red band.
    accuracy (float between 0 and 1, default 0.02): Distance from threshold at which confidence guarantee applies. 
    confidence (float between 0 and 1, default 0.9): Desired probability of correctly classifying workers as green band or red band.
    tolerance (float between 0 and 1, default 0.001): Distance from desired probability at which binary search of number of samples is stopped.
    n_high (int, default 10,000): Maximum possible number of samples for initializing binary search
    n_low (int, default 1): Minimum possible number of samples for initializing binary search
    
    '''
    p_high_green = binom.cdf(int(t_green*n_high), n_high, t_green - accuracy)
    p_low_green = binom.cdf(int(t_green*n_low), n_low, t_green - accuracy)

    p_high_red = 1 - binom.cdf(int(t_red*n_high), n_high, t_red + accuracy)
    p_low_red = 1 - binom.cdf(int(t_red*n_low), n_low, t_red + accuracy)
    
    if not np.logical_and(p_high_green > confidence, p_high_red > confidence):
        if not suppress_warnings:
            print('Increase n_high')
        return
    if not np.logical_and(p_low_green < confidence, p_low_red < confidence):
        if not suppress_warnings:
            print('Decrease n_low')
        return

    while np.logical_and(np.logical_or(np.abs(confidence - p_high_green) > tolerance,
                                       np.abs(confidence - p_high_red) > tolerance), 
                         np.abs(n_high - n_low) > 1):
    
        n_mid = int((n_high + n_low)/2)
        
        p_mid_green = binom.cdf(int(t_green*n_mid), n_mid, t_green - accuracy)
        p_mid_red = 1 - binom.cdf(int(t_red*n_mid), n_mid, t_red + accuracy)

        if np.logical_or(p_mid_green <= confidence - tolerance, p_mid_red <= confidence - tolerance):
            n_low = n_mid
            p_low_green = binom.cdf(int(t_green*n_low), n_low, t_green - accuracy)
            p_low_red = 1 - binom.cdf(int(t_red*n_low), n_low, t_red + accuracy)
        else:
            n_high = n_mid
            p_high_green = binom.cdf(int(t_green*n_high), n_high, t_green - accuracy)
            p_high_red = 1 - binom.cdf(int(t_red*n_high), n_high, t_red + accuracy)
    
    return n_high
    
    
def schematic(t_green, t_red, accuracy, confidence, n):
    
    plt.figure()
    
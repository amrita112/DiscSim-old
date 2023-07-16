import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

def get_n_samples(t_green = 0.3, t_red = 0.7, accuracy = 0.02, confidence = 0.9, tolerance = 0.001, n_high = 10000, n_low = 1):
    
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

    while np.logical_or(p_high1 > p, p_high_red > p):
    
    if p_low1 > p:
        if p_low_red > p:
            n_high = n_low
            n_low = int(n_low/2)
        else:
            n_high = int((n_high + n_low)/2)
    else:
        n_high = int((n_high + n_low)/2)
        
    p_high1 = binom.cdf(int(t_green*n_high), n_high, t_green - accuracy)
    p_low1 = binom.cdf(int(t_green*n_low), n_low, t_green - accuracy)

    p_high_red = 1 - binom.cdf(int(t_red*n_high), n_high, t_red + accuracy)
    p_low_red = 1 - binom.cdf(int(t_red*n_low), n_low, t_red + accuracy)
    
    if np.logical_and(p_high1 < p, p_high_red < p):
        n_low = n_high
        n_high = int(2*n_high)
    
        p_high1 = binom.cdf(int(t_green*n_high), n_high, t_green - accuracy)
        p_low1 = binom.cdf(int(t_green*n_low), n_low, t_green - accuracy)

        p_high_red = 1 - binom.cdf(int(t_red*n_high), n_high, t_red + accuracy)
        p_low_red = 1 - binom.cdf(int(t_red*n_low), n_low, t_red + accuracy)
    
    if np.logical_or(p_high1 <= p - tolerance, p_high_red <= p - tolerance):
        break
    
    
    
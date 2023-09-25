import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
from matplotlib.patches import Rectangle

def get_n_samples_single_threshold(threshold, confidence = 0.9, accuracy = 0.02, tolerance = 0.001, n_high = 10000, n_low = 2):
    
    '''
    Return the number of samples required to accurately estimate very high discrepancy scores for discrete variables.
    
    Inputs:
    threshold (float between 0 and 1): Threshold for classifying workers in 'red band'. Discrepancy scores > threshold will be classified as red band.
    accuracy (float between 0 and 1, default 0.02): Distance from threshold at which confidence guarantee applies. 
    confidence (float between 0 and 1, default 0.9): Desired probability of correctly classifying workers as red band.
    tolerance (float between 0 and 1, default 0.001): Distance from desired probability at which binary search of number of samples is stopped.
    n_high (int, default 10,000): Maximum possible number of samples for initializing binary search
    n_low (int, default 1): Minimum possible number of samples for initializing binary search
    
    '''
    
    p_high = 1 - binom.cdf(int(threshold*n_high), n_high, threshold + accuracy) # Probability of classifying score threshold + accuracy as red, with n_high samples
    p_low = 1 - binom.cdf(int(threshold*n_low), n_low, threshold + accuracy) # Probability of classigying score threshold + accuracy as green, with n_low samples

    if not p_high > confidence:
        return('Increase maximum # samples')
    if not p_low < confidence:
        return('Decrease minimum # samples')

    while np.logical_and(np.abs(p_high - confidence) > tolerance, n_low < n_high - 1):

        n_mid = int((n_high + n_low)/2)

        p_mid = 1 - binom.cdf(int(threshold*n_mid), n_mid, threshold + accuracy)
        if(p_mid > confidence):
            n_high = n_mid
        else:
            n_low = n_mid

        p_high = 1 - binom.cdf(int(threshold*n_high), n_high, threshold + accuracy)
        p_low = 1 - binom.cdf(int(threshold*n_low), n_low, threshold + accuracy)
        
    return n_high

def get_n_samples_two_thresholds(t_green = 0.3, t_red = 0.7, accuracy = 0.02, confidence = 0.9, tolerance = 0.001, n_high = 10000, n_low = 2, suppress_warnings = False, make_plot = False):
    
    '''
    Return the number of samples required to accurately estimate very high and very low discrepancy scores for discrete variables.
    
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
            
    if make_plot:
        schematic(t_green, t_red, accuracy, confidence, n_high, p_high_green, p_high_red)
    
    return n_high
    
    
def schematic(t_green, t_red, accuracy, confidence, n_samples, p_green, p_red):
    
    '''
    Make a plot showing the number of samples required to accurately estimate discrepancy scores for discrete variables.
    
    Inputs:
    t_green (float between 0 and 1, default 0.3): Threshold for classifying workers in 'green band'. Discrepancy scores < t_green will be classified as green band.
    t_red (float between 0 and 1, default 0.7): Threshold for classifying workers in 'red band'. Discrepancy scores > t_red will be classified as red band.
    accuracy (float between 0 and 1, default 0.02): Distance from threshold at which confidence guarantee applies. 
    confidence (float between 0 and 1, default 0.9): Desired probability of correctly classifying workers as green band or red band.
    n_samples (int): output of get_n_samples(), number of samples required to accurately estimate discrepancy scores
    p_green (float, between 0 and 1): Actual probability of correctly classifying workers as green band with n_samples samples.
    p_red (float, between 0 and 1): Actual probability of correctly classifying workers as red band with n_samples samples.
    
    '''

    fig, ax = plt.subplots(figsize = [20, 4])

    width = 1
    box_bottom = 1
    height = 0.1*width

    # Green zone - confidence guarantee
    left = 0
    right = t_green - accuracy
    rect = Rectangle([left, box_bottom], right - left, height, color = 'g')
    ax.add_patch(rect)

    # Green zone - out of confidence guarantee
    left = t_green - accuracy
    right = t_green
    rect = Rectangle([left, box_bottom], right - left, height, color = 'yellowgreen')
    ax.add_patch(rect)

    # Yellow zone
    left = t_green
    right = t_red
    rect = Rectangle([left, box_bottom], right - left, height, color = 'yellow')
    ax.add_patch(rect)

    # Red zone - out of confidence guarantee
    left = t_red 
    right = t_red + accuracy
    rect = Rectangle([left, box_bottom], right - left, height, color = 'orange')
    ax.add_patch(rect)

    # Red zone - confidence guarantee
    left = t_red + accuracy
    right = 1
    rect = Rectangle([left, box_bottom], right - left, height, color = 'r')
    ax.add_patch(rect)

    plt.plot([t_green, t_green], [box_bottom - 0.1*height, box_bottom + 1.1*height], color = 'k', linestyle = '--')
    plt.plot([t_red, t_red], [box_bottom - 0.1*height, box_bottom + 1.1*height], color = 'k', linestyle = '--')
    plt.yticks([])
    plt.xticks(np.round([0, t_green - accuracy, t_green, t_red, t_red + accuracy, 1], 2))
    plt.xlabel('Discrepancy score', fontsize = 15)
    plt.text(t_green/2, 1.04, 'Green zone\nConfidence guarantee = {0}'.format(np.round(p_green, 5)), fontsize = 15, horizontalalignment = 'center')
    plt.text((1 + t_red)/2, 1.04, 'Red zone\nconfidence guarantee = {0}'.format(np.round(p_red, 5)), fontsize = 15, horizontalalignment = 'center')
    plt.ylim([box_bottom, box_bottom + height])

    plt.title('{0} samples'.format(n_samples), fontsize = 15)

    
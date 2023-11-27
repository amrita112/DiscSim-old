import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os.path import sep
from tqdm import tqdm
from scipy.stats import binom
from matplotlib.patches import Rectangle
import numpy as np
from collections import Counter

def binary_search(min_n_samples, max_n_samples, n_sub, n_punish, n_guarantee, confidence = 0.9, n_simulations = 100, min_disc = 0, max_disc = 1, distribution = 'uniform'):
    """ Find the least number of samples between min_n_samples and max_n_samples, such that n_guarantee worst offenders are caught with the specified confidence.
        Uses binary search. Assumes random sampling and binary discrepancy (% mismatch between sub and sup).
        
        Inputs:
        min_n_samples: Least possible number of samples per subordinate
        max_n_samples: Largest possible number of samples per subordinate
        n_sub: number of subordinates
        n_punish: number of subordinates to punish (# worst offenders)
        n_guarantee: number of worst offenders that should be guaranteed to be caught
        confidence: default 0.9, desired confidence with which n_guarantee worst offenders will be caught
        n_simulations: default 100, number of times to run simulation (runtime scales linearly)
        min_disc: default 0, minimum 'true' discrepancy score
        max_disc: default 1, maximum 'true' discrepancy score
        distribution: default 'uniform', distribution from which true discrepancy scores are simulated
        
        Outputs:
        n_samples: least number of samples per subordinate, between min_n_samples and max_n_samples for which n_guarantee worst offenders will be caught 
        
    """
    n_high = max_n_samples
    frac_caught_high = single_sample_size_simulation(n_sub, n_high, n_punish, n_simulations = n_simulations, min_disc = min_disc, max_disc = max_disc,
                                                    distribution = distribution)
    freq_high = get_freq_of_frac_caught(frac_caught_high, n_guarantee/n_punish)
    
    n_low = min_n_samples
    frac_caught_low = single_sample_size_simulation(n_sub, n_low, n_punish, n_simulations = n_simulations, min_disc = min_disc, max_disc = max_disc,
                                                    distribution = distribution)
    freq_low = get_freq_of_frac_caught(frac_caught_low, n_guarantee/n_punish)
    
    if not freq_high > confidence:
        print('Increase maximum # samples')
        return max_n_samples
    if not freq_low < confidence:
        print('Decrease minimum # samples')
        return min_n_samples
    
    while np.logical_and(freq_high > confidence, n_low < n_high - 1):

        n_mid = int((n_low + n_high)/2)

        frac_caught_mid = single_sample_size_simulation(n_sub, n_mid, n_punish, n_simulations = n_simulations, min_disc = min_disc, max_disc = max_disc,
                                                    distribution = distribution)
        freq_mid = get_freq_of_frac_caught(frac_caught_mid, n_guarantee/n_punish)
        
        if(freq_mid > confidence):
            n_high = n_mid
            freq_high = freq_mid
        else:
            n_low = n_mid

    return n_high

def get_freq_of_frac_caught(frac_caught_distribution, frac_caught_threshold):
    
    return np.sum(frac_caught_distribution >= frac_caught_threshold)/len(frac_caught_distribution)

def single_sample_size_simulation(n_sub, n_samples, n_punish, n_simulations = 100, min_disc = 0, max_disc = 1, distribution = 'uniform'):
    """ Simulate discrepancy score measurements for a number of subordinates and report the fraction of worst offenders caught.
        Assumes random sampling and binary discrepancy (% mismatch between sub and sup).
        
        Inputs:
        n_sub: number of subordinates
        n_samples: number of samples per subordinate
        n_punish: number of subordinates to punish (# worst offenders)
        n_simulations: default 100, number of times to run simulation (runtime scales linearly)
        min_disc: default 0, minimum 'true' discrepancy score
        max_disc: default 1, maximum 'true' discrepancy score
        distribution: default 'uniform', distribution from which true discrepancy scores are simulated
        
        Outputs:
        frac_caught: 1Xn_simulations array of fraction of worst offenders caught in each simulation
    """
    
    true_disc = generate_true_disc(n_sub, min_disc = min_disc, max_disc = max_disc, distribution = distribution)
    frac_caught = np.zeros(n_simulations)
    
    for sim in range(n_simulations):
        meas_disc = generate_meas_disc_multi_sub(true_disc, n_samples, random_state = sim)
        true_worst = get_worst_offenders(true_disc, n_punish)
        meas_worst = get_worst_offenders(meas_disc, n_punish)
        frac_caught[sim] = get_fraction_overlap(true_worst, meas_worst)
        
    return frac_caught

def generate_true_disc(n_sub, min_disc = 0, max_disc = 1, distribution = 'uniform'):
    """ Given a number of subordinates n_sub, simulate discrepancy scores between min_disc (default: 0) and max_disc (default: 1) for each subordinate.
        Discrepancy scores are drawn from a distribution (default: uniform) over [min_disc, max_disc]. Assumes binary discrepancy (% mismatch between sub and sup).
    """
    
    if distribution == 'uniform':
        
        true_disc = np.random.uniform(min_disc, max_disc, n_sub)
    
    return true_disc

def generate_meas_disc_single_sub(true_disc, n_samples, random_state = 0):
    """ Given the true discrepancy true_disc (between 0 and 1) of a subordinate, simulate a draw of n_samples samples from the binomial distribution 
        with mean = true_disc and return the average as a simulated measured discrepancy. Assumes random sampling and binary discrepancy (% mismatch between sub and sup).
    """
    assert(true_disc >= 0)
    assert(true_disc <= 1)
    
    meas_disc = binom.rvs(n_samples, true_disc, random_state = random_state)/n_samples
    
    return meas_disc

def generate_meas_disc_multi_sub(true_disc, n_samples, random_state = 0):
    """ Assumes random sampling and binary discrepancy (% mismatch between sub and sup).
        Inputs:
        true_disc: 1Xn_sub array with values between 0 and 1 - true discrepancies of subordinates
        n_samples: number of samples per subordinate
        random_state: optional, seed for random number generator
        
        Outputs:
        meas_disc: 1Xn_sub array with values between 0 and 1 - simulated measured discrepancies of subordinates
    """
    
    #meas_disc = [generate_meas_disc_single_sub(td, n_samples, random_state = random_state) for td in true_disc]
    
    assert(np.all(true_disc >= 0))
    assert(np.all(true_disc <= 1))
    meas_disc = binom.rvs(n_samples, true_disc, random_state = random_state)/n_samples
    
    return meas_disc

def get_worst_offenders(array, n_worst, worse = 'larger'):
    """ Return indices of worst elements in an array, with worse defined as 'larger' or 'smaller'.
    """
    if worse == 'larger':
        worst = np.argsort(array)[-n_worst:]
    else:
        worst = np.argsort(array)[n_worst:]
        
    return worst
        
def get_fraction_overlap(array1, array2):
    """ Returns the fraction of elements of array1 present in array2. Assumes array1 and array2 have the same number of elements. 
    """
    assert(len(array1) == len(array2))
    frac_overlap = len([a for a in array1 if a in array2])/len(array1)
    #frac_overlap = len(set(array1) & set(array2))/len(array1)
    #frac_overlap = len(Counter(array1) & Counter(array2))
    
    return frac_overlap
    
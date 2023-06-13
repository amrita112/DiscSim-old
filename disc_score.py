import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def discrepancy_score(subordinate_variable, supervisor_variable, method):
    """Calculates the discrepancy score between two variables."""
    """The discrepancy score is a measure of the difference between the two variables."""
    
    # Step 1: check that the two variables are the same length
    if len(subordinate_variable) != len(supervisor_variable):
        raise ValueError("The two variables must be the same length.")
    
    # Step 2: check that the two variables are the same type
    if type(subordinate_variable[0]) != type(supervisor_variable[0]):
        raise TypeError("The two variables must be the same type.")
    
    # Step 3: calculate the discrepancy score
    if method == "percent_difference":
        discrepancy_score = np.mean(np.divide((subordinate_variable - supervisor_variable), supervisor_variable)) * 100
    elif method == "absolute_difference":
        discrepancy_score = np.mean(abs(subordinate_variable - supervisor_variable))
    elif method == "absolute_percent_difference":
        discrepancy_score = np.mean(abs((subordinate_variable - supervisor_variable) / supervisor_variable * 100))
    elif method == "simple_difference":
        discrepancy_score = np.mean(subordinate_variable - supervisor_variable)
    elif method == "percent_non_match":
        discrepancy_score = np.sum(subordinate_variable != supervisor_variable) / len(subordinate_variable) * 100
    else:
        raise ValueError("The method must be one of the following: percent_difference, absolute_difference, absolute_percent_difference, simple_difference, or percent_non_match.")
    
    return discrepancy_score


def bootstrap_distribution(subordinate_variable, supervisor_variable, method, n_iterations = 100000, ax = None):
    """Generates a distribution of discrepancy scores between the two variables using bootstrapping."""
        
    n = len(subordinate_variable)
    discrepancy_scores = []

    for i in tqdm(range(n_iterations)):
        indices = np.random.choice(range(n), size=n, replace=True)
        random_sample_sub = np.array([subordinate_variable[j] for j in indices])
        random_sample_sup = np.array([supervisor_variable[j] for j in indices])

        discrepancy_scores.append(discrepancy_score(random_sample_sub, random_sample_sup, method))
        
    real_discrepancy_score = discrepancy_score(subordinate_variable, supervisor_variable, method)
    
    if ax is None:
        fig, ax = plt.subplots()
    ax.hist(discrepancy_scores, color = 'gray', edgecolor = 'black')
    ax.axvline(real_discrepancy_score, color='r', linestyle='dashed', linewidth=2)
    ax.set_xlabel("Discrepancy Score")
    ax.set_ylabel("Frequency")
    ax.set_title("Bootstrap Distribution of Discrepancy Scores")

    return discrepancy_scores

def shuffle_distribution(subordinate_variable, supervisor_variable, method, n_iterations = 100000, ax = None):
    """Generates a null distribution of discrepancy scores between the two variables 
    by shuffling indices of the supervisor variable."""
        
    n = len(subordinate_variable)
    discrepancy_scores = []
    subordinate_variable_array = np.array([subordinate_variable[j] for j in range(n)])

    for i in tqdm(range(n_iterations)):
        indices = np.random.choice(range(n), size=n, replace=False)
        random_sample_sup = np.array([supervisor_variable[j] for j in indices])

        discrepancy_scores.append(discrepancy_score(subordinate_variable_array, random_sample_sup, method))
        
    real_discrepancy_score = discrepancy_score(subordinate_variable, supervisor_variable, method)
    
    if ax is None:
        fig, ax = plt.subplots()
    ax.hist(discrepancy_scores, color = 'gray', edgecolor = 'black')
    ax.axvline(real_discrepancy_score, color='r', linestyle='dashed', linewidth=2)
    ax.set_xlabel("Discrepancy Score")
    ax.set_ylabel("Frequency")
    ax.set_title("Shuffled Null Distribution of Discrepancy Scores")

    return discrepancy_scores

def p_value(shuffle_distribution, real_value):
    """Calculates the p-value of the real discrepancy score: 
    the proportion of samples in the shuffled distribution that are less than the real discrepancy score."""
    
    p_value = sum(shuffle_distribution <= real_value) / len(shuffle_distribution)
    
    return p_value
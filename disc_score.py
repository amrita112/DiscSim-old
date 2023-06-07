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


def bootstrap_distribution(subordinate_variable, supervisor_variable, method, n_iterations = 100000):
    """Generates a distribution of discrepancy scores between the two variables using bootstrapping."""
        
    n = len(subordinate_variable)
    discrepancy_scores = []
    for i in tqdm(range(n_iterations)):
        indices = np.random.choice(range(n), size=n, replace=True)
        random_sample_sub = list(subordinate_variable[indices])
        random_sample_sup = list(supervisor_variable[indices])
        discrepancy_scores.append(discrepancy_score(random_sample_sub, random_sample_sup, method))
    
    plt.hist(discrepancy_scores)
    plt.show()
    plt.xlabel("Discrepancy Score")
    plt.ylabel("Frequency")
    plt.title("Bootstrap Distribution of Discrepancy Scores")

    return discrepancy_scores

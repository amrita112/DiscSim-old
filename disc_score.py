import numpy as np

def discrepancy_score(subordinate_variable, supervisor_variable, method):
    """Calculates the discrepancy score between two variables."""
    """The discrepancy score is a measure of the difference between the two variables."""
    
    # Step 1: check that the two variables are the same length
    if len(subordinate_variable) != len(supervisor_variable):
        raise ValueError("The two variables must be the same length.")
    
    # Step 2: check that the two variables are the same type
    if type(subordinate_variable) != type(supervisor_variable):
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
        discrepancy_score = (subordinate_variable != supervisor_variable) / len(subordinate_variable) * 100
    else:
        raise ValueError("The method must be one of the following: percent_difference, absolute_difference, absolute_percent_difference, simple_difference, or percent_non_match.")
    
    return discrepancy_score




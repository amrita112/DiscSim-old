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
    if method == "mean":
        
# DiscSim

This repository contains code written for a project I am doing as a volunteer with CEGIS (Center for Effective Governance of Indian States), an organization that aims to help state governments in India achieve better development outcomes. 

An important goal of CEGIS is to improve the quality of administrative data collected by state governments. One way in which this is achieved is to re-sample a subset of the data and measure the deviation from the original samples collected. These deviations are quantified as 'discrepancy scores', and large discrepancy scores are flagged for intervention by a third party.

Often, it is not clear what re-sampling strategy should be used to obtain the most accurate and reliable discrepancy scores. The goal of this project is to create a simulator to predict discrepancy scores, and the statistical accuracy of the discrepancy scores, for different re-sampling strategies. This repository will be populated with python scripts and jupter notebooks to implement the simulator. However, no data will be made public as it is sensitive data collected by state governments in India.

Glossary
1. Subordinate: collector of original samples
2. Supervisor: collector of secondary samples (used to calculate discrepancy score)

The work-flow for this project is outlined below: 

1. Using sample data, calculate different types of discrepancy scores.
2. Estimate variance of the calculated scores with bootstrapping, and p-values (a measure of our confidence in the score).
3. Build a simple model to predict the p-value of the score, taking as input
    a. # of subordinate samples (assuming only 1 subordinate)
    b. # of supervisor samples (assuming only 1 supervisor)
    c. # of variables
    d. Method of truth score calculation
    e. Expected discrepancies (to be removed later, this shouldn’t be required as input but is hard to estimate, will require some thinking)
4. Add complexity to the model. 
    a. Add the following as optional inputs:
        i. Exact values of subordinate samples (upload csv)
        ii. Exact values of supervisor samples (upload csv)
        iii. Mean and variance of subordinate samples
        iv. Mean and variance of supervisor samples
        v. Moderation rate (expected change in the variables between subordinate sampling and supervisor sampling)
    b. Estimate expected discrepancy instead of requiring it as an input from the user
    c. Give outputs at different scales (state, district, block, subordinate)
5. Enable multiple subordinates and supervisors: calculate p-values for discrepancy score for each subordinate and overall average p-values. 
6. Think about how to convert p-value to confidence score that’s interpretable for a layperson
7. Create a user-friendly web interface 
8. Implement inverse logic: if you want a particular p-value, what numbers do you need
9. Supervisor sampling algorithm: add the following as inputs: 
    a. Supervisor sampling frequency, as a % of subordinate sampling frequency
    b. Supervisor sampling strategy, for example
        i. Subordinates with highest variance
        ii. Subordinates whose mean values are outliers from the distribution of subordinates
        iii. Random selection of subordinates
        iv. Specific subordinates
    c. Attrition: actual sampling frequency, as a % of subordinate sampling frequency or as a % of intended sampling frequency
10. Add supervisory layers

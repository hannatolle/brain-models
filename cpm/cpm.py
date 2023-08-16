import numpy as np
from scipy.stats import pearsonr 
from sklearn.linear_model import LinearRegression

def predict(fcs, y):
    """
    Predicts the response variable y from functional connectivity matrices fcs using connectome-based
    predictive modelling (Shen, X. et al., 2017; Amico and Goni, 2018).

    Parameters
    ----------
    fcs : nd array
          vectorized functional connectivity matrices of each subject, where rows
          are functional connectivity values and columns are subjects
    
    y : vector array 
        response variable that may be predicted from functional connectivity (e.g. cognitive score)

    Returns
    -------
    result : PearsonRResult
             Pearson correlation object of predicted versus and response variable
             result.statistic = correlation coefficient
             result.pvalue = p-value corresponding to correlation coefficient
    """
    
    allsubs = np.arange(0, len(y), 1)   
    y_pred = np.zeros(len(y))
    for sub in allsubs:
        
        # generate subject indices for implementing leave-one-out cross-validation
        trainsubs = allsubs[allsubs !=sub]
        
        # compute predictor variable ("strength")
        strength = np.zeros(len(allsubs))
        for edge in range(fcs.shape[0]):
            
            # compute correlation between FC value and y for all but one subject
            res = pearsonr(fcs[edge, trainsubs], y[trainsubs])
            
            # edges with significant positive (p<0.01) correlation are summed into a single subject value ("strength")
            if res.pvalue < 0.01 && res.statistic > 0:
                strength += fcs[edge, :].flatten()
                
        # fit linear model and predict y of left-out subject from strength
        reg = LinearRegression().fit(strength[trainsubs], y[trainsubs])
        y_pred(sub) = reg.predict(np.array([[strength(sub)]]))
        
    # compare predicted with true response
    return pearsonr(y_pred, y)
    
        
    
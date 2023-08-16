import numpy as np
from scipy.stats import pearsonr 
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def predict(fcs, y, plot_result = False):
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
        
    plot_result : boolean
                  if True, produces a scatterplot at the end with predictions versus y

    Returns
    -------
    result : y_pred
             predicted labels
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

            # edges with sign. positive (p<0.01) correlation are summed into a single subject value ("strength")
            if res.pvalue < 0.01 and res.statistic > 0:
                 strength += fcs[edge, :]
                    
        # fit linear model and predict y of left-out subject from strength
        x = np.expand_dims(strength[trainsubs], axis=1)
        reg = LinearRegression().fit(x, y[trainsubs])
        y_pred[sub] = reg.predict(np.array([[strength[sub]]]))

    # compare predicted with true response
    corr_result = pearsonr(y_pred, y)
    
    if plot_result:
        plt.scatter(y, y_pred);
        plt.xlabel("true label");
        plt.ylabel("prediction");
        plt.title(f"r = {np.round(corr_result.statistic, 2)}, p = {np.round(corr_result.pvalue, 4)}");
    
    return y_pred
    
        
    
# this needs to be run in an environment with Python 3.6

import fastdmf as dmf
import numpy as np
from bayes_opt import BayesianOptimization, UtilityFunction
from nilearn.connectome import ConnectivityMeasure

class BrainModel():
    """
    Whole-brain model class. As of yet, BrainModel is a DMF whole-brain model as per FastDMF.
    """
    
    def __init__(self, **kwargs):
        # FastDMF attributes
        params = dmf.default_params(**kwargs)
        for k, v in params.items():
            setattr(self, k, v)
            
        # additional attributes
        self.pbounds = kwargs.get('pbounds', {'G': [0.1, 5]}) # bounds of all free model parameters as dict
        self._loss = np.inf 
        
    def get_loss(self):
        return self._loss
    
    def run(self, ms):
        """
        Returns 2d array of synthetic BOLD data where rows=seconds and cols=brain regions.
        """
        return dmf.run(self.__dict__, ms)
            
    def utility(self, empirical_FC, ms = 120000):
        """ 
        Computes negative loss of DMF whole-brain model fit to empirical functioncal connectivity data.

        Parameters
        ----------
        empirical_FC : 0D array
                       vectorized lower/ upper triangular empirical functional connectivity matrix
                       should NOT contain self-correlation values of regional timeseries with themselves

        ms : int
             number of milisecond time steps of bold data to be synthesized for fitting

        Returns
        -------
        result : float
                 negative loss; ks-distance between functional connectivity value 
                 distributions of synthesized versus empirical data
        """

        # simulate BOLD data
        bold = self.run(ms)

        # get functional connectivity of unique pairs of model-brain regions
        FC_measure = ConnectivityMeasure(kind='correlation', vectorize=True, discard_diagonal=True)
        synthetic_FC = FC_measure.fit_transform([transpose(bold)]).flatten()

        # check dimensions of input (TODO: perform check before running simulation)
        if len(synthetic_FC) != len(empirical_FC):
            raise f"empirical_FC must have the shape {synthetic_FC.shape}."

        # return ks-distance between synthetic and empirical functional connectivity distributions    
        return ks_score(synthetic_FC, empirical_FC)

    def fit(self, empirical_FC, ms=120000, init_points=5, n_iter=10):
        """
        Uses Bayesian Optimization to find optimal model parameters so as to fit DMF whole-brain 
        model to empirical data.

        Parameters
        ----------
        empirical_FC : 0D array
                       vectorized lower/ upper triangular empirical functional connectivity matrix
                       should NOT contain self-correlation values of regional timeseries with themselves

        ms : int
             number of milisecond time steps of bold data to be synthesized for fitting
             
        init_points : int
                      number of sampled model parameters to be evaluated at each iteration
                      
        n_iter : int
                 number of iterations
        """
        # create BayesianOptimization optimizer and maximize utility
        optimizer = BayesianOptimization(f = self.utility, pbounds = self.pbounds)
        optimizer.maximize(init_points = init_points, n_iter = n_iter)
        
        # update model parameter and loss
        self.G = optimizer.max['params']['G']
        self._loss = optimizer.max['target']


import matplotlib.pyplot as plt
import numpy as np
import fastdmf as dmf
from ks_metric import ks_score
from bayes_opt import BayesianOptimization, UtilityFunction
from nilearn.connectome import ConnectivityMeasure

class BrainModel():
    """
    Whole-brain model class. As of yet, BrainModel is a DMF whole-brain model as per FastDMF.
    """
    
    def __init__(self, **kwargs):
        # set FastDMF default attributes
        self.params = dmf.default_params()
        
        # override defaults with user inputs
        for k,v in kwargs.items():
            if k in self.params: self.params[k] = v
        
        # additional attributes
        self.pbounds = kwargs.get('pbounds', {'G': [0.01, 5]}) # bounds of all free model parameters as dict
        self._loss = np.inf 
        
    def get_loss(self):
        return self._loss
    
    def set_G(self, G):
        self.params['G'] = G
        
    def get_G(self):
        return self.params['G']
    
    def run(self, ms):
        """
        Returns 2d array of synthetic BOLD data where rows=seconds and cols=brain regions.
        """
        return dmf.run(self.params, ms)
    
    def testrun(self, ms, G=[], plots=[1, 1]):
        """
        synthesizes data and plots BOLD and FC connectivity matrix.
        """
        # set G 
        if G:
            original_G = self.get_G()
            self.set_G(G)
            
        # simulate data
        bold = self.run(ms)

        # plot synthetic BOLD data
        if plots[0] > 0:
            fig, ax = plt.subplots()
            im = ax.imshow(bold.transpose())
            ax.set_ylabel('time (s)');
            ax.set_xlabel('brain regions');
            ax.set_title(f"synthetic BOLD data; G = {np.round(self.get_G(), 3)}");
            plt.colorbar(im, fraction=0.03, pad=0.03);
            plt.show()

        if plots[1] > 0:
            # compute and plot FC
            conn_measure = ConnectivityMeasure(kind='correlation', vectorize=False, discard_diagonal=False)
            FC = conn_measure.fit_transform([bold.transpose()]).squeeze()
            np.fill_diagonal(FC, 0)

            fig, ax = plt.subplots();
            scaling = np.max(FC) if np.max(FC)>(-np.min(FC)) else (-np.min(FC))
            im = plotting.plot_matrix(FC, vmax=scaling, vmin=-scaling, colorbar=False, axes=ax);
            plt.colorbar(im, fraction=0.05, pad=0.03);
            ax.set_title(f"synthetic FC; G = {np.round(self.get_G(), 3)}");
            plt.show()
            
        # set G back to original value    
        if G:
            self.set_G(original_G)
            
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
        -ks-dist : float
                   negative ks-distance between functional connectivity value 
                   distributions of synthesized versus empirical data
        """

        # simulate BOLD data
        bold = self.run(ms)

        # get functional connectivity of unique pairs of model-brain regions
        FC_measure = ConnectivityMeasure(kind='correlation', vectorize=True, discard_diagonal=True)
        synthetic_FC = FC_measure.fit_transform([np.transpose(bold)]).flatten()

        # check dimensions of input (TODO: perform check before running simulation)
        assert len(synthetic_FC) == len(empirical_FC), f"empirical_FC must have the shape {synthetic_FC.shape}."

        # return ks-distance between synthetic and empirical functional connectivity distributions
        category = np.concatenate((np.zeros(len(synthetic_FC)), np.ones(len(empirical_FC))), axis=0)
        stacked_data = np.concatenate((synthetic_FC, empirical_FC), axis=0)
        ks_dist = ks_score(category, stacked_data)
        return -ks_dist
    
    def _evaluate_clone(self, empirical_FC, G, ms = 120000):
        """
        Runs and evaluates a clone of self with different G parameter.
        
        Parameters
        ----------
        empirical_FC : 0D array
                       vectorized lower/ upper triangular empirical functional connectivity matrix
                       should NOT contain self-correlation values of regional timeseries with themselves
        G : float
            global coupling parameter G

        ms : int
             number of milisecond time steps of bold data to be synthesized for fitting
             
        Returns
        -------
        -ks_dist : float
                   negative ks-distance between functional connectivity value 
                   distributions of synthesized versus empirical data
        """
        # make clone
        clone = BrainModel(**self.params)
        # change G
        clone.params['G'] = G
        # evaluate clone
        return clone.utility(empirical_FC, ms=ms)

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
        optimizer = BayesianOptimization(f = lambda G: self._evaluate_clone(empirical_FC, G, ms=ms), 
                                         pbounds = self.pbounds)
        optimizer.maximize(init_points = init_points, n_iter = n_iter)
        
        # update model parameter and loss
        self.set_G(optimizer.max['params']['G'])
        self._loss = optimizer.max['target']
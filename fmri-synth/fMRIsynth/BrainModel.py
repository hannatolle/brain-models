class BrainModel():
    """
    Whole-brain model class. As of yet, BrainModel is a DMF whole-brain model as per FastDMF.
    """
    
    def __init__(self, **kwargs):
        # FastDMF attributes
        params = kwargs.get('params', {})
        self.params = dmf.default_params(**params)
        
        # additional attributes
        self.pbounds = kwargs.get('pbounds', {'G': [0.1, 5]}) # bounds of all free model parameters as dict
        self._loss = np.inf 
        
    def get_loss(self):
        return self._loss
    
    def run(self, ms):
        """
        Returns 2d array of synthetic BOLD data where rows=brain regions and cols=time steps (sec).
        """
        return dmf.run(self.params, ms)
            
    def utility(self, empirical_FC, ms = 120000):
        """ 
        Computes negative loss of DMF whole-brain model fit to empirical functioncal connectivity data.

        Parameters
        ----------
        empirical_FC : 0D array
                       vectorized lower/ upper triangular empirical functional connectivity matrix
                       should NOT contain self-correlation values of regional timeseries with themselves
        
        G : float
            global coupling parameter G
            if given, model will run with a different G parameter than self.params['G']

        ms : int
             number of milisecond time steps of bold data to be synthesized for fitting

        Returns
        -------
        ks_dist : float
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
        Evaluates the fit of a clone BrainModel with same parameters as self except for G.
        
        Parameters
        ----------
        empirical_FC : 0D array
                       vectorized lower/ upper triangular empirical functional connectivity matrix
                       should NOT contain self-correlation values of regional timeseries with themselves
        
        G : float
            global coupling parameter G
            if given, model will run with a different G parameter than self.params['G']

        ms : int
             number of milisecond time steps of bold data to be synthesized for fitting

        Returns
        -------
        result : float
                 negative ks-distance between functional connectivity value 
                 distributions of synthesized versus empirical data
        """
        # make clone
        clone = BrainModel(**self.__dict__)
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
        # lambda x: x if x > threshold_value else 0
        optimizer = BayesianOptimization(f = lambda G: self._evaluate_clone(empirical_FC, G, ms=ms), 
                                         pbounds = self.pbounds)
        optimizer.maximize(init_points = init_points, n_iter = n_iter)
        
        # update model parameter and loss
        self.params['G'] = optimizer.max['params']['G']
        self._loss = optimizer.max['target']


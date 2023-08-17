import BrainModel

def synthesize_subjects(FC, SC, n, t, 
                        params={'TR': 0.72}, 
                        ms=120000, 
                        init_points=5, 
                        n_iter=10, 
                        make_plots=False):
    """
    Synthesizes fMRI BOLD data using dynamic mean field whole-brain models. 
    Uses FastDMF under the hood (Herzog et al., 2022).

    Parameters
    ----------
    FC : 2d nd array
         vectorized functional connectivity matrices of each subject, where rows
         are functional connectivity values of triangular FC matrix without diagonal
         and columns are subjects
         
    SC : 3d nd array 
         structural connectivity matrices of multiple subjects
         subjects are on axis=2
         
    n : int
        number of subjects
        
    t : int or float
        length of synthetic BOLD data in seconds
         
    params : dict
             BrainModel parameters. Default is specified by dmf.default_params(),
             except that the default TR (repetition time) is changed to 0.72 sec to match HCP data.
             
    ms : int
         number of milisecond time steps of bold data to be synthesized for fitting
             
    init_points : int
                  number of sampled model parameters to be evaluated at each iteration of fitting

    n_iter : int
             number of iterations of fitting algorithm
             
    make_plots: boolean
                if True, generates plots to visualize the distribution of model parameters and
                model loss after fitting

    Returns
    -------
    synthetic_data : list of 2d nd arrays
                     synthetic BOLD time series (numTRs X numROIs) of n subjects
                     output format matches nilearn.ConnectivityMeasure.fit_transform() input format
    """

    # fit a DMF BrainModel to the FC matrix of each individual subject
    # and record loss ("badness of fit") and optimal model parameters G
    fitted_model_loss = np.zeros(FC.shape[1])
    fitted_model_G = np.zeros(FC.shape[1])
    for sub in range(FC.shape[1]):
        model = BrainModel(**params)
        model.fit(FC[:, sub].flatten(), ms=ms, init_points=init_points, n_iter=n_iter)
        fitted_model_loss[sub] = model.get_loss()
        fitted_model_G[sub] = model.G
        
    # plot distribution of loss and G, if requested
    if make_plots:
        fig, (ax0, ax1, ax2) = plt.subplots(1, 3)
        # G histogram
        ax0.hist(fitted_model_G)
        ax0.set_xlabel('G')
        ax0.set_ylabel('count')
        ax0.title(f"mean = {np.mean(fitted_model_G)}, std = {np.std(fitted_model_G)}")
        # loss histogram
        ax1.hist(fitted_model_loss)
        ax1.set_xlabel('loss')
        ax1.set_ylabel('count')
        ax1.title(f"mean = {np.mean(fitted_model_loss)}, std = {np.std(fitted_model_loss)}")
        # G versus loss scatterplot
        ax2.scatter(fitted_model_G, fitted_model_loss)
        ax2.set_xlabel('G')
        ax2.set_ylabel('loss')
        
    # sample new Gs from Gaussian distribution fitted to empirical G distribution
    new_Gs = np.random.normal(loc=np.mean(fitted_model_G), scale=np.std(fitted_model_G), size=n)
    
    # generate n synthetic BOLD timeseries with sampled Gs
    synthetic_data = []
    for synthSub in range(n):
        new_params = params
        new_params['G'] = newGs[synthSub]
        model = BrainModel(**new_params)
        synthetic_data.append(model.run(t*1000).transpose())
        
    return synthetic_data
        
        
    
        
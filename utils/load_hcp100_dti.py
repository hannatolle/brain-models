import os
import numpy as np
import pandas as pd

def load_hcp100_dti(path, subjects=range(1, 101)):
    """
    Loads the DTI structural connectivity data of the HCP100 dataset.
    
    Parameters
    ----------
    path : str
           path to data folder

    subjects : iterable
               iterable with ids of subjects to be loaded
               by default, all 100 subjects will be loaded
             
    Returns
    -------
    data : list of 2d nd arrays
           empirical structural connectivity matrices (numROIs X numROIs) of HCP subjects
           output format matches nilearn.ConnectivityMeasure.fit_transform() input format
    """
    data = []
    for sub in subjects:
        fullfile = os.path.join(path, f"sub{sub:03}_DTI_fibers_HCP.csv")
        data.append(np.asarray(pd.read_csv(fullfile, header=None)))
        
    return data
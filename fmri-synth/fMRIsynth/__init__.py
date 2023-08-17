import matplotlib.pyplot as plt
import numpy as np
import fastdmf as dmf
from ks_metric import ks_score
from bayes_opt import BayesianOptimization, UtilityFunction
from nilearn.connectome import ConnectivityMeasure
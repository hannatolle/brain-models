
setup(name             = 'fmri-synth',
      version          = '0.0.1',
      description      = 'tools for augmenting fMRI datasets with synthetic data from brain simulations',
      author           = 'Hanna M. Tolle',
      author_email     = 'hanna.m.tolle@gmail.com',
      url              = 'https://github.com/hannatolle/brain-models',
      long_description = open('../README.md').read(),
#      package_data     = {'fastdmf': ['DTI_fiber_consensus_HCP.csv']},
      install_requires = ['numpy==1.18.0'])
      packages         = ['fastdmf', 'ks_metric', 'nilearn', 'BayesianOptimization'])
    


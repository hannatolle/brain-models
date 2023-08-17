
setup(name             = 'fMRIsynth',
      version          = '0.0.1',
      description      = 'tools for augmenting fMRI datasets with synthetic data from brain simulations',
      author           = 'Hanna M. Tolle, Diana Perez',
      author_email     = 'hanna.m.tolle@gmail.com, dianacperezrivera@gmail.com',
      url              = 'https://github.com/hannatolle/brain-models/fMRIsynth',
      long_description = open('../README.md').read(),
      install_requires = ['numpy==1.18.0'],
      packages         = ['fastdmf', 'ks_metric', 'nilearn', 'BayesianOptimization'])
    


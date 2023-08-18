# fMRIsynth

A library of python functions to synthesize fMRI timeseries data using dynamic mean field (DMF) whole-brain models that are fitted to empirical fMRI data. The synthetic data can for instance be used to augment an existing empirical dataset before training a machine learning model to predict an outcome variable of interest from the neuroimaging data. This library capitalizes on the efficient DMF implementation FastDMF (https://gitlab.com/concog/fastdmf). Therefore, if you use fMRIsynth kindly cite the FastDMF publication (Herzog et al., 2022; https://www.biorxiv.org/content/10.1101/2022.04.11.487903v1).

## Modules in this library

**fMRIsynth**: main user function for fitting whole-brain models to empirical fMRI data and generating synthetic data

**BrainModel**: BrainModel class

## Installation

This package calls FastDMF under the hood, which relies on a C++ interpreter that requires the following installations:

```
apt-get update
apt-get instal libboost-python-dev libbosst-numpy-dev
```

Note that these installations require Python 3.6, which in turn requires numpy version 1.18.0. Thus, we recommend to run fMRIsynth in a virtual environment. For example with Anaconda, this can be done by running:

```
conda create -n py36 python=3.6
conda activate py36
```

And then after cloning the FastDMF repository, edit the fastdmf/python/setup.py file such that line 15 says `install_requires = ['numpy==1.18.0']`. Finally, run the following command within the cloned FastDMF repo.

```
python -m pip install -e .
```

After successful installation of FastDMF, other required packages can be installed in the virtual environment as follows:

```
python -m pip install matplotlib
python -m pip install nilearn --ignore-installed certifi
```

The final command may give a warning that nilearn installed a newer version of numpy, which isn't supported by FastDMF. We must therefore reinstall numpy 1.18.0. To do this, run:

```
python -m pip install --force-reinstall "numpy==1.18.0"
```

Finally, there are two more required packages that we need to clone and subsequently install. One of them is `ks_metric` (https://pypi.org/project/ks-metric/). The other one is BayesianOptimization (https://github.com/bayesian-optimization/BayesianOptimization). After cloning those two repositories to your machine, they are installed by running:

```
python -m pip install ks_metric
python -m pip install bayesian-optimization
```

Now you're ready to use fMRIsnyth! 

**Optional**:
If you would like to use fMRIsynth in a Jupyter Notebook, the py36 conda environment can be exported to your notebook using ipykernel as follows (run this while being in the active py36 conda environment):

```
python -m pip install ipykernel
python -m ipykernel install --user --name=py36
```
You might have to restart your Jupyter to be able to select the newely created py36 kernel for your notebook. 

## License

Copyright 2023 Hanna M. Tolle, Diana C. Perez

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


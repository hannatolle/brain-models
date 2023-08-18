from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fMRIsynth",
    version="0.0.1",
    author="Hanna M. Tolle, Diana Perez",
    author_email="hanna.m.tolle@gmail.com, dianacperezrivera@gmail.com",
    description="synthesizing fMRI timeseries data using brain models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hannatolle/brain-models",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3 License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='==3.6',
    install_requires=["numpy==1.18.0"]
)
    


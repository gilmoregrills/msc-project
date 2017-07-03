from setuptools import setup

setup(name='hrtf_individualiser',
      version='0.1.0',
      packages=['individualiser'],
      install_requires=[
          'lmdb',
          'scipy',
          'numpy',
          'ipython',
          'jupyter',
          'scikit-learn',
          'clint',
      ]
      )

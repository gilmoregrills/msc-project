from setuptools import setup

setup(name='hrtf_individualiser',
      version='0.1.0',
      packages=['individualiser'],
      install_requires=[
          'lmdb',
          'scipy',
          'numpy',
          'matplotlib',
          'ipython',
          'jupyter',
          'scikit-learn',
          'clint',
          'cPickle',
          'asyncore',
      ]
      entry_points={
          'console_scripts': [
              'installer = scripts.install',
              'hrtf_individualiser = individualiser.__main__:main'
          ]
      },
)

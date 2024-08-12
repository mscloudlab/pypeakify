from setuptools import setup, find_packages

setup(
    name='pypeakify',
    author='mscloudlab',
    author_email='mscloudlab@gmail.com',
    description='General purpose peak deconvolution package for Python.',
    packages=find_packages(where='src'),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'tabulate',
        'requests'
    ],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

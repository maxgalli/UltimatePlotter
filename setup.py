from distutils.core import setup
import setuptools
from importlib import import_module

# Check ROOT related requirements and raise error if not found
for pkg in ['ROOT', 'cppyy', 'cppyy_backend']:
    try:
        import_module(pkg)
    except ModuleNotFoundError:
        raise ImportError('{} not found. You need a full working installation of ROOT to install this package.\n' \
                'For more info, see: https://root.cern/install/'.format(pkg))

setup(
    name="ultimate_plotter",
    version="0.0.0",
    author="Massimiliano Galli",
    author_email="massimiliano.galli.95@gmail.com",
    description="HEP data processor and plotter with interfaces to multiple scikit-hep packages",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

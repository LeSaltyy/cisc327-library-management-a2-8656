from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="library-management",
    version="0.1.0",
    py_modules=['library_service', 'database'],
    package_dir={'': '.'},
    install_requires=[],
    python_requires='>=3.8',
)
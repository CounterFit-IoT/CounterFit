'''
Shims for the Seeed Grove Py library for use with the CounterFit Virtual IoT Device app
'''

from codecs import open
from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='counterfit-shims-grove',
    packages=find_packages(include=['counterfit_shims_grove']),
    version='0.1.4.dev5',
    description='Shims for the Seeed Grove sensors for the CounterFit virtual IoT device app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jim Bennett',
    url="https://github.com/CounterFit-IoT/CounterFit",
    license='MIT',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    keywords="iot grove seeed virtual hardware",
    install_requires=['requests','counterfit-connection'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

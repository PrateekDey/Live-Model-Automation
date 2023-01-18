import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'app'
DESCRIPTION = 'Live Model Automation'
URL = 'https://source.syncron.team/admin/repos/pm/analytics/live-models-automation'
EMAIL = 'manoj.veeravalli@syncron.com'
AUTHOR = 'Manoj Veeravalli'
REQUIRES_PYTHON = '>=3.8.1'
VERSION = 1.0

# What packages are required for this module to be executed?
REQUIRED = [
    'requests',
    'structlog==19.1.0',
    'python-json-logger==0.1.11',
    'boto3==1.26.5'
]

# What packages are optional?
EXTRAS = {
    'tests': ['pytest', 'mock', 'pytest-mock', 'pytest-cov', 'pycodestyle', 'pytest-watch', 'coverage',
              'unittest']
}

here = os.path.abspath(os.path.dirname(__file__))


setup(
    name=NAME,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude='tests'),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
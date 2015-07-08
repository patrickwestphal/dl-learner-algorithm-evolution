try:
    from setuptools import setup
except ImportError:
    from distutils import setup

config = {
    'description': 'Collection of scripts that show the performance evolution of DL-Learner algrothms',
    'author': 'Patrick Westphal',
    'url': 'https://github.com/patrickwestphal/dl-learner-regression-stats',
    'download_url': 'https://github.com/patrickwestphal/dl-learner-regression-stats',
    'author_email': 'patrick.westphal@informatik.uni-leipzig.de',
    'version': '0.0.1',
    'tests_require': [
    ],
    'install_requires': [
        'GitPython==1.0.1',
        'numpy==1.9.2',
        'matplotlib==1.4.3'
    ],
    'packages': ['repo', 'output'],
    'scripts': ['bin/makestats'],
    'name': 'dl-learner-regression-stats'
}

setup(**config)
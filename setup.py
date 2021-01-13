#!/usr/bin/env python
# import codecs


import os
import sys
import warnings

# try: # for pip >= 10
#    from pip._internal.req import parse_requirements
# except ImportError: # for pip <= 9.0.3
#    from pip.req import parse_requirements

from setuptools import find_packages, setup

NAME = "jira"

base_path = os.path.dirname(__file__)
if base_path not in sys.path:
    sys.path.insert(0, base_path)

# this should help getting annoying warnings from inside distutils
warnings.simplefilter('ignore', UserWarning)


def _is_ordereddict_needed():
    """ Check if `ordereddict` package really needed """
    try:
        return False
    except ImportError:
        pass
    return True


def get_metadata(*path):
    fn = os.path.join(base_path, *path)
    scope = {'__file__': fn}

    # We do an exec here to prevent importing any requirements of this package.
    # Which are imported from anything imported in the __init__ of the package
    # This still supports dynamic versioning
    with open(fn) as fo:
        code = compile(fo.read(), fn, 'exec')
        exec(code, scope)

    if 'setup_metadata' in scope:
        return scope['setup_metadata']

    raise RuntimeError('Unable to find metadata.')


def read(fname):
    return open(os.path.join(base_path, fname)).read()


def get_requirements(*path):
    req_path = os.path.join(*path)
    with open(req_path) as f:
        return f.read().strip().split('\n')


if __name__ == '__main__':
    setup(
        name=NAME,
        # cmdclass={'release': Release, 'prerelease': PreRelease},
        packages=find_packages(exclude=['tests', 'tools']),
        include_package_data=True,

        install_requires=get_requirements(base_path, 'requirements.txt'),
        setup_requires=['pytest-runner'],
        tests_require=get_requirements(base_path, 'requirements-dev.txt'),
        extras_require={
            'all': [],
            'magic': ['filemagic>=1.6'],
            'shell': ['ipython>=0.13']},
        entry_points={
            'console_scripts':
                ['jirashell = jira.jirashell:main']},

        long_description=open("README.rst").read(),
        provides=[NAME],
        bugtrack_url='https://github.com/pycontribs/jira/issues',
        home_page='https://github.com/pycontribs/jira',
        keywords='jira atlassian rest api',

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development :: Libraries :: Python Modules'],
        # All metadata including version numbering is in here
        **get_metadata(base_path, NAME, 'package_meta.py')
    )

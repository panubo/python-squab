#!/usr/bin/env python

from setuptools import setup

from squab.version import __version__


setup(
    name='squab',
    version=__version__,
    author='Volt Grid Pty Ltd',
    author_email='andrew@voltgrid.com',
    license='MIT',
    description='Simple CouchDB Bindings',
    long_description=open('README.md').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    url='https://github.com/voltgrid/couch-bindings',
    packages=['squab',],
    scripts=[],
    zip_safe=False,
    install_requires=['requests==2.3.0',],
    tests_require=['pytest', 'pytest-capturelog'],
)

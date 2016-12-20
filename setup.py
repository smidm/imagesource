# -*- coding: utf-8 -*-
from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='ImageSource',
    version='1.0b1',
    author='Matěj Šmíd',
    url='https://github.com/smidm/imagesource',
    author_email='m@matejsmid.cz',
    license='The MIT License',
    description='Image sequence abstraction for OpenCV.',
    long_description=read_md('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Recognition',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],    
    keywords='image sequence video',
    packages=['imagesource'],
    install_requires=['joblib', 'numpy'],
    test_suite='nose.collector',
)


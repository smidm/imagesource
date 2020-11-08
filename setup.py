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
    version='1.0',
    author='Matěj Šmíd',
    url='https://github.com/smidm/imagesource',
    author_email='m@matejsmid.cz',
    license='The MIT License',
    description='Image sequence abstraction for OpenCV.',
    long_description=read_md('README.md'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Recognition',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],    
    keywords='image sequence video',
    packages=['imagesource'],
    install_requires=['joblib', 'numpy', 'opencv-python'],
    test_suite='nose.collector',
)


# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ImageSource',
    version='1.0b1',
    author='Matěj Šmíd',
    url='https://github.com/smidm/imagesource',
    author_email='m@matejsmid.cz',
    license='The MIT License',
    description='Image sequence abstraction for OpenCV.',
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
    test_suite = 'nose.collector',
    test_requires=['nose'],
)


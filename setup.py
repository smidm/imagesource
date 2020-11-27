# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='ImageSource',
    version='1.01',
    author='Matěj Šmíd',
    url='https://github.com/smidm/imagesource',
    author_email='m@matejsmid.cz',
    license='The MIT License',
    description='Image sequence abstraction for OpenCV.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
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
    install_requires=['joblib', 'numpy', 'opencv-python-headless', 'tqdm'],
    test_suite='nose.collector',
)

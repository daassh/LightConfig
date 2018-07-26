#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='lightconfig',
    version='0.0.5',
    description=(
        'LightConfig is a simple library to make user read or write config'
    ),
    long_description=open('README.rst').read(),
    author='zhang xuan',
    author_email='testzx@foxmail.com',
    maintainer='zhang xuan',
    maintainer_email='testzx@foxmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/daassh/LightConfig',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
    ],
)
#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pypipe',
    version = read('VERSION'),
    author = 'Chuan Miao',
    author_mail = 'chuan137@gmail.com',
    description = 'write lightweight coroutine pipelines in python',
    license = 'GNU',
    keyword = 'coroutine pipeline',
    packages = ['pypipe']
)

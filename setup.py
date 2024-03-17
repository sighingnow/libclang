#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8', mode='r') as fp:
    long_description = fp.read()

setup(
    name='libclang',
    version='18.1.1',
    description='Clang Python Bindings, mirrored from the official LLVM repo: https://github.com/llvm/llvm-project/tree/main/clang/bindings/python, to make the installation process easier.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tao He',
    author_email='sighingnow@gmail.com',
    url='https://github.com/sighingnow/libclang',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Compilers",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "License :: OSI Approved :: Apache Software License",
    ],
    platforms='any',
    keywords='Clang Python Bindings',


    zip_safe=False,

    package_dir={'': 'python'},
    packages=find_packages('python'),

    test_suite='python/tests',

    project_urls={
        'Documentation': 'https://libclang.readthedocs.io',
        'Source': 'https://github.com/sighingnow/libclang',
        'Tracker': 'https://github.com/sighingnow/libclang/issues',
    },
)

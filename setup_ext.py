#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from distutils.command.build import build
from distutils.dir_util import mkpath
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.bdist_wheel import get_platform, bdist_wheel


def platform_ext(plat):
    if 'linux' in plat:
        return '.so'
    if 'macosx' in plat:
        return '.dylib'
    if 'win' in plat:
        return '.dll'
    raise RuntimeError('Invalid platform value: %s' % plat)


platform = get_platform(None)


class bdist_wheel_injected(bdist_wheel):
    def finalize_options(self):
        super(bdist_wheel_injected, self).finalize_options()
        self.root_is_pure = True

    def run(self):
        global platform
        platform = self.plat_name
        super(bdist_wheel_injected, self).run()


class CopyNativeExtension(Extension):
    def __init__(self, name):
        super(CopyNativeExtension, self).__init__(name, sources=[])


class CopyNativeCommand(build_ext):
    def run(self):
        for ext in self.extensions:
            source_dir = './native/'
            target_dir = os.path.dirname(self.get_ext_fullpath(ext.name))
            libname = 'libclang' + platform_ext(platform)
            mkpath(target_dir)
            self.copy_file(os.path.join(source_dir, libname),
                           os.path.join(target_dir, libname))

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8', mode='r') as fp:
    long_description = fp.read()

setup(
    name='libclang',
    version='19.1.3',
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

    ext_modules=[CopyNativeExtension('clang.native.clang')],
    cmdclass={
        'build_ext': CopyNativeCommand,
        'bdist_wheel': bdist_wheel_injected,
    },

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

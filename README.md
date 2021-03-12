libclang-for-pip
================

![PyPI](https://img.shields.io/pypi/v/libclang)
![Python](https://img.shields.io/pypi/pyversions/libclang)
![Downloads](https://img.shields.io/pypi/dw/libclang)
![License](https://img.shields.io/pypi/l/libclang)

![Linux](https://github.com/sighingnow/libclang/workflows/libclang-linux-amd64/badge.svg)
![MacOS](https://github.com/sighingnow/libclang/workflows/libclang-macosx-amd64/badge.svg)
![Windows](https://github.com/sighingnow/libclang/workflows/libclang-windows-amd64/badge.svg)

The repository contains code that taken from [the LLVM project][1], to make it easier to install
clang's python bindings.

The repository copys necessary Python binding files from LLVM repo, and adds packaging scripts
to make it a valid Python package, the uploads the package to [pypi][2]. To make the libclang
available without install the LLVM toolkits, this package provides bundled static-linked libclang
shared library for different platforms, which, should work well on OSX, Windows, as well as
usual Linux distributions.

The aim of this project is to make the `clang.cindex` (aka., Clang Python Bindings)
available for more Python users, without setup the LLVM environment. To install the package,
you just need to run

```bash
pip install clang
```

Internals
---------

Update class variable `library_path` of `Config` in `cindex.py` as:

```python
    library_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'native')
```

License
-------

This repository follows the license agreement of the LLVM project, see [Apache-2.0 WITH LLVM-exception](./LICENSE.TXT).

[1]: https://github.com/llvm/llvm-project/tree/master/clang/bindings/python
[2]: https://pypi.org/project/libclang

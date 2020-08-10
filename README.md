libclang-for-pip
================

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

License
-------

This repository follows the license agreement of the LLVM project, see [./LICENSE.TXT]
(Apache-2.0 WITH LLVM-exception).

[1]: https://github.com/llvm/llvm-project/tree/master/clang/bindings/python
[2]: https://pypi.org/project/libclang

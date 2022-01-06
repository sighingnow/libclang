#!/bin/sh

set -x

sudo docker run --privileged --network=host --rm -v `pwd`:/work quay.io/pypa/manylinux2014_aarch64:latest \
            sh -c 'mkdir -p /work/build && \
                   cd /work/build && \
					         cmake ../llvm -DLLVM_ENABLE_PROJECTS=clang -DBUILD_SHARED_LIBS=OFF -DLLVM_ENABLE_TERMINFO=OFF -DLLVM_TARGETS_TO_BUILD=X86 -DCMAKE_BUILD_TYPE=MinSizeRel -DCMAKE_CXX_FLAGS_MINSIZEREL="-Os -DNDEBUG -static-libgcc -static-libstdc++ -s" && \
                   make libclang -j2'
sudo chmod -R a+wr `pwd`/build

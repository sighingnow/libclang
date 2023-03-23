#!/bin/sh

set -x

sudo docker run --privileged --network=host --rm -v `pwd`:/work frolvlad/alpine-gxx \
            sh -c 'apk add python3 cmake make && \
                   mkdir -p /work/build && \
                   cd /work/build && \
                   cmake ../llvm \
                     -DLLVM_ENABLE_PROJECTS=clang \
                     -DBUILD_SHARED_LIBS=OFF \
                     -DLLVM_ENABLE_ZLIB=OFF \
                     -DLLVM_ENABLE_ZSTD=OFF \
                     -DLLVM_ENABLE_TERMINFO=OFF \
                     -DLLVM_TARGETS_TO_BUILD=X86 \
                     -DCMAKE_BUILD_TYPE=RelWithDebInfo \
                     -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-O2 -g -DNDEBUG -static-libgcc -static-libstdc++" && \
                   make libclang -j$(nproc) && \
                   strip lib/libclang.so'
sudo chmod -R a+wr `pwd`/build

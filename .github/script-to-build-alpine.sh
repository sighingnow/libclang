#!/bin/sh

sudo docker run --privileged --network=host --rm -v `pwd`:/work frolvlad/alpine-gxx \
            sh -c 'apk add python3 cmake make && \
                   mkdir -p /work/build && \
                   cd /work/build && \
					         cmake ../llvm -DLLVM_ENABLE_PROJECTS=clang -DBUILD_SHARED_LIBS=OFF -DLLVM_ENABLE_TERMINFO=OFF -DLLVM_TARGETS_TO_BUILD=X86 -DCMAKE_BUILD_TYPE=MinSizeRel -DCMAKE_CXX_FLAGS_MINSIZEREL="-Os -DNDEBUG -static-libgcc -static-libstdc++ -s" && \
                   make libclang -j2'

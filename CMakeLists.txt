cmake_minimum_required(VERSION 3.18...3.31)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES C CXX)

# Set a default build type if none was specified
# scikit-build-core defaults to setting this to release, but not sure if it will be empty for multi-config generators?
if(NOT CMAKE_BUILD_TYPE) #AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
  mark_as_advanced(CMAKE_BUILD_TYPE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

include(llvm_version.cmake)

include(ExternalProject)

# Should eventually update this to handle bundling in the LLVM source code for an SDIST

set(_llvm_cache_args)
set(_llvm_build_flags)

if(CMAKE_SYSTEM_PROCESSOR MATCHES "^arm" AND CMAKE_SYSTEM_NAME STREQUAL "Linux")
  message(STATUS "Setting LLVM target triple to arm-linux-gnueabihf for 32-bit ARM build")
  list(APPEND _llvm_cache_args
    -DLLVM_DEFAULT_TARGET_TRIPLE:STRING=arm-linux-gnueabihf
  )
endif()

# Based on manylinux standards, may not actually be necessary to static link libgcc and libstdc++
if(UNIX AND NOT APPLE)
  # LLVM_STATIC_LINK_CXX_STDLIB is used to static link with -static-libstdc++
  # Which performs compile flag checks to make sure it is possible, so not handled here
  include(CheckCXXCompilerFlag)
  include(CheckLinkerFlag)
  check_cxx_compiler_flag("-static-libgcc" CXX_COMPILER_SUPPORTS_STATIC_LIBGCC)
  check_linker_flag(CXX "-static-libgcc" CXX_LINKER_SUPPORTS_STATIC_LIBGCC)
  if(CXX_COMPILER_SUPPORTS_STATIC_LIBGCC AND CXX_LINKER_SUPPORTS_STATIC_LIBGCC)
    message(STATUS "Setting Linux build flags for static linking libgcc")
    string(JOIN " " _llvm_build_flags "-static-libgcc")
  endif()
endif()

if(APPLE)
  message(STATUS "Setting macOS deployment target to ${MACOSX_DEPLOYMENT_TARGET}")
  message(STATUS "Setting macOS architectures to ${CMAKE_OSX_ARCHITECTURES}")
  list(APPEND _llvm_cache_args
    -DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=${MACOSX_DEPLOYMENT_TARGET}
    -DCMAKE_OSX_ARCHITECTURES:STRING=${CMAKE_OSX_ARCHITECTURES}
  )
endif()

if(WIN32)
  message(STATUS "Setting LLVM USE_CRT_MINSIZEREL to MT for Windows build")
  list(APPEND _llvm_cache_args
    -DLLVM_USE_CRT_MINSIZEREL:STRING="MT"
  )
  if(LLVM_TABLEGEN)
    message(STATUS "Setting LLVM tablegen path to ${LLVM_TABLEGEN}")
    list(APPEND _llvm_cache_args
      -DLLVM_TABLEGEN:FILEPATH=${LLVM_TABLEGEN}
    )
  endif()
  # LLVM_NATIVE_TOOL_DIR may be better than setting LLVM_TABLEGEN and CLANG_TABLEGEN separately (built with LLVM_OPTIMIZED_TABLEGEN?)
  # Pre-built versions of the native tools for cross-compilation could be split into a separate project, as perhaps useful for others cross-compiling clang as well?
  # LLVM_BUILD_TOOLS -- native tools for cross-compilation, such as llvm-as, etc? Maybe some useful tools that would be useful to have pre-compiled here as well?
  if(CLANG_TABLEGEN)
    message(STATUS "Setting clang tablegen path to ${CLANG_TABLEGEN}")
    list(APPEND _llvm_cache_args 
      -DCLANG_TABLEGEN:FILEPATH=${CLANG_TABLEGEN} # TODO does this actually exist?
    )
  endif()
  if(MSVC)
    message(STATUS "Setting LLVM build flags for parallel compilation on MSVC")
    string(JOIN " " _llvm_build_flags "/MP")
  endif()
endif()

if(_llvm_build_flags)
  message(STATUS "C/CXX build flags set to ${_llvm_build_flags}")
  list(APPEND _llvm_cache_args
    -DCMAKE_C_FLAGS:STRING=${_llvm_build_flags}
    -DCMAKE_CXX_FLAGS:STRING=${_llvm_build_flags}
  )
endif()

# LLVM_TARGETS_TO_BUILD -- set by CI workflows when cross-compiling, otherwise default to host
if(NOT DEFINED LLVM_TARGETS_TO_BUILD)
  set(LLVM_TARGETS_TO_BUILD "host")
endif()
message(STATUS "Setting LLVM_TARGETS_TO_BUILD to ${LLVM_TARGETS_TO_BUILD}")

# Setting CMAKE_SYSTEM_NAME in the cache causes CMake to set CMAKE_CROSSCOMPILING
# This is needed to prevent LLVM from trying to run certain cross-compiled tools like clang-ast-dump
# https://github.com/llvm/llvm-project/blob/llvmorg-18.1.8/clang/lib/Tooling/CMakeLists.txt#L63 (removed in LLVM v19)
if(DEFINED CACHE{CMAKE_SYSTEM_NAME})
  message(STATUS "Setting CMAKE_SYSTEM_NAME in the cache to ${CMAKE_SYSTEM_NAME} (cross-compiling)")
  list(APPEND _llvm_cache_args
    -DCMAKE_SYSTEM_NAME:STRING=${CMAKE_SYSTEM_NAME}
  )
endif()

set(LLVM_SOURCE_DIR ${CMAKE_BINARY_DIR}/llvm-src)
set(LLVM_BINARY_DIR ${CMAKE_BINARY_DIR}/llvm-build)
ExternalProject_add(build-libclang
    SOURCE_SUBDIR llvm
    SOURCE_DIR ${LLVM_SOURCE_DIR}
    BINARY_DIR ${LLVM_BINARY_DIR}
    URL "https://github.com/llvm/llvm-project/releases/download/llvmorg-${LLVM_VERSION}/llvm-project-${LLVM_VERSION}.src.tar.xz"
    CMAKE_CACHE_ARGS
        -DBUILD_TESTING:BOOL=OFF
        -DLLVM_ENABLE_PROJECTS:STRING=clang
        -DBUILD_SHARED_LIBS:BOOL=OFF
        -DLLVM_BUILD_TOOLS:BOOL=OFF
        -DLLVM_ENABLE_ZLIB:BOOL=OFF
        -DLLVM_ENABLE_ZSTD:BOOL=OFF
        -DLLVM_ENABLE_TERMINFO:BOOL=OFF
        -DLLVM_TARGETS_TO_BUILD:STRING=${LLVM_TARGETS_TO_BUILD}
        -DLLVM_STATIC_LINK_CXX_STDLIB:BOOL=ON
        -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
        -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_C_COMPILER:FILEPATH=${CMAKE_C_COMPILER}
        -DCMAKE_CXX_COMPILER:FILEPATH=${CMAKE_CXX_COMPILER}
        ${_llvm_cache_args}
    UPDATE_COMMAND ""
    INSTALL_COMMAND ""
    # Specify target to build as libclang
    BUILD_COMMAND ${CMAKE_COMMAND} --build . --parallel --target libclang --config ${CMAKE_BUILD_TYPE}
)

# The install line below can install libclang shared library in a cross-platform way
# Unfortunately the LLVM CMake build system doesn't respect CMAKE_INSTALL_LIBDIR/CMAKE_INSTALL_BINDIR
# hopefully a future version of LLVM will fix this
# install(SCRIPT ${LLVM_BINARY_DIR}/tools/clang/tools/libclang/cmake_install.cmake COMPONENT libclang)

if(WIN32)
  set(libclang-library ${LLVM_BINARY_DIR}/bin/libclang${CMAKE_SHARED_LIBRARY_SUFFIX})
elseif(APPLE)
  set(libclang-library ${LLVM_BINARY_DIR}/lib/libclang${CMAKE_SHARED_LIBRARY_SUFFIX})
else()
  # On Linux (and probably other BSD systems?) the shared library is named libclang.so.<SOABIVERSION>
  # The libclang.so file is just a symlink to the actual shared library
  set(libclang-library ${LLVM_BINARY_DIR}/lib/libclang${CMAKE_SHARED_LIBRARY_SUFFIX}.${LLVM_VERSION})
endif()

install(
  PROGRAMS
    ${libclang-library}
  DESTINATION lib
  RENAME libclang${CMAKE_SHARED_LIBRARY_SUFFIX}
)
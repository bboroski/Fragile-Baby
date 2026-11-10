# MCST Elbrus Linux toolchain. This file intentionally requires an E2K compiler.
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR e2k)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

set(E2K_CC "" CACHE FILEPATH "Path to MCST LCC or a verified E2K-target compiler")
set(E2K_SYSROOT "" CACHE PATH "Optional target sysroot")
set(E2K_QEMU "" CACHE FILEPATH "Optional qemu-e2k runner for target executables")
set(FB_E2K_ADDRESS_MODEL "64" CACHE STRING "E2K address model: 32, 64 or 128")
set_property(CACHE FB_E2K_ADDRESS_MODEL PROPERTY STRINGS 32 64 128)
set(FB_E2K_GENERATION "0" CACHE STRING "Target generation: 0=unknown, 1..7=e2k-v1..v7")

if(NOT E2K_CC AND DEFINED ENV{E2K_CC} AND NOT "$ENV{E2K_CC}" STREQUAL "")
  set(E2K_CC "$ENV{E2K_CC}" CACHE FILEPATH "Path to MCST LCC or a verified E2K-target compiler" FORCE)
endif()

if(NOT E2K_CC)
  find_program(_FB_E2K_LCC NAMES lcc)
  if(_FB_E2K_LCC)
    set(E2K_CC "${_FB_E2K_LCC}" CACHE FILEPATH "Path to MCST LCC or a verified E2K-target compiler" FORCE)
  endif()
endif()

if(NOT E2K_CC)
  message(FATAL_ERROR
    "No E2K compiler found. Install the MCST toolchain or pass -DE2K_CC=/path/to/lcc. "
    "A host x86 GCC must not be used as an E2K compiler.")
endif()

if(NOT EXISTS "${E2K_CC}")
  message(FATAL_ERROR "E2K_CC does not exist: ${E2K_CC}")
endif()

if(NOT FB_E2K_ADDRESS_MODEL MATCHES "^(32|64|128)$")
  message(FATAL_ERROR "FB_E2K_ADDRESS_MODEL must be 32, 64 or 128")
endif()

if(NOT FB_E2K_GENERATION MATCHES "^[0-7]$")
  message(FATAL_ERROR "FB_E2K_GENERATION must be 0 or an integer from 1 to 7")
endif()

set(CMAKE_C_COMPILER "${E2K_CC}" CACHE FILEPATH "E2K C compiler" FORCE)
set(CMAKE_C_FLAGS_INIT "-m${FB_E2K_ADDRESS_MODEL}")

if(E2K_SYSROOT)
  if(NOT IS_DIRECTORY "${E2K_SYSROOT}")
    message(FATAL_ERROR "E2K_SYSROOT is not a directory: ${E2K_SYSROOT}")
  endif()
  set(CMAKE_SYSROOT "${E2K_SYSROOT}")
  set(CMAKE_FIND_ROOT_PATH "${E2K_SYSROOT}")
endif()

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

if(E2K_QEMU)
  if(NOT EXISTS "${E2K_QEMU}")
    message(FATAL_ERROR "E2K_QEMU does not exist: ${E2K_QEMU}")
  endif()
  set(CMAKE_CROSSCOMPILING_EMULATOR "${E2K_QEMU}")
endif()

# Fail during configure, rather than silently producing a host executable.
include(CheckCSourceCompiles)
unset(FB_E2K_COMPILER_HAS_TARGET_MACRO CACHE)
check_c_source_compiles("
#ifndef __e2k__
#error Selected compiler does not target Elbrus e2k
#endif
int fragile_baby_e2k_compiler_probe(void) { return 0; }
" FB_E2K_COMPILER_HAS_TARGET_MACRO)

if(NOT FB_E2K_COMPILER_HAS_TARGET_MACRO)
  message(FATAL_ERROR
    "The selected compiler does not define __e2k__. Check E2K_CC, address model and sysroot.")
endif()

set(FB_BUILD_E2K_SMOKE ON CACHE BOOL "Build a compile-time E2K target smoke test" FORCE)

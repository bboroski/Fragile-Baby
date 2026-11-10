# Generic E2K cross-compilation contract.
# The caller must supply the actual compiler and sysroot from its toolchain kit.
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR e2k)

if(NOT DEFINED FRAGILE_BABY_E2K_C_COMPILER OR
   "${FRAGILE_BABY_E2K_C_COMPILER}" STREQUAL "")
    message(FATAL_ERROR
        "Set FRAGILE_BABY_E2K_C_COMPILER to the verified compiler executable.")
endif()

if(NOT DEFINED FRAGILE_BABY_E2K_SYSROOT OR
   "${FRAGILE_BABY_E2K_SYSROOT}" STREQUAL "")
    message(FATAL_ERROR
        "Set FRAGILE_BABY_E2K_SYSROOT to the matching target sysroot.")
endif()

set(CMAKE_C_COMPILER "${FRAGILE_BABY_E2K_C_COMPILER}" CACHE FILEPATH "")
set(CMAKE_SYSROOT "${FRAGILE_BABY_E2K_SYSROOT}" CACHE PATH "")
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

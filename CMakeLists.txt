cmake_minimum_required(VERSION 3.16)
project(FragileBaby VERSION 0.1.0 LANGUAGES C)

include(CTest)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

set(FB_E2K_GENERATION "0" CACHE STRING "Target e2k generation: 0=unknown, 1..7=e2k-v1..v7")
set_property(CACHE FB_E2K_GENERATION PROPERTY STRINGS 0 1 2 3 4 5 6 7)
option(FB_BUILD_E2K_SMOKE "Build a compile-time E2K target smoke test" OFF)

if(NOT FB_E2K_GENERATION MATCHES "^[0-7]$")
  message(FATAL_ERROR "FB_E2K_GENERATION must be 0 or an integer from 1 to 7")
endif()

add_library(fragile_baby_platform STATIC
  src/platform.c
  src/linux_probe.c
)
add_library(FragileBaby::Platform ALIAS fragile_baby_platform)

target_include_directories(fragile_baby_platform
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
         $<INSTALL_INTERFACE:include>
)
target_compile_definitions(fragile_baby_platform
  PUBLIC FB_E2K_GENERATION=${FB_E2K_GENERATION}
  PRIVATE _POSIX_C_SOURCE=200809L
)

if(MSVC)
  target_compile_options(fragile_baby_platform PRIVATE /W4)
else()
  target_compile_options(fragile_baby_platform PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(BUILD_TESTING)
  add_executable(fb_platform_tests tests/test_platform.c)
  target_link_libraries(fb_platform_tests PRIVATE FragileBaby::Platform)
  if(NOT MSVC)
    target_compile_options(fb_platform_tests PRIVATE -Wall -Wextra -Wpedantic)
  endif()
  add_test(NAME fragile_baby_platform_tests COMMAND fb_platform_tests)

  if(FB_BUILD_E2K_SMOKE)
    add_executable(fb_e2k_compile_smoke tests/e2k_compile_smoke.c)
    target_link_libraries(fb_e2k_compile_smoke PRIVATE FragileBaby::Platform)
    if(CMAKE_CROSSCOMPILING AND CMAKE_CROSSCOMPILING_EMULATOR)
      add_test(NAME fragile_baby_e2k_smoke
        COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} $<TARGET_FILE:fb_e2k_compile_smoke>)
    elseif(NOT CMAKE_CROSSCOMPILING)
      add_test(NAME fragile_baby_e2k_smoke COMMAND fb_e2k_compile_smoke)
    endif()
  endif()
endif()

install(TARGETS fragile_baby_platform ARCHIVE DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)

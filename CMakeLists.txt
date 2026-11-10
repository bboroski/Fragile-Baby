cmake_minimum_required(VERSION 3.16)
project(FragileBaby VERSION 0.1.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_library(fragile_baby_elbrus STATIC src/elbrus.c)
target_include_directories(fragile_baby_elbrus PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

include(CTest)
if(BUILD_TESTING)
    add_executable(fragile_baby_elbrus_tests tests/test_elbrus.c)
    target_link_libraries(fragile_baby_elbrus_tests PRIVATE fragile_baby_elbrus)
    add_test(NAME fragile_baby_elbrus_tests COMMAND fragile_baby_elbrus_tests)
endif()

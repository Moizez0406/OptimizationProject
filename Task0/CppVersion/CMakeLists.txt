cmake_minimum_required(VERSION 3.10)
project(OptimizationProject)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(con
    main/convertion.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)
add_executable(main
    main/main.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)
add_executable(box
    main/box.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)
add_executable(ga
    main/ga.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)

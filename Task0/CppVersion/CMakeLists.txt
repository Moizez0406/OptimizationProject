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
add_executable(pm
    main/pm_analysis.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)
add_executable(pop
    main/population_analysis.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)
add_executable(px
    main/px_analysis.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)
add_executable(tour
    main/tournament_analysis.cpp
    src/Subject_solution.cpp
    src/load.cpp
    src/algo.cpp
)

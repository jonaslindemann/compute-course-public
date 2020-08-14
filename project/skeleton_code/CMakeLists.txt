cmake_minimum_required(VERSION 2.6)
project(particles)
enable_language(Fortran)

set (CMAKE_VERBOSE_MAKEFILE OFF)

add_executable(particles main.f90 particle_defs.f90 particle_utils.f90 particle_data.f90
particle_sim.f90 vector_operations.f90)

add_library(particle SHARED particle_defs.f90 particle_utils.f90
particle_data.f90 particle_sim.f90 particle_state.f90 vector_operations.f90)
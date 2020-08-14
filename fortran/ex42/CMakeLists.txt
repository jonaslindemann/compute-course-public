add_executable(ex42 ex42.f90 myfunc.cpp utils.f90)
set_target_properties(ex42 PROPERTIES LINKER_LANGUAGE Fortran)


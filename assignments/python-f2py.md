# Exercise 1 - Implement the Fortran subroutine in M.3 as Python module using f2py

The Fortran code should be implemented without loops and builtin functions for sums and elementwise operations. Make sure to use intent(..) attributes when declaring the subroutine parameters in fortran, so that f2py can identify input and output arguments.

# Exercise 2 - Wrapping an existing Fortran code

We will be reimplementing the Mandelbrot-code found at http://www.fortran90.org/src/rosetta.html#examples. A working code with a CMakeLists.txt file is provided. The CMakeLists.txt also contains a target for building a library of the source code files that the mandelbrot application requires for running. Use this library when building the python module with f2py.

Implement the mandelbrot wrapper in a module. An skeleton module is provided, mandelmod.f90, containing hints on how to complete the implementation. When the wrapper module is implemented, uncomment the section in the CMakeLists.txt file with the f2py target. If everything builds you should have a .so-file in your build directory.

Implement a python main program that will call the mandelbrot code. A skeleton code is provided, mandelbrot.py.

